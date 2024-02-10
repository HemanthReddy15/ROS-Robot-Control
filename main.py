import PIL
from PIL import Image
import customtkinter
import cv2
import pyfirmata2
import time
import os
from tkinter import *
# import openai
import subprocess

# openai.api_key = "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"

global Servo
global Servo_pin
Servo_pin = 12
global Headlight_pin
Headlight_pin = 13

global Pin1
global Pin2
global Pin3
global Pin4

Pin1 = 'd:10:p'
Pin2 = 'd:6:p'
Pin3 = 'd:9:p'
Pin4 = 'd:5:p'



global Temerature_Task
Temerature_Task = True
Robot_Speed = 0.3
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("ROS Robot Control")
        self.geometry(f"{2560}x{1600}")
        self.minsize(1200,700)
        self.maxsize(2560,1600)
        self.Robot_Details_Var = customtkinter.StringVar()
        self.Robot_Module_Var = customtkinter.StringVar()
        global Robot_Speeds
        try:
            self.Port=pyfirmata2.Arduino.AUTODETECT
            self.board = pyfirmata2.Arduino(self.Port)
            print("Setting up the connection to the board ...")
            Servo = self.board.get_pin('d:12:s')
            Servo.write(90)
            in1 = self.board.get_pin(Pin1)
            in2 = self.board.get_pin(Pin2)
            in3 = self.board.get_pin(Pin3)
            in4 = self.board.get_pin(Pin4)
        except:
            print("Board Not Found")
        
        # Grid Layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        def Up(event):
            if switch3.get()==1:
                Robot_Speed = 0.2 + ((1-0.2)/(1-0))*(float(self.slider_1.get()) - 0)
                if Robot_Speed == 0.2:Robot_Speed=0
                try:
                    print("UP arrow is pressed")
                    in1.write(Robot_Speed)
                    in2.write(0)
                    in3.write(Robot_Speed)
                    in4.write(0)
                except:
                    print("Board Not Found!!")
                
        def Down(event):
            if switch3.get()==1:
                Robot_Speed = 0.2 + ((1-0.2)/(1-0))*(float(self.slider_1.get()) - 0)
                if Robot_Speed == 0.2:Robot_Speed=0
                try:
                    print("Down arrow is pressed")
                    in1.write(0)
                    in2.write(Robot_Speed)
                    in3.write(0)
                    in4.write(Robot_Speed)
                except:
                    print("Board Not Found!!")
                
      
        def Left(event):
            if switch3.get()==1:
                Robot_Speed = 0.2 + ((1-0.2)/(1-0))*(float(self.slider_1.get()) - 0)
                if Robot_Speed == 0.2:Robot_Speed=0
                
                try:
                    print("LEFT arrow is pressed")
                    # in1.write(0)
                    # in2.write(Robot_Speed)
                    # in3.write(Robot_Speed)
                    # in4.write(0)
                except:
                    print("Board Not Found!!")
                
        def Right(event):
            if switch3.get()==1:
                Robot_Speed = 0.2 + ((1-0.2)/(1-0))*(float(self.slider_1.get()) - 0)
                if Robot_Speed == 0.2:Robot_Speed=0
               
                in4.write(Robot_Speed)
                try:
                    print("RIGHT arrow is pressed")
                    # in1.write(Robot_Speed)
                    # in2.write(0)
                    # in3.write(0)
                    # in4.write(Robot_Speed)
                except:
                    print("Board Not Found!!")
                
        def Stop(event):
            if switch3.get()==1:
                
                try:
                    print("Stop is pressed")
                    in1.write(0)
                    in2.write(0)
                    in3.write(0)
                    in4.write(0)
                except:
                    print("Board Not Found!!")
            
        def Open_Box(event): # activating servo motor to open Box
            if switch2.get()==1:
                
                Servo.write(0)
                time.sleep(0.01)
                print("Box Opened")
            
                    
        def Close_Box(event): # activating servo motor to close Box
            if switch2.get()==1:
                Servo.write(90)
                time.sleep(0.01)
                print("Box Closed")

            
                    
        def CommandLine_Button_bind(event):
            if self.switch4.get() == 1:
                if self.entry.get()[0:3] == "sSs":
                    textbox_size = int(self.entry.get()[4:])
                    if textbox_size >=35 and textbox_size<=300:
                        self.textbox.configure(height = textbox_size)
                else:
                    self.Answer = ""
                    self.textbox.delete('1.0',END)
                    # completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                    messages=[
                            {"role": "user", "content": self.entry.get()}
                        ]
                    # )
                    # self.Answer  = completion.choices[0].message.content
                    if self.Answer[0] == "\n":self.Answer = self.Answer[2:]
                    self.textbox.insert("0.0", self.Answer)
                    self.entry.delete(0, 'end')
            else :
                # self.textbox.delete('1.0',END)
                if self.entry.get()[0:3] == "sSs":
                    textbox_size = int(self.entry.get()[4:])
                    if textbox_size >=35 and textbox_size<=300:
                        self.textbox.configure(height = textbox_size)
                elif self.entry.get() == "clear":
                    self.textbox.delete('1.0',END)
                else:
                    subprocess_output = subprocess.check_output(self.entry.get())
                    os.system(self.entry.get())
                    self.textbox.insert("end", subprocess_output)
                self.entry.delete(0, 'end')
            
        # create Screen
        def Check_camera():
            if switch1.get() == 1:
                self.vs = cv2.VideoCapture(0)
                self.vs.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
                self.vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
                self.current_image = None  
                self.panel = customtkinter.CTkLabel(self, width=250,text="") 
                self.panel.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
                self.video_loop()
            else:
                self.vs.release()
                cv2.destroyAllWindows()
                
        def Check_Temerature():    
            global Temerature_Task 
            if switch6.get()==1: 
                Temerature_Task = True
                self.Temperature_loop()
            else:
                self.panel = customtkinter.CTkLabel(self, width=250,text="")
                self.panel.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
                Temerature_Task = False
        def Sanitization_Module():
            if switch5.get() == 1:
                print("Sanitizer : ON")
            elif switch5.get() == 0:
                print("Sanitizer : OFF")
            
            

        def Check_Headlight(): 
            if switch.get() == 1:
                try:
                    self.board.digital[Headlight_pin].write(True)
                    print("Headlights Turned On")
                except:
                    print("Board Not Found!! To Turn Headlights On")
                
            elif switch.get() == 0:
                try:
                    self.board.digital[Headlight_pin].write(False)
                    print("Headlights Turned Off")
                except:
                    print("Board Not Found!! To Turn Headlights Off")    
                               
        def Check_servo():
            if switch2.get() == 0:
                try:
                    Servo.write(90)
                    print("Servo module Stopped!! Box Closed!")
                except:
                    print("Servo module Stopped!! Box CLosed!")
                    
            elif switch2.get() == 1:
                try:
                    Servo.write(90)
                    print("Box Closed!")
                except:
                    print("")
                    
        def Check_ChatBot_Dimensions():
            if self.switch4.get() == 1:self.textbox.configure(height= 100)
            else:self.textbox.configure(height= 30)
                  
        def toggle_fullscreen(event):
            self.attributes("-fullscreen", True)
            
        def end_fullscreen(event):
            self.attributes("-fullscreen", False)
         
          
            
        # Pulsanzer Main Frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=3, rowspan=5, sticky="nsew")
        # self.sidebar_frame.grid_rowconfigure(3, weight=1) 
        # self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        # self.logo_image = customtkinter.CTkImage(PIL.Image.open(os.path.join(self.image_path, "robot.png")), size=(150, 150))
        # self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,text = "",image=self.logo_image, compound="left", font=customtkinter.CTkFont(size=25, weight="bold"))
        # self.logo_label.grid(row=0, column=3, padx=20, pady=(20, 10))
        self.logo_label1 = customtkinter.CTkLabel(self.sidebar_frame, text="ROS2",text_color= "Orange", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.logo_label1.grid(row=1, column=3, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text = "START", fg_color= "Green", hover_color="#4fc22b", command=self.start_button_event)
        self.sidebar_button_1.grid(row=2, column=3, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text = "STOP", fg_color= "Red", hover_color="#f75e52", command=self.stop_button_event)
        self.sidebar_button_2.grid(row=3, column=3, padx=20, pady=10)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,text = "Clear Terminal", fg_color= "#faf175",text_color= "Black", hover_color="#fcf8b8", command=self.Clear_Terminal)
        # self.sidebar_button_3.grid(row=3, column=3, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame,text = "Close App", fg_color= "White",text_color= "Black", hover_color="#c4c4c2", command=self.close_button_event)
        self.sidebar_button_4.grid(row=4, column=3, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=3, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=3, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=3, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=3, padx=20, pady=(10, 20))
        
        
        
        # Screen Panel
        self.screen_frame = customtkinter.CTkFrame(self,corner_radius=50)
        self.screen_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.screen_frame.grid_rowconfigure(1,weight=1) 
        self.panel = customtkinter.CTkLabel(self.screen_frame,height=10, width=250,text="")  # initializing image panel
        self.panel.grid(padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        
        #AI Label Box        
        self.textbox = customtkinter.CTkTextbox(self, height=30, corner_radius=8)
        self.textbox.grid(row=3, column=0,columnspan = 3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        
        
        # Command line Entry and Enter button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Command Line")
        self.entry.grid(row=4, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent",text="Enter", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.CommandLine_Button)
        self.main_button_1.grid(row=4, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Robot List
        self.tabview = customtkinter.CTkTabview(self, width=100)
        self.tabview.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Robot 1")
        self.tabview.add("Robot 2")
        self.tabview.tab("Robot 1").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Robot 2").grid_columnconfigure(0, weight=1)
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Robot 1"), dynamic_resizing=False, values=["Manual", "Automatic"],command=self.Robot_Details)
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Robot 1"), values=["Modules","Camera", "Lidar", "Temerature", "AI ChatBot"],command=self.Robot_Module)
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Robot 2"), values=["No  Mode  Detected!!"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(30, 10))
        self.combobox_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Robot 2"), values=["N0 Modules Detected!!"])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(30, 10))
        self.optionmenu_1.set("No Mode Detected!!")
        self.combobox_1.set("No Modules Detected!!")


        # Robot Operation frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = customtkinter.IntVar()
        self.radio_var1 = customtkinter.IntVar()
        self.radio_var2 = customtkinter.IntVar()
        self.radio_var3 = customtkinter.IntVar()
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Robot Operation",text_color= "Yellow", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var,text=  "Operation 1", value=1)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="W")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, text= "Operation 2",value=2)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="W")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, text= "Operation 3", value=3)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="W")
        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, text= "Operation 4",value=4)
        self.radio_button_4.grid(row=4, column=2, pady=10, padx=20, sticky="W")



        # Slider frame
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Robot Speed")
        self.tabview.add("Servo Control")
        self.tabview.tab("Robot Speed").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Servo Control").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Servo Control").grid_columnconfigure(3, weight=1)
        self.progressbar_1 = customtkinter.CTkProgressBar(self.tabview.tab("Robot Speed"), progress_color = "Green")
        self.progressbar_1.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.tabview.tab("Robot Speed"))
        self.progressbar_2.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_0 = customtkinter.CTkSlider(self.tabview.tab("Robot Speed"), from_=0, to=1, number_of_steps=100)
        self.slider_0.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        # self.progressbar_3 = customtkinter.CTkProgressBar(self.tabview.tab("Servo Control"), progress_color = "White")
        # self.progressbar_3.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.tabview.tab("Servo Control"), from_=0, to=1, number_of_steps=50)
        self.slider_1.grid(row=4, column=1, padx=(0, 20), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.tabview.tab("Servo Control"), from_=0, to=1, number_of_steps=50)
        self.slider_2.grid(row=5, column=1, padx=(0, 20), pady=(10, 10), sticky="ew")
        self.slider_3 = customtkinter.CTkSlider(self.tabview.tab("Servo Control"), from_=0, to=1, number_of_steps=50)
        self.slider_3.grid(row=6, column=1, padx=(0, 20), pady=(10, 10), sticky="ew")
        self.slider_4 = customtkinter.CTkSlider(self.tabview.tab("Servo Control"), from_=0, to=1, number_of_steps=50)
        self.slider_4.grid(row=4, column=3, padx=(0, 10), pady=(10, 10), sticky="ew")
        self.slider_5 = customtkinter.CTkSlider(self.tabview.tab("Servo Control"), from_=0, to=1, number_of_steps=50)
        self.slider_5.grid(row=6, column=3, padx=(0, 10), pady=(10, 10), sticky="ew")
        self.slider_6 = customtkinter.CTkSlider(self.tabview.tab("Servo Control"), from_=0, to=1, number_of_steps=5)
        self.slider_6.grid(row=5, column=3, padx=(0, 10), pady=(10, 10), sticky="ew")
        self.label_radio_group1 = customtkinter.CTkLabel(self.tabview.tab("Servo Control"), text="Axis-1")
        self.label_radio_group1.grid(row=4, column=0, columnspan=1, padx=(10,0), pady=10, sticky="")
        self.label_radio_group2 = customtkinter.CTkLabel(self.tabview.tab("Servo Control"), text="Axis-2")
        self.label_radio_group2.grid(row=5, column=0, columnspan=1, padx=(10,0), pady=10, sticky="")
        self.label_radio_group3 = customtkinter.CTkLabel(self.tabview.tab("Servo Control"), text="Axis-3")
        self.label_radio_group3.grid(row=6, column=0, columnspan=1, padx=(10,0), pady=10, sticky="")
        self.label_radio_group4 = customtkinter.CTkLabel(self.tabview.tab("Servo Control"), text="Axis-4")
        self.label_radio_group4.grid(row=4, column=2, columnspan=1, padx=(10,0), pady=10, sticky="")
        self.label_radio_group5 = customtkinter.CTkLabel(self.tabview.tab("Servo Control"), text="Axis-5")
        self.label_radio_group5.grid(row=5, column=2, columnspan=1, padx=(10,0), pady=10, sticky="")
        self.label_radio_group6 = customtkinter.CTkLabel(self.tabview.tab("Servo Control"), text="Axis-6")
        self.label_radio_group6.grid(row=6, column=2, columnspan=1, padx=(10,0), pady=10, sticky="")
        self.Gripper_Stop = customtkinter.CTkButton(self.tabview.tab("Servo Control"),text = "STOP", fg_color= "Red", hover_color="#f75e52")
        self.Gripper_Stop.grid(row=7, column=1, padx=20, pady=10)
        self.Gripper_Pos_save = customtkinter.CTkButton(self.tabview.tab("Servo Control"),text = "SAVE POSITION", fg_color= "Green", hover_color="#4fc22b")
        self.Gripper_Pos_save.grid(row=7, column=3, padx=20, pady=10)
        
        
        
        
        # Robot Settings frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Robot Settings")
        self.scrollable_frame.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        switch = customtkinter.CTkSwitch(master=self.scrollable_frame,  text="HeadLight Light",command=Check_Headlight)
        switch.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="W")
        self.scrollable_frame_switches.append(switch)
        switch1 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="camera Module  ",command=Check_camera)
        switch1.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="W")
        self.scrollable_frame_switches.append(switch1)
        switch2 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Servo Module   ",command=Check_servo)
        switch2.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="W")
        self.scrollable_frame_switches.append(switch2)
        switch3 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Motor Driver   ")
        switch3.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="W")
        self.scrollable_frame_switches.append(switch3)
        self.switch4 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="AI ChatBot     ",command=Check_ChatBot_Dimensions)
        self.switch4.grid(row=4, column=0, padx=10, pady=(0, 20), sticky="W")
        self.scrollable_frame_switches.append(self.switch4)
        switch5 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="RGB Module", command=Sanitization_Module)
        switch5.grid(row=5, column=0, padx=10, pady=(0, 20), sticky="W")
        self.scrollable_frame_switches.append(switch5)
        switch6 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Temperature Module",command=Check_Temerature)
        switch6.grid(row=6, column=0, padx=10, pady=(0, 20), sticky="W")
        self.scrollable_frame_switches.append(switch6)
        switch7 = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Lidar Module   ")
        switch7.grid(row=7, column=0, padx=10, pady=(0, 20), sticky="W")
        self.scrollable_frame_switches.append(switch2)
        
        
        
        # Sensors frame
        self.sensor_frame = customtkinter.CTkScrollableFrame(self, label_text="Sensors")
        self.sensor_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.sensor_frame.grid_columnconfigure(0, weight=1)
        self.Sensor_frame_switch = []
        
        sensor_switch1 = customtkinter.CTkSwitch(master=self.sensor_frame,text="Temerature ")
        sensor_switch1.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="W")
        self.Sensor_frame_switch.append(sensor_switch1)
        
        sensor_switch2 = customtkinter.CTkSwitch(master=self.sensor_frame,text="LDR Module ")
        sensor_switch2.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="W")
        self.Sensor_frame_switch.append(sensor_switch2)
        sensor_switch3 = customtkinter.CTkSwitch(master=self.sensor_frame,text="Encoderㅤㅤ ")
        sensor_switch3.grid(row=4, column=0, pady=(20, 0), padx=20, sticky="W")
        self.Sensor_frame_switch.append(sensor_switch3)
        sensor_switch4 = customtkinter.CTkSwitch(master=self.sensor_frame,text="Humidityㅤㅤ")
        sensor_switch4.grid(row=5, column=0, pady=(20, 0), padx=20, sticky="W")
        self.Sensor_frame_switch.append(sensor_switch4)
        sensor_switch5 = customtkinter.CTkSwitch(master=self.sensor_frame,text="Smokeㅤㅤㅤㅤ")
        sensor_switch5.grid(row=6, column=0, pady=(20, 0), padx=20, sticky="W")
        self.Sensor_frame_switch.append(sensor_switch5)
        
        
        
        # Default values
        sensor_switch4.configure(state="disabled")
        sensor_switch5.configure(state="disabled")
        sensor_switch1.select()
        sensor_switch2.select()
        sensor_switch3.select()
        # self.radio_button_1.select()
        
        
        # self.scrollable_frame_switches[0].select()
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.slider_0.configure(command=self.progressbar_2.set)
        self.progressbar_1.configure(mode="indeterminnate")
        # self.progressbar_3.configure(mode="indeterminnate")
        self.progressbar_1.start()
        # self.progressbar_3.start()
        
        #Bind
        self.bind('<Up>',Up)
        self.bind('<Down>',Down)
        self.bind('<Left>',Left)
        self.bind('<Right>',Right)
        self.bind('s',Stop)
        self.bind('o',Open_Box)
        self.bind('c',Close_Box)
        self.bind("f",toggle_fullscreen)
        self.bind("<Escape>",end_fullscreen)
        self.bind("<Return>",CommandLine_Button_bind)
        

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    def start_button_event(self):
        print("Start")
    def stop_button_event(self):
        print("Stop")
    def Clear_Terminal(self):
        # system("clear")
        print(int(self.slider_1.get()*100))
    def close_button_event(self):
        LOGIN.destroy()
        self.destroy()
    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()
        if ok and self.Robot_Module_Var == "Camera":
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            imgtk = PIL.ImageTk.PhotoImage(master = self,image=PIL.Image.fromarray(cv2image))
            self.panel.imgtk = imgtk 
            self.panel.configure(image=imgtk)
        else:
            self.panel.configure(image="")
        self.after(60, self.video_loop)
    def Temperature_loop(self):
        
        if self.Robot_Module_Var == "Temerature" and Temerature_Task == True:
            self.panel = customtkinter.CTkLabel(self, width=250,text="Temerature", font=customtkinter.CTkFont(size=30, weight="bold"))
            self.panel.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        else:
            self.screen_frame = customtkinter.CTkFrame(self,corner_radius=50)
            self.screen_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
            self.screen_frame.grid_rowconfigure(1,weight=1) 
            self.panel = customtkinter.CTkLabel(self.screen_frame,height=10, width=250,text="")  # initializing image panel
            self.panel.grid(padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.after(1000, self.Temperature_loop)      

    def CommandLine_Button(self):
        if self.switch4.get() == 1:
            if self.entry.get()[0:3] == "sSs":
                textbox_size = int(self.entry.get()[4:])
                if textbox_size >=35 and textbox_size<=300:
                    self.textbox.configure(height = textbox_size)
            else:
                self.Answer = ""
                self.textbox.delete('1.0',END)
                # completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                messages=[
                        {"role": "user", "content": self.entry.get()}
                    ]
                # )
                # self.Answer  = completion.choices[0].message.content
                if self.Answer[0] == "\n":self.Answer = self.Answer[2:]
                self.textbox.insert("0.0", self.Answer)
                self.entry.delete(0, 'end')
        else :
            os.system(self.entry.get())#################################
            self.entry.delete(0, 'end')
    def Robot_Details(self,choice):
        self.Robot_Details_Var = choice
        print(self.Robot_Details_Var)
    def Robot_Module(self,choice):
        self.Robot_Module_Var = choice
        print(self.Robot_Module_Var)
                
        

# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
        
def RUN_ROBOT():
    if __name__ == "__main__":
        app = App()
        app.mainloop()

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

# Our app frame
LOGIN = customtkinter.CTk()
LOGIN.geometry("450x350")
LOGIN.minsize(450,350)
LOGIN.maxsize(450,350)
LOGIN.title("Ros Robot")

# p1 = PhotoImage(file = 'icon.png')
  
# # Setting icon of master window
# LOGIN.iconphoto(False, p1)
global UserName
global Password
UserName = "admin"
Password = "password"
def login():
    global Result
    print("hi")
    if user_entry.get() == UserName and user_pass.get() == Password:
        LOGIN.withdraw()
        RUN_ROBOT()
    elif user_entry.get() != UserName or user_pass.get() != UserName & Password:
        Result = "Check your Username and Password"
    Lable12 = customtkinter.CTkLabel(LOGIN, text=Result)
    Lable12.pack(pady=20)
    
def Login(event):
    global Result
    print("hi")
    if user_entry.get() == UserName and user_pass.get() == Password:
        LOGIN.withdraw()
        RUN_ROBOT()  
    elif user_entry.get() != UserName or user_pass.get() != Password:
        Result = "Check your Username and Password"
    Lable12 = customtkinter.CTkLabel(LOGIN, text=Result)
    Lable12.pack(pady=20)
    
my_font = customtkinter.CTkFont(family="Times New Roman", size=35)

label = customtkinter.CTkLabel(LOGIN,text="Robot Login",font=my_font,text_color="orange")

label.pack(pady=20)

frame = customtkinter.CTkFrame(master=LOGIN)
frame.pack(pady=12,padx=40,fill='both',expand=True)

user_entry= customtkinter.CTkEntry(master=frame,placeholder_text="Username",height=30,width=250)
user_entry.pack(pady=12,padx=10)

user_pass= customtkinter.CTkEntry(master=frame,placeholder_text="Password",show="*",height=30,width=250)
user_pass.pack(pady=12,padx=10)

button = customtkinter.CTkButton(master=frame,text='Login',command=login,height= 30,width=150)
button.pack(pady=20,padx=10)
label = customtkinter.CTkLabel(LOGIN,text="Robot Login",font=my_font,text_color="orange")
LOGIN.bind('<Return>',Login)

LOGIN.mainloop()
