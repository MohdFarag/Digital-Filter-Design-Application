""" Image Viewer Class"""

# pylint: disable=C0103, W0105, C0301, W0613, E1136

# math & matrix computations library
import random
import numpy as np

# Matplotlib
import matplotlib
from  matplotlib import patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from collections import defaultdict
from matplotlib.backend_bases import PickEvent
from zplane_object import Zplane_Object

matplotlib.use('Qt5Agg')

class Zplane(FigureCanvasQTAgg):
    """Z plane Class

    Args:
        FigureCanvasQTAgg (_type_)
    """

    def __init__(self, parent=None, callback_function=None, title="Z plane", axis_exist=True):
        self.fig = Figure(figsize=(6, 6))
        super(Zplane, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        
        # Variables
        self.title = title
        self.zeros = []
        self.poles = []
        self.allpass = []

        self.dragged = None
        self.dragged_conjugate = None
        self.callback_function = callback_function
        if callback_function is None:
            self.callback_function = self.none_function

        self.axis_exist = axis_exist
               
        self.set_theme()
        self.draw_base()
        self.set_events()
        
    # Set Theme
    def set_theme(self):
        self.axes.grid(True, color='0.92', linestyle='-', which='both', axis='both')
        self.fig.set_edgecolor("black")
        self.axes.spines['left'].set_position('center')
        self.axes.spines['bottom'].set_position('center')
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['top'].set_visible(False)

    # Draw basics of Z plane
    def draw_base(self):
        if self.axis_exist:
            font_size = 16
        else:
            font_size = 10
        title_style = {'fontsize': font_size,
                    'fontweight' : 900,
                    'verticalalignment': 'top'}
        self.axes.set_title(self.title, title_style)
        
        if self.axis_exist:
            self.vertical_line   = self.axes.axvline(0, color='k', lw=0.6, ls='--')
            self.horizontal_line = self.axes.axhline(0, color='k', lw=0.6, ls='--')

        
        if self.axis_exist:
            coord_style = {'fontsize': 14,
                        'fontweight' : 500,
                        'verticalalignment': 'top'}
            self.i_text = self.axes.text(0.22, 0.9, '', transform=self.axes.transAxes, fontdict=coord_style)
            self.j_text = self.axes.text(0.72, 0.9, '', transform=self.axes.transAxes, fontdict=coord_style)

        # create the unit circle
        unit_circle = patches.Circle((0,0), radius=1, fill=False,
                                 color='black', ls='solid', alpha=0.5)
        self.axes.add_patch(unit_circle)

        # set the ticks
        r = 1.5            
        self.axes.axis("scaled")
        self.axes.axis([-r, r, -r, r])

        if self.axis_exist:
            ticks = [-1.0, -0.5, 0.5, 1.0]
        else:
            ticks = []

        self.axes.set_xticks(ticks)
        self.axes.set_yticks(ticks)
    
    # Set Cross Hair Visible
    def set_cross_hair_visible(self, visible):
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.i_text.set_visible(visible)
        self.j_text.set_visible(visible)

    # Functions
    ## Check if click in region of item
    def in_region(self, x, y, r, click):
        return (x-r <= click.xdata <= x+r) and (y-r <= click.ydata <= y+r)
    
    def get_obj_conj(self, obj):
        conj = None
        for zero in self.zeros:
            if zero.get_original_object() == obj:
                conj = zero.get_conjugate_object()
            if zero.get_conjugate_object() == obj:
                conj = zero.get_original_object()

        for pole in self.poles:
            if pole.get_original_object() == obj:
                conj = pole.get_conjugate_object()
            if pole.get_conjugate_object() == obj:
                conj = pole.get_original_object()

        return conj
        
    ## Get Zeros
    def get_zeros(self):
        # Get Zeros
        zeros = []
        for zero_obj in self.zeros:
            # Get Original Object
            zero = zero_obj.get_original_object()
            zero_value = zero.get_xdata()[0] + zero.get_ydata()[0] * 1j
            zeros.append(zero_value)
            # Get Conjugate Object
            zero_conj = zero_obj.get_conjugate_object()
            if zero_conj:
                zero_conj_value = zero_conj.get_xdata()[0] + zero_conj.get_ydata()[0] * 1j
                zeros.append(zero_conj_value)

        return zeros + self.allpass

    ## Get Poles
    def get_poles(self):
        # Get All-Pass
        allpass_conj = [1/np.conjugate(allpass) for allpass in self.allpass]
        # Get Poles
        poles = []
        for pole_obj in self.poles:
            # Get Original Object
            pole = pole_obj.get_original_object()
            pole_value = pole.get_xdata()[0] + pole.get_ydata()[0] * 1j
            poles.append(pole_value)
            # Get Conjugate Object
            pole_conj = pole_obj.get_conjugate_object()
            if pole_conj:
                pole_conj_value = pole_conj.get_xdata()[0] + pole_conj.get_ydata()[0] * 1j
                poles.append(pole_conj_value)
        
        return poles + allpass_conj
    
    ## Add Zero
    def add_zero(self, z:complex=0+0j, conjugate:bool=False):
        # Create Z Plane Object
        zero_obj = Zplane_Object()
        
        # Plot The Object
        zero = self.axes.plot(z.real, z.imag, 'o', markersize=10, alpha=0.9, color='none', markeredgecolor='red', picker=True, pickradius=5)                
        zero_obj.set_original_object(zero[0])
        
        if conjugate:
            c = np.conj(z)
            conj = self.axes.plot(c.real, c.imag, 'o', markersize=10, alpha=0.9, color='none', markeredgecolor='red', picker=True, pickradius=5)                
            zero_obj.set_conjugate_object(conj[0])
            
        self.zeros.append(zero_obj)
        self.draw()
        self.callback_function()

    ## Add Pole
    def add_pole(self, p:complex=0+0j, conjugate:bool=False):
        # Create Z Plane Object
        pole_obj = Zplane_Object()

        # Plot The Object
        pole = self.axes.plot(p.real, p.imag, 'x', markersize=10, alpha=0.9, color='none', markeredgecolor='blue', picker=True, pickradius=5)
        pole_obj.set_original_object(pole[0])

        if conjugate:
            c = np.conj(p)
            conj = self.axes.plot(c.real, c.imag, 'x', markersize=10, alpha=0.9, color='none', markeredgecolor='blue', picker=True, pickradius=5)
            pole_obj.set_conjugate_object(conj[0])
        
        self.poles.append(pole_obj)
        self.draw()
        self.callback_function()

    ## Add AllPass
    def set_allpass(self, allpass_list:list[complex]):
        self.allpass = allpass_list
        self.callback_function(False)
                
    ## Clear All Zeros  
    def clear_zeros(self):
        [zero.remove() for zero in self.zeros]
        self.zeros.clear()
        self.draw()
        self.callback_function()
    
    ## Clear All Poles
    def clear_poles(self):
        [pole.remove() for pole in self.poles]
        self.poles.clear()
        self.draw()
        self.callback_function()
    
    ## Clear All
    def clear_all(self):
        self.clear_zeros()
        self.clear_poles()
        self.callback_function()

    # Events        
    def set_events(self):
        self.mpl_connect("motion_notify_event", self.on_move)
        self.mpl_connect("pick_event", self.on_pick)
        self.mpl_connect("motion_notify_event", self.on_move_item)
        self.mpl_connect("button_release_event", self.on_release)
        self.mpl_connect('button_press_event', self.on_dbl_click)

    # Event when mouse move
    def on_move(self, event):
        if not event.inaxes:
            self.set_cross_hair_visible(False)
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata

            # update the line positions
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([x])
            self.i_text.set_text(f"i={x:.2f}")
            self.j_text.set_text(f"j={y:.2f}")
        self.draw_idle()
        self.blit()

    # Event when object picking
    def on_pick(self, event:PickEvent):
        self.dragged = event.artist
        self.dragged.set_markeredgecolor("black")
        self.axes.draw_artist(self.dragged)

        self.dragged_conjugate = self.get_obj_conj(self.dragged)    
        if self.dragged_conjugate:
            self.dragged_conjugate.set_markeredgecolor("green")
            self.axes.draw_artist(self.dragged_conjugate)
    
    # Event when item moving
    def on_move_item(self, event):
        if self.dragged is None: return
                      
        # New Position
        new_x = event.xdata 
        new_y = event.ydata
        
        self.dragged.set_xdata(new_x)
        self.dragged.set_ydata(new_y)

        self.axes.draw_artist(self.dragged)

        if self.dragged_conjugate:
            self.dragged_conjugate.set_xdata(new_x)
            self.dragged_conjugate.set_ydata(-new_y)
            self.axes.draw_artist(self.dragged_conjugate)
        
        # self.callback_function()

    # Event when mouse releasing
    def on_release(self, event):
        if self.dragged is None: return

        # Original Color of dragged item
        if self.dragged.get_marker() == "o":
            self.dragged.set_markeredgecolor("red")
        else:
            self.dragged.set_markeredgecolor("blue")
        self.axes.draw_artist(self.dragged)
        
        # Original Color of dragged item
        if self.dragged_conjugate:
            if self.dragged_conjugate.get_marker() == "o":
                self.dragged_conjugate.set_markeredgecolor("red")
            else:
                self.dragged_conjugate.set_markeredgecolor("blue")
            self.axes.draw_artist(self.dragged_conjugate)
                
        self.callback_function()
        self.dragged = None
        self.dragged_conjugate = None

    # Event when double click
    def on_dbl_click(self, event):
        if event.dblclick:
            r = 0.045
            for i, zero_obj in enumerate(self.zeros):
                zero = zero_obj.get_original_object()
                is_in_zero_region = self.in_region(zero.get_xdata()[0], zero.get_ydata()[0], r, event)

                zero_conj = zero_obj.get_conjugate_object()
                if zero_conj:
                    is_in_zero_conj_region = self.in_region(zero_conj.get_xdata()[0], zero_conj.get_ydata()[0], r, event)
                else:
                    is_in_zero_conj_region = False
                    
                if is_in_zero_region or is_in_zero_conj_region:
                    zero_obj.remove()
                    self.zeros.pop(i)

            for i, pole_obj in enumerate(self.poles):
                pole = pole_obj.get_original_object()
                is_in_pole_region = self.in_region(pole.get_xdata()[0], pole.get_ydata()[0], r, event)

                pole_conj = pole_obj.get_conjugate_object()
                if pole_conj:
                    is_in_pole_conj_region = self.in_region(pole_conj.get_xdata()[0], pole_conj.get_ydata()[0], r, event)
                else:
                    is_in_pole_conj_region = False
                    
                if is_in_pole_region or is_in_pole_conj_region:
                    pole_obj.remove()
                    self.poles.pop(i)

        self.draw_idle()
        self.blit()
        self.callback_function()
    
    # When callback is none
    def none_function(self):
        pass