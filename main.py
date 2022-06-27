import sys
import datetime
import json
import requests
from requests.exceptions import HTTPError
from PyQt6 import uic, QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    ServerAdress = "http://localhost:5000"
    MessageID = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messenger.ui', self)
        self.pushButton.clicked.connect(self.pushButton_clicked)

    def pushButton_clicked(self):
        self.SendMessage()

    def SendMessage(self):
        UserName = self.lineEdit1.text()
        MessageText = self.lineEdit2.text()
        TimeStamp = str(datetime.datetime.today())
        msg = f"{{\"UserName\": \"{UserName}\", \"MessageText\": \"{MessageText}\", \"TimeStamp\": \"{TimeStamp}\"}}"
        print("Отправлено сообщение: " + msg)
        url = self.ServerAdress + "/api/messenger"
        data = json.loads(msg)  # string to json
        r = requests.post(url, json=data)
        # print(r.status_code, r.reason)

    def GetMessage(self, id):
        url = self.ServerAdress + "/api/messenger/" + str(id)
        try:
            response = requests.get(url)
            # если ответ успешен, исключения задействованы не будут
            response.raise_for_status()
        except HTTPError as http_err:
            # print(f'HTTP error occurred: {http_err}')  # Python 3.6
            return None
        except Exception as err:
            # print(f'Other error occurred: {err}')  # Python 3.6
            return None
        else:
            text = response.text
            return text

    def timerEvent(self):
        msg = self.GetMessage(self.MessageID)
        while msg is not None:
            msg = json.loads(msg)
            UserName = msg["UserName"]
            MessageText = msg["MessageText"]
            TimeStamp = msg["TimeStamp"]
            msgtext =f"{TimeStamp} : <{UserName}> : {MessageText}"
            self.listWidget1.insertItem(self.MessageID, msgtext)
            self.MessageID += 1
            msg = self.GetMessage(self.MessageID)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.timerEvent)
    timer.start(5000)
    sys.exit(app.exec())