# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

#py文件名称
import test
import pandas as pd
import numpy as np

class Example(test.Ui_Dialog):

    # def __init__(self):
    #     super().__init__()
    #     self.MainWindow = QtWidgets.QDialog()
    #     self.ui = test.Ui_Dialog()
    #     self.ui.setupUi(self.MainWindow)
    #     self.MainWindow.show()

    def __init__(self, Dialog):
        super().setupUi(Dialog)  # 调用父类的setupUI函数
        self.pushButton.clicked.connect(self.setBrowerPath)  # 将按钮点击事件和函数绑定
        self.pushButton_2.clicked.connect(self.creat_table_show)
        self.pushButton_3.clicked.connect(self.menu_list_confirm)
        self.pushButton_4.clicked.connect(self.save_table_excel)

    # def closeEvent(self, event):
    #     reply = QtWidgets.QMessageBox.question(self, '确认', '确认退出吗', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    #     if reply == QtWidgets.QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def clickButton(self):
        # sender = self.sender()
        print( '被点击')


    def warning_box(self, msg):
        QtWidgets.QMessageBox.warning(None, '警告', msg)

    def success_box(self):
        QtWidgets.QMessageBox.information(None, '成功', '文件已导出')

    # 选择excel文件路径
    def setBrowerPath(self):
        # download_path = QtWidgets.QFileDialog.getExistingDirectory(None,
        #                                                            "浏览",
        #                                                            "C:")
        download_path = QtWidgets.QFileDialog.getOpenFileName(None, "选择文件", "C:",
                                               "Excel files(*.xlsx , *.xls)")  # 多个时用分号分开
        self.textEdit.setText(download_path[0])
        self.creat_table_show()

    # 打开excel文件并读取表格
    def creat_table_show(self):
        self.creat_table_show_index(0)

    def creat_table_show_index(self, index):
        ###===========读取表格，转换表格，===========================================
        global path_openfile_name
        global input_table
        global sheet_index
        global sheet_size
        path_openfile_name = self.textEdit.toPlainText()
        if len(path_openfile_name) > 0:
            sheet_index = index
            input_table = pd.read_excel(path_openfile_name, sheet_name=sheet_index)
            excel_file = pd.ExcelFile(path_openfile_name)
            sheet_size = len(excel_file.sheet_names)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.columns.size
            self.label_2.setText("工作簿数量："+str(sheet_size)+"个，当前工作簿："+str(excel_file.sheet_names[sheet_index])+"，行："+str(input_table_rows)+"，列："+str(input_table_colunms))
            input_table_header = input_table.columns.values.tolist()
            for header in input_table_header:
                input_table_header[input_table_header.index(header)] = str(header)

            ###======================给tablewidget设置行列表头============================

            self.tableWidget.setColumnCount(input_table_colunms)
            self.tableWidget.setRowCount(input_table_rows)
            self.tableWidget.setHorizontalHeaderLabels(input_table_header)

            ###================遍历表格每个元素，同时添加到tablewidget中========================

            for i in range(input_table_rows):
                for j in range(input_table_colunms):
                    newItem = QtWidgets.QTableWidgetItem(str(input_table.iloc[i, j]))
                    newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, newItem)

        else:
            self.warning_box('未选择文件')


    # 保持excel文件并导出成文件
    def save_table_excel(self):
        global path_openfile_name
        global input_table
        path_openfile_name = self.textEdit.toPlainText()
        if len(path_openfile_name) == 0:
            self.warning_box('未选择文件')
        else:
            out_file_name = str(path_openfile_name).replace(".", "_out.")
            pd.DataFrame(input_table).to_excel(out_file_name, sheet_name='Sheet1', index=False, header=True)
            self.success_box()

    def menu_list_confirm(self):
        if self.comboBox.currentText().__eq__("常用功能"):
            self.warning_box('未选择功能')
        elif self.comboBox.currentText().__eq__("切换打开下一个工作簿"):
            self.change_next_sheet()


    def change_next_sheet(self):
        global path_openfile_name
        global input_table
        global sheet_index
        global sheet_size
        path_openfile_name = self.textEdit.toPlainText()
        if len(path_openfile_name) > 0:
            if sheet_index + 2 > sheet_size:
                sheet_index = 0
                self.creat_table_show_index(sheet_index)
            else:
                sheet_index = sheet_index + 1
                self.creat_table_show_index(sheet_index)



# 程序入口
if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Example()  # 注意把类名修改为myDialog
    # sys.exit(app.exec())

    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QDialog()
    # ui = test.Ui_Dialog()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    ui = Example(MainWindow)  # 页面加载..
    # ui.setupUi(MainWindow)  myDialog类的构造函数已经调用了这个函数，这行代码可以删去
    MainWindow.show()
    sys.exit(app.exec_())

