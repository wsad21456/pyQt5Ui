# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import QSettings, QDateTime, Qt
import ocrTest

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
        self.textEdit.textChanged.connect(self.edit_change)
        self.pushButton.clicked.connect(self.setBrowerPath)  # 将按钮点击事件和函数绑定
        self.pushButton_2.clicked.connect(self.creat_table_show)
        self.pushButton_3.clicked.connect(self.menu_list_confirm)
        self.pushButton_4.clicked.connect(self.save_table_excel)
        # table widget 右键菜单 放在主窗口__init__(self):下
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        self.tableWidget.customContextMenuRequested.connect(self.tableWidget_VTest_menu)  # 右键菜单
        self.tableWidget.itemClicked.connect(self.show_data) # 鼠标单击


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

    def edit_change(self):
        if self.textEdit.toPlainText().find('file:///') >= 0:
            self.textEdit.setText(self.textEdit.toPlainText().replace('file:///', ''))

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
            path_openfile_name = ''
            self.warning_box('未选择文件')


    # 保持excel文件并导出成文件
    def save_table_excel(self):
        global path_openfile_name
        global input_table
        try:
            if len(path_openfile_name) == 0:
                self.warning_box('未选择文件')
            else:
                out_file_name = str(path_openfile_name).replace(".", "_out.")
                pd.DataFrame(input_table).to_excel(out_file_name, sheet_name='Sheet1', index=False, header=True)
                self.success_box()
        except NameError:
            self.warning_box('未选择文件')

    # 功能菜单
    def menu_list_confirm(self):
        if self.comboBox.currentText().__eq__("常用功能"):
            self.warning_box('未选择功能')
        elif self.comboBox.currentText().__eq__("切换打开下一个工作簿"):
            self.change_next_sheet()
        elif self.comboBox.currentText().__eq__("图像识别输出到右侧单元格"):
            reply = QtWidgets.QMessageBox.question(None, '确认', '使用GPU模式输出', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.download_and_ocr(True)
            else:
                self.download_and_ocr(False)
        elif self.comboBox.currentText().__eq__("拖拽文件识别到excel格中"):
            self.local_url_ocr()

    # 切换打开下一个工作簿
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

    #右键点击菜单
    def tableWidget_VTest_menu(self, pos):
        """
        :return:
        """
        menu = QtWidgets.QMenu() #实例化菜单
        item1 = menu.addAction(u"添加单个单元格")
        item2 = menu.addAction(u"添加整列")
        item3 = menu.addAction(u"清除选中并刷新")
        action = menu.exec_(self.tableWidget.mapToGlobal(pos))

        if action == item1:
            self.on_menu_add_cell()
            print("添加单个单元格")
        elif action == item2:
            self.on_menu_add_column()
            print("添加整列")
        elif action == item3:
            self.clear_select_cell()
            print("清除选中并刷新")

    # 添加单元格
    global index_cell
    index_cell = []
    global index_column
    index_column = []
    def on_menu_add_cell(self):
        # 通过selectedIndexes方法可以获得点中的所有项
        selected_indexes = self.tableWidget.selectedIndexes()
        if len(selected_indexes) > 0:
            data_idx = selected_indexes[0].row()
            data_idx_c = selected_indexes[0].column()
            data = self.tableWidget.item(data_idx, data_idx_c).text()
            print(f'row -> {[data_idx]} column -> {[data_idx_c]} data -> {[data]}')
            #添加这个单元格到数组内
            index_cell.append(f'{data_idx},{data_idx_c}')
            # 背景颜色（红色）
            self.tableWidget.item(data_idx, data_idx_c).setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))

    # 表格添加整列
    def on_menu_add_column(self):
        # 通过selectedIndexes方法可以获得点中的所有项
        selected_indexes = self.tableWidget.selectedIndexes()
        if len(selected_indexes) > 0:
            data_idx_c = selected_indexes[0].column()
            print(f'column -> {data_idx_c}')
            #添加这个单元格到数组内
            index_column.append(f'{data_idx_c}')
            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    if j.__eq__(data_idx_c):
                        # 背景颜色（红色）
                        self.tableWidget.item(i, j).setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))

    # 下载并ocr识别
    def download_and_ocr(self, gpu_boolean):
        global input_table
        if len(index_cell) > 0:
            print(index_cell)
            for cell in index_cell:
                cell_str = str(cell)
                print(self.tableWidget.item(int(cell_str.split(',')[0]), int(cell_str.split(',')[1])).text())
                path = ocrTest.download_url(str(self.tableWidget.item(int(cell_str.split(',')[0]), int(cell_str.split(',')[1])).text()))
                ocr_result = ocrTest.pic_ocr(path, gpu_boolean)
                if (ocr_result is not None) and (not ''.__eq__(ocr_result)):
                    self.tableWidget.item(int(cell_str.split(',')[0]), int(cell_str.split(',')[1]) + 1).setText(ocr_result)
                    input_table.iloc[int(cell_str.split(',')[0]), int(cell_str.split(',')[1]) + 1] = ocr_result
        if len(index_column) > 0:
            print(index_column)
            for column in index_column:
                for i in range(self.tableWidget.rowCount()):
                    path = ocrTest.download_url(str(self.tableWidget.item(i, int(column)).text()))
                    ocr_result = ocrTest.pic_ocr(path, gpu_boolean)
                    if (ocr_result is not None) and (not ''.__eq__(ocr_result)):
                        self.tableWidget.item(i, int(column) + 1).setText(ocr_result)
                        input_table.iloc[i, int(column) + 1] = ocr_result

    # 清除标红的单元格
    def clear_select_cell(self):
        global index_cell
        index_cell = []
        global index_column
        index_column = []
        global path_openfile_name
        global sheet_index
        global sheet_size
        path_openfile_name = self.textEdit.toPlainText()
        if len(path_openfile_name) > 0:
            self.creat_table_show_index(sheet_index)


    # 这里会接收到被点击的单元格对象参数
    def show_data(self, Item=None):
        # 如果单元格对象为空
        if Item is None:
            return
        else:
            global data_row
            global data_col
            data_row = Item.row()  # 获取行数
            data_col = Item.column()  # 获取列数 注意是column而不是col哦
            # text = Item.text()  # 获取内容

    # 拖拽文件识别到excel格中
    def local_url_ocr(self):
        global data_row
        global data_col
        global input_table
        try:
            result = str(ocrTest.pic_ocr(self.textEdit.toPlainText(), True))
        except:
            self.warning_box('文件OCR识别失败')
        try:
            newItem = QtWidgets.QTableWidgetItem(result, True)
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(data_row, data_col, newItem)
            input_table.iloc[data_row, data_col] = result
        except NameError:
            self.warning_box('未选择excel单元格')

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

