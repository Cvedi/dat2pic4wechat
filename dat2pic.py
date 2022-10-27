#coding=utf-8
import sys
import os
import time
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

today = datetime.datetime.now().strftime('%Y-%m-%d')

class MyWindow(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUI()
        # sys.stdout = EmittingStr(textWritten=self.outputWritten)
        # sys.stderr = EmittingStr(textWritten=self.outputWritten)

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def setupUI(self):
        self.setWindowTitle('微信图片转换')
        self.resize(600,240)
        self.label = QtWidgets.QLabel(self)
        self.label.move(10, 15)
        self.label.setText('微信文件存放路径:')
        self.label.setFont(QtGui.QFont('微软雅黑',12,QtGui.QFont.Black))
        self.lineedit = QtWidgets.QLineEdit(self)
        self.lineedit.setGeometry(150,15,400,20)
        self.lineedit.setReadOnly(True)
        self.label1 = QtWidgets.QLabel(self)
        self.label1.move(10,55)
        self.label1.setText('转换文件存放路径:')
        self.label1.setFont(QtGui.QFont('微软雅黑',12,QtGui.QFont.Black))
        self.lineedit1 = QtWidgets.QLineEdit(self)
        self.lineedit1.setGeometry(150,55,400,20)
        self.lineedit1.setReadOnly(True)
        self.label2 = QtWidgets.QLabel(self)
        self.label2.move(10,95)
        self.label2.setText('转换码(填写0x41):')
        self.label2.setFont(QtGui.QFont('微软雅黑',12,QtGui.QFont.Black))
        self.lineedit2 = QtWidgets.QLineEdit(self)
        self.lineedit2.setGeometry(150,95,400,20)
        self.lineedit2.setText('0x41')
        self.label3 = QtWidgets.QLabel(self)
        self.label3.move(10,145)
        self.label3.setText('日期(xxxx-xx-xx):')
        self.label3.setFont(QtGui.QFont('微软雅黑',12,QtGui.QFont.Black))
        self.lineedit3 = QtWidgets.QLineEdit(self)
        self.lineedit3.setGeometry(150,145,400,20)
        self.lineedit3.setText(today)
        self.mybutton=QtWidgets.QPushButton(self)
        self.mybutton.setGeometry(480,180,80,40)
        self.mybutton.setText('开始转换')
        self.mybutton.clicked.connect(self.trans)
        self.mybutton1=QtWidgets.QPushButton(self)
        self.mybutton1.setGeometry(260,180,180,40)
        self.mybutton1.setText('选择转换文件存放路径')
        self.mybutton1.clicked.connect(self.open_savepath)
        self.mybutton2=QtWidgets.QPushButton(self)
        self.mybutton2.setGeometry(40,180,180,40)
        self.mybutton2.setText('选择微信文件所在路径')
        self.mybutton2.clicked.connect(self.open_datapath)
        # self.textbrowser = QtWidgets.QTextBrowser(self)
        # self.textbrowser.setGeometry(10,230,580,260)
    def open_savepath(self):
        dir_choose = QtWidgets.QFileDialog.getExistingDirectory(self,'选择文件夹',r"D:")
        self.lineedit1.setText(dir_choose)
    def open_datapath(self):
        dir_choose = QtWidgets.QFileDialog.getExistingDirectory(self,'选择文件夹',r"D:\WeChat Files\xxx\FileStorage\MsgAttach")
        self.lineedit.setText(dir_choose)
    def infomsg(self):
        QtWidgets.QMessageBox.information(self, '提示','转换成功!',QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Yes)
    def erromsg(self):
        QtWidgets.QMessageBox.warning(self,'提示','转换失败!',QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Yes)
    def textbrowser(self,text):
        self.textbrowser.setText(text)
    def trans(self):
        data_path = self.lineedit.text()
        save_path = self.lineedit1.text()
        trans_code = self.lineedit2.text()
        trans_date = self.lineedit3.text()
        try:
            pic_trans = dat2pic(data_path,save_path,trans_date,trans_code)
            pic_trans.dat2pic()
            self.infomsg()
        except:
            self.erromsg()

class dat2pic:
    # 传入完整路径名,存储路径,转换日期,程序将转换创建日期为*转换日期*的dat文件,转换日期格式为'yyyy-mm-dd'
    def __init__(self,file_path,save_path,trans_date,trans_code):
        self.file_path = file_path
        self.save_path = save_path
        self.trans_date = trans_date
        self.trans_code = trans_code
    
    # 时间戳转日期
    def TimeStampToDay(self,timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d',timeStruct)

    # 时间戳转日期时间
    def TimeStampToTime(self,timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y%m%d%H%M%S',timeStruct)
    
    # 获取文件创建日期
    def get_FileCreateDay(self,filepath_name):
        t = os.path.getctime(filepath_name)
        createday = self.TimeStampToDay(t)
        return createday

    # 获取文件创建时间,用于转换后的文件命名
    def get_FileCreateTime(self,filePath_name):
        t = os.path.getctime(filePath_name)
        createtime = self.TimeStampToTime(t)
        return createtime

    # 图片转换
    def pic_trans(self,filepath_name,createtime,filename):
        save_path = self.save_path
        trans_code = self.trans_code
        trans_code = int(trans_code, 16)
        dat_read = open(filepath_name, "rb")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        out_path=save_path+ "\\" + createtime + "-" + filename +".JPG"
        jpg_write = open(out_path, "wb")
        for now in dat_read:
            for nowByte in now:
                newByte = nowByte ^ trans_code #转换码需通过16进制查看器,结合JPG、PNG十六进制值通过异或计算获得
                jpg_write.write(bytes([newByte]))
        dat_read.close()
        jpg_write.close()

    # 遍历文件目录,获取dat文件,根据创建日期进行转换
    def dat2pic(self):
        file_path = self.file_path
        trans_date = self.trans_date
        trans_month = trans_date[0:7]
        try:
            for i in os.scandir(file_path):
                for e in os.scandir(i.path):
                    if e.path[-5:] == 'Image':
                        for j in os.scandir(e.path):
                            if j.path[-7:] == trans_month:
                                files = os.listdir(j.path)
                                for filename in files:
                                    filepath_name = os.path.join(j.path,filename)
                                    createtime = self.get_FileCreateTime(filepath_name)
                                    createday = self.get_FileCreateDay(filepath_name)
                                    if createday == trans_date:
                                        self.pic_trans(filepath_name,createtime,filename)
        except Exception as errmsg:
            print(errmsg)


if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    myshow=MyWindow()
    myshow.show()
    sys.exit(app.exec_())
