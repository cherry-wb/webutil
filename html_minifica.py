#!/usr/bin/env python
# -*- coding: utf-8 -*-


UNNEEDED_TAGS = ('</area>', '</base>', '<body>', '</body>', '</br>', '</col>',
    '</colgroup>', '</dd>', '</dt>', '<head>', '</head>', '</hr>', '<html>',
    '</html>', '</img>', '</input>', '</li>', '</link>', '</meta>', '</option>',
    '</p>', '</param>', '<tbody>', '</tbody>', '</td>', '</tfoot>', '</th>',
    '</thead>', '</tr>', '</basefont>', '</isindex>', '</param>')


SCRIPT_TAGS = ('<script type="text/javascript" language="javascript">',
    '<script language="javascript" type="text/javascript">',
    '<script type="text/javascript">', '<script language="javascript">',
    '<script type="application/ecmascript">', '<script type="text/ecmascript">',
    '<script type="application/javascript">', '<script type="text/jscript">',
    '<script type="text/x-ecmascript">', '<script type="text/livescript">',
    '<script type="text/x-javascript">', '<script type="text/javascript1.0">',
    '<script type="text/javascript1.1">', '<script type="text/javascript1.2">',
    '<script type="text/javascript1.3">', '<script type="text/javascript1.4">',
    '<script type="text/javascript1.5">', '<script type="text/javascript">',
    '<script type="application/x-ecmascript">',
    '<script type="application/x-javascript">')


DOCTYPE_TAGS = (
    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
    '<!DOCTYPE html PUBLIC"-//W3C//DTD HTML 4.01 Transitional//EN">',
    '<!DOCTYPE html PUBLIC"-//W3C//DTD HTML 4.01//EN">',
    '<!DOCTYPE html PUBLIC"-//W3C//DTD HTML 4.01 Frameset//EN">',
    '<!DOCTYPE html PUBLIC"-//W3C//DTD HTML 4.0//EN">',
    '<!DOCTYPE html PUBLIC"-//W3C//DTD HTML 3.2 Final//EN">',
    '<!DOCTYPE html PUBLIC"-//IETF//DTD HTML 2.0//EN">',
    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN">')


def condense_style(txt):
    ' condense style html tags '
    return txt.replace('<style type="text/css">', '<style>')


def condense_doc_ready(txt):
    ' condense document ready jquery '
    return txt.replace('$(document).ready(function()', '$(function()')


def condense_href_src(txt):
    ' condense href and src '
    return txt.replace('href="http://', 'href="//').replace('href="https://', 'href="//').replace('src="http://', 'src="//').replace('src="https://', 'src="//')


def condense_script(txt):
    ' condense script html tags '
    for tag_to_remove in iter(SCRIPT_TAGS):
            txt = txt.replace(tag_to_remove, '<script>')
    return txt


def condense_doctype(txt):
    ' condense doctype html tags '
    for tag_to_remove in iter(DOCTYPE_TAGS):
            txt = txt.replace(tag_to_remove.lower(), '<!doctype html>')
    return txt


def clean_unneeded_tags(txt):
    ' clean unneeded optional html tags '
    for tag_to_remove in iter(UNNEEDED_TAGS):
            txt = txt.replace(tag_to_remove, '')
    return txt