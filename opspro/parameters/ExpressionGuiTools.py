import pint

from PySide2.QtWidgets import (
    QApplication, QLineEdit, QCompleter,
    QStyleOptionFrame
)
from PySide2.QtGui import (
    QStandardItemModel, QStandardItem,
    QColor, QFontMetrics,
    QPainter, QPalette
)
from PySide2.QtCore import (
    Qt, QRegExp, QEvent, QRect,
    QTimer
)

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
    tooltip_format_ext = (
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
        "<tr>"
        "<td style='text-align: right; font-weight: bold; padding: 4px 8px;'>Quantity:</td>"
        "<td style='padding: 4px 8px;'>{}</td>"
        "</tr>"
        "</table>"
    )
    @staticmethod
    def make_tooltip(value: pint.Quantity) -> str:
        bval = value.to_base_units()
        qstring = ParameterManager.unit_common_quantity_map.get(str(bval.units.dimensionality), None)
        if qstring is not None:
            return _expression_gui_utils.tooltip_format_ext.format(
                value, 
                bval, 
                bval.units.dimensionality,
                qstring)
        else:
            return _expression_gui_utils.tooltip_format.format(
                value, 
                bval, 
                bval.units.dimensionality)
    @staticmethod
    def make_error_tooltip(msg: str) -> str:
        return f"<span style='color: red; font-weight: bold;'>{msg}</span>"

class ExpressionHighlighter:
    """Logic-only syntax highlighter usable on any string."""

    def __init__(self, symbols=None):
        # Define text colors and styles
        # TODO: make configurable
        # TODO: make it static/shared and update it when needed
        self._default_color = QColor("black")
        self._unit_color = QColor(50, 100, 200)
        self._symbol_color = QColor(200, 0, 200)
        self._error_color = QColor("red")

        # Regex rules
        self._rules = []

        # Symbols from list
        if symbols:
            pattern = r"\b(" + "|".join(map(QRegExp.escape, symbols)) + r")\b"
            self._rules.append((QRegExp(pattern), self._symbol_color))

        # Units inside [ ... ]
        self._rules.append((QRegExp(r"\[[^\]]+\]"), self._unit_color))

    def highlight(self, text: str, has_error=False):
        """
        Given text, return a list of (substring, QColor) tuples.
        If has_error=True, all text is red.
        """
        if has_error:
            return [(text, self._error_color)]

        result = []
        last_index = 0

        # Collect matches
        matches = []
        for regex, color in self._rules:
            i = regex.indexIn(text, 0)
            while i >= 0:
                matches.append((i, regex.matchedLength(), color))
                i = regex.indexIn(text, i + regex.matchedLength())

        # Sort by position
        matches.sort(key=lambda m: m[0])

        # Remove overlapping matches (keep first)
        non_overlapping = []
        current_end = -1
        for start, length, color in matches:
            if start >= current_end:
                non_overlapping.append((start, length, color))
                current_end = start + length
            # else: skip because it overlaps

        # Build final segment list
        for start, length, color in non_overlapping:
            if start > last_index:
                result.append((text[last_index:start], self._default_color))
            result.append((text[start:start + length], color))
            last_index = start + length
        if last_index < len(text):
            result.append((text[last_index:], self._default_color))

        # Ensure at least one segment
        if not result:
            result.append((text, self._default_color))

        # done
        return result

class ExpressionLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Store state
        self._value: pint.Quantity = pint.Quantity(0)
        self._error: str = ""

        # initial setup
        self.setPlaceholderText("Enter expression, e.g. 5[m]")
        self.setClearButtonEnabled(True)

        # Attach syntax highlighter
        symbols = ParameterManager.getAllSymbols()

        # Completer
        self._completer = QCompleter(self)
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setWidget(self)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        model = QStandardItemModel(self._completer)
        for w in symbols:
            model.appendRow(QStandardItem(w))
        self._completer.setModel(model)

        # Syntax highlighter helper
        self._highlighter = ExpressionHighlighter(symbols)

        # blinking cursor support
        self._cursor_visible = False
        self._blink_timer = QTimer(self)
        self._blink_timer.setInterval(QApplication.cursorFlashTime() // 2)

        # Connections
        self._completer.activated.connect(self._insert_completion)
        self.textChanged.connect(self._evaluate_expression)
        self._blink_timer.timeout.connect(self._toggle_cursor_visible)
        self.textEdited.connect(self._cursor_blink_restart)
        self.cursorPositionChanged.connect(self._cursor_blink_restart)
        self.selectionChanged.connect(self._cursor_blink_restart)

    @property
    def value(self) -> pint.Quantity:
        return self._value

    @property
    def error(self) -> str:
        return self._error

    def _evaluate_expression(self):
        try:
            expr = self.text()
            if expr.strip():
                self._eval_set(ParameterManager.evaluate(expr))
            else:
                self._eval_clear()
        except Exception as e:
            self._eval_set_error(str(e))

    def _eval_clear(self):
        self._value = pint.Quantity(0)
        self._error = ""
        self.setToolTip("")

    def _eval_set(self, val: pint.Quantity):
        self._value = val
        self._error = ""
        tooltip_html = _expression_gui_utils.make_tooltip(val)
        self.setToolTip(tooltip_html)

    def _eval_set_error(self, msg: str):
        self._value = pint.Quantity(0)
        self._error = msg
        self.setToolTip(_expression_gui_utils.make_error_tooltip(msg))

    def _insert_completion(self, completion):
        # handle the insertion of the selected completion
        text = self.text()
        pos = self.cursorPosition()
        # Find the start of the "word under cursor"
        start = pos
        while start > 0 and (text[start - 1].isalnum() or text[start - 1] in "_."):
            start -= 1
        # Find the end of the word under cursor
        end = pos
        while end < len(text) and (text[end].isalnum() or text[end] in "_."):
            end += 1
        # Replace the word with the completion
        new_text = text[:start] + completion + text[end:]
        self.setText(new_text)
        # Move cursor to the end of inserted completion
        self.setCursorPosition(start + len(completion))

    def _toggle_cursor_visible(self):
        if self.hasFocus():
            self._cursor_visible = not self._cursor_visible
            self.update(self.cursorRect())
        else:
            self._cursor_visible = True  # reset when not focused
    
    def _cursor_blink_stop(self):
        if self._blink_timer.isActive():
            self._blink_timer.stop()
            self._cursor_visible = False
    
    def _cursor_blink_start(self):
        if not self._blink_timer.isActive():
            self._blink_timer.start()
            self._cursor_visible = True
    
    def _cursor_blink_restart(self):
        self._cursor_blink_stop()
        self._cursor_blink_start()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self._cursor_blink_start()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self._cursor_blink_stop()
        self.update()

    def keyPressEvent(self, event):
        try:

            # Force single-line behavior
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                event.ignore()
                return

            # Default QLineEdit behavior
            super().keyPressEvent(event)
            
            # Completer trigger
            if not self._completer or not self._completer.model():
                return
            
            # Find the current "word" (simulate cursor.WordUnderCursor)
            text = self.text()
            pos = self.cursorPosition()
            start = pos
            while start > 0 and (text[start - 1].isalnum() or text[start - 1] in "_."):
                start -= 1
            end = pos
            while end < len(text) and (text[end].isalnum() or text[end] in "_."):
                end += 1
            prefix = text[start:pos]
            if len(prefix) >= 1:
                self._completer.setCompletionPrefix(prefix)
                # Calculate popup position near cursor
                cursor_rect = self.cursorRect()
                popup = self._completer.popup()
                cursor_rect.setWidth(
                    popup.sizeHintForColumn(0)
                    + popup.verticalScrollBar().sizeHint().width()
                )
                self._completer.complete(cursor_rect)
            else:
                self._completer.popup().hide()

        except Exception as e:
            print(f"Error in keyPressEvent: {e}")

    def _paint_cursor(self, painter: QPainter):
        if self.hasFocus():
            cursor_rect = self.cursorRect()
            painter.setRenderHint(QPainter.Antialiasing, False)
            painter.setCompositionMode(QPainter.CompositionMode_Multiply)
            painter.setPen(self.palette().color(QPalette.Text if self._cursor_visible else QPalette.Base))
            cx = cursor_rect.center().x() + 1
            painter.drawLine(cx, cursor_rect.top(), cx, cursor_rect.bottom() - 1)

    def _paint_highlighted_text(self, painter: QPainter):
        # get text
        text = self.text()
        if not text:
            return
        
        # setup painter
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        # init style option
        opt = QStyleOptionFrame()
        self.initStyleOption(opt)

        # before loop: get a reliable background brush
        bg_brush = self.palette().brush(QPalette.Base)
            
        # clip to text area
        contents_rect = self.style().subElementRect(self.style().SE_LineEditContents, opt, self)
        painter.setClipRect(contents_rect)

        # text position
        fm = QFontMetrics(self.font())
        x = contents_rect.left() + 2
        y = contents_rect.bottom() - fm.descent() - 1

        # Selection info
        sel_start = self.selectionStart()
        sel_len = len(self.selectedText())
        sel_end = sel_start + sel_len if sel_len > 0 else -1

        # highlight
        segments = self._highlighter.highlight(text, has_error=bool(self._error))
        text_index = 0
        for token, color in segments:
            token_len = len(token)
            token_start = text_index
            token_end = token_start + token_len
            # If no selection or token fully outside selection
            if sel_len == 0 or token_end <= sel_start or token_start >= sel_end:
                hadv = fm.horizontalAdvance(token)
                if color != QColor("black"):
                    current_rect = QRect(int(x), int(y - fm.ascent()), int(hadv), int(fm.height()))
                    painter.fillRect(current_rect, bg_brush)
                    painter.setPen(color)
                    painter.drawText(x, y, token)
                x += hadv
            else:
                # There is an overlap — split the token visually
                for i, ch in enumerate(token):
                    idx = token_start + i
                    in_selection = sel_start <= idx < sel_end
                    hadv = fm.horizontalAdvance(ch)
                    if not in_selection and color != QColor("black"):
                        current_rect = QRect(int(x), int(y - fm.ascent()), int(hadv), int(fm.height()))
                        painter.fillRect(current_rect, bg_brush)
                        painter.setPen(color)
                        painter.drawText(x, y, ch)
                    x += hadv
            text_index += token_len

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        try:
            self._paint_highlighted_text(painter)
            #self._paint_cursor(painter)
        except Exception as e:
            print(f"Error in paintEvent: {e}")
        finally:
            painter.end()

    def event(self, e):
        # Intercept Tab key before default focus handling
        try:
            if (
                e.type() == QEvent.KeyPress
                and e.key() == Qt.Key_Tab
                and self._completer
                and self._completer.popup()
                and self._completer.popup().isVisible()
            ):
                popup = self._completer.popup()
                index = popup.currentIndex()
                if not index.isValid() and self._completer.completionCount() > 0:
                    # Select first item in the popup
                    first_index = self._completer.completionModel().index(0, 0)
                    popup.setCurrentIndex(first_index)
                self._completer.popup().hide()
                self._completer.activated.emit(self._completer.currentCompletion())
                return True  # mark event as handled
        except Exception as e:
            print(f"Error in event handling: {e}")
        # default behavior
        return super().event(e)



def example_expression_line_edit():
    # get current application
    app = QApplication.instance()
    # make a QDialog with the name of the application as title
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLineEdit
    dialog = QDialog()
    dialog.setWindowTitle(app.applicationName())
    dialog.setLayout(QVBoxLayout())
    w = ExpressionLineEdit()
    # add a 20 point font to the widget
    #font = w.font()
    #font.setPointSize(20)
    #w.setFont(font)
    dialog.layout().addWidget(w)
    dialog.layout().addWidget(QLineEdit())
    # add a spacer
    from PySide2.QtWidgets import QSpacerItem, QSizePolicy
    dialog.layout().addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    # execute the dialog
    dialog.exec_()