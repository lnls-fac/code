<?php

class FacParameter {
    const parameter_namespace = "Parameter:";

    static $valid_fields = array(
        'group', 'symbol', 'units', 'is_derived', 'value'
    );

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

    protected $parameter;

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
            if ($value === false) // empty string is valid
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
        }
        
        return $table->write_parameter($values);
    }

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
        $table->erase_dependencies($this->parameter);
        $table->erase_expression($this->parameter);
        return $table->erase_parameter($this->parameter);
    }
}

class FacConnection {
    const server_address = '10.0.21.152';
    const user = 'prm_editor';
    const password = 'prm0';
    const database = 'parameters';

    protected $mysqli;

    function FacConnection()
    {
        $this->mysqli = new mysqli(
            self::server_address,
            self::user,
            self::password,
            self::database
        );
        if ($this->mysqli->connect_errno) {
            echo "Failed to connect to MySQL: " . $this->mysqli->connect_error;
            $this->mysqli = false;
        }
    }
}

class FacTable extends FacConnection {
    function FacTable()
    {
        $this->FacConnection();
    }

    function read_parameter($name)
    {
        if (!$this->mysqli)
            return false;

        $query = "SELECT * FROM parameter WHERE name='" .
            $this->mysqli->real_escape_string($name) . "';";
                
        $result = $this->mysqli->query($query);
        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();            
            return $this->get_text_fields($row);
        } else
            return false;
    }

    function get_text_fields($row)
    {
        $fields = array();
        foreach ($row as $col => $value) {
            $field = $this->convert_col_to_field($col);
            if ($field == 'symbol')
                $fields[$field] = $this->convert_symbol_to_text($value);
            elseif ($field == 'is_derived')
                $fields[$field] = $this->convert_is_derived_to_text($value);
            else
                $fields[$field] = $value;
        }
        return $fields;
    }

    function convert_col_to_field($col)
    {
        if ($col == 'team')
            return 'group';
        else
            return $col;
    }

    function convert_symbol_to_text($value)
    {
        return "<math>" . $value . "</math>";
    }

    function convert_is_derived_to_text($value)
    {
        if ($value)
            return "True";
        else
            return "False";
    }

    function write_parameter($fields)
    {
        if (!$this->mysqli)
            return false;

        $db_fields = $this->get_db_fields($fields);

        $result = $this->read_parameter($db_fields['name']);
        if (!$result)
            $query = $this->build_insert_parameter_query($db_fields);
        else
            $query = $this->build_update_parameter_query($db_fields);

        $this->mysqli->query($query);

        return true;
    }

    function build_insert_parameter_query($db_fields)
    {
        $query = "INSERT INTO parameter VALUES (" .
            "'" . $db_fields['name'] . "', " .
            "'" . $db_fields['group'] . "', " .
            "'" . $db_fields['symbol'] . "', " .
            "'" . $db_fields['units'] . "', " .
            "'" . $db_fields['is_derived'] . "', " .
            "'" . $db_fields['value'] . "');";

        return $query;
    }

    function build_update_parameter_query($db_fields)
    {
        $query = "UPDATE parameter SET " .
            "team='" . $db_fields['group'] . "', " .
            "symbol='" . $db_fields['symbol'] . "', " .
            "units='" . $db_fields['units'] . "', " .
            "is_derived='" . $db_fields['is_derived'] . "', " .
            "value='" . $db_fields['value'] . "' " .
            "WHERE name='" . $db_fields['name'] . "';";

        return $query;
    }

    function get_db_fields($fields)
    {
        $db_fields = array();
        foreach ($fields as $key => $value) {
            if ($key == 'symbol')
                $db_fields[$key] = $this->convert_symbol_to_db($value);
            elseif ($key == 'is_derived')
                $db_fields[$key] = $this->convert_is_derived_to_db($value);
            else
                $db_fields[$key] = $this->convert_identity($value);
        }
        return $db_fields;
    }

    function convert_identity($value)
    {
        return $this->mysqli->real_escape_string($value);
    }

    function convert_symbol_to_db($value)
    {
        return $this->mysqli->real_escape_string(strip_tags($value));
    }

    function convert_is_derived_to_db($value)
    {
        if (strtoupper($value) == 'TRUE')
            return 1;
        else
            return 0;
    }

    function write_dependencies($parameter, array $dependencies)
    {
        $query = "INSERT INTO dependency VALUES ";
        $values = array();
        foreach($dependencies as $dep) {
            $value = "('" . $parameter . "', '" . $dep . "')";
            array_push($values, $value);
        }
        $query .= implode(', ', $values) . ";";

        return $this->mysqli->query($query);
    }

    function write_expression($parameter, $expression)
    {
        $query = "SELECT * FROM expression WHERE name='" .
            $parameter . "';";

        $result = $this->mysqli->query($query);
        if ($result->num_rows > 0) {
            $query = "UPDATE expression SET expression='" .
                $expression . "' WHERE name='" .
                $parameter . "';";
        } else {
            $query = "INSERT INTO expression VALUES ('" .
                $parameter . "', '" . $expression . "');";
        }

        return $this->mysqli->query($query);
    }

    function rename_parameter($name, $new_name)
    {
        $tables = array('parameter', 'dependency', 'expression');
        foreach ($tables as $table) {
            $query = "UPDATE " . $table . " SET name='" .
                $new_name . "' WHERE name='" .
                $name . "';";

            $this->mysqli->query($query);
        }
    }

    function erase_parameter($parameter)
    {
        return $this->erase('parameter', $parameter);
    }

    function erase_dependencies($parameter)
    {
        return $this->erase('dependency', $parameter);
    }

    function erase_expression($parameter)
    {
        return $this->erase('expression', $parameter);
    }

    function erase($table, $parameter)
    {
        $query = "DELETE FROM " . $table . " WHERE name='" .
            $parameter . "';";

        return $this->mysqli->query($query);
    }
}

class FacEvaluator extends FacConnection {
    static $valid_symbols = array(
        ' ', '.', '(', ')', ',',
        '0', '1', '2', '3', '4',
        '5', '6', '7', '8', '9'
    );
    static $valid_operators = array('+', '-', '*', '/');
    static $valid_functions = array(
        'sqrt', 'pow', 'exp',
        'asin', 'acos', 'atan',
        'sin', 'cos', 'tan'
    );

    public $expression;
    private $parameters;

    function FacEvaluator($expression)
    {
        $this->FacConnection();

        $this->expression = $expression;
        $this->parameters = array();
    }

    function evaluate()
    {
        $expr = $this->replace_parameters($this->expression);
        if (!$this->validate_final_expression($expr))
            throw new Exception('invalid expression');
        else
            return eval($expr);
    }

    function replace_parameters($expression)
    {
        if (substr_count($expression, '"') % 2)
            throw new Exception('double quotes not matching');

        $parameters = array();
        $split = explode('"', $parameters);
        for ($i = 0; $i < count($split); $i++)
            if ($i % 2)
                array_push($parameters, $split[$i]);

        foreach ($parameters as $p) {
            if (!in_array($p, $this->parameters))
                $this->parameters[$p] = $this->get_value_or_expression($p);

            $parameter = '"' . $p . '"';
            $value = strval($this->parameters[$p]);
            $expression = str_replace($parameter, $value, $expression);
        }

        return $expression;
    }

    function get_value_or_expression($parameter)
    {
        $p = $this->read_parameter($parameter);
        if ($p['is_derived'])
            return '(' . $this->replace_parameters($p['value']) . ')';
        else
            return $p['value'];
    }

    function read_parameter($parameter)
    {
        $query = "SELECT * FROM parameter WHERE name='" .
            $parameter . "';";
        $result = $this->mysqli->query($query);

        $row = $result->fetch_assoc();
        if (!$row)
            throw new Exception('parameter ' . $parameter . ' not found');

        if ($row['is_derived'])
            $value = $this->read_expression($parameter);
        else
            $value = $row['value'];

        return array($row['is_derived'], $value);
    }

    function read_expression($parameter)
    {
        $query = "SELECT * FROM expression WHERE name='" .
            $parameter . "';";
        $result = $this->mysqli->query($query);

        $row = $result->fetch_assoc();
        if (!$row)
            throw new Exception('expression for ' . $parameter . ' not found');
        else
            return $row['expression'];
    }

    function validate_final_expression($expression)
    {
        foreach (self::$valid_symbols as $s)
            $expression = str_replace($s, '', $expression);
        foreach (self::$valid_operators as $o)
            $expression = str_replace($o, '', $expression);
        foreach (self::$valid_functions as $f)
            $expression = str_replace($f, '', $expression);

        if ($expression === '')
            return true;
        else
            return false;
    }
}

class FacDependentTracker extends FacConnection {
    private $parameter;

    function FacDependentTracker($parameter)
    {
        $this->FacConnection();
        $this->parameter = $parameter;
    }

    function get_dependents()
    {
        $query = "SELECT * FROM dependency;";
        $result = $this->mysqli->query($query);
        $table = $result->fetch_all();

        $s = new FacSet();
        $t = new FacSet($this->parameter);
        $n = count($s->elements);
        while (true) {
            $u = new FacSet();
            foreach ($table as $row)
                foreach($t->elements as $e)
                    if ($row[1] == $e) {
                        $u->put($row[0]);
                        $s->put($row[0]);
                    }

            $new_n = count($s->elements);
            if ($new_n > $n) {
                $n = $new_n;
                $t = $u;
            } else
                break;            
        }

        return $s->elements;
    }
}

class FacSet {
    public $elements = array();

    function FacSet(array $elements)
    {
        foreach ($elements as $x)
            $this->put($x);
    }

    function put($x)
    {
        if (!in_array($x, $this->elements))
            array_push($this->elements, $x);
    }
}

?>
