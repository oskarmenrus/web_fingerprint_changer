from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

from fingerprint_changer import *

import os
import sys


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("RinasBrowser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Версия 1.0"))
        layout.addWidget(QLabel("Информационная безопасность 2020"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.screenShape = QDesktopWidget().screenGeometry()
        self.width = self.screenShape.width()
        self.height = self.screenShape.height()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://google.com"))
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Навигация")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Вернуться на предыдущую страницу", self)
        back_btn.setStatusTip("Вернуться на предыдущую страницу")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Вернуться на следующую страницу", self)
        next_btn.setStatusTip("Вернуться на следующую страницу")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Перезагрузить страницу", self)
        reload_btn.setStatusTip("Перезагрузить страницу")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Домашняя страница", self)
        home_btn.setStatusTip("Домашняя страница")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        change_btn = QAction("Изменить браузерный отпечаток", self)
        change_btn.setStatusTip("Изменить браузерный отпечаток")
        change_btn.setFont(QFont("Times", 10))
        change_btn.triggered.connect(self.change_fingerprint)
        navtb.addAction(change_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Стоп", self)
        stop_btn.setStatusTip("Остановить загрузку страницы")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        file_menu = self.menuBar().addMenu("&Файл")

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Открыть файл...", self)
        open_file_action.setStatusTip("Открыть файл")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Сохранить страницу как...", self)
        save_file_action.setStatusTip("Сохранить текущую страницу как...")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Распечатать...", self)
        print_action.setStatusTip("Распечатать текущую страницу...")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Помощь")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "О браузере...", self)
        about_action.setStatusTip("Узнать больше о RinasBrowser...")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')), "RinasBrowser - Домашняя страница", self)
        navigate_action.setStatusTip("Перейти на домашнюю страницу RinasBrowser")
        navigate_action.triggered.connect(self.navigate_rinasbrowser)
        help_menu.addAction(navigate_action)

        self.show()
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))

    def random_settings(self):
        true_false = [True, False]
        self.browser.page().profile().clearAllVisitedLinks()
        self.browser.page().profile().clearHttpCache()
        self.browser.page().profile().setHttpCacheType(QWebEngineProfile.NoCache)
        self.browser.page().profile().setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        self.browser.page().settings().setAttribute(QWebEngineSettings.AutoLoadImages, random.choice(true_false))
        self.browser.page().settings().setAttribute(QWebEngineSettings.JavascriptEnabled, random.choice(true_false))
        self.browser.page().settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, random.choice(true_false))
        self.browser.page().settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, random.choice(true_false))
        self.browser.page().settings().setAttribute(QWebEngineSettings.PluginsEnabled, random.choice(true_false))
        self.browser.page().settings().setAttribute(QWebEngineSettings.WebGLEnabled, random.choice(true_false))
        self.browser.page().settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, random.choice(true_false))

    def random_time(self):
        # time_zone = random.choice(QTimeZone.availableTimeZoneIds())
        # print(QTimeZone.ianaIdToWindowsId(time_zone))
        # print(QTimeZone.systemTimeZone())
        print(self.QDateTime.date())

    def change_fingerprint(self):
        self.random_settings()
        self.random_time()
        change_user_agent(self)
        generate_accept_language(self)
        change_screen_size(self, self.width, self.height)
        print('Браузерные отпечатки были успешно изменены!')
        separator()

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - RinasBrowser" % title)

    def navigate_rinasbrowser(self):
        self.browser.setUrl(QUrl("https://vk.com/khuysosi13"))

    @staticmethod
    def about():
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "Все файлы (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить страницу как...", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "Все файлы (*.*)")

        if filename:
            html = self.browser.page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):
        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("RinasBrowser")
app.setOrganizationName("RinasBrowser")
app.setOrganizationDomain("RinasBrowser.org")

window = MainWindow()
window.showMaximized()

app.exec_()
