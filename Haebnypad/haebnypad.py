import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic


def main():
    # python 실행파일 디렉토리
    base_dir = os.path.dirname(os.path.abspath(__file__))

    form_class = uic.loadUiType(base_dir + r'\haebnypad.ui')[0]

    class WindowClass(QMainWindow, form_class):
        def __init__(self):
            super().__init__()
            self.setupUi(self)

            self.actionOpen.triggered.connect(self.openFunction)
            self.actionSave.triggered.connect(self.saveFunction)

        # 파일 열기
        def openFunction(self):
            # 파일 탐색기 호출
            fname = QFileDialog.getOpenFileName(self)
            if fname[0]:
                with open(fname[0], encoding="UTF8") as f:
                    data = f.read()

                self.plainTextEdit.setPlainText(data)

                print("Open {}".format(fname[0]))

        # 파일 저장
        def saveFunction(self):
            fname = QFileDialog.getSaveFileName(self)
            if fname[0]:
                data = self.plainTextEdit.toPlainText()
                with open(fname[0], 'w', encoding="UTF8") as f:
                    f.write(data)

                print("Save {}".format(fname[0]))

    app = QApplication(sys.argv)
    main_window = WindowClass()
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
