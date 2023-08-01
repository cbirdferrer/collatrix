#---------------------------------------------------------------
#__main__.py
#this script collates measurements from individual csv outputs of
#the morphometriX GUI
#the csvs can be saved either all in one folder or within each individual
#animals folder.
#this version includes a safety net that recalculates the measurement using
#accurate altitude and focal lengths that the user must provie in csvs.
# this version uses PyQt5 instead of easygui (used in v2.0)
#created by: Clara Bird (clara.birdferrer#gmail.com), March 2020
#updated by: Clara Bird, June 2021
#----------------------------------------------------------------

#import modules
import pandas as pd
import os, sys
# import math
import webbrowser
from pathlib import Path
from PySide6 import QtCore
from PySide6.QtWidgets import QFileDialog, QApplication, QMainWindow, QPushButton, QCheckBox, QVBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, QMetaObject
from PySide6.QtGui import QFont

class FileSelector:
    def select_file():
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Select File", '', 'CSV Files (*.csv)'
        )
        if file_path:
            print(f"Selected File: {file_path}")
            return file_path
        return None

class DirSelector:
    def select_dir():
        file_dialog = QFileDialog()
        dir_path = file_dialog.getExistingDirectory(
            None, "Select Directory"
        )
        if dir_path:
            return dir_path
        return None
    
class lidarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pull LiDAR Data")

        #set sizing
        D = self.screen().availableGeometry()
        self.move(0,0)#center.x() + .25*D.width() , center.y() - .5*D.height() )
        self.resize( int(.4*D.width()), int(.5*D.height()) )
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized
                            | QtCore.Qt.WindowState.WindowActive)
        self.activateWindow()
        
        grid_layout = QGridLayout()

        #add inputs
        welcome_label = QLabel("Welcome to the lidar match up tool!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        welcome_label.setFont(font)

        #add labels and buttons to grid layout
        grid_layout.addWidget(welcome_label,0,0,1,2)
        # grid_layout.addItem(spacer, 1, 0,1,2)
        # grid_layout.addWidget(aID_label,2,1,1,1)
        # grid_layout.addWidget(self.aIDcheckbox,2,0,1,1)
        # grid_layout.addWidget(safecheckbox_label,3,1,1,1)
        # grid_layout.addWidget(self.safecheckbox,3,0,1,1)
        # grid_layout.addWidget(safetyfile_label,4,1,1,1)
        # grid_layout.addWidget(self.safety_button, 4, 0,1,1)
        # grid_layout.addWidget(prefix_label,5,1,1,1)
        # grid_layout.addWidget(self.prefix_box, 5, 0,1,1)
        # grid_layout.addWidget(mmxfold_label,6,1,1,1)
        # grid_layout.addWidget(mmxfold_button, 6, 0,1,1)
        # grid_layout.addWidget(savefold_label,7,1,1,1)
        # grid_layout.addWidget(savefold_button, 7, 0,1,1)
        # grid_layout.addItem(spacer, 8, 0,1,2)
        # grid_layout.addWidget(collate_button,9,0,1,2)

        self.setLayout(grid_layout)

class collateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collate MorphoMetriX Outputs")

        #set sizing
        D = self.screen().availableGeometry()
        self.move(0,0)#center.x() + .25*D.width() , center.y() - .5*D.height() )
        self.resize( int(.4*D.width()), int(.5*D.height()) )
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized
                            | QtCore.Qt.WindowState.WindowActive)
        self.activateWindow()

        #layout grid settings
        grid_layout = QGridLayout()

        #add inputs
        welcome_label = QLabel("Welcome to the collating tool!\nthis tool will collate your morphometrix outputs into on clean csv")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        welcome_label.setFont(font)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        #animal ID
        aID_label = QLabel("Check if you want the Animal ID to be assigned\nbased on the name of the folder")
        self.aIDcheckbox = QCheckBox("Use folder names for AID?", self)

        #safety y/n
        safecheckbox_label = QLabel("Check if you want to use a safety")
        self.safecheckbox = QCheckBox("Use safety?", self)
        self.safecheckbox.stateChanged.connect(self.toggle_file_upload_button)

        safetyfile_label = QLabel("Click to upload safety file")
        self.safety_button = QPushButton("Safety File",self)
        self.safety_button.setEnabled(False)
        self.safety_button.clicked.connect(self.select_file)
        self.safety_sel_label = QLabel("",self)
        self.safety_sel_label.setStyleSheet("border: 1px dashed black; padding: 2px; font-style: italic;")

        #output prefix
        prefix_label = QLabel("Enter the prefix you'd like for output files")
        self.prefix_box = QLineEdit()

        #folder w/ mmx outputs
        mmxfold_label = QLabel("Click to select folder\ncontaining MorphoMetriX outputs")
        mmxfold_button = QPushButton("MMX folder",self)
        mmxfold_button.clicked.connect(lambda: self.select_dir(1))
        self.mmxfold_sel_label = QLabel("", self)
        self.mmxfold_sel_label.setStyleSheet("border: 1px dashed black; padding: 2px; font-style: italic;")

        #folder where output should be saved
        savefold_label = QLabel("Click to select folder where\noutputs should be saved")
        savefold_button = QPushButton("Output folder",self)
        savefold_button.clicked.connect(lambda: self.select_dir(2))
        self.savefold_sel_label = QLabel("",self)
        self.savefold_sel_label.setStyleSheet("border: 1px dashed black; padding: 2px; font-style: italic;")

        #choose output options
        outtypes_label = QLabel("Select which outputs you'd like")
        self.outtypes_list = QComboBox(self)
        self.outtypes_list.addItems(['Both in one file','Both in seperate files',
                                     'Just pixels','Just meters'])

        #run buttons
        collate_button = QPushButton("Collate Data! (click to run)",self)
        collate_button.clicked.connect(self.collate)

        #end message
        self.end_msg = QLabel("",self)
        self.end_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        self.end_msg.setFont(font)

        #add labels and buttons to grid layout
        grid_layout.addWidget(welcome_label,0,0,1,2)
        grid_layout.addItem(spacer, 1, 0,1,2)

        grid_layout.addWidget(aID_label,2,1,1,1)
        grid_layout.addWidget(self.aIDcheckbox,2,0,1,1)

        grid_layout.addItem(spacer, 3, 0,1,2)

        grid_layout.addWidget(safecheckbox_label,4,1,1,1)
        grid_layout.addWidget(self.safecheckbox,4,0,1,1)

        grid_layout.addWidget(safetyfile_label,5,1,1,1)
        grid_layout.addWidget(self.safety_button, 5, 0,1,1)

        grid_layout.addWidget(self.safety_sel_label,6,0,1,2)

        grid_layout.addItem(spacer, 7, 0,1,2)

        grid_layout.addWidget(prefix_label,8,1,1,1)
        grid_layout.addWidget(self.prefix_box, 8, 0,1,1)

        grid_layout.addItem(spacer, 9, 0,1,2)

        grid_layout.addWidget(mmxfold_label,10,1,1,1)
        grid_layout.addWidget(mmxfold_button, 10, 0,1,1)

        grid_layout.addWidget(self.mmxfold_sel_label,11,0,1,2)

        grid_layout.addItem(spacer, 12, 0,1,2)

        grid_layout.addWidget(savefold_label,13,1,1,1)
        grid_layout.addWidget(savefold_button, 13, 0,1,1)

        grid_layout.addWidget(self.savefold_sel_label,14,0,1,2)

        grid_layout.addItem(spacer, 15, 0,1,2)

        grid_layout.addWidget(outtypes_label,16,1,1,1)
        grid_layout.addWidget(self.outtypes_list,16,0,1,1)

        grid_layout.addItem(spacer, 17, 0,1,2)

        grid_layout.addWidget(collate_button,18,0,1,2)

        grid_layout.addWidget(self.end_msg,19,0,1,2)

        self.setLayout(grid_layout)

        ##set up paths
        self.mmxpath = None
        self.savepath = None

    def toggle_file_upload_button(self):
        self.safety_button.setEnabled(self.safecheckbox.isChecked())

    def select_file(self):
        file_path = FileSelector.select_file()
        if file_path:
            self.safety_sel_label.setText(file_path)
            # Read the file using pandas
            self.dfsafe = pd.read_csv(file_path)
            self.safe_file_path = file_path
        

    def select_dir(self, button_id):
        dir_path = DirSelector.select_dir()
        if dir_path:
            if button_id == 1:
                self.mmxpath = dir_path
                self.mmxfold_sel_label.setText(dir_path)
            elif button_id == 2:
                self.savepath = dir_path
                self.savefold_sel_label.setText(dir_path)
        
    def collate(self):
        self.end_msg.setText("....running....")
        #pull in prefix for naming and saving
        prefix = self.prefix_box.text()
        outfold = self.savepath
        out_option = self.outtypes_list.currentText()

        #make lists
        #for csvs
        csvs_all = []
        csvs = []
        not_mmx = []

        #walk through all folders in GUI folder and collect all csvs
        for root,dirs,files in os.walk(self.mmxpath):
            csvs_all += [os.path.join(root,f) for f in files if f.endswith('.csv') & ~f.startswith(".")]
        #make sure the csvs are morphometrix outputs by checking first row
        csvs += [c for c in csvs_all if 'Value_unit' in pd.read_csv(c).columns]
        #make list of all csvs that were not morphometrix csvs to tell user
        not_mmx += [x for x in csvs_all if x not in csvs]

        #combine all csvs
        df_all = pd.DataFrame()
        #list of csvs containing duplicate measurement names
        dup_csvs = []
        for c in csvs:
            df_temp = pd.read_csv(c)
            image_name = os.path.split(df_temp.loc[df_temp['Object']=='Image Path','Value'].item())[-1]
            df_temp['Image'] = image_name
            df_temp['csv'] = c

            #if use folder name for aID is checked, replace Image ID w/ folder name
            if self.aIDcheckbox.isChecked():
                Image_ID = Path(df_temp.loc[df_temp['Object']=='Image Path','Value'].item()).parts[-2]
                df_temp.loc[df_temp['Object']=='Image ID','Value'] = Image_ID
            else: pass
            
            #if this df contains duplicate measurement names (ex. TL twice), add to list, this throws problems when pivoting
            dup_check = df_temp.loc[df_temp['Value_unit'] == 'Meters']
            if dup_check.duplicated(subset=['Object']).any() == True:
                dup_csvs += [c]
            else: pass

            df_all = pd.concat([df_all,df_temp])

        #stop run if duplicate measurement names exist
        if len(dup_csvs) > 0:
            #export text file containg list of csvs containing duplicate names
            with open(os.path.join(outfold,"{0}_csvs containing duplicate measurements.txt").format(prefix), "w") as f:
                f.write(f"{dup_csvs}")
            #update message to alert user to this
            self.end_msg.setText("edit duplicate Object names and run script again, see file in output folder for list of csvs")
        else: pass

        #split out into metadata, meters, and pixels
        df_meta = df_all.loc[df_all['Value_unit'] == 'Metadata']
        df_meters = df_all.loc[df_all['Value_unit'] == 'Meters']
        df_pixels = df_all.loc[df_all['Value_unit'] == 'Pixels']

        #TEMPORARY!!!!!!!!
        df_pixels['Object'] = [x.replace(".0",".00") for x in df_pixels['Object']]

        #pivot metadata
        df_meta1= df_meta.pivot(index=["Image",'csv'],columns='Object',values='Value').reset_index().rename(columns={"Image ID":"Image_ID",
                                                                                                             "Image Path":"Image_Path",
                                                                                                             "Focal Length":"Focal_Length",
                                                                                                             "Pixel Dimension":"Pixel_Dimension",
                                                                                                             "Mirror Side":"Mirror_Side"
                                                                                                             })

        #if safety
        if self.safecheckbox.isChecked():
            #merge with safety to get scaling metadata
            df_safe = df_meta1[['csv','Image','Image_ID','Image_Path','Mirror_Side','Notes']].merge(self.dfsafe,how='left',on='Image')
            df_sx = df_pixels.merge(df_safe,how='left',on=['Image','csv'])

            #set up to run equation
            alt = df_sx['Altitude'].values
            focl = df_sx['Focal_Length'].values
            pixd = df_sx['Pixel_Dimension'].values
            pixc = df_sx['Value'].values.astype(float)
            #run equation to calculate scaled measurements
            df_sx['Value_m'] = ((alt/focl)*pixd)*pixc

            print(df_sx)

            #make meters output df
            df_mx = df_sx.pivot(index=['Image','csv'],columns='Object',values='Value_m').merge(df_safe,how='left',on=['Image','csv'])
            df_mx['metadata_source'] = "safety_file"

            #make pixels output df
            df_px = df_sx.pivot(index=['Image','csv'],columns='Object',values='Value').merge(df_safe,how='left',on=['Image','csv'])
            df_px['metadata_source'] = "safety_file"

            #make both m and px output df
            df_mpx = df_mx.merge(df_sx.pivot(index=['Image','csv'],columns='Object',values='Value'),how='left',on=['Image','csv'],suffixes=['_m','_px'])
            
        else:
            #prep meters output df
            df_mx = df_meters.pivot(index=['Image','csv'],columns='Object',values='Value').merge(df_meta1,how='left',on=['Image','csv'])
            df_mx['metadata_source'] = 'mmx_input'

            #prep pixels output df
            df_px = df_pixels.pivot(index=['Image','csv'],columns='Object',values='Value').merge(df_meta1,how='left',on=['Image','csv']) 
            df_px['metadata_source'] = 'mmx_input'

            #make both m and px output df
            df_mpx = df_mx.merge(df_pixels.pivot(index=['Image','csv'],columns='Object',values='Value'),how='left',on=['Image','csv'],suffixes=['_m','_px'])
            
        #sort columns in all dataframes
        start_columns = ['csv','Image','Image_ID','Image_Path','Altitude','Focal_Length',
                         'Pixel_Dimension','Mirror_Side','Notes','metadata_source']
        #here we split and concatenate so that the start columns are now first
        df_mpx = pd.concat([df_mpx[start_columns],df_mpx.drop(start_columns,axis=1)],axis=1)
        df_px = pd.concat([df_px[start_columns],df_px.drop(start_columns,axis=1)],axis=1)
        df_mx = pd.concat([df_mx[start_columns],df_mx.drop(start_columns,axis=1)],axis=1)

        #export based on option selected
        if out_option == 'Both in one file':
            df_mpx.to_csv(os.path.join(outfold,"{0}_MetersAndPixels.csv".format(prefix)),index=False)
        elif out_option == 'Both in seperate files':
            df_mx.to_csv(os.path.join(outfold,"{0}_Meters.csv".format(prefix)),index=False) 
            df_px.to_csv(os.path.join(outfold,"{0}_Pixels.csv".format(prefix)),index=False)
        elif out_option == 'Just pixels':
            df_px.to_csv(os.path.join(outfold,"{0}_Pixels.csv".format(prefix)),index=False)
        elif out_option == 'Just meters':
            df_mx.to_csv(os.path.join(outfold,"{0}_Meters.csv".format(prefix)),index=False)

        self.end_msg.setText("Done running - check output folders for files!")
        
        #export text file of input data
        #make notes as string
        notes = "CollatriX Run: {0} \n\nAnimal ID from folder name?: {1} \n\nSafety file: {2}\n\nNumber of files collated: {3}\n\n".format(prefix,("yes" if self.aIDcheckbox.isChecked() else "no"), (self.safe_file_path if self.safecheckbox.isChecked() else "no safety used"), len(csvs))
        #write to text file
        with open(os.path.join(outfold,"{0}_ProcessingNotes.txt").format(prefix), "w") as f:
            f.write(f"{notes}")

class bodycondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculate Body Condition Metrics")

        #set sizing
        D = self.screen().availableGeometry()
        self.move(0,0)#center.x() + .25*D.width() , center.y() - .5*D.height() )
        self.resize( int(.4*D.width()), int(.5*D.height()) )
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized
                            | QtCore.Qt.WindowState.WindowActive)
        self.activateWindow()
        
        self.label = QLabel("Window 3 Content:", self)
        self.button = QPushButton("Click Me", self)
        self.button.clicked.connect(self.on_button_click)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
    
    def on_button_click(self):
        print("Button in Window 3 clicked!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #set window title
        self.setWindowTitle("CollatriX Home")

        #set sizing of window
        D = self.screen().availableGeometry()
        self.move(0,0)
        self.resize( int(.4*D.width()), int(.2*D.height()) )
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized
                            | QtCore.Qt.WindowState.WindowActive)
        self.activateWindow()

        #layout grid settings
        grid_layout = QGridLayout()
        grid_layout.setColumnMinimumWidth(0, 1) #column 0
        grid_layout.setColumnMinimumWidth(1, 1) #column 1
        grid_layout.setRowMinimumHeight(0, 1) # row 0
        grid_layout.setRowMinimumHeight(1, 1) #row 1
        grid_layout.setRowMinimumHeight(2, 1) # row 2
        grid_layout.setRowMinimumHeight(3, 1) # row 3
        grid_layout.setRowMinimumHeight(4, 1) # row 3

        #create labels and buttons
        welcome_label = QLabel("Welcome to the CollatriX home page!\nfrom here click on the tool you'd like use")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        welcome_label.setFont(font)

        manual_label = QLabel("Click here to see our online manual")
        manual = QPushButton("Manual",self)
        manual.clicked.connect(lambda: webbrowser.open('https://github.com/cbirdferrer/collatrix'))

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        button1_label = QLabel("Click here to open a tool to pull\nin your LiDAR data")
        button1 = QPushButton("Pull LiDAR Data", self)
        button1.clicked.connect(lambda: self.open_window(lidarWindow()))
        
        button2_label = QLabel("Click here to open a tool to collate\nyour MorphoMetriX outputs")
        button2 = QPushButton("Collate MMX Outputs", self)
        button2.clicked.connect(lambda: self.open_window(collateWindow()))
        
        button3_label = QLabel("Click here to open a tool to calculate\ncetacean body condition metrics")
        button3 = QPushButton("Calculate Body Condition Metrics", self)
        button3.clicked.connect(lambda: self.open_window(bodycondWindow()))
        
        #add labels and buttons to grid layout
        grid_layout.addWidget(welcome_label,0,0,1,2)
        grid_layout.addWidget(manual_label,1,1,1,1)
        grid_layout.addWidget(manual,1,0,1,1)
        grid_layout.addItem(spacer, 2, 0,1,2)
        grid_layout.addWidget(button1_label,3,1,1,1)
        grid_layout.addWidget(button1,3,0,1,1)
        grid_layout.addWidget(button2_label,4,1,1,1)
        grid_layout.addWidget(button2, 4, 0,1,1)
        grid_layout.addWidget(button3_label,5,1,1,1)
        grid_layout.addWidget(button3, 5, 0,1,1)

        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

    def open_window(self,window):
        window.show()

    def closeEvent(self, event):
        event.accept()

# Program crash hook for error logging
def except_hook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Icon.Critical)
    dialog.setWindowTitle("Error")
    dialog.setText("Error: Crash caught, save details to file.")
    dialog.setDetailedText(tb)
    dialog.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel)
    ret = dialog.exec()   # Show dialog box
    if ret == QMessageBox.StandardButton.Save:
        path = QFileDialog().getExistingDirectory(dialog,'Select a directory')
        if(path):
            path += '/' + str(date.today()) + "_CollatriX_Crashlog" + ".txt"
            print("saving: ", path)
            with open(path, 'w') as file:
                file.write("System: " + platform.system() + '\n')
                file.write("OS: " + os.name + '\n')
                file.write("Python Version: " + platform.python_version() + '\n')
                file.write("Python Implementation: " + platform.python_implementation() + '\n')
                file.write("Release: " + platform.release() + '\n')
                file.write("Version: " + platform.version() + '\n')
                file.write("Machine: " + platform.machine() + '\n')
                file.write("Processor: " + platform.processor() + '\n' + '\n')
                file.write(tb)

    QApplication.quit() # Quit application

if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    sys.exit()
