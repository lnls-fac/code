<?php

require_once('FacTable.php');
require_once('FacValueExtractor.php');

class FacTextReplacer {
    private $text;

    function __construct($text)
    {
        $this->text = $text;
    }

    function replace_value($value)
    {
        $value_extractor = new FacValueExtractor($this->text);
        $expression = $value_extractor->get_value('value');
        return str_replace($expression, $value, $this->text); 
    }
}

?>
