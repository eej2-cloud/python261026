#demmoform.py
#demoform.ui(화면단) + demoform.py(로직단)

import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic

#화면 로딩
form_class = uic.loadUiType("demoform.ui")[0]

#폼클래스 정의
class demoform(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("PyQt6 사용하기")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = demoform()
    demo.show()
    app.exec()