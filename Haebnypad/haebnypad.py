import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor


def main():
    # python 실행파일 디렉토리
    base_dir = os.path.dirname(os.path.abspath(__file__))

    class findWindow(QDialog):
        def __init__(self, parent):
            super(findWindow, self).__init__(parent)
            uic.loadUi(base_dir + r'\find.ui', self)
            self.show()

            self.parent = parent
            self.pe = parent.plainTextEdit
            self.cursor = self.pe.plainTextEdit.textCursor()


            self.pushButton_findnext.clicked.connect(self.findNext)
            self.pushButton_cancel.clicked.connect(self.close)

        def keyReleaseEvent(self, event):
            if self.lineEdit.text():
                self.pushButton_findnext.setEnabled(True)
            else:
                self.pushButton_findnext.setEnabled(False)

        def findNext(self):
            pattern = self.lineEdit.text()
            text =  self.pe.toPlainText()
            print(pattern, text)

            reg = QtCore.QRegExp(pattern)
            index = reg.indexIn(text, 0)
            if index != -1:
                self.setCursor(index, len(pattern)+index)

        def setCursor(self, start, end):
            print(self.cursor.selectionStart(), self.cursor.selectionEnd())
            self.cursor.setPosition(start)  # 앞에 커서를 찍고
            self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start)  # 뒤로 커서를 움직임
            self.pe.setTextCursor(self.cursor)

    form_class = uic.loadUiType(base_dir + r'\haebnypad.ui')[0]

    class WindowClass(QMainWindow, form_class):
        def __init__(self):
            super().__init__()
            self.setupUi(self)

            self.actionOpen.triggered.connect(self.openFunction)
            self.actionSave.triggered.connect(self.saveFunction)
            self.actionSave_As.triggered.connect(self.saveAsFunction)
            self.actionClose.triggered.connect(self.closeEvent)

            # short cuts
            self.actionUndo.triggered.connect(self.undoFunction)
            self.actionCut.triggered.connect(self.cutFunction)
            self.actionCopy.triggered.connect(self.copyFunction)
            self.actionPaste.triggered.connect(self.pasteFunction)
            self.actionFind.triggered.connect(self.findFunction)

            self.opened = False
            self.opened_file_path = "Untitled"
            self.origin = self.plainTextEdit.toPlainText()

        def is_changed(self):
            if not self.opened:
                if self.plainTextEdit.toPlainText().strip():    # 열린적은 없지만 변경사항이 있는 경우
                    return True
                return False
            # 현재 데이터
            current_data = self.plainTextEdit.toPlainText()

            # 파일에 저장된 데이터
            with open(self.opened_file_path, encoding='UTF8') as f:
                file_data = f.read()

            if current_data == file_data:   # 열린적이 있고 변경사항이 없는 경우
                return False
            else:   # 열린적이 있고 변경사항이 있는 경우
                return True

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
            # 취소를 누른 경우에만 종료 이벤트 무시
            if ret == 0:
                self.saveFunction()
            else:
                return ret

        def closeEvent(self, event):
            if self.is_changed():
                ret = self.save_changed_data()
                if ret == 2:
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
            if self.is_changed():
                ret = self.save_changed_data()
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

        # 단축키 함수
        def undoFunction(self):
            self.plainTextEdit.undo()

        def cutFunction(self):
            self.plainTextEdit.cut()

        def copyFunction(self):
            self.plainTextEdit.copy()

        def pasteFunction(self):
            self.plainTextEdit.paste()

        def findFunction(self):
            findWindow(self)


    app = QApplication(sys.argv)
    main_window = WindowClass()
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
