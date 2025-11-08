from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTranslator, QCoreApplication
from PyQt6.uic import loadUi
import os, subprocess, pkrpy, upkrpy

class rpa(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./pak_ui.ui", self)

        self.translator = QTranslator()
        
        self.setWindowTitle(self.tr("renpy解封包qt版"))
        self.setFixedSize(800, 690)

        self.retranslateUi()

        self.cho_will_dir.clicked.connect(self.wait_dir1)
        self.cho_out_rpa_dir.clicked.connect(self.wait_dir2)
        self.op_rpa_out.clicked.connect(self.op_out1)
        self.pack_me.clicked.connect(self.pk)

        self.cho_will_pk_dir.clicked.connect(self.wait_dir3)
        self.cho_rpa_out_dir.clicked.connect(self.wait_dir4)
        self.op_unpk_out.clicked.connect(self.op_out2)
        self.unpack_me.clicked.connect(self.upk)

        self.tl_change.currentIndexChanged.connect(self.change_lang)

    def change_lang(self):
        # 切换前先移除旧的翻译
        QCoreApplication.instance().removeTranslator(self.translator)
        index = self.tl_change.currentIndex()

        if index == 0:
            qm_file = './chs_menu_patch.qm'
        else:
            qm_file = './en_patch.qm'

        if self.translator.load(qm_file):
            QCoreApplication.instance().installTranslator(self.translator)
            self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(self.tr("renpy解封包qt版"))
        self.pk_label.setText(f"<html><head/><body><p><span style=\" font-size:16pt; font-weight:700;\">{self.tr('封包')}</span></p></body></html>")
        self.ex_title.setText(f"<html><head/><body><p><span style=\" font-size:16pt; font-weight:700;\">{self.tr('解包')}</span></p></body></html>")

        self.cho_will_dir.setText(self.tr("导入文件夹"))
        self.cho_out_rpa_dir.setText(self.tr("选导出目录"))
        self.cl_will_pk_dir.setText(self.tr("清除"))
        self.cl_put_rpa_dir.setText(self.tr("清除"))
        self.cl_pk_name.setText(self.tr("清除"))
        self.cl_pk_rpa.setText(self.tr("全部清除"))
        self.pack_me.setText(self.tr("封包"))
        self.op_rpa_out.setText(self.tr("打开导出目录"))
        self.will_pk_dir.setPlaceholderText(self.tr("导入含游戏资产的文件夹"))
        self.put_rpa_dir.setPlaceholderText(self.tr("选择封包导出目录"))
        self.pk_name.setPlaceholderText(self.tr("输入包名"))

        self.cho_will_pk_dir.setText(self.tr("选择封包"))
        self.cl_will_ex_dir.setText(self.tr("清除"))
        self.cho_rpa_out_dir.setText(self.tr("选存放目录"))
        self.cl_put_out_dir.setText(self.tr("清除"))
        self.cl_ex_rpa.setText(self.tr("全部清除"))
        self.unpack_me.setText(self.tr("解包"))
        self.op_unpk_out.setText(self.tr("打开存放目录"))
        self.will_ex_dir.setPlaceholderText(self.tr("导入封包"))
        self.put_out_dir.setPlaceholderText(self.tr("选择解包导出目录"))

    def wait_dir1(self):
        self.will_pk_dir.setText(QFileDialog.getExistingDirectory(self, "选择待封包的文件夹", "/"))

    def wait_dir2(self):
        self.put_rpa_dir.setText(QFileDialog.getExistingDirectory(self, "选择封包导出目录", "/"))

    def op_out1(self):
        if self.put_rpa_dir.text():
            subprocess.Popen(["explorer", self.put_rpa_dir.text().replace("/", "\\")])

    def wait_dir3(self):
        get_rpa, _ = QFileDialog.getOpenFileName(self, "选择rpa包", "/", "rpa包 (*.rpa)")
        self.will_ex_dir.setText(get_rpa)

    def wait_dir4(self):
        self.put_out_dir.setText(QFileDialog.getExistingDirectory(self, "选择解包导出目录", "/"))

    def op_out2(self):
        if self.put_out_dir.text():
            subprocess.Popen(["explorer", self.put_out_dir.text().replace("/", "\\")])

    def upk(self):
        try:
            ok, get = upkrpy.unpack_rpa(self.will_ex_dir.text(), self.put_out_dir.text())
            if ok:
                QMessageBox.information(self, self.tr("成功"), self.tr("解包完成！"))
        except FileNotFoundError:
            pass

    def pk(self):
        if not self.put_rpa_dir.text() or not self.will_pk_dir.text() or not self.pk_name.text():
            pass
        else:
            pkrpy.archive(self.put_rpa_dir.text(), self.will_pk_dir.text(), self.pk_name.text())
            QMessageBox.information(self, self.tr("成功"), self.tr("封包完成！"))

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication([])
    window = rpa()
    window.show()
    app.exec()