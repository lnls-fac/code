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

    function replace($values)
    {
        $text = $this->text;
        $ve = new FacValueExtractor($text);

        foreach ($values as $field => $value) {
            $start = FacValueExtractor::tag_begin_open . $field .
                FacValueExtractor::tag_close;
            $end = FacValueExtractor::tag_end_open . $field .
                FacValueExtractor::tag_close;
            $pos_s = strpos($text, $start);
            $pos_e = strpos($text, $end);
            $text = substr($text, 0, $pos_s+strlen($start)) . $value .
                substr($text, $pos_e);
        }

        return $text;
    }
}

?>
