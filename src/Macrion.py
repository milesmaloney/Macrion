import keyboard, sys, time, pyautogui, traceback


keyList = []        #main list to hold all macro keys
actionList = []     #main list to hold all macro responses


#Notes: Mouse-only macros can use mouse.record to maintain all mouse actions. Mouse + keyboard macros should escape keyboard recording to add a mouse recording then record the action as a combination of the recordings.



def commandInterface():
    commandHelp()
    while True:
        currCmd = input()
        if currCmd.lower() == 'add':
            addMacro()
        elif currCmd.lower() == 'del':
            deleteMacro()
        elif currCmd.lower() == 'edit':
            changeMacros()
        elif currCmd.lower() == 'view':
            viewMacros()
        elif currCmd.lower() == 'act':
            macroLoop()
        elif currCmd.lower() == 'help':
            commandHelp()
        elif currCmd.lower() == 'exit':
            exitMacrion()
        else:
            print("Command not recognized. Please try again or type HELP for a list of commands.")



def addMacro():
    time.sleep(1)
    print("Press your macro button now or press esc to cancel. Each macro key should use only one key press. (Shouldn't use modifiers such as shift, ctrl, or alt.)")
    while True:                                     #while loop to ensure the user does not use esc as a macro
        btn = keyboard.read_key(suppress = True)    #reads the key without sending it as an output to any other programs
        if btn == 'esc':
            print("Cancelling and returning to command line...")
            return
        else:
            print("Your macro will be activated using the " + btn + " key.\n")
            break
    print("Your actions will be recorded in a couple seconds. You may record your actions at your own pace; the speed at which you record your actions will not affect the speed at which they playback.")
    time.sleep(2)                                   #prevents the macro button from being recorded as one of the actions
    print("Your actions are being recorded now. End recording by pressing esc.")
    recorded = keyboard.record(until='esc')         #records actions taken by the keyboard
    print("Done recording. Preparing macro...\n")
    time.sleep(0.5)
    keyList.append(btn)                             #adds the macro key to the list of macro keys
    del recorded[-1]                                #deletes the esc press from the recording
    actionList.append(recorded)                     #adds the action to the list of corresponding actions
    releaseKeysAfterMacros(btn)                     #ensures that no key is left pressed at the end of a macro
    print("You may now type ACT to use your macro(s).\n")
    commandHelp()



def releaseKeysAfterMacros(macroKey):               #function to go through and release any unreleased keys at the end of macros
    index = keyList.index(macroKey)
    buttonPressed = []
    for kE in actionList[index]:
        if kE.event_type == "down":
            buttonPressed.append(kE.name)
        elif kE.event_type == "up":
            buttonPressed.remove(kE.name)
    if buttonPressed:                               #checks if there is an element in buttonPressed list
        for button in buttonPressed:
            print(button)
            btnRelease = keyboard.KeyboardEvent("up", button.scan_code, name = button.name, time = button.time + 0.000001, device = button.device, modifiers = button.modifiers, is_keypad = button.is_keypad)      #creates a new release keyboard event for the given key
            actionList(index).append(btnRelease)    #adds each new keyboard event to the overall action that is missing releases




def deleteMacro():                          #command to delete a macro from your macros
    while True:
        time.sleep(0.5)
        print("Please type in the key that triggers the macro you would like to delete, press enter to view your macros, or press esc to cancel.")
        macroDeletion = keyboard.read_key(suppress = True)
        if macroDeletion == 'enter':        #checks if enter was pressed
            viewMacros()                    #displays the macros for the user
        elif macroDeletion == 'esc':        #checks if esc was pressed
            print("Macro deletion cancelled.")
            break
        else:
            if macroDeletion in keyList:    #checks that the key is used as a macro
                print("Macro found. Are you sure you would like to delete the macro for the " + macroDeletion + " key? (y/n)")
                deleteCheck = input()
                if deleteCheck.lower() == 'y':
                    index = keyList.index(macroDeletion)
                    del keyList[index]      #deletes intended the macro key from the list
                    del actionList[index]   #deletes the corresponding response from the list
                elif deleteCheck.lower() == 'n':
                    continue                #continues to a new iteration of the while loop for the user to try again or cancel
                else:
                    print("Input not recognized. Please respond with y or n.")
                    continue                #see above comment
            else:
                print("No macro found that uses " + macroDeletion + ". Please try again.")
                continue                    #see above comment
    commandHelp()



def changeMacros():
    if not actionList:
        print("No macros found.")
    while True:
        time.sleep(0.5)
        print("Please type in the key that triggers the macro you would like to edit, press enter to view your macros, or press esc to cancel.")
        macroChange = keyboard.read_key(suppress = True)
        if macroChange == 'enter':        #checks if enter was pressed
            viewMacros()                    #displays the macros for the user
        elif macroChange == 'esc':        #checks if esc was pressed
            print("Macro editing cancelled.")
            break
        else:
            if macroChange in keyList:    #checks that the key is used as a macro
                print("Macro found. Are you sure you would like to edit the macro for the " + macroChange + " key? (y/n)")
                editCheck = input()
                if editCheck.lower() == 'y':
                    index = keyList.index(macroChange)
                    print("Recording new actions for the " + macroChange + " key in a couple seconds.")
                    time.sleep(2)
                    print("Your actions are being recorded now. End recording by pressing esc.")
                    recorded = keyboard.record(until='esc')         #records actions taken by the keyboard
                    print("Done recording. Preparing macro...\n")
                    time.sleep(0.5)
                    del recorded[-1]    #deletes the esc press from the recording
                    actionList[index] = recorded
                    releaseKeysAfterMacros(macroChange)
                elif editCheck.lower() == 'n':
                    continue                #continues to a new iteration of the while loop for the user to try again or cancel
                else:
                    print("Input not recognized. Please respond with y or n.")
                    continue                #see above comment
            else:
                print("No macro found that uses " + macroChange + ". Please try again.")
                continue                    #see above comment
    commandHelp()


def viewMacros():
    if not actionList:
        print("No macros found.")
    buttonPressed = []          #stores the first press of each key
    responsesToView = []        #stores the key at its release
    for action in actionList:   #gets the list of actions
        actionString = ""       #string to be concatenated with all key events taken in an action
        for kE in action:       #gets the list of keyboard events
            if kE.name in buttonPressed:
                actionString = actionString + (kE.name + " released, ")
                buttonPressed.remove(kE.name)
            else:
                actionString = actionString + (kE.name + " pressed, ")
                buttonPressed.append(kE.name)
        responsesToView.append(actionString)
    for key in keyList:
        idx = keyList.index(key)
        action = responsesToView[idx]
        print(key + "  -->  " + responsesToView[idx])



def macroLoop():
    print("Macros are now activated. Press any of your macro keys to perform their corresponding action or esc to deactivate your macros.")
    currKey = ''
    while currKey != 'esc':
        keyboard.read_key(suppress = True)                          #reads the key being pressed. Does not give that key to any programs
        keySet = set(keyList)                                       #set lookups are more efficient than list lookups
        if currKey in keySet:
            index = keyList.index(currKey)                          #need list index in order to match to the action
            action = actionList[index]                              #gets the corresponding action
            keyboard.play(action, speed_factor=5)                   #plays the corresponding action at 5 times the speed it was recorded
        else:
            keyboard.press(currKey)                                 #presses the key that the user pressed if it is not any of the macros
            if keyboard.read_key(suppress = False) != currKey:      #checks if the user is still pressing the key
                keyboard.release(currKey)                           #releases the non-macro key the user pressed when the user presses a different key
                currKey = keyboard.read_key(suppress = True)        #marks the new key as the current key in case it is esc
    print("Macros deactivated.")
    commandHelp()



def commandHelp():
    print("Type ADD to add a new macro, DEL to delete a macro, VIEW to view your macros, *EDIT to change your macros, ACT to use your macros, HELP to view the commands again, or EXIT to exit.   *WIP")



def exitMacrion():     #exits macrion and writes the macro keys and corresponding actions to a file.     
    try:
        fmc = open("macrokeys.txt","w+")
        for key in keyList:
            fmc.write(key)
            fmc.write("\n") #separates keys by line, trimmed off on reading in keys
        fmc.close()
    except:
        print(traceback.format_exc())
        print("Writing to macro file failed.\n")
    try:
        fac = open("macroactions.txt", "w+")
        for action in actionList:   #gets full macro response
            for event in action:    #gets individual key event within macro response
                fac.write(str(event.event_type) + "_;_" + str(event.scan_code) + "_;_" + str(event.name) + "_;_" + str(event.time) + "_;_" + str(event.device) + "_;_" + str(event.modifiers) + "_;_" + str(event.is_keypad) + "_-_")   #writes all fields of keyboard events separated by _;_ with overall events separated by _-_
            fac.write("\n")         #separates actions by line, unproblematic when reading in responses
        fac.close()
    except:
        print(traceback.format_exc())
        print("Writing to action file failed.\n")
    sys.exit("Program exiting now. Thank you for using Macrion!")



def readMacros():   #reads the macros from the macrokeys and macroactions files
    try:
        fm = open("macrokeys.txt", "r+")
        keys = fm.readlines()
        for key in keys:  
            trimmedKey = key.replace('\n','')
            keyList.append(trimmedKey)
        fm.close()
        fa = open("macroactions.txt", "r+")
        actions = fa.readlines()
        for action in actions:
            newAction = []
            actionpiece = action.split('_-_')   #each key event is separated by _-_
            for keyEvent in actionpiece:    #gets each key event from the line
                if len(keyEvent) <= 1:
                    continue
                eventPiece = keyEvent.split('_;_')  #each key event field is separated by _;_
                revivedKeyEvent = keyboard.KeyboardEvent(eventPiece[0], int(eventPiece[1]), name = eventPiece[2], time = float(eventPiece[3]), device = eventPiece[4], modifiers = eventPiece[5], is_keypad = bool(eventPiece[6]))    #eventPiece[0] is the event type and eventPiece[1] is the scan code
                newAction.append(revivedKeyEvent)
            actionList.append(newAction)
        fa.close()
    except:
        print(traceback.format_exc())
        print("Reading macro files failed. Resuming first time startup...\n")
    if len(keyList) != len(actionList):
        print("Imbalanced macro : action ratio. Would you like to reset your macros? You may also repair the files manually. (Y/N)")
        while True:
            macroErrorCheck = input()
            if macroErrorCheck.lower() == 'y':
                keyList.clear()
                actionList.clear()
                break
            elif macroErrorCheck.lower() == 'n':
                sys.exit("Exiting program. Files can be found in the same file as this program. Actions are separated by '_;_' and macro keys are separated by lines.")
            else:
                print("Please select Y or N. Would you like to reset your macros or repair files manually?")



def printBugs():
    print("\nWelcome to Macrion! Currently known bugs include: \n")
    print("When macro keys use a combination of keys, it will sometimes leave a held key pressed after the macros are deactivated. To fix this, press that button again when your macros are deactivated and it will release.")
    print("When using macros in a very quick succession, the macro will not always complete before the next keypress is recieved and the macro will not do what it is intended to.")
    print("Mouse clicks are not yet included, but are planned to be included in the future.")
    print("Some key combinations are read in incorrectly while macros are activated. Deactivate macros to type normally if you run into this issue.")
    print(" ")



def main():
    try:
        readMacros()
    except:
        print(traceback.format_exc())
        print("Macro files not found. Resuming first time startup.")
    printBugs()
    commandInterface()



if __name__ == "__main__":
    main()
