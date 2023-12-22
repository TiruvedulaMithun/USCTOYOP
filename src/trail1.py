import time
import mouse
import pyautogui
import csv
import sys
import os

# # Window size
# width, height = pyautogui.size()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def enterNumber(num, justClickOnNumber=False):
    number_labels = list(pyautogui.locateAllOnScreen(resource_path('./number_label.png')))
    choice = 0
    if len(number_labels) > 1:
        print("[WARN] More than one label found for number_label")
        print("[ACTION] Select one of the options")
        for number_label in number_labels:
            print(number_label)
        choice = input("Enter the number of the label you want to use: ")
    elif len(number_labels) == 0:
        print("[ERROR] no number_label found")
        return
    number_label = number_labels[int(choice)]
    # print("Number box:", number_label)
    number_box_coords = (number_label[0] + number_label[2] + 15, number_label[1] + 5)
    pyautogui.moveTo(number_box_coords[0], number_box_coords[1], duration=0.25)
    pyautogui.click(number_box_coords[0], number_box_coords[1])
    if justClickOnNumber:
        return
    pyautogui.keyDown('ctrl') 
    pyautogui.press('a') 
    pyautogui.keyUp('ctrl') 
    pyautogui.write(num) 
    pyautogui.press('enter') 

def openActivity():
    activity_buttons = list(pyautogui.locateAllOnScreen(resource_path('./activity_button1.png')))
    choice = 0
    if len(activity_buttons) > 1:
        print("[WARN] More than one button found for activity_button")
        print("[ACTION] Select one of the options")
        for activity_button in activity_buttons:
            print(activity_button)
        choice = input("Enter the number of the button you want to use: ")
    elif len(activity_buttons) == 0:
        print("[ERROR] no activity_button found")
        return
    activity_button = activity_buttons[int(choice)]
    # print("activity_button:", activity_button)
    pyautogui.click(pyautogui.center(activity_button))

def enterYOP(num):
    football_list = list(pyautogui.locateAllOnScreen(resource_path('./football_label.png')))
    is_football = False
    if len(football_list) > 0:
        choice = 0
        if len(football_list) > 1:
            print("[WARN] More than one label found for football_label")
            print("[ACTION] Select one of the options")
            for football_label in football_list:
                print(football_label)
            choice = input("Enter the number of the label you want to use: ")
        football_label = football_list[int(choice)]
        # print("football_label:", football_label)
        football_box_coords = (football_label[0] + football_label[2] + 115, football_label[1] + 5)
        pyautogui.moveTo(football_box_coords[0], football_box_coords[1], duration=0.25)
        pyautogui.click(football_box_coords[0], football_box_coords[1])
    elif len(football_list) == 0:
        # goto activity label
        activity_labels = list(pyautogui.locateAllOnScreen(resource_path('./activity_label.png')))
        choice = 0
        if len(activity_labels) > 1:
            print("[WARN] More than one label found for activity_label")
            print("[ACTION] Select one of the options")
            for activity_label in activity_labels:
                print(activity_label)
            choice = input("Enter the number of the label you want to use: ")
        elif len(activity_labels) == 0:
            print("[ACTION] no activity_label found, please enter manually: "+ str(num))
            return
        activity_label = activity_labels[int(choice)]
        # print("activity_label:", activity_label)
        activity_box_coords = (activity_label[0] + (activity_label[2]/2), activity_label[1] + 25)
        pyautogui.click(activity_box_coords[0], activity_box_coords[1], duration=0.25)
        pyautogui.press('F') 
        pyautogui.press('tab') 
        
    pyautogui.keyDown('ctrl') 
    pyautogui.press('a') 
    pyautogui.keyUp('ctrl') 
    pyautogui.write(num) 
    pyautogui.press('f2') 

def setMousePosition(cords):
    pyautogui.moveTo(cords[0], cords[1], duration=0.1)
    pyautogui.move(0, 25, duration=0.1)
    pyautogui.click()

def clickConfirm():
    is_sb = False
    sb_list = list(pyautogui.locateAllOnScreen(resource_path('./SB_Dialog.png')))
    # print("sb_list", len(sb_list))
    if len(sb_list) <= 0:
        print("[WARN] No Confirm Dialog found")
        return

    confirm_buttons = list(pyautogui.locateAllOnScreen(resource_path('./yes_button.png')))
    choice = 0
    if len(confirm_buttons) > 1:
        print("[WARN] More than one button found for activity_button")
        print("[ACTION] Select one of the options")
        for activity_button in confirm_buttons:
            print(activity_button)
        choice = input("Enter the number of the button you want to use: ")
    activity_button = confirm_buttons[int(choice)]
    # print("activity_button:", activity_button)
    pyautogui.click(pyautogui.center(activity_button))

try:
    im = pyautogui.screenshot()
    # read csv file
    firstFlag = True
    HAS_ACTIVITY_COL = True
    HAS_COLUMN_NAMES = True
    FILE_NAME = "./data.csv"
    mouse_position = pyautogui.position()
    with open(FILE_NAME, 'r') as file:
        reader = csv.reader(file)
        input("[ACTION] Please put TrES and this window side by side and Press Enter to continue...")

        for row in reader:
            if HAS_COLUMN_NAMES:
                HAS_COLUMN_NAMES = False
                continue
            if HAS_ACTIVITY_COL:
                number, name, activity, yop = row
            else:
                number, name, yop = row
                activity = "F"
            print("-----------------------------------------")
            print("[INFO] Setting", name, number, activity, yop)
            enterNumber(number)
            time.sleep(3)
            # while(not pyautogui.locateOnScreen('activity_button.png') == None):
            openActivity()
            time.sleep(1)
            enterYOP(yop)
            setMousePosition(mouse_position)
            firstFlag = False
            input("[ACTION] Is everything good for "+ str(number) +"? Press Enter to continue...")
            print("-----------------------------------------")
            print()
            mouse_position = pyautogui.position()
            enterNumber(number, True)
            # time.sleep(0.5)
            pyautogui.press('f2') 
            clickConfirm()
            time.sleep(1.8)
except Exception as e:
    print("[ERROR] Something went wrong", e)
    input("Press Enter to quit. Don't forget to CHANGE THE DATA FILE FOR NEXT ITERATION.")
input("[INFO] Done. Press Enter to quit. Don't forget to CHANGE THE DATA FILE FOR NEXT ITERATION.")
