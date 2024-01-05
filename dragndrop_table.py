from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt, QMimeData


class DragDropTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.rearrange_cells = True  # if True - empty cells and rows will be deleted after drop event
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setDropIndicatorShown(False)
        self.setSelectionBehavior(QTableWidget.SelectItems)
        self.drag_indicator_row = -1
        self.drag_indicator_col = -1
        self.shift_pressed = False
        self.indicator_color = Qt.red   # drop indicator color
        self.indicator_width = 2  # drop indicator width

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = True
            self.viewport().repaint()
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = False
            self.viewport().repaint()
        else:
            super().keyReleaseEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.drag_indicator_row != -1 and self.drag_indicator_col != -1:
            painter = QPainter(self.viewport())
            painter.setRenderHint(QPainter.Antialiasing)

            # Draw a custom indicator (e.g., a line in InsertMode and Rect in OverwriteMode)
            pen = QPen(self.indicator_color)
            pen.setWidth(self.indicator_width)
            painter.setPen(pen)
            
            rect = self.visualRect(self.model().index(self.drag_indicator_row, self.drag_indicator_col))
            if self.shift_pressed:
                painter.drawLine(rect.topLeft(), rect.topRight())
            else:
                painter.drawRect(rect)

    def mimeData(self, items):
        mime_data = QMimeData()
        text = ""
        for item in items:
            if item:
                text += item.text()
                mime_data.setData('text/plain', text.encode('utf-8'))
                return mime_data

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # Update the custom drag-and-drop indicator position
        self.drag_indicator_row = self.indexAt(event.pos()).row()
        self.drag_indicator_col = self.indexAt(event.pos()).column()

        # Trigger a repaint to update the custom indicator
        self.viewport().repaint()

        if event.mimeData().hasFormat('text/plain'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            # Get the target cell coordinates
            target_index = self.indexAt(event.pos())
            if target_index.isValid():
                # Get the source cell
                source_widget = event.source()
                source_item = source_widget.currentItem()
                if not source_item:
                    return
                source_row = source_item.row()
                source_col = source_item.column()
                target_row = target_index.row()
                target_col = target_index.column()

                if isinstance(source_widget, QTableWidget):
                    # set modifiers
                    insert_mode = event.modifiers() & Qt.ShiftModifier
                    copy_mode = event.modifiers() & Qt.AltModifier
                    if not copy_mode:
                        source_item = self.takeItem(source_row, source_col)
                    if insert_mode:
                        # Insert a row within the column where data is dropped
                        self.insertRow(target_row)
                        # Set the text and data in the dropped cell
                        target_item = QTableWidgetItem(source_item.text())
                        target_item.setData(Qt.UserRole, source_item.data(Qt.UserRole))
                        self.setItem(target_row, target_col, target_item)
                    else:
                        # Set the text and data from the source to the target cell
                        target_item = QTableWidgetItem(source_item.text())
                        target_item.setData(Qt.UserRole, source_item.data(Qt.UserRole))  # Copy user data
                        self.setItem(target_row, target_col, target_item)

                    if self.rearrange_cells:
                        self.remove_empty_cells()
        else:
            event.ignore()

        # delete indicator after drop event
        self.drag_indicator_row = -1
        self.drag_indicator_col = -1
        self.viewport().repaint()

    def remove_empty_cells(self):
        # remove empty cells in every column
        for col in range(self.columnCount()):
            items = reversed([self.takeItem(row, col) for row in range(self.rowCount(), -1, -1)])  # get column items list
            sorted_items = sorted(items, key=lambda x: x is None)  # move None items to the end
            for row, item in enumerate(sorted_items):
                self.setItem(row, col, item)

        # remove empty rows
        for row in range(self.rowCount()):
            items = [self.item(row, col) for col in range(self.columnCount())]  # get row items list
            is_empty = all([item is None for item in items])  # check all cells in row are empty
            if is_empty:
                self.removeRow(row)

