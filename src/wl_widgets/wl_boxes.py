# ----------------------------------------------------------------------
# Wordless: Widgets - Boxes
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_utils import wl_misc

# Combo boxes
class Wl_Combo_Box(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setMaxVisibleItems(20)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QComboBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Combo_Box_Adjustable(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

class Wl_Combo_Box_Yes_No(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems([
            self.tr('Yes'),
            self.tr('No')
        ])

class Wl_Combo_Box_Lang(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['langs']))

class Wl_Combo_Box_Encoding(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['file_encodings']))

class Wl_Combo_Box_File_To_Filter(Wl_Combo_Box):
    def __init__(self, parent, table):
        super().__init__(parent)

        self.table = table

        self.table.model().itemChanged.connect(self.table_item_changed)

        self.table_item_changed()

    def table_item_changed(self):
        self.blockSignals(True)

        file_to_filter_old = self.currentText()

        self.clear()

        for file in self.table.settings['file_area']['files_open']:
            if file['selected']:
                self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        self.setCurrentText(file_to_filter_old)

        self.blockSignals(False)

        self.currentTextChanged.emit(self.currentText())

class Wl_Combo_Box_File(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        # Clip long file names
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.addItems(self.main.wl_files.get_selected_file_names())

        self.main.wl_files.table.model().itemChanged.connect(self.wl_files_changed)

        self.wl_files_changed()

    def wl_files_changed(self):
        pass

    def get_file(self):
        return self.main.wl_files.find_file_by_name(self.currentText(), selected_only = True)

class Wl_Combo_Box_Font_Family(QFontComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setMaxVisibleItems(20)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QComboBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Combo_Box_Font_Size(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.FONT_SIZES = {
            'Extra Small': 10,
            'Small': 12,
            'Medium (Recommended)': 14,
            'Large': 16,
            'Extra Large': 18
        }

        self.main = wl_misc.find_wl_main(parent)

        self.addItems(list(self.FONT_SIZES))

    def set_text(self, font_size):
        for text, val in self.FONT_SIZES.items():
            if val == font_size:
                self.setCurrentText(text)

                break

    def get_val(self):
        return self.FONT_SIZES[self.currentText()]

# Spin boxes
class Wl_Spin_Box(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QSpinBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Double_Spin_Box(QDoubleSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QSpinBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Spin_Box_Window(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(-100, 100)

        self.valueChanged.connect(self.value_changed)

    def stepBy(self, steps):
        if self.prefix() == 'L':
            super().stepBy(-steps)
        elif self.prefix() == 'R':
            super().stepBy(steps)

    def value_changed(self):
        if self.value() <= 0:
            if self.prefix() == 'L':
                self.setPrefix('R')
            else:
                self.setPrefix('L')

            self.setValue(-self.value() + 1)

class Wl_Spin_Box_Font_Size(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(8, 72)

# Text browsers
class Wl_Text_Browser(QTextBrowser):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setOpenExternalLinks(True)
        self.setContentsMargins(3, 3, 3, 3)

# Item delegates
class Wl_Item_Delegate_Combo_Box(QStyledItemDelegate):
    def __init__(self, parent, items = [], row = None, col = None, editable = False):
        super().__init__(parent)

        self.items = items
        self.row = row
        self.col = col
        self.enabled = True
        self.editable = editable

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if self.is_editable(index):
            painter.save()

            height = option.rect.height()

            top_right = option.rect.topRight()
            top_right_x = top_right.x()
            top_right_y = top_right.y()

            painter.setBrush(QBrush(QColor(73, 74, 76)))

            painter.drawLine(
                top_right_x - 7 - 8,
                top_right_y + math.ceil((height - 5) / 2),
                top_right_x - 7 - 4,
                top_right_y + math.ceil((height - 5) / 2) + 4
            )
            painter.drawLine(
                top_right_x - 7 - 4,
                top_right_y + math.ceil((height - 5) / 2) + 4,
                top_right_x - 7,
                top_right_y + math.ceil((height - 5) / 2)
            )

            painter.restore()

    def createEditor(self, parent, option, index):
        if self.is_editable(index):
            combo_box = Wl_Combo_Box(parent)
            combo_box.addItems(self.items)

            combo_box.setEditable(self.editable)

            if not self.enabled:
                combo_box.setEnabled(False)

            return combo_box

    def is_editable(self, index):
        rows_editable = cols_editable = False

        if self.row is None or self.row == index.row():
            rows_editable = True
        if self.col is None or self.col == index.column():
            cols_editable = True

        return rows_editable and cols_editable

    def set_enabled(self, enabled):
        self.enabled = enabled

class Wl_Item_Delegate_Combo_Box_Custom(Wl_Item_Delegate_Combo_Box):
    def __init__(self, parent, Combo_Box, row = None, col = None):
        super().__init__(parent, row = row, col = col)

        self.Combo_Box = Combo_Box

    def createEditor(self, parent, option, index):
        if self.is_editable(index):
            combo_box = self.Combo_Box(parent)

            if not self.enabled:
                combo_box.setEnabled(False)

            return combo_box