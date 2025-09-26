import pint
import sys
from PySide2.QtWidgets import (
    QApplication, QPlainTextEdit, QCompleter
)
from PySide2.QtGui import (
    QStandardItemModel, QStandardItem, QSyntaxHighlighter,
    QTextCharFormat, QColor, QFont
)
from PySide2.QtCore import Qt, QRegExp, QTimer, QSignalBlocker

sys.path.append('C:/Develop/STKO/external_solvers')
from opspro.parameters.ParameterManager import ParameterManager

class _expression_gui_utils:
    tooltip_format = (
        "<table style='border-collapse: collapse;'>"
        "<tr>"
        "<td style='text-align: right; font-weight: bold; width: 150px; padding: 4px 8px;'>Input:</td>"
        "<td style='padding: 4px 8px;'>{:.4g~P}</td>"
        "</tr>"
        "<tr>"
        "<td style='text-align: right; font-weight: bold; padding: 4px 8px;'>Value (Base units):</td>"
        "<td style='padding: 4px 8px;'>{:.4g~P}</td>"
        "</tr>"
        "<tr>"
        "<td style='text-align: right; font-weight: bold; padding: 4px 8px;'>Dimensionality:</td>"
        "<td style='padding: 4px 8px;'>{:P}</td>"
        "</tr>"
        "</table>"
    )
    @staticmethod
    def make_tooltip(value: pint.Quantity) -> str:
        bval = value.to_base_units()
        return _expression_gui_utils.tooltip_format.format(value, bval, bval.units.dimensionality)
    @staticmethod
    def make_error_tooltip(msg: str) -> str:
        return f"<span style='color: red; font-weight: bold;'>{msg}</span>"

class ExpressionHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, symbols=None, pwidget : 'ExpressionLineEdit' = None):
        super().__init__(parent)

        # Reference to the parent widget to check for errors
        self._pwidget = pwidget

        # The default formats
        self._default_format = QTextCharFormat()
        self._default_format.setForeground(QColor("black"))
        self._unit_format = QTextCharFormat()
        self._unit_format.setForeground(QColor(50, 100, 200))
        self._symbol_format = QTextCharFormat()
        self._symbol_format.setForeground(QColor(200, 0, 200))
        self._symbol_format.setFontWeight(QFont.Bold)
        self._error_format = QTextCharFormat()
        self._error_format.setForeground(QColor("red"))
        self._error_format.setFontWeight(QFont.Bold)

        # Regex rules
        self._rules = []

        # Units inside [ ... ]
        self._rules.append((QRegExp(r"\[[^\]]+\]"), self._unit_format))

        # Symbols from list
        self._symbols = symbols or []
        if self._symbols:
            pattern = r"\b(" + "|".join(map(QRegExp.escape, self._symbols)) + r")\b"
            self._rules.append((QRegExp(pattern), self._symbol_format))

    def highlightBlock(self, text: str):

        # If there's an error, highlight the whole line in error format
        if self._pwidget and self._pwidget.error:
            self.setFormat(0, len(text), self._error_format)
            return
        
        # Default first
        self.setFormat(0, len(text), self._default_format)

        # Apply rules
        for regex, fmt in self._rules:
            i = regex.indexIn(text, 0)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, fmt)
                i = regex.indexIn(text, i + length)


class ExpressionLineEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Store state
        self._value: pint.Quantity = pint.Quantity(0)
        self._error: str = ""

        # Make it look like a QLineEdit
        self.setPlaceholderText("Enter expression, e.g. 5[m]")
        self.setMaximumHeight(28)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Attach syntax highlighter
        symbols = ParameterManager.getAllSymbols()
        self._highlighter = ExpressionHighlighter(self.document(), symbols=symbols, pwidget=self)

        # Completer
        self._completer = QCompleter(self)
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setWidget(self)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        model = QStandardItemModel(self._completer)
        for w in symbols:
            model.appendRow(QStandardItem(w))
        self._completer.setModel(model)

        # Connections
        self._completer.activated.connect(self.insert_completion)
        self.textChanged.connect(self.evaluate_expression)

    @property
    def value(self) -> pint.Quantity:
        return self._value

    @property
    def error(self) -> str:
        return self._error

    def text(self) -> str:
        return self.toPlainText()

    def setText(self, text: str):
        self.setPlainText(text)

    def evaluate_expression(self):
        try:
            self.blockSignals(True)
            expr = self.text()
            if expr.strip():
                self.eval_set(ParameterManager.evaluate(expr))
            else:
                self.eval_clear()
        except Exception as e:
            self.eval_set_error(str(e))
        finally:
            self._highlighter.rehighlight()
            self.blockSignals(False)

    def eval_clear(self):
        self._value = pint.Quantity(0)
        self._error = ""
        self.setToolTip("")

    def eval_set(self, val: pint.Quantity):
        self._value = val
        self._error = ""
        tooltip_html = _expression_gui_utils.make_tooltip(val)
        self.setToolTip(tooltip_html)

    def eval_set_error(self, msg: str):
        self._value = pint.Quantity(0)
        self._error = msg
        self.setToolTip(_expression_gui_utils.make_error_tooltip(msg))

    def insert_completion(self, completion):
        cursor = self.textCursor()
        cursor.select(cursor.WordUnderCursor)
        cursor.insertText(completion)

    def keyPressEvent(self, event):
        # Force single-line behavior
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            event.ignore()
            return

        # Default behavior
        super().keyPressEvent(event)

        # Completer trigger
        if not self._completer or not self._completer.model():
            return
        cursor = self.textCursor()
        cursor.select(cursor.WordUnderCursor)
        prefix = cursor.selectedText()
        if len(prefix) >= 1:
            self._completer.setCompletionPrefix(prefix)
            rect = self.cursorRect()
            rect.setWidth(
                self._completer.popup().sizeHintForColumn(0)
                + self._completer.popup().verticalScrollBar().sizeHint().width()
            )
            self._completer.complete(rect)
        else:
            self._completer.popup().hide()

app = QApplication(sys.argv)
w = ExpressionLineEdit()
w.show()
sys.exit(app.exec_())
