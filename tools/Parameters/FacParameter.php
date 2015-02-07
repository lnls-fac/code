<?php

require('FacTable.php');
require('FacValueExtractor.php');

/**
 * Base class for parameters.
 */
class FacParameter {
    const parameter_namespace = "Parameter:";

    static $valid_fields = array(
        'group', 'symbol', 'units', 'is_derived', 'value'
    );

    protected $parameter;

    /**
     * Check if title is in parameter namespace and return name.
     * @return Name if in parameter namespace, false otherwise
     */
    public static function get_name_if_parameter($title)
    {
        $n = strlen(self::parameter_namespace);
        if (substr($title, 0, $n) != self::parameter_namespace)
            return false;
        else    
            return substr($title, $n);
    }

    /**
     * Get parameter template text for edit pages.
     * @return String with template text
     */
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
        $this->value_extractor = new FacValueExtractor($text);
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

    private function get_values()
    {
        $values = array('name' => $this->parameter);
        foreach (self::$valid_fields as $field)
            $values[$field] = $this->get_value($field);

        return $values;
    }

    private function get_value($field)
    {
        if (in_array($field, self::$valid_fields)) {
            return $this->value_extractor->get_value($field);
        } else
            return false;
    }

    private function write_all($values)
    {
        $table = new FacTable();
        $r = true;

        if ($values['is_derived'] === 'True')  {
            $e = new FacEvaluator($values['value']);
            $r = $r and $this->write_derived_fields(
                $values['value'],
                $e->get_dependencies(),
                $table
            );
            $values['value'] = $e->evaluate();
        }
        
        $r = $r and $table->write_parameter($values);

        $d = new FacDependentTracker($values['name']);            
        $dependents = $d->get_dependents();
        return $r and $this->update_dependents($dependents, $table);
    }

    private function write_derived_fields($expression, $dependencies, $table)
    {
        if ($dependencies === false)
            return false;

        $r = $table->erase_dependencies($this->parameter);
        if ($r === false)
            return false;

        $r = $table->write_dependencies($this->parameter, $dependencies);
        if ($r === false)
            return false;

        $r = $table->write_expression($this->parameter, $expression);
        if ($r === false)
            return false;

        return true;
    }

    private function update_dependents($dependents, $table)
    {
        $result = true;
        foreach($dependents as $d) {
            $p = $table->read_parameter($d);
            if (!$p) {
                $result = false;
                break;
            }
            $e = new FacEvaluator($table->read_expression($p['name']));
            $p['value'] = $e->evaluate();
            $result = $result and $table->write_parameter($p);
        }

        return $result;
    }

    function rename($new_name)
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

        $r = true;
        $r = $r and $table->erase_dependencies($this->parameter);
        $r = $r and $table->erase_expression($this->parameter);
        $r = $r and $table->erase_parameter($this->parameter);

        return $r;
    }
}

?>
