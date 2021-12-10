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
            self.actionSave_As.triggered.connect(self.saveAsFunction)
            self.actionClose.triggered.connect(self.closeEvent)

            self.opened = False
            self.opened_file_path = "Untitled"
            self.origin = self.plainTextEdit.toPlainText()

        def save_changed_data(self):
            # 변경 사항이 없으면 바로 종료
            if self.origin == self.plainTextEdit.toPlainText():
                print("Close")
                return 1

            # 저장 관련 메세지 박스 생성
            msg_box = QMessageBox()
            msg_box.setText("Do you want to save changes to {}?".format(self.opened_file_path))
            msg_box.addButton("Save", QMessageBox.YesRole) #0
            msg_box.addButton("Don't save", QMessageBox.NoRole) #1
            msg_box.addButton("Cancel", QMessageBox.RejectRole) #2
            ret = msg_box.exec_()
            # 저장 안함
            if ret == 1:
                print("Close")
                
            return ret

        def closeEvent(self, event):
            ret = self.save_changed_data()
            # 취소를 누른 경우에만 종료 이벤트 무시
            if ret == 0:
                self.saveFunction()
            elif ret == 2:
                event.ignore()
                print("Cancel")

        # 기능 분리 -----------------------------------------------------------------------------------------------------
        # 저장
        def save_file(self, fname):
            data = self.plainTextEdit.toPlainText()

            with open(fname, 'w', encoding="UTF8") as f:
                f.write(data)

            # 파일이 열려 있음을 기록
            self.opened = True
            self.opened_file_path = fname
            self.origin = self.plainTextEdit.toPlainText()

            print("Save {}".format(fname))

        # 열기
        def open_file(self, fname):
            with open(fname, encoding="UTF8") as f:
                data = f.read()
            self.plainTextEdit.setPlainText(data)

            # 파일이 열려 있음을 기록
            self.opened = True
            self.opened_file_path = fname
            self.origin = self.plainTextEdit.toPlainText()

            print("Open {}".format(fname))

        # 파일 열기
        def openFunction(self):
            # 파일 탐색기 호출
            fname = QFileDialog.getOpenFileName(self)
            if fname[0]:
                self.open_file(fname[0])

        # 파일 저장
        def saveFunction(self):
            # 기존 파일이 존재하는 경우
            if self.opened:
                self.save_file(self.opened_file_path)
            else:
                self.saveAsFunction()

        # 다른 이름으로 파일 저장
        def saveAsFunction(self):
            # 항상 파일 탐색기 열림
            fname = QFileDialog.getSaveFileName(self)
            if fname[0]:
                self.save_file(fname[0])


    app = QApplication(sys.argv)
    main_window = WindowClass()
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
