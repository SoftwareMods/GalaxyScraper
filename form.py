from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QFormLayout,
    QApplication,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QSizePolicy,
    QFrame,
    QMessageBox,
    QFileDialog,
    QCheckBox,
    QProgressBar,
)
from PyQt5.QtCore import QSize, QThread, QObject, QMetaObject, QCoreApplication
from PyQt5.QtGui import QPixmap, QFont
import requests, sys
from bs4 import BeautifulSoup
from helpers import *

def sizeof_fmt(num):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}"
        num /= 1024.0


checkBoxes = {}

results = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36"
}
file_server = "https://files01.galaxyaudiobook.com/audio/"


class FetchBookObject(object):
    def setupUi(self, Form):
        self.lengths = {}
        self.sizes = {}
        self.exts = {}
        Form.setObjectName("Form")
        Form.resize(1030, 530)
        Form.setMinimumSize(QSize(1030, 530))

        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.gridLayout = QGridLayout()
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        
        self.fetch_button = QPushButton(Form)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fetch_button.sizePolicy().hasHeightForWidth())
        self.fetch_button.setSizePolicy(sizePolicy)
        self.fetch_button.setMinimumSize(QSize(105, 0))
        self.fetch_button.setMaximumSize(QSize(16777215, 40))
        self.fetch_button.setObjectName("fetch_button")
        self.fetch_button.setStyleSheet('background-color: skyblue; color: black;')
        self.fetch_button.clicked.connect(self.fetch_book_details)
        self.gridLayout.addWidget(self.fetch_button, 0, 1, 1, 1)

        self.url_entry = QLineEdit(Form)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.url_entry.sizePolicy().hasHeightForWidth())
        self.url_entry.setSizePolicy(sizePolicy)
        self.url_entry.setMinimumSize(QSize(713, 38))
        self.url_entry.setMaximumSize(QSize(10000, 38))
        self.url_entry.setBaseSize(QSize(0, 0))
        self.url_entry.setStyleSheet("padding-left: 8px; font-size: 16px;")
        self.url_entry.setObjectName("url_entry")
        self.gridLayout.addWidget(self.url_entry, 0, 0, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.formLayout = QFormLayout()
        self.formLayout.setLabelAlignment(Qt.AlignTop)
        self.formLayout.setSpacing(7)
        self.formLayout.setObjectName("formLayout")

        self.label_grid = QGridLayout()
        self.label_grid.setObjectName("gridLayout_2")

        self.name_label = QLabel(Form)
        self.name_label.setMinimumSize(QSize(500, 40))
        self.name_label.setMaximumSize(QSize(16777215, 40))
        self.name_label.setStyleSheet("background-color: #2c4c97; color: white; border: 1px solid black; font-size: 18px;")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setObjectName("name_label")
        self.name_label.hide()
        self.label_grid.addWidget(self.name_label, 0, 0, 1, 1)

        self.size_label = QLabel(Form)
        self.size_label.setMinimumSize(QSize(100, 40))
        self.size_label.setMaximumSize(QSize(16777215, 40))
        self.size_label.setStyleSheet("background-color: #2c4c97; color: white; border: 1px solid black; font-size: 18px;")
        self.size_label.setAlignment(Qt.AlignCenter)
        self.size_label.setObjectName("size_label")
        self.size_label.hide()
        self.label_grid.addWidget(self.size_label, 0, 2, 1, 1)

        self.length_label = QLabel(Form)
        self.length_label.setMinimumSize(QSize(100, 40))
        self.length_label.setMaximumSize(QSize(16777215, 40))
        self.length_label.setStyleSheet("background-color: #2c4c97; color: white; border: 1px solid black; font-size: 18px;")
        self.length_label.setAlignment(Qt.AlignCenter)
        self.length_label.setObjectName("length_label")
        self.length_label.hide()
        self.label_grid.addWidget(self.length_label, 0, 1, 1, 1)

        self.ext_label = QLabel(Form)
        self.ext_label.setMinimumSize(QSize(100, 40))
        self.ext_label.setMaximumSize(QSize(16777215, 40))
        self.ext_label.setStyleSheet("background-color: #2c4c97; color: white; border: 1px solid black; font-size: 18px;")
        self.ext_label.setAlignment(Qt.AlignCenter)
        self.ext_label.setObjectName("ext_label")
        self.ext_label.hide()
        self.label_grid.addWidget(self.ext_label, 0, 3, 1, 1)
        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.label_grid)
        self.formLayout.setLayout(1, QFormLayout.FieldRole, gridLayout_results)

        self.verticalLayout_3.addLayout(self.formLayout)
        download_grid.setObjectName("download_grid")
        folder_select.setMinimumSize(QSize(0, 38))
        folder_select.setStyleSheet("padding-left: 8px")
        folder_select.setObjectName("folder_select")
        folder_select.setDisabled(True)
        folder_select.clicked.connect(self.save_to)
        folder_select.hide()
        self.gridLayout.addWidget(folder_select, 1, 0, 1, 1)

        download_button.setMinimumSize(QSize(0, 40))
        download_button.setObjectName("download_button")
        download_button.setText("Download")
        download_button.setDisabled(True)
        download_button.clicked.connect(self.startDownloadWorker)
        download_button.hide()
        download_button.setStyleSheet('background-color: skyblue; color: black;')
        self.gridLayout.addWidget(download_button, 1, 1, 1, 1)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 8)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.fetch_button.setText(_translate("Form", "Fetch"))
        self.url_entry.setPlaceholderText(_translate("Form", "https://galaxyaudiobook.com/your_audiobook_url/"))
        self.name_label.setText(_translate("Form", "Name"))
        self.size_label.setText(_translate("Form", "Size"))
        self.length_label.setText(_translate("Form", "Length"))
        self.ext_label.setText(_translate("Form", "Format"))
        folder_select.setPlaceholderText(_translate("Form", "Select Folder"))

    def fetch_book_details(self):
        Form.resize(QSize(Form.width(),530))
        Form.setMinimumHeight(530)
        url = self.url_entry.text()
        download_button.setDisabled(True)
        # Before populating make sure there are no previous entries present.
        if gridLayout_results.rowCount() > 1:

            index = gridLayout_results.indexOf(self.name_label) + 1
            column = gridLayout_results.getItemPosition(index)[0]
            row_count = gridLayout_results.rowCount()
            for row in range(row_count):
                for column in range(gridLayout_results.columnCount()):
                    if row == 0: continue
                    layout = gridLayout_results.itemAtPosition(row,column)
                    do_not_delete = ['download_button','folder_select']
                    if layout is not None and layout.widget().objectName() not in do_not_delete:
                        print(layout.widget().objectName())
                        layout.widget().deleteLater()
                        gridLayout_results.removeItem(layout)

        if url == "" or "https://galaxyaudiobook.com/" not in url:
            msg = QMessageBox()
            msg.setWindowTitle("Oops!")
            msg.setText(f"You must enter a valid https://galaxyaudiobook.com/ URL")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Warning)
            self.fetch_button.setText("Fetch")
            self.fetch_button.setEnabled(True)
            response = msg.exec_()
            return False
        else:
            self.fetch_button.setText("Fetching...")
            self.fetch_button.setStyleSheet('background-color: #802828; color: white;')
            self.fetch_button.setDisabled(True)

            self.startFetchBookWorker(url)

    def save_to(self):
        global folder_save_to
        folder_save_to = QFileDialog.getExistingDirectory(Form, "Select Folder")
        folder_select.setText(folder_save_to)

    def addAudioRow(self, index, result):
        if self.name_label.isHidden(): self.name_label.show()
        if self.length_label.isHidden(): self.length_label.show()
        if self.size_label.isHidden(): self.size_label.show()
        if self.ext_label.isHidden(): self.ext_label.show()
        if index >= 10:
            new_height = Form.height() + 40
            Form.resize(QSize(Form.width(),new_height))
            Form.setMinimumHeight(new_height)
            
        checkBoxes[index] = QCheckBox(Form)
        checkBoxes[index].setMinimumSize(QSize(500, 30))
        checkBoxes[index].setMaximumSize(QSize(16777215, 16777215))
        checkBoxes[index].setText(result["name"])
        checkBoxes[index].setChecked(True)
        checkBoxes[index].setObjectName("checkBox")
        checkBoxes[index].setStyleSheet("font-size: 18px;")
        checkBoxes[index].setFont(QFont('Times New Roman'))
        gridLayout_results.addWidget(checkBoxes[index], index + 1, 1, 1, 1)

        self.lengths[index] = QLabel(Form)
        self.lengths[index].setStyleSheet("font-size: 18px;")
        self.lengths[index].setAlignment(Qt.AlignCenter)
        self.lengths[index].setObjectName("length")
        self.lengths[index].setText(result["duration"])
        self.lengths[index].setFont(QFont('Times New Roman'))
        gridLayout_results.addWidget(self.lengths[index], index + 1, 2, 1, 1)

        self.sizes[index] = QLabel(result["size"])
        self.sizes[index].setStyleSheet("font-size: 18px;")
        self.sizes[index].setAlignment(Qt.AlignCenter)
        self.sizes[index].setFont(QFont('Times New Roman'))
        gridLayout_results.addWidget(self.sizes[index], index + 1, 3, 1, 1)

        self.exts[index] = QLabel(result["ext"])
        self.exts[index].setStyleSheet("font-size: 18px;")
        self.exts[index].setAlignment(Qt.AlignCenter)
        self.exts[index].setFont(QFont('Times New Roman'))
        gridLayout_results.addWidget(self.exts[index], index + 1, 4, 1, 1)

    def fetchFinished(self, index, results):
        download_button.setEnabled(True)
        folder_select.setEnabled(True)
        pbar.hide()
        self.fetch_button.setText("Fetch")
        self.fetch_button.setStyleSheet('background-color: skyblue; color: black;')
        self.fetch_button.setEnabled(True)

        self.results = results
        checkBoxes[index + 2] = QCheckBox(Form)
        checkBoxes[index + 2].setText("")
        checkBoxes[index + 2].hide()
        checkBoxes[index + 2].setObjectName("checkBox")
        gridLayout_results.addWidget(checkBoxes[index + 2], index + 1, 0, 1, 1)

        pbar.setMinimum(0)
        pbar.setMaximum(len(checkBoxes))
        pbar.setAlignment(Qt.AlignCenter)
        pbar.setStyleSheet('font-size: 16px;')

        download_button.show()
        folder_select.show()
        self.gridLayout.addWidget(pbar, 2, 0, 1, 2)
        

    def displayFileDownloading(self, n):
        download_button.hide()
        folder_select.hide()
        rn = self.results[n]["name"]
        pbar.setValue(n)
        pbar.setFormat(f"Downloading {rn}")

    def downloadFinished(self, failures):
        pbar.hide()
        download_button.show()
        folder_select.show()
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Download Status")
        if not failures:
            msg.setText(f"Successfully downloaded {len(self.results)} tracks")
            msg.setIcon(QMessageBox.Information)
        elif len(failures) == len(self.results):
            msg.setText(f"Failed to download any tracks!")
            msg.setIcon(QMessageBox.Critical)
            msg.setInformativeText("\n".join(failures))
        else:
            missed = len(self.results) - len(failures)
            msg.setText(f"Failed to download {missed} of {len(self.results)}")
            msg.setInformativeText("\n".join(failures))
            msg.setIcon(QMessageBox.Warning)
        response = msg.exec_()

    def startDownloadWorker(self):
        pbar.show()
        self.thread = QThread()
        self.worker = DownloadWorker(self.results)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.displayFileDownloading)
        self.worker.finished.connect(self.downloadFinished)
        self.thread.start()

    def startFetchBookWorker(self, url):
        self.thread = QThread()
        self.worker = FetchBookWorker(url)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.addAudioRow)
        self.worker.finished.connect(self.fetchFinished)
        self.thread.start()

class FetchBookWorker(QObject):
    finished = pyqtSignal(int, list)
    progress = pyqtSignal(int, dict)

    def __init__(self, url):
        super(FetchBookWorker, self).__init__()
        self.url = url
        self.results = []

    def run(self):
        url = self.url
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        self.script_tags = str(soup.find_all("script")).split("\n")

        result_index = 0
        for index, line in enumerate(self.script_tags):
            if (
                '"chapter_link_dropbox":' in line
                and "welcome-you-to-galaxyaudio" not in line
            ):
                duration = (
                    self.script_tags[index + 1].split('"duration": ')[-1].split('"')[1]
                )
                mp3_path = (
                    line.split('"chapter_link_dropbox": ')[1]
                    .lstrip('"')
                    .rstrip('",')
                    .replace(" ", "%20")
                    .replace("\/", "/")
                )
                name = (
                    mp3_path.split("/")[-1]
                    .replace("%20", " ")
                    .replace(".mp3", "")
                    .replace(" - ", "SAVE+SAVE")
                    .replace("-", " ")
                    .replace("SAVE+SAVE", " - ")
                )
                ext = mp3_path[-3:]
                size = sizeof_fmt(
                    int(
                        requests.get(file_server + mp3_path, stream=True).headers[
                            "Content-length"
                        ]
                    )
                )
                result = {
                    "name": name,
                    "mp3_path": file_server + mp3_path,
                    "duration": duration,
                    "size": size,
                    "ext": ext,
                }
                self.results.append(result)
                self.progress.emit(result_index, result)
                result_index += 1
        self.finished.emit(result_index, self.results)

class DownloadWorker(QObject):
    finished = pyqtSignal(list)
    progress = pyqtSignal(int)

    def __init__(self, results):
        super(DownloadWorker, self).__init__()
        self.results = results

    def run(self):
        download_list = []
        failures = []
        for index, cb in enumerate(checkBoxes):
            if checkBoxes[cb].isChecked():
                download_list.append(self.results[index])

        s = requests.session()
        s.headers = headers

        for index, dl in enumerate(download_list):
            self.filename = dl["mp3_path"].split("/")[-1].replace("%20", " ")
            try:
                self.progress.emit(index)
                doc = s.get(dl["mp3_path"])
                if doc.status_code == 200:
                    with open(f"{folder_save_to}/{self.filename}", "wb") as f:
                        print(f"Saving file to {folder_save_to}/{self.filename}")
                        f.write(doc.content)
                else:
                    failures.append(f"{doc.status_code}: {self.filename}")
            except Exception as e:
                failures.append(f"{e} - {self.filename}")
        s.close()
        self.finished.emit(failures)


if __name__ == "__main__":

    app = QApplication([])

    gridLayout_results = QGridLayout()
    download_grid = QGridLayout()

    folder_select = ClickableLineEdit()
    download_button = QPushButton()
    pbar = QProgressBar()

    Form = QWidget()
    ui = FetchBookObject()
    ui.setupUi(Form)

    scroll = QScrollArea()
    scroll.setWindowTitle("GalaxyScraper")
    scroll.setStyleSheet('width: 0px;')
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll.setWidgetResizable(True)
    scroll.setMinimumSize(QSize(1030, 530))
    scroll.setWidget(Form)
    scroll.show()

    sys.exit(app.exec_())
