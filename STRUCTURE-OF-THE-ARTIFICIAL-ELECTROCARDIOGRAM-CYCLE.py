import random
import sys
import math
import numpy as np
import json
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QPushButton, QDialog, QLabel, \
    QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class NoMainWindow(QMainWindow):
    def __init__(self, _params, _n, _fh, _noise_lvl, _alt_lvl):
        super(NoMainWindow, self).__init__()

        # Параметри необхідні для обрахунків графіку
        self.fh = _fh
        self.t0 = 60 / self.fh
        self.params = _params
        self.n = _n
        self.alt_lvl = _alt_lvl
        self.noise_lvl = _noise_lvl

        # Налаштування параметрів головного вікна
        self.setWindowTitle("Генерація")
        self.setGeometry(100, 100, 1000, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Розміщення графіку на головному вікні
        self.fig = Figure(figsize=(5, 4), dpi=100)

        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.canvas.setFixedSize(QSize(1000, 650))
        # Відображення графіку
        self.ax = self.fig.add_subplot(111)

        if not self.alt_lvl:
            self.plot_data()
        else:
            self.plot_data_with_alt()

    # Функція виведення графіку
    def plot_data(self):
        self.ax.clear()
        self.ax.grid()
        self.ax.set_ylim(ymin=-1, ymax=1.5)
        XX = np.arange(0, self.t0 + 0.001, 0.001)
        YY = np.arange(0, self.t0 + 0.001, 0.001)

        dct_keys = list(self.params.keys())
        for f in range(1, len(dct_keys)):
            i = dct_keys[f - 1]
            i_next = dct_keys[f]
            for j in range(len(YY)):
                if self.params[i]['t1'] <= XX[j] <= self.params[i_next]['t1']:
                    bt = float
                    if XX[j] <= self.params[i]['m']:
                        bt = self.params[i]['b1']
                    else:
                        bt = self.params[i]['b2']
                    YY[j] = self.params[i]['a'] * math.exp(-((math.pow(XX[j] - self.params[i]['m'], 2)) / (
                        (2 * math.pow(bt, 2)) if (2 * math.pow(bt, 2)) != 0 else 0.0001)))

        for j in range(len(YY)):
            if self.params['T']['t1'] <= XX[j] <= 1 * self.t0:
                bt = float
                if XX[j] <= self.params["T"]['m']:
                    bt = self.params["T"]['b1']
                else:
                    bt = self.params["T"]['b2']
                YY[j] = self.params["T"]['a'] * math.exp(-((math.pow(XX[j] - self.params["T"]['m'], 2)) / (
                    (2 * math.pow(bt, 2)) if (2 * math.pow(bt, 2)) != 0 else 0.0001)))
        x = np.arange(0, (self.t0 + 0.001) * self.n, 0.001)
        y = YY
        for i in range(self.n - 1):
            y = np.concatenate((y, YY), axis=0)
        for j in range(len(y)):
            y[j] = y[j] + random.uniform(0, self.noise_lvl)
        self.ax.plot(x, y)
        with open('data1.json', 'w') as f:
            json.dump([x.tolist(), y.tolist()], f)

        self.canvas.draw()

    def plot_data_with_alt(self):
        self.ax.clear()
        self.ax.grid()
        self.ax.set_ylim(ymin=-1, ymax=1.5)
        XX1 = np.arange(0, self.t0 + 0.001, 0.001)
        YY1 = np.arange(0, self.t0 + 0.001, 0.001)
        XX2 = np.arange(0, self.t0 + 0.001, 0.001)
        YY2 = np.arange(0, self.t0 + 0.001, 0.001)

        dct_keys = list(self.params.keys())
        for f in range(1, len(dct_keys)):
            i = dct_keys[f - 1]
            i_next = dct_keys[f]
            for j in range(len(YY1)):
                if self.params[i]['t1'] <= XX1[j] <= self.params[i_next]['t1']:
                    bt = float
                    if XX1[j] <= self.params[i]['m']:
                        bt = self.params[i]['b1']
                    else:
                        bt = self.params[i]['b2']
                    YY1[j] = self.params[i]['a'] * math.exp(-((math.pow(XX1[j] - self.params[i]['m'], 2)) / (
                        (2 * math.pow(bt, 2)) if (2 * math.pow(bt, 2)) != 0 else 0.0001)))

        for j in range(len(YY1)):
            if self.params['T']['t1'] <= XX1[j] <= 1 * self.t0:
                bt = float
                if XX1[j] <= self.params["T"]['m']:
                    bt = self.params["T"]['b1']
                else:
                    bt = self.params["T"]['b2']
                YY1[j] = self.params["T"]['a'] * math.exp(-((math.pow(XX1[j] - self.params["T"]['m'], 2)) / (
                    (2 * math.pow(bt, 2)) if (2 * math.pow(bt, 2)) != 0 else 0.0001)))

        dct_keys = list(self.params.keys())
        for f in range(1, len(dct_keys)):
            i = dct_keys[f - 1]
            i_next = dct_keys[f]
            for j in range(len(YY2)):
                if self.params[i]['t1'] <= XX2[j] <= self.params[i_next]['t1']:
                    bt = float
                    if XX2[j] <= self.params[i]['m']:
                        bt = self.params[i]['b1']
                    else:
                        bt = self.params[i]['b2']
                    YY2[j] = self.params[i]['a'] * math.exp(-((math.pow(XX2[j] - self.params[i]['m'], 2)) / (
                        (2 * math.pow(bt, 2)) if (2 * math.pow(bt, 2)) != 0 else 0.0001)))

        for j in range(len(YY2)):
            if self.params['T']['t1'] <= XX2[j] <= 1 * self.t0:
                bt = float
                if XX2[j] <= self.params["T"]['m']:
                    bt = self.params["T"]['b1']
                else:
                    bt = self.params["T"]['b2']
                YY2[j] = (self.params["T"]['a'] + self.alt_lvl) * math.exp(
                    -((math.pow(XX2[j] - self.params["T"]['m'], 2)) / (
                        (2 * math.pow(bt, 2)) if (2 * math.pow(bt, 2)) != 0 else 0.0001)))

        x = np.arange(0, (self.t0 + 0.001) * self.n, 0.001)
        y = YY1
        for i in range(self.n - 1):
            if i % 2 == 0:
                y = np.concatenate((y, YY2), axis=0)
            else:
                y = np.concatenate((y, YY1), axis=0)
        for j in range(len(y)):
            y[j] = y[j] + random.uniform(0, self.noise_lvl)

        self.ax.plot(x, y)
        with open('data1.json', 'w') as f:
            json.dump([x.tolist(), y.tolist()], f)
        self.canvas.draw()


# Підкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Параметри необхідні для обрахунків графіку
        self.fh = 60
        self.t0 = 60 / self.fh
        self.n = 30
        self.noise_lvl = 0
        self.alt_lvl = 0
        self.static_params = {"P": {"a": .11, "m": .35, "b1": .03, "b2": .03, "t1": 0, "t2": .44},
                              "Q": {"a": -.1, "m": .47, "b1": .01, "b2": .01, "t1": .44, "t2": .48},
                              "R": {"a": 1, "m": .49, "b1": .01, "b2": .01, "t1": .48, "t2": .51},
                              "S": {"a": -.17, "m": .516, "b1": .01, "b2": .02, "t1": .51, "t2": .58},
                              "ST": {"a": .01, "m": .6, "b1": .01, "b2": .01, "t1": .58, "t2": .6},
                              "T": {"a": .2, "m": .712, "b1": .04, "b2": .04, "t1": .58, "t2": 1}}

        self.params = {"P": {"a": .11, "m": .35, "b1": .03, "b2": .03, "t1": 0, "t2": .44},
                       "Q": {"a": -.1, "m": .47, "b1": .01, "b2": .01, "t1": .44, "t2": .48},
                       "R": {"a": 1, "m": .49, "b1": .01, "b2": .01, "t1": .48, "t2": .51},
                       "S": {"a": -.17, "m": .516, "b1": .01, "b2": .02, "t1": .51, "t2": .58},
                       "ST": {"a": .01, "m": .6, "b1": .01, "b2": .01, "t1": .58, "t2": .6},
                       "T": {"a": .2, "m": .712, "b1": .04, "b2": .04, "t1": .58, "t2": 1}}

        # Налаштування параметрів головного вікна
        self.setWindowTitle("Модель Кардіоцикла")
        self.setGeometry(100, 100, 950, 520)
        # self.setFixedSize(QSize(1200, 700))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Розміщення графіку на головному вікні
        self.fig = Figure(figsize=(1, 1), dpi=100)
        self.fig.canvas.draw()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFixedSize(QSize(700, 450))
        layout.addWidget(self.canvas)
        # Відображення графіку
        self.ax = self.fig.add_subplot(111)
        self.plot_data()

        # Розміщення кнопок на головному вікні
        self.bp = QPushButton("P", self)
        self.bp.setMaximumWidth(100)
        self.bp.setMaximumHeight(25)
        self.bp.clicked.connect(self.update_data_p)
        self.bp.move(760, 60)
        # layout.addWidget(self.bp)

        self.bq = QPushButton("Q", self)
        self.bq.setMaximumWidth(100)
        self.bq.setMaximumHeight(25)
        self.bq.clicked.connect(self.update_data_q)
        self.bq.move(760, 80)
        self.br = QPushButton("R", self)
        self.br.setMaximumWidth(100)
        self.br.setMaximumHeight(25)
        self.br.clicked.connect(self.update_data_r)
        self.br.move(760, 100)
        self.bs = QPushButton("S", self)
        self.bs.setMaximumWidth(100)
        self.bs.setMaximumHeight(25)
        self.bs.clicked.connect(self.update_data_s)
        self.bs.move(760, 120)
        self.bst = QPushButton("ST", self)
        self.bst.setMaximumWidth(100)
        self.bst.setMaximumHeight(25)
        self.bst.clicked.connect(self.update_data_st)
        self.bst.move(760, 140)
        self.bt = QPushButton("T", self)
        self.bt.setMaximumWidth(100)
        self.bt.setMaximumHeight(25)
        self.bt.clicked.connect(self.update_data_t)
        self.bt.move(760, 160)

        # ЧСС
        self.lb1 = QLabel('ЧСС(уд/хв)', self)
        self.lb1.setFixedSize(QSize(100, 20))
        self.lb1.move(760, 180)
        self.qle = QLineEdit(self)
        self.qle.move(760, 200)
        self.qle.setMaximumHeight(100)
        self.qle.setText(str(self.fh))
        self.qle.textChanged.connect(self.update_qle_1)

        # Генерація
        self.gen_b = QPushButton("Генерація", self)
        self.gen_b.setFixedSize(QSize(120, 30))
        self.gen_b.move(760, 250)
        self.gen_b.clicked.connect(self.generation)
        self.lb2 = QLabel('Кількість повторів', self)
        self.lb2.setFixedSize(QSize(120, 30))
        self.lb2.move(760, 280)
        self.qle2 = QLineEdit(self)
        self.qle2.move(760, 310)
        self.qle2.setFixedSize(QSize(100, 30))
        self.qle2.setText(str(self.n))
        self.qle2.textChanged.connect(self.update_qle_2)

        self.lb_alt = QLabel('Рівень альтернації, мв', self)
        self.lb_alt.setFixedSize(QSize(200, 30))
        self.lb_alt.move(760, 340)
        self.sl_alt = QSlider(Qt.Orientation.Horizontal, self)
        self.sl_alt.setRange(0, 100)
        self.sl_alt.setValue(0)
        self.sl_alt.valueChanged.connect(self.update_alt)
        self.sl_alt.move(760, 360)

        self.lb_noise = QLabel('Рівень шуму', self)
        self.lb_noise.setFixedSize(QSize(200, 30))
        self.lb_noise.move(760, 390)
        self.sl_noise = QSlider(Qt.Orientation.Horizontal, self)
        self.sl_noise.setRange(0, 100)
        self.sl_noise.setValue(0)
        self.sl_noise.valueChanged.connect(self.update_noise)
        self.sl_noise.move(760, 410)

    def update_alt(self, value):
        self.alt_lvl = value / 100

    def update_noise(self, value):
        self.noise_lvl = value / 100

    def update_qle_2(self, value):
        if value != '':
            self.n = int(value)
        else:
            self.n = 30

    def generation(self):
        window2 = NoMainWindow(self.params, self.n, self.fh, self.noise_lvl, self.alt_lvl)

        window2.show()

    def update_qle_1(self, value):

        if value != '':
            self.fh = int(value)
            self.t0 = 60 / self.fh
            if 300 >= int(value) >= 20:

                for i in self.params.keys():
                    self.params[i]['m'] = self.static_params[i]['m'] * self.t0
                    self.params[i]['t1'] = self.static_params[i]['t1'] * self.t0
                    self.params[i]['b1'] = self.static_params[i]['b1'] * self.t0
                    self.params[i]['b2'] = self.static_params[i]['b2'] * self.t0
                self.plot_data()
        else:
            self.fh = 60
            self.t0 = 1
            for i in self.params.keys():
                self.params[i]['m'] = self.static_params[i]['m'] * self.t0
                self.params[i]['t1'] = self.static_params[i]['t1'] * self.t0
            self.plot_data()

    # Функція виведення графіку
    def plot_data(self):
        self.ax.clear()
        self.ax.grid()
        self.ax.set_ylim(ymin=-.3, ymax=1)
        XX = np.arange(0, self.t0 + 0.001, 0.001)
        YY = 0 * XX
        dct_keys = list(self.params.keys())
        for f in range(1, len(dct_keys)):
            i = dct_keys[f - 1]
            i_next = dct_keys[f]
            # t1 = self.params[i]['m'] - 3 * self.params[i]['b1']
            # t2 = self.params[i]['m'] + 3 * self.params[i]['b2']
            # print(t1, t2)
            for j in range(len(YY)):
                if self.params[i]['t1'] <= XX[j] <= self.params[i_next][
                    't1']:  # self.params[i]['t1'] <= XX[j] <= self.params[i_next]['t1']     t1 <= XX[j] <= t2
                    bt = float
                    if XX[j] <= self.params[i]['m']:
                        bt = self.params[i]['b1']
                    else:
                        bt = self.params[i]['b2']
                    YY[j] = self.params[i]['a'] * math.exp(-((math.pow(XX[j] - self.params[i]['m'], 2)) / (
                        (2 * math.pow(bt, 2)) if (2 * math.pow(bt, 2)) != 0 else 0.0001)))
        # t1 = self.params["T"]['m'] - 3 * self.params["T"]['b1']
        # t2 = self.params["T"]['m'] + 3 * self.params["T"]['b2']
        for j in range(len(YY)):
            if self.params['T']['t1'] <= XX[j] <= 1 * self.t0:  # t1 <= XX[j] <= t2    self.params['T']['t1']
                bt = float
                if XX[j] <= self.params["T"]['m']:
                    bt = self.params["T"]['b1']
                else:
                    bt = self.params["T"]['b2']
                YY[j] = self.params["T"]['a'] * math.exp(-((math.pow(XX[j] - self.params["T"]['m'], 2)) / (
                    (2 * math.pow(bt, 2)) if (2 * math.pow(bt, 2)) != 0 else 0.0001)))

        self.ax.plot(XX, YY)
        self.canvas.draw()

    # Відкриття діалогових вікон
    def update_data_p(self):
        param = "P"

        def updateLabel1(value):
            lb1.setText(str(value / 1000))
            self.params[param]["a"] = value / 1000
            self.plot_data()

        def updateLabel2(value):
            lb2.setText(str(value / 1000))
            self.params[param]["m"] = value / 1000
            self.plot_data()

        def updateLabel3(value):
            lb3.setText(str(value / 1000))
            self.params[param]["b1"] = value / 1000
            self.plot_data()

        def updateLabel4(value):
            lb4.setText(str(value / 1000))
            self.params[param]["b2"] = value / 1000
            self.plot_data()

        d = QDialog()
        d.setWindowTitle("Параметри зубця {}".format(param))
        d.setFixedSize(250, 220)

        lb1 = QLabel(str(round(self.params[param]["a"], 3)), d)
        lb1.setMinimumWidth(30)
        lb1.move(20, 30)
        lb2 = QLabel(str(round(self.params[param]["m"], 3)), d)
        lb2.setMinimumWidth(30)
        lb2.move(20, 60)
        lb3 = QLabel(str(round(self.params[param]["b1"], 3)), d)
        lb3.setMinimumWidth(30)
        lb3.move(20, 90)
        lb4 = QLabel(str(round(self.params[param]["b2"], 3)), d)
        lb4.setMinimumWidth(30)
        lb4.move(20, 120)
        lb11 = QLabel('Aмплітуда', d)
        lb11.setMinimumWidth(30)
        lb11.move(180, 30)
        lb12 = QLabel('Час', d)
        lb12.setMinimumWidth(30)
        lb12.move(180, 60)
        lb13 = QLabel('Ширина(1)', d)
        lb13.setMinimumWidth(30)
        lb13.move(180, 90)
        lb14 = QLabel('Ширина(2)', d)
        lb14.setMinimumWidth(30)
        lb14.move(180, 120)

        sl1 = QSlider(Qt.Orientation.Horizontal, d)
        sl1.setRange(-300, 1000)
        sl1.setValue(self.params[param]["a"] * 1000)
        sl1.valueChanged.connect(updateLabel1)
        sl1.move(80, 30)
        sl2 = QSlider(Qt.Orientation.Horizontal, d)
        sl2.setRange(0, 1000)
        sl2.setValue(self.params[param]["m"] * 1000)
        sl2.valueChanged.connect(updateLabel2)
        sl2.move(80, 60)
        sl3 = QSlider(Qt.Orientation.Horizontal, d)
        sl3.setRange(0, 1000)
        sl3.setValue(self.params[param]["b1"] * 1000)
        sl3.valueChanged.connect(updateLabel3)
        sl3.move(80, 90)
        sl4 = QSlider(Qt.Orientation.Horizontal, d)
        sl4.setRange(0, 1000)
        sl4.setValue(self.params[param]["b2"] * 1000)
        sl4.valueChanged.connect(updateLabel4)
        sl4.move(80, 120)

        def close_dialog():
            d.close()

        b = QPushButton("Зберігти", d)
        b.clicked.connect(close_dialog)
        b.move(100, 150)

        d.show()
        d.exec()

    def update_data_q(self):
        param = "Q"

        def updateLabel1(value):
            lb1.setText(str(value / 1000))
            self.params[param]["a"] = value / 1000
            self.plot_data()

        def updateLabel2(value):
            lb2.setText(str(value / 1000))
            self.params[param]["m"] = value / 1000
            self.plot_data()

        def updateLabel3(value):
            lb3.setText(str(value / 1000))
            self.params[param]["b1"] = value / 1000
            self.plot_data()

        def updateLabel4(value):
            lb4.setText(str(value / 1000))
            self.params[param]["b2"] = value / 1000
            self.plot_data()

        d = QDialog()
        d.setWindowTitle("Параметри зубця {}".format(param))
        d.setFixedSize(250, 220)

        lb1 = QLabel(str(round(self.params[param]["a"], 3)), d)
        lb1.setMinimumWidth(30)
        lb1.move(20, 30)
        lb2 = QLabel(str(round(self.params[param]["m"], 3)), d)
        lb2.setMinimumWidth(30)
        lb2.move(20, 60)
        lb3 = QLabel(str(round(self.params[param]["b1"], 3)), d)
        lb3.setMinimumWidth(30)
        lb3.move(20, 90)
        lb4 = QLabel(str(round(self.params[param]["b2"], 3)), d)
        lb4.setMinimumWidth(30)
        lb4.move(20, 120)
        lb11 = QLabel('Aмплітуда', d)
        lb11.setMinimumWidth(30)
        lb11.move(180, 30)
        lb12 = QLabel('Час', d)
        lb12.setMinimumWidth(30)
        lb12.move(180, 60)
        lb13 = QLabel('Ширина(1)', d)
        lb13.setMinimumWidth(30)
        lb13.move(180, 90)
        lb14 = QLabel('Ширина(2)', d)
        lb14.setMinimumWidth(30)
        lb14.move(180, 120)

        sl1 = QSlider(Qt.Orientation.Horizontal, d)
        sl1.setRange(-300, 1000)
        sl1.setValue(self.params[param]["a"] * 1000)
        sl1.valueChanged.connect(updateLabel1)
        sl1.move(80, 30)
        sl2 = QSlider(Qt.Orientation.Horizontal, d)
        sl2.setRange(0, 1000)
        sl2.setValue(self.params[param]["m"] * 1000)
        sl2.valueChanged.connect(updateLabel2)
        sl2.move(80, 60)
        sl3 = QSlider(Qt.Orientation.Horizontal, d)
        sl3.setRange(0, 1000)
        sl3.setValue(self.params[param]["b1"] * 1000)
        sl3.valueChanged.connect(updateLabel3)
        sl3.move(80, 90)
        sl4 = QSlider(Qt.Orientation.Horizontal, d)
        sl4.setRange(0, 1000)
        sl4.setValue(self.params[param]["b2"] * 1000)
        sl4.valueChanged.connect(updateLabel4)
        sl4.move(80, 120)

        def close_dialog():
            d.close()

        b = QPushButton("Зберігти", d)
        b.clicked.connect(close_dialog)
        b.move(100, 150)

        d.show()
        d.exec()

    def update_data_r(self):
        param = "R"

        def updateLabel1(value):
            lb1.setText(str(value / 1000))
            self.params[param]["a"] = value / 1000
            self.plot_data()

        def updateLabel2(value):
            lb2.setText(str(value / 1000))
            self.params[param]["m"] = value / 1000
            self.plot_data()

        def updateLabel3(value):
            lb3.setText(str(value / 1000))
            self.params[param]["b1"] = value / 1000
            self.plot_data()

        def updateLabel4(value):
            lb4.setText(str(value / 1000))
            self.params[param]["b2"] = value / 1000
            self.plot_data()

        d = QDialog()
        d.setWindowTitle("Параметри зубця {}".format(param))
        d.setFixedSize(250, 220)

        lb1 = QLabel(str(round(self.params[param]["a"], 3)), d)
        lb1.setMinimumWidth(30)
        lb1.move(20, 30)
        lb2 = QLabel(str(round(self.params[param]["m"], 3)), d)
        lb2.setMinimumWidth(30)
        lb2.move(20, 60)
        lb3 = QLabel(str(round(self.params[param]["b1"], 3)), d)
        lb3.setMinimumWidth(30)
        lb3.move(20, 90)
        lb4 = QLabel(str(round(self.params[param]["b2"], 3)), d)
        lb4.setMinimumWidth(30)
        lb4.move(20, 120)
        lb11 = QLabel('Aмплітуда', d)
        lb11.setMinimumWidth(30)
        lb11.move(180, 30)
        lb12 = QLabel('Час', d)
        lb12.setMinimumWidth(30)
        lb12.move(180, 60)
        lb13 = QLabel('Ширина(1)', d)
        lb13.setMinimumWidth(30)
        lb13.move(180, 90)
        lb14 = QLabel('Ширина(2)', d)
        lb14.setMinimumWidth(30)
        lb14.move(180, 120)

        sl1 = QSlider(Qt.Orientation.Horizontal, d)
        sl1.setRange(-300, 1000)
        sl1.setValue(self.params[param]["a"] * 1000)
        sl1.valueChanged.connect(updateLabel1)
        sl1.move(80, 30)
        sl2 = QSlider(Qt.Orientation.Horizontal, d)
        sl2.setRange(0, 1000)
        sl2.setValue(self.params[param]["m"] * 1000)
        sl2.valueChanged.connect(updateLabel2)
        sl2.move(80, 60)
        sl3 = QSlider(Qt.Orientation.Horizontal, d)
        sl3.setRange(0, 1000)
        sl3.setValue(self.params[param]["b1"] * 1000)
        sl3.valueChanged.connect(updateLabel3)
        sl3.move(80, 90)
        sl4 = QSlider(Qt.Orientation.Horizontal, d)
        sl4.setRange(0, 1000)
        sl4.setValue(self.params[param]["b2"] * 1000)
        sl4.valueChanged.connect(updateLabel4)
        sl4.move(80, 120)

        def close_dialog():
            d.close()

        b = QPushButton("Зберігти", d)
        b.clicked.connect(close_dialog)
        b.move(100, 150)

        d.show()
        d.exec()

    def update_data_s(self):
        param = "S"

        def updateLabel1(value):
            lb1.setText(str(value / 1000))
            self.params[param]["a"] = value / 1000
            self.plot_data()

        def updateLabel2(value):
            lb2.setText(str(value / 1000))
            self.params[param]["m"] = value / 1000
            self.plot_data()

        def updateLabel3(value):
            lb3.setText(str(value / 1000))
            self.params[param]["b1"] = value / 1000
            self.plot_data()

        def updateLabel4(value):
            lb4.setText(str(value / 1000))
            self.params[param]["b2"] = value / 1000
            self.plot_data()

        d = QDialog()
        d.setWindowTitle("Параметри зубця {}".format(param))
        d.setFixedSize(250, 220)

        lb1 = QLabel(str(round(self.params[param]["a"], 3)), d)
        lb1.setMinimumWidth(30)
        lb1.move(20, 30)
        lb2 = QLabel(str(round(self.params[param]["m"], 3)), d)
        lb2.setMinimumWidth(30)
        lb2.move(20, 60)
        lb3 = QLabel(str(round(self.params[param]["b1"], 3)), d)
        lb3.setMinimumWidth(30)
        lb3.move(20, 90)
        lb4 = QLabel(str(round(self.params[param]["b2"], 3)), d)
        lb4.setMinimumWidth(30)
        lb4.move(20, 120)
        lb11 = QLabel('Aмплітуда', d)
        lb11.setMinimumWidth(30)
        lb11.move(180, 30)
        lb12 = QLabel('Час', d)
        lb12.setMinimumWidth(30)
        lb12.move(180, 60)
        lb13 = QLabel('Ширина(1)', d)
        lb13.setMinimumWidth(30)
        lb13.move(180, 90)
        lb14 = QLabel('Ширина(2)', d)
        lb14.setMinimumWidth(30)
        lb14.move(180, 120)

        sl1 = QSlider(Qt.Orientation.Horizontal, d)
        sl1.setRange(-300, 1000)
        sl1.setValue(self.params[param]["a"] * 1000)
        sl1.valueChanged.connect(updateLabel1)
        sl1.move(80, 30)
        sl2 = QSlider(Qt.Orientation.Horizontal, d)
        sl2.setRange(0, 1000)
        sl2.setValue(self.params[param]["m"] * 1000)
        sl2.valueChanged.connect(updateLabel2)
        sl2.move(80, 60)
        sl3 = QSlider(Qt.Orientation.Horizontal, d)
        sl3.setRange(0, 1000)
        sl3.setValue(self.params[param]["b1"] * 1000)
        sl3.valueChanged.connect(updateLabel3)
        sl3.move(80, 90)
        sl4 = QSlider(Qt.Orientation.Horizontal, d)
        sl4.setRange(0, 1000)
        sl4.setValue(self.params[param]["b2"] * 1000)
        sl4.valueChanged.connect(updateLabel4)
        sl4.move(80, 120)

        def close_dialog():
            d.close()

        b = QPushButton("Зберігти", d)
        b.clicked.connect(close_dialog)
        b.move(100, 150)

        d.show()
        d.exec()

    def update_data_st(self):
        param = "ST"

        d = QDialog()
        d.setWindowTitle("Параметри зубця {}".format(param))
        d.setFixedSize(250, 60)

        def close_dialog():
            d.close()

        b = QPushButton("Скористайтесь іншим параметром", d)
        b.clicked.connect(close_dialog)
        b.move(0, 10)

        d.show()
        d.exec()

    def update_data_t(self):
        param = "T"

        def updateLabel1(value):
            lb1.setText(str(value / 1000))
            self.params[param]["a"] = value / 1000
            self.plot_data()

        def updateLabel2(value):
            lb2.setText(str(value / 1000))
            self.params[param]["m"] = value / 1000
            self.plot_data()

        def updateLabel3(value):
            lb3.setText(str(value / 1000))
            self.params[param]["b1"] = value / 1000
            self.plot_data()

        def updateLabel4(value):
            lb4.setText(str(value / 1000))
            self.params[param]["b2"] = value / 1000
            self.plot_data()

        d = QDialog()
        d.setWindowTitle("Параметри зубця {}".format(param))
        d.setFixedSize(250, 330)

        lb1 = QLabel(str(round(self.params[param]["a"], 3)), d)
        lb1.setMinimumWidth(30)
        lb1.move(20, 30)
        lb2 = QLabel(str(round(self.params[param]["m"], 3)), d)
        lb2.setMinimumWidth(30)
        lb2.move(20, 60)
        lb3 = QLabel(str(round(self.params[param]["b1"], 3)), d)
        lb3.setMinimumWidth(30)
        lb3.move(20, 90)
        lb4 = QLabel(str(round(self.params[param]["b2"], 3)), d)
        lb4.setMinimumWidth(30)
        lb4.move(20, 120)
        lb11 = QLabel('Aмплітуда', d)
        lb11.setMinimumWidth(30)
        lb11.move(180, 30)
        lb12 = QLabel('Час', d)
        lb12.setMinimumWidth(30)
        lb12.move(180, 60)
        lb13 = QLabel('Ширина(1)', d)
        lb13.setMinimumWidth(30)
        lb13.move(180, 90)
        lb14 = QLabel('Ширина(2)', d)
        lb14.setMinimumWidth(30)
        lb14.move(180, 120)

        sl1 = QSlider(Qt.Orientation.Horizontal, d)
        sl1.setRange(-300, 1000)
        sl1.setValue(self.params[param]["a"] * 1000)
        sl1.valueChanged.connect(updateLabel1)
        sl1.move(80, 30)
        sl2 = QSlider(Qt.Orientation.Horizontal, d)
        sl2.setRange(0, 1000)
        sl2.setValue(self.params[param]["m"] * 1000)
        sl2.valueChanged.connect(updateLabel2)
        sl2.move(80, 60)
        sl3 = QSlider(Qt.Orientation.Horizontal, d)
        sl3.setRange(0, 1000)
        sl3.setValue(self.params[param]["b1"] * 1000)
        sl3.valueChanged.connect(updateLabel3)
        sl3.move(80, 90)
        sl4 = QSlider(Qt.Orientation.Horizontal, d)
        sl4.setRange(0, 1000)
        sl4.setValue(self.params[param]["b2"] * 1000)
        sl4.valueChanged.connect(updateLabel4)
        sl4.move(80, 120)

        def close_dialog():
            d.close()

        b = QPushButton("Зберігти", d)
        b.clicked.connect(close_dialog)
        b.move(100, 150)

        d.show()
        d.exec()


# Початок виконання програми
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
