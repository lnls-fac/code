<?php

require('FacTable.php');
require('ValueExtractor.php');

class FacParameter {
    const parameter_namespace = "Parameter:";

    static $valid_fields = array(
        'group', 'symbol', 'units', 'is_derived', 'value'
    );

    protected $parameter;

    public static function get_name_if_parameter($title)
    {
        $n = strlen(self::parameter_namespace);
        if (substr($title, 0, $n) != self::parameter_namespace)
            return false;
        else    
            return substr($title, $n);
    }

    public static function get_parameter_template()
    {
        $template = "==Data==\n" .
            "<section begin=data/>\n" .
            "* Group: <section begin=group/><section end=group/>\n" .
            "* Symbol: <section begin=symbol/><section end=symbol/>\n" .
            "* Derived: <section begin=is_derived/>False<section end=is_derived/>\n" .
            "* Value: <section begin=value/><section end=value/>\n" .
            "* Units: <section begin=units/><section end=units/>\n" .
            "* Deps: <section begin=deps/><section end=deps/>\n" .
            "<section end=data/>\n" .
            "==Observations==\n" .
            "<section begin=obs/>\n" .
            "<section end=obs/>";
        return $template;
    }

    function FacParameter($name)
    {
        $this->parameter = $name;
    }
}

class FacParameterReader extends FacParameter {
    function FacParameterReader($name)
    {
        $this->FacParameter($name);
    }

    function read()
    {
        $table = new FacTable();
        return $table->read_parameter($this->parameter);
    }
}

class FacParameterWriter extends FacParameter {
    public $missing_fields = array();
    private $value_extractor;

    function FacParameterWriter($name, $text)
    {
        $this->FacParameter($name);
        $this->value_extractor = new ValueExtractor($text);
    }

    function write()
    {
        $values = $this->get_values();
        
        foreach ($values as $field => $value)
            if ($value === false) # empty string is valid, so check for ===
                array_push($this->missing_fields, $field);

        if (count($this->missing_fields) > 0)
            return false;
        else
            return $this->write_all($values);
    }

    function get_values()
    {
        $values = array('name' => $this->parameter);
        foreach (self::$valid_fields as $field)
            $values[$field] = $this->get_value($field);

        return $values;
    }

    function get_value($field)
    {
        if (in_array($field, self::$valid_fields)) {
            return $this->value_extractor->get_value($field);
        } else
            return false;
    }

    function write_all($values)
    {
        $table = new FacTable();

        if ($values['is_derived'] === 'True') {
            $table->erase_dependencies($values['name']);

            $deps = $this->get_dependencies($values['value']);
            if ($deps === false)
                return false;
            
            $r = $table->write_dependencies($values['name'], $deps);
            if ($r === false)
                return false;

            $r = $table->write_expression($values['name'], $values['value']);
            if ($r === false)
                return false;
        } else {
            ;
        }
        
        return $table->write_parameter($values);
    }

    # Should move?
    function get_dependencies($expression)
    {
        $n = substr_count($expression, '"');
        if ($n % 2)
            return false;

        $deps = array();
        $split = explode('"', $expression);

        for ($i = 0; $i < count($split); $i++)
            if ($i % 2)
                array_push($deps, $split[$i]);

        return $deps;
    }

    function rename_parameter($new_name)
    {
        $table = new FacTable();
        $table->rename_parameter($this->parameter, $new_name);
    }
}

class FacParameterEraser extends FacParameter {
    function FacParameterEraser($name)
    {
        $this->FacParameter($name);
    }

    function erase()
    {
        $table = new FacTable();

        $rd = $table->erase_dependencies($this->parameter);
        $re = $table->erase_expression($this->parameter);
        $rp = $table->erase_parameter($this->parameter);

        return ($rd && $re && $rp);
    }
}

?>
