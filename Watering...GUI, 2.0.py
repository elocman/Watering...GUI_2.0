#######################################################################################################################
# Cole Varnado, Connor Rodenbeck, Timothy Winiarski
# CSC 132-002
# 11.07.19
# GUI for taking care of plants
#######################################################################################################################
from Tkinter import *
import datetime as dt
import RPi.GPIO as GPIO
from random import randint

class Plant(object):
    def __init__(self, plntName, lghtAmnt, watrAmnt):
        self.plntName = plntName
        self.lghtAmnt = lghtAmnt
        self.watrAmnt = watrAmnt

    @property
    def plntName(self):
        return self._plntName
    @plntName.setter
    def plntName(self, value):
        self._plntName = value

    @property
    def lghtAmnt(self):
        return self._lghtAmnt
    @lghtAmnt.setter
    def lghtAmnt(self, value):
        self._lghtAmnt = value

    @property
    def watrAmnt(self):
        return self._watrAmnt
    @watrAmnt.setter
    def watrAmnt(self, value):
        self._watrAmnt = value

    def __str__(self):
        s = "{}: Light={}hrs, Water={}mL\n~per day~".format(self.plntName, self.lghtAmnt, self.watrAmnt)
        return s

class MainGUI(Frame):
    # the constructor
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="white")
        #parent.attributes("-fullscreen", True)
        self.setupGUI()

    # sets up the GUI
    def setupGUI(self):
        # function to add plant
        def addPlant():
            # variable to check for wrong values
            altr = 0
            # make plant list 6 long
            if (len(plntList) <= nmbrPlnt):
                # check if any input
                if (self.input.get() == ""):
                    stat = ""
                else:
                    # split input by comma
                    stat = self.input.get().split(',')
                # check if Plant class has all inputs needed
                if (len(stat) == 3):
                    # test if user input was a number
                    try:
                        # if user inputs aren't integers it will throw an error
                        stat[1] = int(stat[1])
                        stat[2] = int(stat[2])
                    except:
                        altr = 1
                        # clear input
                        self.input.delete(0, END)
                        # display error messages
                        self.label2 = Label(self, text="Please enter numbers for \nlight amount and water amount.")
                        self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)
                    # make sure the amount of hours is within a day
                    maxValue = 24 - startTime
                    if (stat[1] > maxValue):
                        self.label2 = Label(self, text="Please enter a value \nless than {}".format(maxValue))
                        self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)
                        altr = 1
                    if (stat[2] > 420):
                        self.label2 = Label(self, text="Please enter a value \nless than 420")
                        self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)
                        altr = 1
                    # check if plant is already in list
                    for i in range(len(plntNameList)):
                        # if new plant name = plant name in list
                        if (stat[0] == plntNameList[i]):
                            altr = 1
                            # clear input
                            self.input.delete(0, END)
                            # display error messages
                            self.label2 = Label(self, text="Please enter a plant that \nisn't already in the list.")
                            self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)
                    if (altr == 0):
                        # create new plant
                        newPlnt = Plant(stat[0], stat[1], stat[2])
                        plntList.append(newPlnt)
                        plntNameList.append(newPlnt.plntName)
                        # new menu for new list
                        self.drop = OptionMenu(self, clicked, *plntNameList)
                        self.drop.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W)
                        # display error messages
                        self.label2 = Label(self, text=niceMesg[randint(0, len(niceMesg)-1)])
                        self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)
                        # clear input
                        self.input.delete(0, END)
                else:
                    # clear input
                    self.input.delete(0, END)
                    # display error messages
                    self.label2 = Label(self, text="Please use format: \nPlant,LightHours,WaterAmount")
                    self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)
            else:
                # clear input
                self.input.delete(0, END)

                # display error messages
                self.label2 = Label(self, text="The plant list is full.")
                self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)

        # function to delete plant
        def deletePlant():
            # variable for checking plant
            altr = 0
            # check every plant for one selected
            for i in range(len(plntList)):
                # check which plant to remove
                if (clicked.get() == plntList[i].plntName and i != 0):
                    # j is the index that will be removed
                    j = i
                    altr = 1
            # remove plant
            if (altr == 1):
                # remove from name list and plant list
                plntNameList.remove(plntList[j].plntName)
                plntList.remove(plntList[j])
                # new menu for new list
                clicked.set(plntNameList[0])
                self.drop = OptionMenu(self, clicked, *plntNameList)
                self.drop.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W)
                self.label1 = Label(self, text=plntList[0])
                self.label1.grid(row=0, column=4, columnspan=4, sticky=N+S+E+W)
                # display error messages
                self.label2 = Label(self, text=niceMesg[randint(0, len(niceMesg)-1)])
                self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)

        # function to apply plant selected
        def secret():
            # display error messages
            self.label2 = Label(self, text=niceMesg[randint(0, len(niceMesg)-1)])
            self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)

        # default plant in list for name and values
        plntList = [p1]
        plntNameList = [p1.plntName]

        # set drop down
        clicked = StringVar()
        # set default selection
        clicked.set(plntNameList[0])

        # delete plant button
        self.button2 = Button(self, text="Delete Selection", command=deletePlant)
        self.button2.grid(row=0, column=0, columnspan=4, sticky=N+S+E+W)

        # plant drop-down menu
        self.drop = OptionMenu(self, clicked, *plntNameList)
        self.drop.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W)

        # apply button
        self.button3 = Button(self, text="Secret", command=secret)
        self.button3.grid(row=2, column=0, columnspan=4, sticky=N+S+E+W)

        # add plant button
        self.button1 = Button(self, text="Add Entered Plant", command=addPlant)
        self.button1.grid(row=3, column=0, columnspan=4, sticky=N+S+E+W)

        # text input
        self.input = Entry(self, bg="white")
        self.input.grid(row=4, column=0, columnspan=4, sticky=N+S+E+W)

        # plant info.
        self.label1 = Label(self, text=plntList[0])
        self.label1.grid(row=0, column=4, columnspan=4, sticky=N+S+E+W)

        # function which reads input values and displays them
        def update():
            # time setup
            hourTime = dt.datetime.now().hour
            minuteTime = dt.datetime.now().minute
            secondTime = dt.datetime.now().second
            
            # check plant selected
            for i in range(len(plntList)):
                if (clicked.get() == plntList[i].plntName):
                    plnt = plntList[i]
                    endTime = startTime + plntList[i].lghtAmnt
                    waterSeconds = (float(plntList[i].watrAmnt) / 7)

            # if no plant dont run
            if (clicked.get() != plntList[0].plntName):
                # check for moisture
                if GPIO.input(moistureSensor):
                    moisture = "Off"
                else:
                    moisture = "On"

                # use time period do turn light on/off
                if (hourTime >= startTime and hourTime <= endTime):
                    GPIO.output(lightRelay, GPIO.HIGH)
                    light = "On"
                else:
                    GPIO.output(lightRelay, GPIO.LOW)
                    light = "Off"

                # use time period to decide when to apply nutirents
                if (hourTime == 7 and minuteTime == 0 and secondTime < secondLength):
                    GPIO.output(nutrientRelay, GPIO.HIGH)
                    nutrients = "On"
                else:
                    GPIO.output(nutrientRelay, GPIO.LOW)
                    nutrients = "Off"

                # check time period and moisture and apply water according
                flowTime = waterSeconds * 100
                if (hourTime >= 7 and hourTime <= 16):
                    if (moisture == "Off"):
                        for i in range(int(flowTime)):
                            GPIO.output(waterRelay, GPIO.HIGH)
                            print i
                        GPIO.output(waterRelay, GPIO.LOW)
                else:
                    GPIO.output(waterRelay, GPIO.LOW)
            else:
                GPIO.output(lightRelay, GPIO.LOW)
                GPIO.output(nutrientRelay, GPIO.LOW)
                GPIO.output(waterRelay, GPIO.LOW)
                light = "Off"
                nutrients = "Off"
                moisture = "Off"
                
            # print plant's items
            self.label1 = Label(self, text=plnt)
            self.label1.grid(row=0, column=4, columnspan=4, sticky=N+S+E+W)
            # status
            self.label2 = Label(self, text="STATUS:"+"\nMoisture = "+str(moisture)+\
                "\nNutrients = "+str(nutrients)+"\nLight = "+str(light))
            self.label2.grid(row=1, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)

            self.after(1000, update)
        update()

        # display error messages
        self.label2 = Label(self, text=niceMesg[randint(0, len(niceMesg)-1)])
        self.label2.grid(row=3, column=4, columnspan=4, rowspan=2, sticky=N+S+E+W)

        # resize gui
        for row in range(4):
            Grid.rowconfigure(self, row, weight=1)
        for col in range(8):
            Grid.columnconfigure(self, col, weight=1)

        # pack the GUI
        self.pack(fill=BOTH, expand=1)

#######################################################################################################################
p1 = Plant("No Plant", 0, 0) # initial plant
nmbrPlnt = 5 # length plant list
startTime = 0 # hour start time for light
secondLength = 3 # length of time for nutrient flow

# random messages in place of errors
niceMesg = ["Pretty Flowers",
            "Tree Hugger",
            "Dandy Lions",
            "Eat Grass",
            "420?"]

# GPIO
GPIO.setwarnings(False)
moistureSensor = 21
lightRelay = 17 # light
nutrientRelay = 13
waterRelay = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(moistureSensor, GPIO.IN)
GPIO.setup(lightRelay, GPIO.OUT)
GPIO.setup(nutrientRelay, GPIO.OUT)
GPIO.setup(waterRelay, GPIO.OUT)

#TK
root = Tk()
root.title("Watering...")
root.geometry("600x300")
p = MainGUI(root)
root.mainloop()
