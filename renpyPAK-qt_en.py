from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog,QLabel, QLineEdit, QPushButton,QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
import os,subprocess,pkrpy,upkrpy,platform

class rpa(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./pak_ui_en.ui", self)
        self.setWindowTitle("renpyPAK-qt")
        #self.setWindowIcon(QIcon(".png"))
        self.setFixedSize(800,690)

        self.cho_will_dir.clicked.connect(self.wait_dir1)
        self.cho_out_rpa_dir.clicked.connect(self.wait_dir2)
        self.op_rpa_out.clicked.connect(self.op_out1)
        self.pack_me.clicked.connect(self.pk)

        self.cho_will_pk_dir.clicked.connect(self.wait_dir3)
        self.cho_rpa_out_dir.clicked.connect(self.wait_dir4)
        self.op_unpk_out.clicked.connect(self.op_out2)
        self.unpack_me.clicked.connect(self.upk)

    def wait_dir1(self):
        self.will_pk_dir.setText(QFileDialog.getExistingDirectory(self, "Select folder to be packaged", "/"))
    def wait_dir2(self):   
        self.put_rpa_dir.setText(QFileDialog.getExistingDirectory(self, "Select export directory for the package", "/"))
    def op_out1(self):
        if not self.put_rpa_dir.text():
            pass
        else:
            if platform.system() == "Windows":
                subprocess.Popen(["explorer", self.put_rpa_dir.text().replace("/", "\\")])
            if platform.system() == "Linux":
                subprocess.Popen(["xdg-open", self.put_rpa_dir.text()])
            if platform.system() == "Haiku":
                subprocess.Popen(["open", self.put_rpa_dir.text()])
            else:
                print("There will be a wonderful DE A E next time!")

    
    def wait_dir3(self):
        get_rpa, _ = QFileDialog.getOpenFileName(self, "Select .rpa package", "/", "rpa (*.rpa)")
        self.will_ex_dir.setText(get_rpa)
    def wait_dir4(self):
        self.put_out_dir.setText(QFileDialog.getExistingDirectory(self, "Select unpack export directory", "/"))
    def op_out2(self):
        if not self.put_out_dir.text():
            pass
        else:
            subprocess.Popen(["explorer", self.put_out_dir.text().replace("/", "\\")])

    def upk(self):

        try:
            ok, get = upkrpy.unpack_rpa(self.will_ex_dir.text(), self.put_out_dir.text())
            if ok:
                QMessageBox.information(self, "Done", f"{get} file(s) have been obtained")
        except FileNotFoundError:
            pass

    def pk(self):
        
        if not self.put_rpa_dir.text() or not self.will_pk_dir.text() or not self.pk_name.text():
            pass
        else:
            pkrpy.archive(self.put_rpa_dir.text(), self.will_pk_dir.text(), self.pk_name.text())
            QMessageBox.information(self, "Done", "Packed ✓")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication([])
    window = rpa()
    window.show()
    app.exec()