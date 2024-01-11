""" Image Viewer Class"""

# pylint: disable=C0103, W0105, C0301, W0613, E1136

# math & matrix computations library
import random
import numpy as np

# Matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from collections import defaultdict
from matplotlib.backend_bases import PickEvent

class MousePad(FigureCanvasQTAgg):
    """Z plane Class

    Args:
        FigureCanvasQTAgg (_type_)
    """

    def __init__(self, parent=None, callback_function=None, title="Mouse Pad"):
        self.fig = Figure(figsize=(6, 6))
        super(MousePad, self).__init__(self.fig)
        
        # Axes of figure
        self.axes = self.fig.add_subplot(111)
        
        # Variables
        self.clicked = None
        self.mouse_real_time_signal = []
        self.counter = 0

        # Callback function
        self.callback_function = callback_function

        # Set settings of the matplotlib axes
        self.set_settings()
        # Set Title
        style = {'fontsize': 40,
                'fontweight' : 1000,
                'fontfamily': 'fantasy',
                'color': '#0080ff'}
        self.axes.text(0.5, 
                       0.5, 
                       s=title, 
                       fontdict=style,
                       horizontalalignment='center', 
                       verticalalignment='center',
                       alpha=0.2)

        # Set Events connections
        self.set_events()
        
    # Set Theme
    def set_settings(self):
        self.fig.set_facecolor("#EAEAF2")
        self.axes.set_facecolor("#EAEAF2")
        self.axes.spines['bottom'].set_color('#c7c9d8')
        self.axes.spines['top'].set_color('#c7c9d8')  
        self.axes.spines['right'].set_color('#c7c9d8')
        self.axes.spines['left'].set_color('#c7c9d8')
        
        self.axes.grid(True, color='0.95', linestyle='-', which='both', axis='both')
        
        self.fig.set_tight_layout(True)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
    
    # Events        
    def set_events(self):
        self.mpl_connect("button_press_event", self.on_press)
        self.mpl_connect("motion_notify_event", self.on_move)
        self.mpl_connect("button_release_event", self.on_release)

    def on_press(self, event):
        self.clicked = True
   
    def on_move(self, event):
        if self.clicked is None: return
        if event.xdata is None: return
        if event.ydata is None: return
        
        interval = 100
        self.mouse_real_time_signal.append(event.xdata)
        if len(self.mouse_real_time_signal) > interval: 
            self.mouse_real_time_signal.pop(0)
            self.callback_function(self.mouse_real_time_signal, self.counter, interval)
        self.counter += 1
            
    def on_release(self, event):
        if self.clicked is None: return
        self.clicked = None