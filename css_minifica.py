#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO  # lint:ok
import re


EXTENDED_NAMED_COLORS = {
    'DarkBlue': '', 'MediumBlue': '',
    'DarkGreen': '', 'DarkCyan': '',
    'DeepSkyBlue': '', 'SpringGreen': '',
    'DarkTurquoise': '', 'MediumSpringGreen': '',
    'MidnightBlue': '', 'DodgerBlue': '',
    'LightSeaGreen': '', 'ForestGreen': '',
    'DarkSlateGray': '', 'LimeGreen': '',
    'MediumSeaGreen': '', 'Turquoise': '',
    'RoyalBlue': '', 'SeaGreen': '',
    'SteelBlue': '', 'DarkSlateBlue': '',
    'MediumTurquoise': '', 'Indigo': '', 'DarkOliveGreen': '',
    'CadetBlue': '', 'CornflowerBlue': '',
    'MediumAquaMarine': '', 'DimGray': '', 'SlateBlue': '',
    'OliveDrab': '', 'SlateGray': '',
    'SkyBlue': '', 'LightSlateGray': '', 'MediumSlateBlue': '',
    'LawnGreen': '', 'Chartreuse': '',
    'Aquamarine': '', 'LightSkyBlue': '', 'BlueViolet': '',
    'DarkRed': '', 'DarkMagenta': '',
    'SaddleBrown': '', 'Sienna': '', 'DarkSeaGreen': '',
    'LightGreen': '', 'MediumPurple': '',
    'DarkViolet': '', 'PaleGreen': '', 'Ivory': '',
    'DarkOrchid': '', 'YellowGreen': '', 'Brown': '',
    'DarkGray': '', 'LightBlue': '', 'FireBrick': '',
    'GreenYellow': '', 'PaleTurquoise': '', 'LightSteelBlue': '',
    'PowderBlue': '',
    'DarkGoldenRod': '', 'MediumOrchid': '', 'RosyBrown': '',
    'DarkKhaki': '',
    'MediumVioletRed': '', 'IndianRed': '', 'Chocolate': '',
    'LightGray': '', 'Thistle': '',
    'Orchid': '', 'GoldenRod': '', 'PaleVioletRed': '',
    'Crimson': '', 'Gainsboro': '',
    'BurlyWood': '', 'LightCyan': '', 'Lavender': '',
    'Violet': '', 'DarkSalmon': '',
    'PaleGoldenRod': '', 'LightCoral': '', 'Khaki': '',
    'AliceBlue': '', 'HoneyDew': '', 'Azure': '',
    'SandyBrown': '', 'Wheat': '', 'Beige': '',
    'WhiteSmoke': '', 'MintCream': '', 'GhostWhite': '',
    'Salmon': '', 'AntiqueWhite': '', 'LightGoldenRodYellow': '',
    'OldLace': '',
    'Magenta': '', 'DeepPink': '', 'OrangeRed': '',
    'Tomato': '', 'HotPink': '', 'Coral': '',
    'DarkOrange': '', 'LightPink': '', 'LightSalmon': '',
    'PeachPuff': '',
    'NavajoWhite': '', 'Moccasin': '', 'Bisque': '',
    'MistyRose': '', 'BlanchedAlmond': '',
    'PapayaWhip': '', 'LavenderBlush': '', 'SeaShell': '',
    'Cornsilk': '', 'LemonChiffon': '',
    'FloralWhite': '', 'LightYellow': ''}


def remove_comments(css):
    """Remove all CSS comment blocks."""
    iemac = False
    preserve = False
    comment_start = css.find("/*")
    while comment_start >= 0:
        preserve = css[comment_start + 2:comment_start + 3] == "!"
        comment_end = css.find("*/", comment_start + 2)
        if comment_end < 0:
            if not preserve:
                css = css[:comment_start]
                break
        elif comment_end >= (comment_start + 2):
            if css[comment_end - 1] == "\\":
                comment_start = comment_end + 2
                iemac = True
            elif iemac:
                comment_start = comment_end + 2
                iemac = False
            elif not preserve:
                css = css[:comment_start] + css[comment_end + 2:]
            else:
                comment_start = comment_end + 2
        comment_start = css.find("/*", comment_start)
    return css


def remove_unnecessary_whitespace(css):
    """Remove unnecessary whitespace characters."""

    def pseudoclasscolon(css):

        """
        Prevents 'p :link' from becoming 'p:link'.

        Translates 'p :link' into 'p ___PSEUDOCLASSCOLON___link'; this is
        translated back again later.
        """

        regex = re.compile(r"(^|\})(([^\{\:])+\:)+([^\{]*\{)")
        match = regex.search(css)
        while match:
            css = ''.join([
                css[:match.start()],
                match.group().replace(":", "___PSEUDOCLASSCOLON___"),
                css[match.end():]])
            match = regex.search(css)
        return css

    css = pseudoclasscolon(css)
    # Remove spaces from before things.
    css = re.sub(r"\s+([!{};:>+\(\)\],])", r"\1", css)

    # If there is a `@charset`, then only allow one, and move to the beginning.
    css = re.sub(r"^(.*)(@charset \"[^\"]*\";)", r"\2\1", css)
    css = re.sub(r"^(\s*@charset [^;]+;\s*)+", r"\1", css)

    # Put the space back in for a few cases, such as `@media screen` and
    # `(-webkit-min-device-pixel-ratio:0)`.
    css = re.sub(r"\band\(", "and (", css)

    # Put the colons back.
    css = css.replace('___PSEUDOCLASSCOLON___', ':')

    # Remove spaces from after things.
    css = re.sub(r"([!{}:;>+\(\[,])\s+", r"\1", css)
    return css


def remove_unnecessary_semicolons(css):
    """Remove unnecessary semicolons."""
    return re.sub(r";+\}", "}", css)


def remove_empty_rules(css):
    """Remove empty rules."""
    return re.sub(r"[^\}\{]+\{\}", "", css)


def normalize_rgb_colors_to_hex(css):
    """Convert `rgb(51,102,153)` to `#336699`."""
    regex = re.compile(r"rgb\s*\(\s*([0-9,\s]+)\s*\)")
    match = regex.search(css)
    while match:
        colors = map(lambda s: s.strip(), match.group(1).split(","))
        hexcolor = '#%.2x%.2x%.2x' % tuple(map(int, colors))
        css = css.replace(match.group(), hexcolor)
        match = regex.search(css)
    return css


def condense_zero_units(css):
    """Replace `0(px, em, %, etc)` with `0`."""
    return re.sub(r"([\s:])(0)(px|em|%|in|cm|mm|pc|pt|ex)", r"\1\2", css)


def condense_multidimensional_zeros(css):
    """Replace `:0 0 0 0;`, `:0 0 0;` etc. with `:0;`."""
    css = css.replace(":0 0 0 0;", ":0;")
    css = css.replace(":0 0 0;", ":0;")
    css = css.replace(":0 0;", ":0;")
    css = css.replace("background-position:0;", "background-position:0 0;")
    return css


def condense_floating_points(css):
    """Replace `0.6` with `.6` where possible."""
    return re.sub(r"(:|\s)0+\.(\d+)", r"\1.\2", css)


def condense_hex_colors(css):
    """Shorten colors from #AABBCC to #ABC where possible."""
    regex = re.compile(r"([^\"'=\s])(\s*)#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])")
    match = regex.search(css)
    while match:
        first = match.group(3) + match.group(5) + match.group(7)
        second = match.group(4) + match.group(6) + match.group(8)
        if first.lower() == second.lower():
            css = css.replace(match.group(), match.group(1) +
                              match.group(2) + '#' + first)
            match = regex.search(css, match.end() - 3)
        else:
            match = regex.search(css, match.end())
    return css


def condense_whitespace(css):
    """Condense multiple adjacent whitespace characters into one."""
    return re.sub(r"\s+", " ", css)


def condense_semicolons(css):
    """Condense multiple adjacent semicolon characters into one."""
    return re.sub(r";;+", ";", css)


def wrap_css_lines(css, line_length):
    """Wrap the lines of the given CSS to an approximate length."""
    lines = []
    line_start = 0
    for i, char in enumerate(css):
        if char == '}' and (i - line_start >= line_length):
            lines.append(css[line_start:i + 1])
            line_start = i + 1
    if line_start < len(css):
        lines.append(css[line_start:])
    return '\n'.join(lines)


def condense_font_weight(css):
    """Condense multiple font weights into shorter integer equals."""
    return css.replace(':normal;', ':400;').replace(':bold;', ':700;').replace(':lighter;', '100').replace(':bolder;', '900')


def condense_percentage_values(css):
    "Condense multiple percentage value to shorter replacement by taking off 1%"
    return css.replace('100%', '99%').replace('10%', '9%')


def condense_pixel_values(css):
    "Condense multiple pixel values to shorter replacement by taking off 1 px"
    return css.replace('1000px', '999px').replace('100px', '99px').replace('10px', '9px')


def condense_std_named_colors(css):
    "Condense multiple named color values to shorter replacement by using HEX "
    for k, v in iter(list({'aqua': '#0ff', 'black': '#000', 'blue': '#00f',
        'fuchsia': '#f0f', 'white': '#fff', 'yellow': '#ff0'}.items())):
        css = css.replace(k, v)
    return css


def condense_xtra_named_colors(css):
    "Condense multiple named color values to shorter replacement by using HEX "
    for k, v in iter(list(EXTENDED_NAMED_COLORS.items())):
        css = css.replace(k, v)
    return css


def remove_url_quotes(txt):
    ' url() does not need quotes '
    return re.sub(r'url\((["\'])([^)]*)\1\)', r'url(\2)', txt)


def add_encoding(txt):
    ' add @charset "UTF-8"; if missing '
    return '@charset "utf-8";' + txt if '@charset "utf-8";' not in txt.lower() or "@charset 'utf-8';" not in txt.lower() else txt


def cssmin(css, wrap=None):
    css = remove_comments(css)
    css = condense_whitespace(css)
    css = remove_unnecessary_whitespace(css)
    css = remove_unnecessary_semicolons(css)
    css = condense_zero_units(css)
    css = condense_multidimensional_zeros(css)
    css = condense_floating_points(css)
    css = normalize_rgb_colors_to_hex(css)
    css = condense_hex_colors(css)
    if wrap is not None:
        css = wrap_css_lines(css, wrap)
    css = condense_semicolons(css)
    return css.strip()
