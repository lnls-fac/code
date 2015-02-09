<?php
/**
 * Parameters extension.
 *
 * Read and write parameters to and from database.
 */

if (!defined('MEDIAWIKI')) {
    echo("This is an extension to the MediaWiki package and cannot be run ".
        "standalone.\n");
    die(-1);
}

require('FacParameter.php');

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
$wgHooks['TitleMove'][] = 'fac_title_move';
$wgHooks['AbortMove'][] = 'fac_abort_move';
$wgHooks['ArticleDelete'][] = 'fac_article_delete';

function fac_parameter_parser_init(Parser $parser)
{
    $parser->setHook("parameter", "fac_parameter_render");
    return true;
}

function fac_parameter_render($input, array $args, Parser $parser,
    PPFrame $frame)
{
    $prm = new FacParameterReader($input);

    try {
        $fields = $prm->read($input);
        $output = fac_get_parameter_field($fields, $args);
        return htmlspecialchars($parser->recursiveTagParse($output, $frame));
    } catch(FacException $e) {
        $output = fac_get_error_message('Error: ' . $e->getMessage());
        return $parser->recursiveTagParse($output, $frame);
    }
}

function fac_get_error_message($msg, $bold=true)
{
    if ($bold)
        $s = "'''";
    else
        $s = "";

    return $s . "<span style=\"color: red\">" . $msg . "</span>" . $s;
}

function fac_get_parameter_field($fields, array $args)
{
    $field = fac_get_field_arg($args);
    if ($field)
        return $fields[$field];
    else
        return $fields['value'] . " " . $fields['units'];
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
        return true; # not a parameter page

    $text = FacParameter::get_parameter_template();
}

function fac_edit_filter($editor, $text, $section, &$error, $summary)
{
    $name = FacParameter::get_name_if_parameter($editor->getTitle());
    if (!$name)
        return true; # not a parameter page

    try {
        $prm = new FacParameterWriter($name, $text);
        $result = $prm->write();
        if (!$result)
            $error = fac_get_missing_fields_message($prm->missing_fields);
    } catch (FacException $e) {
        $error = fac_get_error_message('Error: ' . $e->getMessage());
    }

    return true;
}

function fac_get_missing_fields_message($missing_fields)
{
    $msg = "Missing field";
    if (count($missing_fields) > 1)
        $msg .= "s";
    $field_list = htmlspecialchars(implode(', ', $missing_fields));
    $msg .= ": " . $field_list;

    return fac_get_error_message($msg, false);
}

function fac_title_move(Title $title, Title $newTitle, User $user)
{
    $ns = substr(FacParameter::parameter_namespace, 0, -1); # remove colon

    $old_ns = $title->getSubjectNsText();
    $new_ns = $newTitle->getSubjectNsText();

    if(($old_ns != $ns) or ($new_ns != $ns))
        return true; # not in parameter namespace
   
    $prm = new FacParameterWriter($title->getText());
    $prm->rename($newTitle->getText());

    return true;
}

function fac_abort_move(Title $oldTitle, Title $newTitle, User $user,
    &$error, $reason)
{
    $ns = substr(FacParameter::parameter_namespace, 0, -1); # remove colon

    if ($oldTitle->getSubjectNsText() != $ns) {
        if ($newTitle->getSubjectNsText() == $ns) {
            $error = 'Cannot move to parameter namespace!';
            return false;
        }
    } else {
        if ($newTitle->getSubjectNsText() != $ns) {
            $error = 'Cannot move out of parameter namespace!';
            return false;
        } else {
            if ($newTitle->exists()) {
                $error = 'Cannot overwrite existing parameter!';
                return false;
            }
        }
    }

    return true;
}

function fac_article_delete(WikiPage &$wikiPage, User &$user, &$reason,
    &$error)
{
    $name = FacParameter::get_name_if_parameter($wikiPage->getTitle());
    if (!$name)
        return true; # not a parameter page

    $prm = new FacParameterEraser($name);
    return $prm->erase();
}

?>
