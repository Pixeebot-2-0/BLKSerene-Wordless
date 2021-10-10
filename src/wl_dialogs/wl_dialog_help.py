#
# Wordless: Dialogs - Help
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import csv
import platform
import re

import openpyxl
import requests

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialog
from wl_utils import wl_misc, wl_threading
from wl_widgets import wl_box, wl_label, wl_layout, wl_table

class Wl_Dialog_Citing(wl_dialog.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Citing'),
                         width = 450,
                         no_buttons = True)

        self.label_citing = wl_label.Wl_Label_Dialog(
            self.tr('''
                <div>
                    If you publish work that uses Wordless, please cite as follows.
                </div>
            '''),
            self
        )

        self.label_citation_sys = QLabel(self.tr('Citation System:'), self)
        self.combo_box_citation_sys = wl_box.Wl_Combo_Box(self)
        self.text_edit_citing = QTextEdit(self)
    
        self.button_copy = QPushButton(self.tr('Copy'), self)
        self.button_close = QPushButton(self.tr('Close'), self)
    
        self.combo_box_citation_sys.addItems([
            self.tr('APA (7th Edition)'),
            self.tr('MLA (8th Edition)')
        ])
    
        self.button_copy.setFixedWidth(100)
        self.button_close.setFixedWidth(100)
    
        self.text_edit_citing.setFixedHeight(100)
        self.text_edit_citing.setReadOnly(True)
    
        self.combo_box_citation_sys.currentTextChanged.connect(self.citation_sys_changed)
    
        self.button_copy.clicked.connect(self.copy)
        self.button_close.clicked.connect(self.accept)
    
        layout_citation_sys = wl_layout.Wl_Layout()
        layout_citation_sys.addWidget(self.label_citation_sys, 0, 0)
        layout_citation_sys.addWidget(self.combo_box_citation_sys, 0, 1)
    
        layout_citation_sys.setColumnStretch(2, 1)
    
        self.wrapper_info.layout().addWidget(self.label_citing, 0, 0, 1, 2)
        self.wrapper_info.layout().addLayout(layout_citation_sys, 1, 0, 1, 2)
        self.wrapper_info.layout().addWidget(self.text_edit_citing, 2, 0, 1, 2)
    
        self.wrapper_buttons.layout().addWidget(self.button_copy, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_close, 0, 1)

        self.load_settings()

        self.set_fixed_height()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['citing'])

        self.combo_box_citation_sys.setCurrentText(settings['citation_sys'])

        self.citation_sys_changed()

    def citation_sys_changed(self):
        settings = self.main.settings_custom['menu']['help']['citing']

        settings['citation_sys'] = self.combo_box_citation_sys.currentText()

        if settings['citation_sys'] == self.tr('APA (7th Edition)'):
            self.text_edit_citing.setHtml(f'Ye, L. (2021). <i>Wordless</i> (Version {self.main.ver}) [Computer software]. Github. https://github.com/BLKSerene/Wordless')
        elif settings['citation_sys'] == self.tr('MLA (8th Edition)'):
            self.text_edit_citing.setHtml(f'Ye Lei. <i>Wordless</i>, version {self.main.ver}, 2021. <i>Github</i>, https://github.com/BLKSerene/Wordless.')

    def copy(self):
        self.text_edit_citing.setFocus()
        self.text_edit_citing.selectAll()
        self.text_edit_citing.copy()

class Wl_Dialog_Acks(wl_dialog.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Acknowledgments'),
                         width = 650)

        self.label_acks = wl_label.Wl_Label_Dialog(
            self.tr('''
                <div>
                    I would like to extend my sincere gratitude to the following open-source projects without which this project would not have been possible:
                </div>
            '''),
            self
        )
        self.table_acks = wl_table.Wl_Table(
            self,
            headers = [
                self.tr('Name'),
                self.tr('Version'),
                self.tr('Authors'),
                self.tr('License')
            ]
        )

        self.table_acks.setFixedHeight(300)

        self.wrapper_info.layout().addWidget(self.label_acks, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_acks, 1, 0)

        self.set_fixed_height()

        # Load acknowledgments
        acks = []

        workbook = openpyxl.load_workbook('wl_acks.xlsx')
        worksheet = workbook[workbook.sheetnames[0]]

        for i, rows in enumerate(worksheet.rows):
            if i > 0:
                name = rows[0].value
                home_page = rows[1].value
                ver = str(rows[2].value)
                authors = rows[3].value.replace('\n', '<br>')
                license = rows[4].value
                license_url = rows[5].value

                acks.append([name, home_page, ver, authors, license, license_url])

        self.table_acks.clear_table()

        self.table_acks.blockSignals(True)
        self.table_acks.setUpdatesEnabled(False)

        self.table_acks.setRowCount(len(acks))

        for i, (name, home_page, ver, authors, license, licence_url) in enumerate(acks):
            name = f'<a href="{home_page}">{name}</a>'
            license = f'<a href="{licence_url}">{license}</a>'

            # Pad cells with whitespace
            name = name.replace('<br>', '&nbsp;<br>&nbsp;')
            ver = ver.replace('<br>', '&nbsp;<br>&nbsp;')
            authors = authors.replace('<br>', '&nbsp;<br>&nbsp;')
            license = license.replace('<br>', '&nbsp;<br>&nbsp;')

            name = f'&nbsp;{name}&nbsp;'
            ver = f'&nbsp;{ver}&nbsp;'
            authors = f'&nbsp;{authors}&nbsp;'
            license = f'&nbsp;{license}&nbsp;'

            self.table_acks.setCellWidget(i, 0, wl_label.Wl_Label_Html(name, self))
            self.table_acks.setCellWidget(i, 1, wl_label.Wl_Label_Html_Centered(ver, self))
            self.table_acks.setCellWidget(i, 2, wl_label.Wl_Label_Html(authors, self))
            self.table_acks.setCellWidget(i, 3, wl_label.Wl_Label_Html_Centered(license, self))

        self.table_acks.blockSignals(False)
        self.table_acks.setUpdatesEnabled(True)

class Wl_Dialog_Need_Help(wl_dialog.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Need Help?'),
                         width = 550,
                         height = 450)

        self.label_need_help = wl_label.Wl_Label_Dialog(
            self.tr('''
                <div>
                    If you encounter a problem, find a bug, or require any further information, feel free to ask questions, submit bug reports, or provide feedback by <a href="https://github.com/BLKSerene/Wordless/issues/new">creating an issue</a> on Github if you fail to find the answer by searching <a href="https://github.com/BLKSerene/Wordless/issues">existing issues</a> first.
                </div>

                <div>
                    If you need to post sample texts or other information that cannot be shared or you do not want to share publicly, you may send me an email.
                </div>
            '''),
            self
        )

        self.table_need_help = wl_table.Wl_Table(
            self,
            headers = [
                self.tr('Channel'),
                self.tr('Contact Information')
            ],
            cols_stretch = [
                self.tr('Contact Information')
            ]
        )

        self.table_need_help.setFixedHeight(300)
        self.table_need_help.setRowCount(3)
        self.table_need_help.verticalHeader().setHidden(True)

        self.table_need_help.setCellWidget(0, 0, wl_label.Wl_Label_Html_Centered(self.tr('Documentation'), self))
        self.table_need_help.setCellWidget(0, 1, wl_label.Wl_Label_Html('<a href="https://github.com/BLKSerene/Wordless#documentation">https://github.com/BLKSerene/Wordless#documentation</a>', self))
        self.table_need_help.setCellWidget(1, 0, wl_label.Wl_Label_Html_Centered(self.tr('Email'), self))
        self.table_need_help.setCellWidget(1, 1, wl_label.Wl_Label_Html(self.main.email_html, self))
        self.table_need_help.setCellWidget(2, 0, wl_label.Wl_Label_Html_Centered(self.tr('<a href="https://www.wechat.com/en/">WeChat</a><br>Official Account'), self))
        self.table_need_help.setCellWidget(2, 1, wl_label.Wl_Label_Html_Centered('<img src="imgs/wechat_official_account.jpg">', self))

        self.wrapper_info.layout().addWidget(self.label_need_help, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_need_help, 1, 0)

class Wl_Dialog_Donating(wl_dialog.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('Donating'),
                         width = 450)

        self.label_donating = wl_label.Wl_Label_Dialog(
            self.tr('''
                <div>
                    If you would like to support the development of Wordless, you may donate via <a href="https://www.paypal.com/">PayPal</a>, <a href="https://global.alipay.com/">Alipay</a>, or <a href="https://pay.weixin.qq.com/index.php/public/wechatpay_en">WeChat Pay</a>.
                </div>
            '''),
            self
        )
        self.label_donating_via = QLabel(self.tr('Donating via:'), self)
        self.combo_box_donating_via = wl_box.Wl_Combo_Box(self)
        self.label_donating_via_img = wl_label.Wl_Label_Html('', self)

        self.combo_box_donating_via.addItems([
            self.tr('PayPal'),
            self.tr('Alipay'),
            self.tr('WeChat Pay')
        ])

        self.combo_box_donating_via.currentTextChanged.connect(self.donating_via_changed)

        layout_donating_via = wl_layout.Wl_Layout()
        layout_donating_via.addWidget(self.label_donating_via, 0, 0)
        layout_donating_via.addWidget(self.combo_box_donating_via, 0, 1)

        layout_donating_via.setColumnStretch(2, 1)

        self.wrapper_info.layout().addWidget(self.label_donating, 0, 0)
        self.wrapper_info.layout().addLayout(layout_donating_via, 1, 0)
        self.wrapper_info.layout().addWidget(self.label_donating_via_img, 2, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        # Calculate height
        donating_via_old = self.main.settings_custom['menu']['help']['donating']['donating_via']

        self.combo_box_donating_via.setCurrentText('PayPal')
        self.donating_via_changed()

        height_donating_via_paypal = self.label_donating_via_img.sizeHint().height()
        self.height_paypal = self.heightForWidth(self.width())

        self.combo_box_donating_via.setCurrentText('Alipay')
        self.donating_via_changed()

        height_donating_via_alipay = self.label_donating_via_img.sizeHint().height()
        self.height_alipay = self.heightForWidth(self.width()) + (height_donating_via_alipay - height_donating_via_paypal)

        self.main.settings_custom['menu']['help']['donating']['donating_via'] = donating_via_old

        self.load_settings()

    def load_settings(self):
        settings = copy.deepcopy(self.main.settings_custom['menu']['help']['donating'])

        self.combo_box_donating_via.setCurrentText(settings['donating_via'])

        self.donating_via_changed()

    def donating_via_changed(self):
        settings = self.main.settings_custom['menu']['help']['donating']

        settings['donating_via'] = self.combo_box_donating_via.currentText()

        if settings['donating_via'] == self.tr('PayPal'):
            self.label_donating_via_img.setText('<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32"><img src="imgs/donating_paypal.gif"></a>')
        elif settings['donating_via'] == self.tr('Alipay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_alipay.png">')
        elif settings['donating_via'] == self.tr('WeChat Pay'):
            self.label_donating_via_img.setText('<img src="imgs/donating_wechat_pay.png">')

        if 'height_alipay' in self.__dict__:
            if settings['donating_via'] == self.tr('PayPal'):
                self.setFixedHeight(self.height_paypal)
            elif settings['donating_via'] in [self.tr('Alipay'), self.tr('WeChat Pay')]:
                self.setFixedHeight(self.height_alipay)

        if platform.system() in ['Windows', 'Linux']:
            self.move_to_center()

class Worker_Check_Updates(QObject):
    worker_done = pyqtSignal(str, str)

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.stopped = False

    def run(self):
        ver_new = ''

        try:
            r = requests.get('https://raw.githubusercontent.com/BLKSerene/Wordless/master/src/VERSION', timeout = 10)

            if r.status_code == 200:
                for line in r.text.splitlines():
                    if line and not line.startswith('#'):
                        ver_new = line.rstrip()

                if self.is_newer_version(ver_new):
                    updates_status = 'updates_available'
                else:
                    updates_status = 'no_updates'
            else:
                updates_status = 'network_error'
        except Exception as e:
            print('Warning: An error occurred when checking for updates!')
            print(f'Error: {e}')

            updates_status = 'network_error'

        if self.stopped:
            updates_status == 'canceled'

        self.worker_done.emit(updates_status, ver_new)

    def is_newer_version(self, ver_new):
        ver_major_new, ver_minor_new, ver_patch_new = wl_misc.split_wl_ver(ver_new)

        if (self.main.ver_major < ver_major_new or
            self.main.ver_minor < ver_minor_new or
            self.main.ver_patch < ver_patch_new):
            return True
        else:
            return False

    def stop(self):
        self.stopped = True

class Wl_Dialog_Check_Updates(wl_dialog.Wl_Dialog_Info):
    def __init__(self, main, on_startup = False):
        super().__init__(main, main.tr('Check for Updates'),
                         width = 420,
                         no_buttons = True)

        self.on_startup = on_startup

        self.label_check_updates = wl_label.Wl_Label_Dialog('', self)
        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for updates on startup'), self)
        
        self.button_try_again = QPushButton(self.tr('Try Again'), self)
        self.button_cancel = QPushButton(self.tr('Cancel'), self)

        self.checkbox_check_updates_on_startup.stateChanged.connect(self.check_updates_on_startup_changed)

        self.button_try_again.clicked.connect(self.check_updates)

        self.wrapper_info.layout().addWidget(self.label_check_updates, 0, 0)

        self.wrapper_buttons.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_try_again, 0, 2)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 3)

        self.wrapper_buttons.layout().setColumnStretch(1, 1)

        self.load_settings()

        self.set_fixed_height()

    def check_updates(self):
        self.updates_status_changed('checking')

        self.main.worker_check_updates = Worker_Check_Updates(self.main)
        thread_check_updates = wl_threading.Wl_Thread(self.main.worker_check_updates)

        self.main.threads_check_updates.append(thread_check_updates)

        thread_check_updates.destroyed.connect(lambda: self.main.threads_check_updates.remove(thread_check_updates))

        if self.on_startup:
            self.main.worker_check_updates.worker_done.connect(self.updates_status_changed_on_startup)

        self.main.worker_check_updates.worker_done.connect(self.updates_status_changed)
        self.main.worker_check_updates.worker_done.connect(thread_check_updates.quit)
        self.main.worker_check_updates.worker_done.connect(self.main.worker_check_updates.deleteLater)

        thread_check_updates.start()

    def check_updates_stopped(self):
        self.main.worker_check_updates.stop()

        self.reject()

    def updates_status_changed(self, status, ver_new = ''):
        if status == 'checking':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    Checking for updates...<br>
                    Please wait, it may take a few seconds.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('Cancel'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.check_updates_stopped)
        elif status == 'no_updates':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    Hooray, you are using the latest version of Wordless!
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'updates_available':
            self.label_check_updates.set_text(self.tr(f'''
                <div>
                    Wordless v{ver_new} is out, click <a href="https://github.com/BLKSerene/Wordless/releases/tag/v{ver_new}"><b>HERE</b></a> to download the latest version of Wordless.
                </div>
            '''))

            self.button_try_again.hide()
            self.button_cancel.setText(self.tr('OK'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)
        elif status == 'network_error':
            self.label_check_updates.set_text(self.tr('''
                <div>
                    A network error occurred, please check your network settings and try again or <a href="https://github.com/BLKSerene/Wordless/releases">manually check for updates</a>.
                </div>
            '''))

            self.button_try_again.show()
            self.button_cancel.setText(self.tr('Close'))

            self.button_cancel.disconnect()
            self.button_cancel.clicked.connect(self.accept)

    def updates_status_changed_on_startup(self, status):
        if status == 'updates_available':
            self.open()
            self.setFocus()
        else:
            self.accept()

    def load_settings(self):
        settings = self.main.settings_custom['general']['update_settings']

        self.checkbox_check_updates_on_startup.setChecked(settings['check_updates_on_startup'])

        self.check_updates()

    def check_updates_on_startup_changed(self):
        settings = self.main.settings_custom['general']['update_settings']

        settings['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

class Wl_Dialog_Changelog(wl_dialog.Wl_Dialog_Info):
    def __init__(self, main):
        changelog = []

        try:
            with open('CHANGELOG.md', 'r', encoding = 'utf_8') as f:
                for line in f:
                    # Changelog headers
                    if line.startswith('## '):
                        release_ver = re.search(r'(?<=\[)[^\]]+?(?=\])', line).group()
                        release_link = re.search(r'(?<=\()[^\)]+?(?=\))', line).group()
                        release_date = re.search(r'(?<=\- )[0-9?]{2}/[0-9?]{2}/[0-9?]{4}', line).group()

                        changelog.append({
                            'release_ver': release_ver,
                            'release_link': release_link,
                            'release_date': release_date,
                            'changelog_sections': []
                        })

                    # Changelog section headers
                    elif line.startswith('### '):
                        changelog[-1]['changelog_sections'].append({
                            'section_header': line.replace('###', '').strip(),
                            'section_list': []
                        })
                    # Changelog section lists
                    elif line.startswith('- '):
                        line = re.sub(r'^- ', r'', line).strip()
                        
                        changelog[-1]['changelog_sections'][-1]['section_list'].append(line)
        except:
            pass

        changelog_text = f'''
            {main.settings_global['styles']['style_changelog']}
            <body>
        '''

        for release in changelog:
            changelog_text += f'''
                <div class="changelog">
                    <div class="changelog-header"><a href="{release['release_link']}">{release['release_ver']}</a> - {release['release_date']}</div>
                    <hr>
            '''

            for changelog_section in release['changelog_sections']:
                changelog_text += f'''
                    <div class="changelog-section">
                        <div class="changelog-section-header">{changelog_section['section_header']}</div>
                        <ul>
                '''

                for item in changelog_section['section_list']:
                    changelog_text += f'''
                        <li>{item}</li>
                    '''

                changelog_text += f'''
                        </ul>
                    </div>
                '''

            changelog_text += f'''
                </div>
            '''

        changelog_text += f'''
            </body>
        '''

        super().__init__(main, main.tr('Changelog'),
                         width = 480,
                         height = 420)

        text_edit_changelog = wl_box.Wl_Text_Browser(self)

        text_edit_changelog.setHtml(changelog_text)

        self.wrapper_info.layout().addWidget(text_edit_changelog, 0, 0)

class Wl_Dialog_About(wl_dialog.Wl_Dialog_Info):
    def __init__(self, main):
        super().__init__(main, main.tr('About Wordless'))

        img_wl_icon = QPixmap('imgs/wl_icon_about.png')
        img_wl_icon = img_wl_icon.scaled(64, 64)

        label_about_icon = QLabel('', self)
        label_about_icon.setPixmap(img_wl_icon)

        label_about_title = wl_label.Wl_Label_Dialog_No_Wrap(
            self.tr(f'''
                <div style="text-align: center;">
                    <h2>Wordless {main.ver}</h2>
                    <div>
                        An Integrated Corpus Tool with Multilingual Support<br>
                        for the Study of Language, Literature, and Translation
                    </div>
                </div>
            '''),
            self
        )
        label_about_copyright = wl_label.Wl_Label_Dialog_No_Wrap(
            self.tr('''
                <hr>
                <div style="text-align: center;">
                    Copyright (C) 2018-2021 Ye Lei (<span style="font-family: simsun">叶磊</span>)<br>
                    Licensed Under GNU GPLv3<br>
                    All Other Rights Reserved
                </div>
            '''),
            self
        )

        self.wrapper_info.layout().addWidget(label_about_icon, 0, 0)
        self.wrapper_info.layout().addWidget(label_about_title, 0, 1)
        self.wrapper_info.layout().addWidget(label_about_copyright, 1, 0, 1, 2)

        self.wrapper_info.layout().setColumnStretch(1, 1)
        self.wrapper_info.layout().setVerticalSpacing(0)

        self.set_fixed_size()
        self.setFixedWidth(self.width() + 10)
