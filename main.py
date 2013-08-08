# -*- coding: utf-8 -*-
# PEP8:NO, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" Ninja Web Util "
__version__ = ' 0.8 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 15/08/2013 '
__prj__ = ' webutil '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import path
from sip import setapi
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen  # lint:ok


from PyQt4.QtGui import (QLabel, QCompleter, QDirModel, QPushButton, QWidget,
  QFileDialog, QDockWidget, QVBoxLayout, QCursor, QLineEdit, QIcon, QGroupBox,
  QCheckBox, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QColor, QComboBox,
  QApplication, QMessageBox, QScrollArea, QProgressBar)

from PyQt4.QtCore import Qt, QDir

try:
    from PyKDE4.kdeui import KTextEdit as QPlainTextEdit
except ImportError:
    from PyQt4.QtGui import QPlainTextEdit  # lint:ok

from ninja_ide.gui.explorer.explorer_container import ExplorerContainer
from ninja_ide.core import plugin

from css_minifica import *
from html_minifica import *
from js_minifica import *


# API 2
(setapi(a, 2) for a in ("QDate", "QDateTime", "QString", "QTime", "QUrl",
                        "QTextStream", "QVariant"))


# constans
HELPMSG = '''
<h3>Ninja Web Util</h3>
This is an HTML5/CSS3/JS Optimizer Non-Obfuscating Compressor tool for Ninja.
<ul>
<li>Average compress better than YUI Compressor
<li>The only tool to remove optional HTML tags
<li>The only tool to compress HTML tags
<li>The only tool to compress Percentage/Pixel CSS values
<li>Does Not Obfuscate JS (its a feature or a bug, you decide)
</ul>
<br><br>
''' + ''.join((__doc__, __version__, __license__, 'by', __author__, __email__))

SAMPLE_TEXT = '''
/* -----------------------------------------------------------------------------
####################TEST SAMPLE, THIS COMMENT WILL BE REMOVED###################
----------------------------------------------------------------------------- */


.chun.li  {
    color:       rgb(255, 255, 255);
    width:       100%;
    height:      1000px;
    font-weight: normal;
    backgroud:   url("example.com/img.gif");
    color:       #00ff00;
    line-height: 0.5;
    border:      0px solid yellow;
}   ;;


empty.selector.will.be.removed {}

/*--------------------------------------------------------------------------- */
'''


###############################################################################


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        ec = ExplorerContainer()
        super(Main, self).initialize(*args, **kwargs)

        self.editor_s = self.locator.get_service('editor')
        # directory auto completer
        self.completer = QCompleter(self)
        self.dirs = QDirModel(self)
        self.dirs.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.completer.setModel(self.dirs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)

        self.group0 = QGroupBox()
        self.group0.setTitle(' Source ')
        self.source = QComboBox()
        self.source.addItems(['Clipboard', 'Local File', 'Remote URL', 'Ninja'])
        self.source.currentIndexChanged.connect(self.on_source_changed)
        self.infile = QLineEdit(path.expanduser("~"))
        self.infile.setPlaceholderText(' /full/path/to/file.html ')
        self.infile.setCompleter(self.completer)
        self.open = QPushButton(QIcon.fromTheme("folder-open"), 'Open')
        self.open.setCursor(QCursor(Qt.PointingHandCursor))
        self.open.clicked.connect(lambda: self.infile.setText(str(
            QFileDialog.getOpenFileName(self.dock, "Open a File to read from",
            path.expanduser("~"), ';;'.join(['{}(*.{})'.format(e.upper(), e)
            for e in ['css', 'html', 'js', 'txt', '*']])))))
        self.inurl = QLineEdit('http://www.')
        self.inurl.setPlaceholderText('http://www.full/url/to/remote/file.html')
        self.output = QPlainTextEdit(SAMPLE_TEXT)
        vboxg0 = QVBoxLayout(self.group0)
        for each_widget in (self.source, self.infile, self.open, self.inurl,
            self.output, ):
            vboxg0.addWidget(each_widget)
        [a.hide() for a in iter((self.infile, self.open, self.inurl))]

        self.group1 = QGroupBox()
        self.group1.setTitle(' CSS3 ')
        self.group1.setCheckable(True)
        self.group1.setGraphicsEffect(QGraphicsBlurEffect(self))
        self.group1.graphicsEffect().setEnabled(False)
        self.group1.toggled.connect(self.toggle_css_group)
        self.ckcss1 = QCheckBox('Remove unnecessary Comments')
        self.ckcss2 = QCheckBox('Remove unnecessary Whitespace characters')
        self.ckcss3 = QCheckBox('Remove unnecessary Semicolons')
        self.ckcss4 = QCheckBox('Remove unnecessary Empty rules')
        self.ckcss5 = QCheckBox('Condense and Convert Colors from RGB to HEX')
        self.ckcss6 = QCheckBox('Condense all Zero units')
        self.ckcss7 = QCheckBox('Condense Multidimensional Zero units')
        self.ckcss8 = QCheckBox('Condense Floating point numbers')
        self.ckcss9 = QCheckBox('Condense HEX Colors')
        self.ckcss10 = QCheckBox('Condense multiple adjacent Whitespace chars')
        self.ckcss11 = QCheckBox('Condense multiple adjacent semicolon chars')
        self.ckcss12 = QCheckBox('Wrap the lines of the to 80 character length')
        self.ckcss13 = QCheckBox('Condense Font Weight values')
        self.ckcss14 = QCheckBox('Condense the 17 Standard Named Colors values')
        self.ckcss15 = QCheckBox('Condense the 124 Extra Named Colors values')
        self.ckcss16 = QCheckBox('Condense all Percentages values when posible')
        self.ckcss17 = QCheckBox('Condense all Pixels values when posible')
        self.ckcss18 = QCheckBox('Remove unnecessary quotes from url()')
        self.ckcss19 = QCheckBox('Add standard Encoding Declaration if missing')
        vboxg1 = QVBoxLayout(self.group1)
        for each_widget in (self.ckcss1, self.ckcss2, self.ckcss3, self.ckcss4,
            self.ckcss5, self.ckcss6, self.ckcss7, self.ckcss8, self.ckcss9,
            self.ckcss10, self.ckcss11, self.ckcss12, self.ckcss13,
            self.ckcss14, self.ckcss15, self.ckcss16, self.ckcss17,
            self.ckcss18, self.ckcss19):
            vboxg1.addWidget(each_widget)
            each_widget.setToolTip(each_widget.text())

        self.group2 = QGroupBox()
        self.group2.setTitle(' HTML5 ')
        self.group2.setCheckable(True)
        self.group2.setGraphicsEffect(QGraphicsBlurEffect(self))
        self.group2.graphicsEffect().setEnabled(False)
        self.group2.toggled.connect(self.toggle_html_group)
        self.ckhtml0 = QCheckBox('Condense Style and Script HTML Tags')
        self.ckhtml1 = QCheckBox('Condense DOCTYPE to new HTML5 Tags')
        self.ckhtml2 = QCheckBox('Condense Href and Src to protocol agnostic')
        self.ckhtml4 = QCheckBox('Remove unnecessary Tags but keep HTML valid')
        self.help1 = QLabel('''<a href=
            "https://developers.google.com/speed/articles/optimizing-html">
            <small><center>Help about Unneeded Unnecessary HTML tags ?</a>''')
        self.help1.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.help1.setOpenExternalLinks(True)
        vboxg2 = QVBoxLayout(self.group2)
        for each_widget in (self.ckhtml0, self.ckhtml1, self.ckhtml2,
            self.ckhtml4, self.help1, ):
            vboxg2.addWidget(each_widget)
            each_widget.setToolTip(each_widget.text())

        self.group3 = QGroupBox()
        self.group3.setTitle(' Javascript ')
        self.ckjs0 = QCheckBox('Condense and Compress Javascript')
        self.ckjs1 = QCheckBox('Condense $(document).ready(function(){ });')
        vboxg2 = QVBoxLayout(self.group3)
        for each_widget in (self.ckjs0, self.ckjs1):
            vboxg2.addWidget(each_widget)
            each_widget.setToolTip(each_widget.text())

        self.group4 = QGroupBox()
        self.group4.setTitle(' General ')
        self.chckbx1 = QCheckBox('Lower case ALL the text')
        self.chckbx2 = QCheckBox('Remove Spaces, Tabs, New Lines, Empty Lines')
        self.befor, self.after = QProgressBar(), QProgressBar()
        self.befor.setFormat("%v Chars")
        self.after.setFormat("%v Chars")
        vboxg4 = QVBoxLayout(self.group4)
        for each_widget in (self.chckbx1, self.chckbx2,
            QLabel('<b>Before:'), self.befor, QLabel('<b>After:'), self.after):
            vboxg4.addWidget(each_widget)
            each_widget.setToolTip(each_widget.text())

        [a.setChecked(True) for a in iter((self.ckcss1, self.ckcss2,
            self.ckcss3, self.ckcss4, self.ckcss5, self.ckcss6, self.ckcss7,
            self.ckcss8, self.ckcss9, self.ckcss10, self.ckcss11, self.ckcss12,
            self.ckcss13, self.ckcss14, self.ckcss15, self.ckcss16,
            self.ckcss17, self.ckcss18, self.ckcss19, self.ckjs1, self.ckhtml0,
            self.ckhtml1, self.ckhtml2, self.ckhtml4, self.chckbx1,
            self.chckbx2))]

        self.button = QPushButton(QIcon.fromTheme("face-cool"), 'Process Text')
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setMinimumSize(100, 50)
        self.button.clicked.connect(self.run)

        def must_glow(widget_list):
            ' apply an glow effect to the widget '
            for glow, each_widget in enumerate(widget_list):
                try:
                    if each_widget.graphicsEffect() is None:
                        glow = QGraphicsDropShadowEffect(self)
                        glow.setOffset(0)
                        glow.setBlurRadius(99)
                        glow.setColor(QColor(99, 255, 255))
                        each_widget.setGraphicsEffect(glow)
                        glow.setEnabled(True)
                except:
                    pass

        must_glow((self.button, ))

        class TransientWidget(QWidget):
            ' persistant widget thingy '
            def __init__(self, widget_list):
                ' init sub class '
                super(TransientWidget, self).__init__()
                vbox = QVBoxLayout(self)
                for each_widget in widget_list:
                    vbox.addWidget(each_widget)

        tw = TransientWidget((QLabel('<b>HTML5/CSS3/JS Optimizer Compressor'),
            self.group0, self.group1, self.group2, self.group3, self.group4,
            self.button, ))
        self.scrollable = QScrollArea()
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setWidget(tw)
        self.dock = QDockWidget()
        self.dock.setWindowTitle(__doc__)
        self.dock.setStyleSheet('QDockWidget::title{text-align: center;}')
        self.dock.setMinimumWidth(350)
        self.dock.setWidget(self.scrollable)
        ec.addTab(self.dock, "Web")
        QPushButton(QIcon.fromTheme("help-about"), 'About', self.dock
          ).clicked.connect(lambda: QMessageBox.information(self.dock, __doc__,
            HELPMSG))

    def run(self):
        ' run the string replacing '
        if self.source.currentText() == 'Local File':
            with open(path.abspath(str(self.infile.text()).strip()), 'r') as f:
                txt = f.read()
        elif self.source.currentText() == 'Remote URL':
            txt = urlopen(str(self.inurl.text()).strip()).read()
        elif  self.source.currentText() == 'Clipboard':
            txt = str(self.output.toPlainText()) if str(self.output.toPlainText()) is not '' else str(QApplication.clipboard().text())
        else:
            txt = self.editor_s.get_text()
        self.output.clear()
        self.befor.setMaximum(len(txt) + 10)
        self.after.setMaximum(len(txt) + 10)
        self.befor.setValue(len(txt))
        txt = txt.lower() if self.chckbx1.isChecked() is True else txt
        txt = condense_style(txt) if self.ckhtml0.isChecked() is True else txt
        txt = condense_script(txt) if self.ckhtml0.isChecked() is True else txt
        txt = condense_doctype(txt) if self.ckhtml1.isChecked() is True else txt
        txt = condense_href_src(txt) if self.ckhtml2 is True else txt
        txt = clean_unneeded_tags(txt) if self.ckhtml4.isChecked() is True else txt
        txt = condense_doc_ready(txt) if self.ckjs1.isChecked() is True else txt
        txt = jsmin(txt) if self.ckjs0.isChecked() is True else txt
        txt = remove_comments(txt) if self.ckcss1.isChecked() is True else txt
        txt = condense_whitespace(txt) if self.ckcss10.isChecked() is True else txt
        txt = remove_empty_rules(txt) if self.ckcss4.isChecked() is True else txt
        txt = remove_unnecessary_whitespace(txt) if self.ckcss2.isChecked() is True else txt
        txt = remove_unnecessary_semicolons(txt) if self.ckcss3.isChecked() is True else txt
        txt = condense_zero_units(txt) if self.ckcss6.isChecked() is True else txt
        txt = condense_multidimensional_zeros(txt) if self.ckcss7.isChecked() is True else txt
        txt = condense_floating_points(txt) if self.ckcss8.isChecked() is True else txt
        txt = normalize_rgb_colors_to_hex(txt) if self.ckcss5.isChecked() is True else txt
        txt = condense_hex_colors(txt) if self.ckcss9.isChecked() is True else txt
        txt = wrap_css_lines(txt, 80) if self.ckcss12.isChecked() is True else txt
        txt = condense_semicolons(txt) if self.ckcss11.isChecked() is True else txt
        txt = condense_font_weight(txt) if self.ckcss13.isChecked() is True else txt
        txt = condense_std_named_colors(txt) if self.ckcss14.isChecked() is True else txt
        # txt = condense_xtra_named_colors(txt) if self.ckcss14.isChecked() is True else txt  # FIXME
        txt = condense_percentage_values(txt) if self.ckcss16.isChecked() is True else txt
        txt = condense_pixel_values(txt) if self.ckcss17.isChecked() is True else txt
        txt = remove_url_quotes(txt) if self.ckcss18.isChecked() is True else txt
        txt = add_encoding(txt) if self.ckcss19.isChecked() is True else txt
        txt = " ".join(txt.strip().split()) if self.chckbx2.isChecked() is True else txt
        self.after.setValue(len(txt))
        self.output.setPlainText(txt)
        self.output.show()
        self.output.setFocus()
        self.output.selectAll()

    def on_source_changed(self):
        ' do something when the desired source has changed '
        if self.source.currentText() == 'Local File':
            self.open.show()
            self.infile.show()
            self.inurl.hide()
            self.output.hide()
        elif  self.source.currentText() == 'Remote URL':
            self.inurl.show()
            self.open.hide()
            self.infile.hide()
            self.output.hide()
        elif  self.source.currentText() == 'Clipboard':
            self.output.show()
            self.open.hide()
            self.infile.hide()
            self.inurl.hide()
            self.output.setText(QApplication.clipboard().text())
        else:
            self.output.show()
            self.open.hide()
            self.infile.hide()
            self.inurl.hide()
            self.output.setText(self.editor_s.get_text())

    def toggle_css_group(self):
        ' toggle on or off the css checkboxes '
        if self.group1.isChecked() is True:
            [a.setChecked(True) for a in iter((self.ckcss1, self.ckcss2,
            self.ckcss3, self.ckcss4, self.ckcss5, self.ckcss6, self.ckcss7,
            self.ckcss8, self.ckcss9, self.ckcss10, self.ckcss11, self.ckcss12,
            self.ckcss13, self.ckcss14, self.ckcss15, self.ckcss16,
            self.ckcss17, self.ckcss18, self.ckcss19))]
            self.group1.graphicsEffect().setEnabled(False)
        else:
            [a.setChecked(False) for a in iter((self.ckcss1, self.ckcss2,
            self.ckcss3, self.ckcss4, self.ckcss5, self.ckcss6, self.ckcss7,
            self.ckcss8, self.ckcss9, self.ckcss10, self.ckcss11, self.ckcss12,
            self.ckcss13, self.ckcss14, self.ckcss15, self.ckcss16,
            self.ckcss17, self.ckcss18, self.ckcss19))]
            self.group1.graphicsEffect().setEnabled(True)

    def toggle_html_group(self):
        ' toggle on or off the css checkboxes '
        if self.group2.isChecked() is True:
            [a.setChecked(True) for a in iter((self.ckhtml0, self.ckhtml1,
                                               self.ckhtml2, self.ckhtml4))]
            self.group2.graphicsEffect().setEnabled(False)
        else:
            [a.setChecked(False) for a in iter((self.ckhtml0, self.ckhtml1,
                                                self.ckhtml2, self.ckhtml4))]
            self.group2.graphicsEffect().setEnabled(True)


###############################################################################


if __name__ == "__main__":
    print(__doc__)
