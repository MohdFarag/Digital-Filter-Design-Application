# Package Importing

import sys
# Pandas & Numpy
import pandas as pd
import numpy as np
## PyQt5
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from main_rc import * # Icons QRC
from stylesheet import * # Styles of PyQt elements
## Classes
from zplane import Zplane
from plotter import Plotter
from mouse_pad import MousePad
from signal_processing import * # Functions of the dsp

# Main Window
class MainWindow(QMainWindow):

    # Constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Realtime Digital Filter Design")
        self.setWindowIcon(QIcon(":icon"))
        self.setStyleSheet(general_stylesheet)
        
        # Variables
        self.time = [] # Time array
        self.original_signal = [] # Original Signal Array
        self.filtered_signal = [] # Filtered Signal Array
        
        self.curr = 0 # Current Time
        self.speed = 500 # Speed Value
        self.resolution = 200 # Resolution Value

        # PyQt Elements Creation
        self.create_actions()
        self.create_menu()
        self.create_toolbar()
        self.create_central_ui()
        self.create_statusbar()

        # Set timers & threads for realtime
        self.set_timers()
        
        # Connect signals and slots
        self.connect()
    
    # Connect signals and slots         
    def connect(self):
        # Control Buttons
        self.play_btn.clicked.connect(self.filter_data)
        self.increase_btn.clicked.connect(lambda: self.speed_change(self.speed+100))
        self.decrease_btn.clicked.connect(lambda: self.speed_change(self.speed-100))
        # Control Sliders
        self.speed_slider.valueChanged[int].connect(self.speed_change)
        self.resolution_slider.valueChanged[int].connect(self.resolution_change)
        # All-Pass
        self.allpass_add_btn.clicked.connect(self.allpass_add_btn_function)
        self.allpass_remove_btn.clicked.connect(self.allpass_remove_btn_function)
        self.allpass_text_edit.textChanged[str].connect(self.allpass_input_change)

    ###############################################
    """Realtime Functions"""
    ###############################################

    # Set timers & threads for realtime
    def set_timers(self):
        # Setup a timer to trigger the redraw by calling filter_process_update.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.calc_speed())
        self.timer.timeout.connect(self.filter_process_update)

    # Calculate Speed 
    def calc_speed(self):
        return self.speed_slider.maximum() - self.speed

    # Realtime Signal Filtering Update
    def filter_process_update(self):       
        start_point = self.curr
        end_point = self.curr + self.resolution
        realtime_original_signal = self.original_signal[start_point:end_point]
        realtime_filtered_signal = self.filtered_signal[start_point:end_point]
        realtime_time = self.time[start_point:end_point]
        self.curr += 1
        
        self.original_signal_plotter.plot_signal(realtime_time, realtime_original_signal)
        self.filtered_signal_plotter.plot_signal(realtime_time, realtime_filtered_signal)
    
    ###############################################
    """UI Functions"""
    ###############################################
    
    # Add Separator
    def addSeparator(self, parent):
        # Creating a separator action
        self.separator = QAction(self)
        self.separator.setSeparator(True)
        parent.addAction(self.separator)
    
    # Create the menu bar
    def create_menu(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.exit_action)

    # Context Menu Event
    def contextMenuEvent(self, event):
        # Creating a menu object with the central widget as parent
        menu = QMenu(self)
        # Populating the menu with actions
        menu.addAction(self.open_action)
        self.addSeparator(menu)
        menu.addAction(self.exit_action)
        menu.addAction(self.test_action)
        # Launching the menu
        menu.exec(event.globalPos())
    
    # Create Actions
    def create_actions(self):
        # Open Action
        self.open_action = QAction(QIcon(":open"), "&Open Signal...", self)
        self.open_action.setStatusTip('Open a new signal')
        self.open_action.setShortcut("Ctrl+o")
        self.open_action.triggered.connect(self.open_data)

        # Exit Action
        self.exit_action = QAction(QIcon(":exit"), "&Exit", self)
        self.exit_action.setStatusTip('Good Bye !')
        self.exit_action.setShortcut("Ctrl+q")
        self.exit_action.triggered.connect(self.exit)
    
        # Add ZERO
        self.add_zero_action = QAction(QIcon(":zero"), "&Add Zero...", self)
        self.add_zero_action.setStatusTip('Add a new zero')
        self.add_zero_action.setShortcut("Ctrl+z")
        self.add_zero_action.triggered.connect(self.add_zero)

        # Add POLE
        self.add_pole_action = QAction(QIcon(":pole"), "&Add Pole...", self)
        self.add_pole_action.setStatusTip('Add a new pole')
        self.add_pole_action.setShortcut("Ctrl+p")
        self.add_pole_action.triggered.connect(self.add_pole)

        # Add All Zeros
        self.clear_zeros_action = QAction(QIcon(":clear-zeros"), "&Clear Zeros...", self)
        self.clear_zeros_action.setStatusTip('Clear all zeros')
        self.clear_zeros_action.setShortcut("Ctrl+1")
        self.clear_zeros_action.triggered.connect(self.clear_zeros)

        # Clear All Poles
        self.clear_poles_action = QAction(QIcon(":clear-poles"), "&Clear Poles...", self)
        self.clear_poles_action.setStatusTip('Clear all poles')
        self.clear_poles_action.setShortcut("Ctrl+2")
        self.clear_poles_action.triggered.connect(self.clear_poles)

        # Clear All
        self.clear_all_action = QAction(QIcon(":clear-all"), "&Clear All...", self)
        self.clear_all_action.setStatusTip('Clear all poles')
        self.clear_all_action.setShortcut("Ctrl+0")
        self.clear_all_action.triggered.connect(self.clear_all)
        
        # Test Action
        self.test_action = QAction("Test...", self)
        self.test_action.setShortcut("Ctrl+~")
        # self.test_action.triggered.connect(self.test_function)
    
    # Create Toolbar
    def create_toolbar(self):
        self.toolbar = QToolBar("Toolbar")
        # self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # Using a title
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)  
        self.toolbar.addAction(self.add_zero_action)
        self.toolbar.addAction(self.add_pole_action)
        self.toolbar.addAction(self.clear_zeros_action)
        self.toolbar.addAction(self.clear_poles_action)
        self.toolbar.addAction(self.clear_all_action)
        
        self.conjugate_checkbox = QCheckBox("Add Conjugate")
        self.toolbar.addWidget(self.conjugate_checkbox)
            
    # Create Statusbar
    def create_statusbar(self):
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet(f"""font-size:15px;
                                 padding: 4px;""")
        self.statusbar.showMessage("Ready", 3000)

        # Adding a permanent message
        self.statusbar.addPermanentWidget(QLabel("Realtime Digital Filter Design..."))

    # Central user interface    
    def create_central_ui(self):
        # Create a central widget and set the layout
        central_widget = QWidget()
        central_layout = QHBoxLayout()
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"font-size:15px;")

        self.filter_design_tab = QWidget()
        self.phase_correction_tab = QWidget()
        self.applying_filter_tab = QWidget()

        self.filter_design_ui()
        self.phase_correction_ui()
        self.applying_filter_ui()
        
        # Add tabs
        self.tabs.addTab(self.filter_design_tab,"Filter Design")
        self.tabs.addTab(self.phase_correction_tab,"Phase Correction")
        self.tabs.addTab(self.applying_filter_tab,"Apply Filter")
                       
        # Set the central widget
        central_layout.addWidget(self.tabs)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    ## Filter Design user interface
    def filter_design_ui(self):
        filter_design_layout = QVBoxLayout()
        
        self.z_plane = Zplane(callback_function=self.update_response)
        self.magnitude_response_plotter = Plotter(title="Magnitude Response", x_axis="frequency", y_axis="magnitude")
        self.phase_response_plotter = Plotter(title="Phase Response", x_axis="frequency", y_axis="phase")
        
        # Set up the main layout
        main_splitter = QSplitter(Qt.Horizontal)
        
        left_splitter = QSplitter(QtCore.Qt.Vertical)
        left_splitter.addWidget(self.z_plane)
        
        right_splitter = QSplitter(QtCore.Qt.Vertical)
        right_splitter.addWidget(self.magnitude_response_plotter)
        right_splitter.addWidget(self.phase_response_plotter)
    
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)
        filter_design_layout.addWidget(main_splitter)
        
        self.filter_design_tab.setLayout(filter_design_layout)

    ## Phase Correction user interface
    def phase_correction_ui(self):
        phase_correction_layout = QVBoxLayout()
        main_splitter = QSplitter(Qt.Horizontal)
        
        ### All-Pass Library Area
        allpass_library_scroll_area = QScrollArea()             
        allpass_library_widget = QWidget()                 
        self.allpass_library_layout = QVBoxLayout()             
        allpass_library_widget.setLayout(self.allpass_library_layout)

        ### Scroll Area Properties
        allpass_library_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        allpass_library_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        allpass_library_scroll_area.setWidgetResizable(True)
        allpass_library_scroll_area.setWidget(allpass_library_widget)

        self.create_allpass_library()
        
        ### All-Pass list of added "a"
        allpass_control = QWidget()
        allpass_control_layout = QVBoxLayout()
        allpass_control.setLayout(allpass_control_layout)

        #### Title
        allpass_control_title = QLabel("ALll-Pass Filters")
        #### List of All-Pass Button
        self.allpass_list = QListWidget()
        self.allpass_list.itemSelectionChanged.connect(self.allpass_list_item_check)

        #### All-Pass input
        allpass_input_layout = QHBoxLayout()
        self.allpass_text_edit = QLineEdit("")
        self.allpass_text_edit.setPlaceholderText("Enter all-pass filter...")
        button_style = """height: 20px;
                          border-radius: 5px;"""
        self.allpass_text_edit.setStyleSheet(button_style)
        self.allpass_add_btn = QPushButton("Add")
        self.allpass_add_btn.setStyleSheet(button_style+"background: #2e2e2e; color:#fff;")
        self.allpass_add_btn.setEnabled(False)
        allpass_input_layout.addWidget(self.allpass_text_edit)
        allpass_input_layout.addWidget(self.allpass_add_btn)
        #### Remove Button
        self.allpass_remove_btn = QPushButton("Remove")
        self.allpass_remove_btn.setStyleSheet(button_style+"background: #2e2e2e; color:#fff;")
        
        allpass_control_layout.addWidget(allpass_control_title, 1, alignment=Qt.AlignCenter)
        allpass_control_layout.addWidget(self.allpass_list, 100)
        allpass_control_layout.addLayout(allpass_input_layout, 1)
        allpass_control_layout.addWidget(self.allpass_remove_btn, 1)
        
        ### Phase Plots Area
        phase_plotter = QWidget()
        phase_plotter_layout = QVBoxLayout()
        phase_plotter.setLayout(phase_plotter_layout)
        
        self.original_phase_plotter = Plotter(title="Original Phase Response", x_axis="frequency", y_axis="phase")
        self.allpass_phase_plotter = Plotter(title="All-Pass Response", x_axis="frequency", y_axis="phase")
        
        phase_plotter_layout.addWidget(self.original_phase_plotter)
        phase_plotter_layout.addWidget(self.allpass_phase_plotter)
        
        main_splitter.addWidget(allpass_library_scroll_area)
        main_splitter.addWidget(allpass_control)
        main_splitter.addWidget(phase_plotter)
        
        main_splitter.setStretchFactor(0, 2)
        main_splitter.setStretchFactor(1, 5)
        main_splitter.setStretchFactor(2, 5)        
                
        phase_correction_layout.addWidget(main_splitter)
        self.phase_correction_tab.setLayout(phase_correction_layout)
    
    ## Applying filter user interface
    def applying_filter_ui(self):
        applying_filter_layout = QVBoxLayout()
        signal_splitter = QSplitter(Qt.Vertical)
        
        mouse_pad_area = MousePad(callback_function=self.draw_signal_by_mouse, title="M  o  u  s  e      P  a  d")
        plot_splitter = QSplitter(Qt.Horizontal)
        self.original_signal_plotter = Plotter(title="Realtime Signal", x_axis="time", y_axis="amplitude")
        self.filtered_signal_plotter = Plotter(title="Filtered Signal", x_axis="time", y_axis="amplitude")
        plot_splitter.addWidget(self.original_signal_plotter)
        plot_splitter.addWidget(self.filtered_signal_plotter)

        signal_splitter.addWidget(mouse_pad_area)
        signal_splitter.addWidget(plot_splitter)
        signal_splitter.setStretchFactor(0, 1)
        signal_splitter.setStretchFactor(1, 3)

        container = QWidget(self)
        control_layout = QVBoxLayout(container)
        container.setStyleSheet("background-color:#EAEAF2; border-radius:15px;")
        
        ## Upper Control Layout
        upper_control_layout = QHBoxLayout()
        self.decrease_btn = QPushButton()
        self.decrease_btn.setIcon(QIcon(":decrease"))
        self.decrease_btn.setStyleSheet("font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: black")
        self.decrease_btn.setDisabled(True)
        
        ### Play Button
        self.play_btn = QPushButton()
        self.play_btn.setIcon(QIcon(":play"))
        self.play_btn.setStyleSheet("font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.play_btn.setDisabled(True)
        
        ### Increase Button
        self.increase_btn = QPushButton()
        self.increase_btn.setIcon(QIcon(":increase"))
        self.increase_btn.setStyleSheet("font-size:15px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: black")
        self.increase_btn.setDisabled(True)

        ### Decrease Button        
        upper_control_layout.addSpacerItem(QSpacerItem(400, 5))
        upper_control_layout.addWidget(self.decrease_btn,4)
        upper_control_layout.addWidget(self.play_btn,5)
        upper_control_layout.addWidget(self.increase_btn,4)
        upper_control_layout.addSpacerItem(QSpacerItem(400, 5))

        ## Lower Control Layout        
        lower_control_layout = QHBoxLayout()

        ### Speed Slider Layout
        speed_layout = QHBoxLayout()
        speed_slider_title = QLabel("Speed")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setValue(self.speed)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setDisabled(True)
        self.speed_slider_counter = QLabel(f"{self.speed}")

        speed_layout.addWidget(speed_slider_title,1)
        speed_layout.addWidget(self.speed_slider,8)
        speed_layout.addWidget(self.speed_slider_counter,1)

        ### Resolution Slider Layout
        resolution_layout = QHBoxLayout()
        resolution_slider_title = QLabel("Resolution")
        self.resolution_slider = QSlider(Qt.Horizontal)
        self.resolution_slider.setMinimum(2)
        self.resolution_slider.setValue(self.resolution)
        self.resolution_slider.setMaximum(1000)
        self.resolution_slider.setDisabled(True)
        self.resolution_slider_counter = QLabel(f"{self.resolution}")

        resolution_layout.addWidget(resolution_slider_title,1)
        resolution_layout.addWidget(self.resolution_slider,8)
        resolution_layout.addWidget(self.resolution_slider_counter,1)

        lower_control_layout.addSpacerItem(QSpacerItem(300, 5))
        lower_control_layout.addLayout(speed_layout)
        lower_control_layout.addSpacerItem(QSpacerItem(50, 5))
        lower_control_layout.addLayout(resolution_layout)
        lower_control_layout.addSpacerItem(QSpacerItem(300, 5))

        control_layout.addLayout(upper_control_layout)
        control_layout.addLayout(lower_control_layout)

        applying_filter_layout.addWidget(signal_splitter,100)
        applying_filter_layout.addWidget(container,1)
        
        self.applying_filter_tab.setLayout(applying_filter_layout)
    
    ###############################################
    """Data Processing Functions"""
    ###############################################
    
    # Open data
    def open_data(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Signal Files (*.csv)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            if len(filenames) > 0:
                filename = filenames[0]
                try:
                    self.load_data(filename)
                except Exception as e:
                    print(e)
                    QMessageBox.critical(self, "Error", "Unable to open the audio file.")                    

    # Load data
    def load_data(self, path):
        # load the signal & time
        csv_file = pd.read_csv(path)
        if csv_file.shape[0] > 10000:
            self.original_signal = csv_file.iloc[:,1].values.tolist()
            self.time = csv_file.iloc[:,0].values.tolist()
        else:
            QMessageBox.critical(self,
                                "Error !",
                                f"The signal must be 10,000 points at minimum.")
            return
        
        # Plot
        self.original_signal_plotter.plot_signal(self.time, self.original_signal)
        
        # Enable control buttons
        self.play_btn.setEnabled(True)
        self.decrease_btn.setEnabled(True)
        self.increase_btn.setEnabled(True)
        self.speed_slider.setEnabled(True)
        self.resolution_slider.setEnabled(True)
                        
        # Move to Filter Applying Tab
        self.tabs.setCurrentIndex(2)

    # Filter Data based on zeros & poles
    def filter_data(self):
        if self.timer.isActive() == False:
            self.play_btn.setIcon(QIcon(":pause"))
            z = self.z_plane.get_zeros()
            p = self.z_plane.get_poles()
            self.filtered_signal = filter_signal(self.original_signal, z, p)
            self.timer.start()
        else:
            self.play_btn.setIcon(QIcon(":play"))
            self.timer.stop()

    ###############################################
    """Z Plane Functions"""
    ###############################################

    # Zeros & Poles Functions
    ## Add zero to Z plane
    def add_zero(self):
        state = self.conjugate_checkbox.isChecked()
        self.z_plane.add_zero(conjugate=state)
    
    ## Add pole to Z plane    
    def add_pole(self):
        state = self.conjugate_checkbox.isChecked()
        self.z_plane.add_pole(conjugate=state)
    
    ## Clear all zeros in Z plane
    def clear_zeros(self):
        self.z_plane.clear_zeros()
    
    ## Clear all poles in Z plane
    def clear_poles(self):
        self.z_plane.clear_poles()
    
    ## Clear all zeros & poles in Z plane
    def clear_all(self):
        self.z_plane.clear_all()
    
    # Callback function when change on Z plane to update magnitude & phase Response
    def update_response(self, go_to_zplane=True):
        # Get Zeros & Poles
        z = self.z_plane.get_zeros()
        p = self.z_plane.get_poles()
        
        # Get Frequency Response (magnitude & phase)
        w, mag, phase = get_frequency_response(z,p)

        # Plot Responses
        self.magnitude_response_plotter.plot_signal(w, mag)
        self.phase_response_plotter.plot_signal(w, phase)
        self.original_phase_plotter.plot_signal(w, phase)

        # If TRUE: Go to zplane tab
        if go_to_zplane:
            self.tabs.setCurrentIndex(0) # 0 is index of Z plane tab

    ###############################################
    """Control Slider Functions"""
    ###############################################

    # When Speed Change
    def speed_change(self, speed):
        self.speed_slider_counter.setText(f"{speed}")
        self.speed = speed
        self.timer.setInterval(self.calc_speed())
    
    # When Resolution Change
    def resolution_change(self, resolution):
        self.resolution_slider_counter.setText(f"{resolution}")
        self.resolution = resolution

    ###############################################
    """Mouse Pad Functions"""
    ###############################################
    
    # Callback function when mouse draw on mouse pad to generate a signal
    def draw_signal_by_mouse(self, y=[0], counter=0, interval=10):
        if len(y) < interval: return
        
        # Generate x axis
        x = np.arange(counter, counter+interval)
        self.original_signal_plotter.plot_signal(x[10:], y[10:]) # Plot signal drawn
        
        # Get zeros & poles
        z = self.z_plane.get_zeros()
        p = self.z_plane.get_poles()

        # Filter signal drawn then plot
        filtered_y = filter_signal(y, z, p)
        self.filtered_signal_plotter.plot_signal(x[1:], filtered_y[1:])

    ###############################################
    """All-Pass Functions"""
    ###############################################

    # Plot phase response of all-pass value    
    def plot_phase_response(self, a=1+1j):
        try:
            if type(a) is str:
                a = complex(a.replace(' ',''))
            a_conj = 1/np.conjugate(a)
            w, _, phase = get_frequency_response([a],[a_conj])
            self.allpass_phase_plotter.plot_signal(w, phase)
        except Exception as e:
            print(e)

    # Update All-Pass in Z plane when there is change in all-pass list
    def phase_correction_update(self):
        allpass_filters = []
        n = self.allpass_list.count()
        for x in range(n):
            allpass_value_text = self.allpass_list.item(x).text().replace(' ','')
            allpass_filters.append(complex(allpass_value_text))
        
        self.z_plane.set_allpass(allpass_filters)

    # Add Allpass to phase correction
    def allpass_add_to_correction_phase(self, value:str):
        try:
            if type(value) is str:
                value = complex(value.replace(' ',''))
            self.allpass_list.addItem(f"{value.real} + {value.imag}j")
            self.phase_correction_update()
        except Exception as e:
            print(e)

    # When item in all-pass list checked
    def allpass_list_item_check(self):
        selected_items = self.allpass_list.selectedItems()
        if selected_items != []:
            self.plot_phase_response(selected_items[0].text())
    
    # All-Pass Add Button
    def allpass_add_btn_function(self):
        allpass_value = self.allpass_text_edit.text()
        self.allpass_add_to_correction_phase(allpass_value)
        
    # All-Pass Remove Button
    def allpass_remove_btn_function(self):
        selected_items = self.allpass_list.selectedItems()
        for i in range(len(selected_items)):
            self.allpass_list.takeItem(i)
        self.phase_correction_update()
        
    # When change in all-pass input text    
    def allpass_input_change(self, value:str):
        try:
            a = complex(value)
        except:
            self.allpass_add_btn.setEnabled(False)
        else:
            self.allpass_add_btn.setEnabled(True)
            self.plot_phase_response(a)
        finally:
            pass
    
    # All-Pass Library
    ## Create all-pass Library ui
    def create_allpass_library(self):
        # Library of allpass
        self.add_allpass_to_library(a=1+1.2j)
        self.add_allpass_to_library(a=-1.1+0.9j)
        self.add_allpass_to_library(a=-1.3+0.7j)

    ## Add all-pass item to library
    def add_allpass_to_library(self, a=0+0j):
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        
        a_conj = 1/np.conjugate(a)
        allpass_plane = Zplane(title=f"{a.real} + {a.imag}j", axis_exist=False)
        allpass_plane.setEnabled(False)
        
        allpass_plane.add_zero(a)
        allpass_plane.add_pole(a_conj)
        
        a_btn = QPushButton("Add")
        a_btn.clicked.connect(lambda _: self.allpass_add_to_correction_phase(a))

        layout.addWidget(allpass_plane)
        layout.addWidget(a_btn)
        layout.addWidget(QHLine())
        
        widget.setCursor(QCursor(Qt.PointingHandCursor))
        widget.mousePressEvent = lambda _: self.plot_phase_response(a)
        self.allpass_library_layout.addWidget(widget)
    
    ###############################################
    """Destructor Functions"""
    ###############################################

    ## Close the application
    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
    
    # Exit the application  
    def exit(self):
        exitDialog = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        defaultButton=QMessageBox.StandardButton.Yes)

        if exitDialog == QMessageBox.StandardButton.Yes:
            # Exit the application
            sys.exit()
            
# Horizontal Line            
class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

# Vertical Line
class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)