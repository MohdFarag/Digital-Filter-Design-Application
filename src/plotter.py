# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class Plotter(FigureCanvasQTAgg):

    def __init__(self, parent=None, title="Signal Plot", x_axis="x", y_axis="y"):       
        self.fig = Figure(facecolor="white")
        self.axes = self.fig.add_subplot(111)

        # Set Labels
        self.axes.set_title(title, fontweight ="bold", color="black")
        self.axes.set_xlabel(x_axis)
        self.axes.set_ylabel(y_axis)

        self.set_settings()
        super(Plotter, self).__init__(self.fig)

    def set_settings(self):
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['bottom'].set_color("#EAEAF2")
        self.axes.spines['left'].set_color("#EAEAF2")

        self.axes.set_facecolor("#EAEAF2")
        self.axes.grid(True, color='w', linestyle='-', which='both', axis='both')

    def plot_signal(self, x, y):
        self.clear()
        self.axes.plot(x, y, color="#64B5CD", linewidth=2.5, dash_joinstyle='round', dash_capstyle="round")
        self.draw_idle()
        self.blit()

    def clear(self):
        self.axes.cla()
        self.set_settings()