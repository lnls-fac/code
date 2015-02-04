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
        $table = new FacParameterTable();
        return $table->read($this->parameter);
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
        $table = new FacParameterTable();
        $values = $this->get_values();
        
        foreach ($values as $field => $value)
            if ($value === false) // empty string is valid
                array_push($this->missing_fields, $field);

        if (count($this->missing_fields) > 0)
            return false;
        else
            return $table->write($values);
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
}

class FacParameterEraser extends FacParameter {
    function FacParameterEraser($name)
    {
        $this->FacParameter($name);
    }

    function erase()
    {
        $table = new FacParameterTable();
        return $table->erase($this->parameter);
    }
}

class FacParameterTable {
    const server_address = '127.0.0.1';
    const user = 'prm_editor';
    const password = 'prm0';
    const database = 'parameters';

    protected $mysqli;

    function FacParameterTable()
    {
        $this->mysqli = new mysqli(
            self::server_address,
            self::user,
            self::password,
            self::database
        );
        if ($this->mysqli->connect_errno) {
            echo "Failed to connect to MySQL: " . $mysqli->connect_error;
            $this->mysqli = false;
        }
    }

    function read($name)
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

    function write($fields)
    {
        if (!$this->mysqli)
            return false;

        $db_fields = $this->get_db_fields($fields);

        $result = $this->read($db_fields['name']);
        if (!$result)
            $query = $this->build_insert_query($db_fields);
        else
            $query = $this->build_update_query($db_fields);

        $this->mysqli->query($query);

        return true;
    }

    function build_insert_query($db_fields)
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

    function build_update_query($db_fields)
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

    function erase($name)
    {
        $query = "DELETE FROM parameter WHERE name='" .
            $name . "';";
        return $this->mysqli->query($query);
    }
}

?>
