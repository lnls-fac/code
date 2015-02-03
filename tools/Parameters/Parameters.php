<?php
/**
 * Parameters extension.
 *
 * Custom create and edit pages for machine parameters, with tags for
 * inclusion in other pages.
 */

if (!defined('MEDIAWIKI')) {    
    echo("This is an extension to the MediaWiki package and cannot be run ".
        "standalone.\n");
    die(-1);
}

require('FacParameter.php');
require('ValueExtractor.php');

$wgExtensionCredits['other'][] = array(
    'name' => 'Parameters',
    'version' => 0.0,
    'author' => array('Afonso'),
    'url' => 'http://10.0.21.132/',
    'description' => 'Create, edit and include machine parameters'
);

$wgHooks['ParserFirstCallInit'][] = 'fac_parameter_parser_init';
$wgHooks['EditFormPreloadText'][] = 'fac_edit_form_preload_text';
$wgHooks['EditFilter'][] = 'fac_edit_filter';
$wgHooks['ArticleDelete'][] = 'fac_article_delete';

function fac_parameter_parser_init(Parser $parser)
{
    $parser->setHook("parameter", "fac_parameter_render");
    return true;
}

function fac_parameter_render($input, array $args, Parser $parser, PPFrame $frame)
{
    $field = fac_get_field_arg($args);

    $prm = new FacParameterReader($input);
    $fields = $prm->read($input);

    if (!$fields) {
        $output = '<pre style="color: red">' .
            'Error: parameter ' . $input . ' not found!</pre>';
        return $parser->recursiveTagParse($output, $frame);
    }

    if ($field)
        $output = $fields[$field];
    else
        $output = $fields['value'] . " " . $fields['units'];

    return htmlspecialchars($parser->recursiveTagParse($output, $frame));
}

function fac_get_field_arg(array $args)
{
    if (array_key_exists('field', $args))
        return $args['field'];
    else
        return false;
}

function fac_edit_form_preload_text(&$text, &$title)
{
    $name = FacParameter::get_name_if_parameter($title);
    if (!$name)
        return true; // not a parameter page

    $text = FacParameter::get_parameter_template();
}

function fac_edit_filter($editor, $text, $section, &$error, $summary)
{
    $name = FacParameter::get_name_if_parameter($editor->getTitle());
    if (!$name)
        return true; // not a parameter page

    $prm = new FacParameterWriter($name, $text);
    $result = $prm->write();

    if (!$result) {
        $error = '<span style="color: red">Missing field';
        if (count($prm->missing_fields) > 1)
            $error .= 's';
        $error .= ': ' . implode(', ', $prm->missing_fields) . '</span>';
    }

    return true;
}

function fac_article_delete(WikiPage &$wikiPage, User &$user, &$reason, &$error)
{
    $name = FacParameter::get_name_if_parameter($wikiPage->getTitle());
    if (!$name)
        return true; // not a parameter page

    $prm = new FacParameterEraser($name);
    $result = $prm->erase();    
    if (!$result)
        return false;
    else
        return true;
}

?>
