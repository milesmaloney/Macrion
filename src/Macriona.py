#______________________________________________________Libraries______________________________________________________________________________


import keyboard,sys,time,mouse,traceback
from tkinter import *
from tkinter import ttk, font



#________________________________________________________Notes__________________________________________________________________________________



#states: home, startAddMacro, aMRecord, finishAddMacro, startChangeMacro, cMRecord, finishChangeMacro
#TODO: test responses against each other so two keys don't do the same thing
#TODO: make the message, buttons, & border look nicer



#_______________________________________________________Global Variables________________________________________________________________________



keyList = []        #main list to hold all macro keys
actionList = []     #main list to hold all macro responses
state = 'home'      #global variable initialization
btn = 'no key entered'  #global variable initialization
macroLabelList = []     #list to hold all macro key -> response strings for view macros



#___________________________________________________Important Helper Functions______________________________________________________________________



def changeState(newState):                    #prepares the frame for the state we are changing to
    global state, btn, macroLabelList
    saveMacros(False)                              #saves macros every time the state changes
    for widget in frame.winfo_children():     #clears the screen of widgets
        widget.grid_forget()
    ##########home##############
    if newState == 'home':
        #message, label, and button labels
        cancelButton.configure(text="Cancel")
        message.set("Welcome to Macriona! Please select what you would like to do.")
        #variable reinitializations
        macroKey.set('')
        btn = 'no key entered'
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = N, columnspan = 6)
        addMacroButton.grid(column = 0, row = 1, sticky = (N,W,E), columnspan = 3)
        deleteMacroButton.grid(column = 3, row = 1, sticky = (N,E,W), columnspan = 3)
        editMacroButton.grid(column = 0, row = 2, sticky = (W,E), columnspan = 3)
        viewMacrosButton.grid(column = 3, row = 2, sticky = (E,W), columnspan = 3)
        activateMacroButton.grid(column = 0, row = 3, sticky = (S,W,E), columnspan = 3)
        saveExitButton.grid(column = 3, row = 3, sticky = (S,E,W), columnspan = 3)
        #state change
        state = 'home'
    ###########addMacro###########
    elif newState == 'startAddMacro':
        #message, label, and button labels
        message.set("Type the key you would like to store your macro on in the box and click next.")
        buttonLabel.set('Next')
        #next button command configuration (in startFunction states)
        nextButton.configure(command = addMacro)
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        nextButton.grid(column = 18, row = 1, sticky = (S,E))
        cancelButton.grid(column = 19, row = 1, sticky = (S,E))
        macrKeyLabel.grid(column = 0, row = 1, sticky = (N,W))
        macroEntry.grid(column = 1, row = 1, sticky = (N,W))
        #state change
        state = 'startAddMacro'
    elif newState == 'aMRecord':
        #message, label, and button labels
        messageLabel.configure(font = subMessageFont)
        message.set("Your macro will use the '" + btn + "' key. If this is correct, click record to begin recording (End at any time by pressing esc). Otherwise, click cancel to return to the home screen.")
        macroLabel.configure(text = btn)
        buttonLabel.set("Record")
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        macrKeyLabel.grid(column = 0, row = 1, sticky = (N,W))
        macroLabel.grid(column = 1, row = 1, sticky = (N,W))
        nextButton.grid(column = 18, row = 1, sticky = (S,E))
        cancelButton.grid(column = 19, row = 1, sticky = (S,E))
        #state change
        state = 'aMRecord'
    elif newState == 'finishAddMacro':
        #message, label, and button labels
        buttonLabel.set("Activate")
        messageLabel.configure(font = messageFont)
        cancelButton.configure(text = "Home")
        message.set("You may now press Activate to use your macro(s) or Home to go back to the starting page.\n")
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        nextButton.grid(column = 18, row = 2, sticky = (S,E))
        cancelButton.grid(column = 19, row = 2, sticky = (S,E))
        macrKeyLabel.grid(column = 0, row = 1, sticky = (N,W))
        macroLabel.grid(column = 1, row = 1, sticky = (N,W))
        responseLabel.grid(column = 0, row = 2, sticky = (S,W))
        recordingLabel.grid(column = 1, row = 2, sticky = (S,W), columnspan = 17)
        #state change
        state = 'finishAddMacro'
    ###############deleteMacro##############
    elif newState == 'startDeleteMacro':
        #message, label, and button labels
        message.set("Please type in the key that triggers the macro you would like to delete, click View Macros to view your macros, or click Cancel to return to the main menu.")
        buttonLabel.set("Next")
        #next button command configuration
        nextButton.configure(command = deleteMacro)
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        macrKeyLabel.grid(column = 0, row = 1, sticky = W)
        macroEntry.grid(column = 1, row = 1, sticky = W)
        nextButton.grid(column = 18, row = 1, sticky = (S,E))
        cancelButton.grid(column = 19, row = 1, sticky = (S,E))
        viewMacrosButton.grid(column = 17, row = 1, sticky = (S,E))
        #state change
        state = 'startDeleteMacro'
    elif newState == 'deleteCheck':
        #message, label, and button labels
        message.set("You are about to delete the macro bound to the '" + btn + "' key. Click Delete to delete the macro or Cancel to go back to the main menu.")
        buttonLabel.set("Delete")
        macroLabel.configure(text = btn)
        macroResponse.set(extractRecordingToPrint(getResponseFromKey(btn)))
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        macrKeyLabel.grid(column = 0, row = 1, sticky = (N,W))
        macroLabel.grid(column = 1, row = 1, sticky = (N,W))
        responseLabel.grid(column = 0, row = 2, sticky = (S,W))
        recordingLabel.grid(column = 1, row = 2, sticky = (S,W), columnspan = 17)
        nextButton.grid(column = 18, row = 2, sticky = (S,E))
        cancelButton.grid(column = 19, row = 2, sticky = (S,E))
        #state change
        state = 'deleteCheck'
    elif newState == 'finishDeleteMacro':
        #message, label, and button labels
        message.set("Macro bound to the '" + btn + "' key has been deleted. Click delete another to delete another macro or Home to go home.")
        buttonLabel.set("Delete another")
        cancelButton.configure(text="Home")
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        nextButton.grid(column = 18, row = 1, sticky = (S,E))
        cancelButton.grid(column = 19, row = 1, sticky = (S,E))
        #state change
        state = 'finishDeleteMacro'
    ################changeMacro##############
    elif newState == 'startChangeMacro':
        #message, label, and button labels
        message.set("Please type in the key that triggers the macro you would like to edit, click View Macros to view your macros, or click Cancel to return to the main menu.")
        buttonLabel.set("Next")
        #next button command configuration
        nextButton.configure(command = changeMacros)
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        macrKeyLabel.grid(column = 0, row = 1, sticky = W)
        macroEntry.grid(column = 1, row = 1, sticky = W)
        nextButton.grid(column = 18, row = 1, sticky = (S,E))
        cancelButton.grid(column = 19, row = 1, sticky = (S,E))
        viewMacrosButton.grid(column = 17, row = 1, sticky = (S,E))
        #state change
        state = 'startChangeMacro'
    elif newState == 'cMRecord':
        #message, label, and button labels
        message.set("You are about to change the macro bound to the '" + btn + "' key? Click Record to start recording (Stop by pressing esc) or click Cancel to cancel.")
        buttonLabel.set("Record")
        macroLabel.configure(text=btn)
        macroResponse.set(extractRecordingToPrint(getResponseFromKey(btn)))
        #grid placements
        macrKeyLabel.grid(column = 0, row = 1, sticky = (N,W))
        macroLabel.grid(column = 1, row = 1, sticky = (N,W))
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        nextButton.grid(column = 18, row = 2, sticky = (S,E))
        cancelButton.grid(column = 19, row = 2, sticky = (S,E))
        responseLabel.grid(column = 0, row = 2, sticky = (S,W))
        recordingLabel.grid(column = 1, row = 2, sticky = (S,W), columnspan = 17)
        #state change
        state = 'cMRecord'
    elif newState == 'finishChangeMacro':
        #message, label, and button labels
        buttonLabel.set("Activate")
        cancelButton.configure(text = "Home")
        message.set("You may now press Activate to use your macro(s) or Home to go back to the starting page.\n")
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E), columnspan = 20)
        nextButton.grid(column = 18, row = 2, sticky = (S,E))
        cancelButton.grid(column = 19, row = 2, sticky = (S,E))
        macrKeyLabel.grid(column = 0, row = 1, sticky = (N,W))
        macroLabel.grid(column = 1, row = 1, sticky = (N,W))
        responseLabel.grid(column = 0, row = 2, sticky = (S,W))
        recordingLabel.grid(column = 1, row = 2, sticky = (S,W), columnspan = 17)
        #state change
        state = 'finishAddMacro'
    #############viewMacros#############
    elif newState == 'macroView':
        #message, label, and button labels
        cancelButton.configure(text="Home")
        message.set("Here are all of the macros you have already created.")
        #grid placements
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E))
        cancelButton.grid(column = 1, row = len(actionList), sticky = (S,E))
        getMacroLabelList()
        for currRow in range(0,len(actionList)):
            macroLabelList[currRow].grid(column = 0, row = currRow + 1, sticky = (N,W))
        #state change
        state = 'macroView'
    else:
        message.set("Something went wrong. Please try again.")
        cancelButton.configure(text="Home")
        messageLabel.grid(column = 0, row = 0, sticky = (N,W,E,S), columnspan = 20)
        cancelButton.grid(column = 19, row = 1, sticky = (S,E))



def recordInput(commandCalling):    #records keyboard input; takes in a string representing the command calling it
    global btn
    if commandCalling == 'addMacro':
        recorded = keyboard.record(until='esc')
        del recorded[-1]                                    #erases the esc press at the end of the recording
        keyList.append(btn)
        actionList.append(recorded)
        macroResponse.set(extractRecordingToPrint(recorded))                          #sets the response string variable to the recorded events
    elif commandCalling == 'changeMacros':
        recorded = keyboard.record(until='esc')
        del recorded[-1]
        index = keyList.index(btn)
        actionList[index] = recorded                        #replaces the action at the key's index with the action just recorded
        macroResponse.set(extractRecordingToPrint(recorded))                          #sets the response string variable to the recorded events



def getMacrosFromFiles():
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
#        print("Reading macro files failed. Resuming first time startup...\n")
'''    if len(keyList) != len(actionList):
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
                print("Please select Y or N. Would you like to reset your macros or repair files manually?")'''         #This code is useful but needs to be altered to be used in the UI



def getMacroLabelList():                        #updates the macroLabelList for the viewMacros command
    global macroLabelList
    if macroLabelList:                          #destroys all the labels from the list if any exist
        destroyLabelsFromList(macroLabelList)
        macroLabelList.clear()
    for label in range(0, len(actionList)):     #gets rows from 1 -> len(actionList) (not including 0 because 0th row is reserved for message)
        newLabel = ttk.Label(frame, text = keyList[label] + ' -> ' + extractRecordingToPrint(actionList[label]), font = smallFont)
        macroLabelList.append(newLabel)



def destroyLabelsFromList(labelList):           #destroys labels from a list of labels; helper function used for getMacroLabelList
    for label in labelList:
        label.destroy()



def deleteMacroFromLists(key):           #takes in a macro key and deletes its macro
    index = keyList.index(key)
    del actionList[index]
    del keyList[index]



def getResponseFromKey(key):            #takes in a key and returns its action
    index = keyList.index(key)
    return actionList[index]



def extractRecordingToPrint(recorded):  #takes in a recording and returns a readable version of it as a string
    toPrint = ''
    for action in recorded:                             #gets a keyboard event in recorded
        if action.event_type == 'down':
            toPrint = toPrint + action.name + ' pressed, '
        elif action.event_type == 'up':
            toPrint = toPrint + action.name + ' released, '
    toPrint = toPrint[:len(toPrint) - 2] + '.'
    return toPrint



#__________________________________________________Command functions____________________________________________________________________



def addMacro():
    global state, btn
    if state == 'home':                                             #Add Macro button is pressed on home page
        changeState('startAddMacro')                                #State changes to startAddMacro
        return
    if state == 'startAddMacro':                                    #Next button is pressed after user is prompted for macro key
        btn = macroEntry.get()                                      #Gets the key entered in the macro key prompt (TODO: Input validation)
        if btn == 'no key entered':                                 #Checks that a key was entered
            message.set("No macro key entered. Please try again.")
            return                                                  #Returns do not change the state, so the screen will not be changed
        elif btn in keyList:                                        #Checks that the key is not already mapped to an action
            message.set("Macro key already has a response. Please try again or choose edit macros from the home page.")
            return                                                  #see above
        else:
            changeState('aMRecord')                           #moves to next state if all checks were passed
            return
    elif state == 'aMRecord':
        recordInput('addMacro')
        changeState('finishAddMacro')
        return
    elif state == 'finishAddMacro':                     #corresponds to an "Activate" button press
        macroLoop()
        #state change to activate macro state needed
        return



def deleteMacro():                          #command to delete a macro from your macros
    global state, btn
    message.set("This command not yet been implemented.")
    if not actionList:                      #checks that there are macros to delete
        message.set("No macros found.")
        return
    if state == 'home':                     #delete macro button on home page clicked
        changeState('startDeleteMacro')   
        return
    elif state == 'startDeleteMacro':       #next button clicked after macro key was prompted
        btn = macroEntry.get()
        if btn == 'no key entered':                 #no key entered
            message.set("No macro key entered. Please try again.")
            return
        elif btn in keyList:                        #macro is ready to delete
            changeState('deleteCheck')
            return
        else:                                       #btn not in keyList
            message.set("No macro found corresponding to that key. Please try again.")
            return
    elif state == 'deleteCheck':
        deleteMacroFromLists(btn)
        changeState('finishDeleteMacro')
        return
    elif state == 'finishDeleteMacro':
        changeState('startDeleteMacro')
        return



def changeMacros():
    global state, btn
    if not actionList:                      #checks if there are macros that exist
        message.set("No macros found.")
        return
    if state == 'home':                     #button was pressed from home screen
        changeState('startChangeMacro')
        return
    elif state == 'startChangeMacro':       #next button after macro key prompt pressed
        btn = macroEntry.get()
        if btn == 'no key entered':         #checks if a key was put into the entry
            message.set("No macro key entered. Please try again.")
            return
        elif btn in keyList:                #checks that the button is used in a macro
            changeState('cMRecord')         #continues the function to the next state
            return
        else:                               #key wasn't found in the key list
            message.set("No macro found corresponding to that key. Please try again.")
            return
    elif state == 'cMRecord':               #record button pressed
        recordInput('changeMacros')
        changeState('finishChangeMacro')
        return
    elif state == 'finishChangeMacro':      #activate button pressed
        macroLoop()
        return
    else:                                   #unrecognized or no state given
        message.set("Something went wrong. Please try again.")




def viewMacros():
    global state
    if not actionList:
        message.set("No macros found.")
        return
    else:
        changeState('macroView')
        return



def macroLoop():
    message.set("Macros are now activated. Press any of your macro keys to perform their corresponding action or esc to deactivate your macros.")
    currKey = ''
    while currKey != 'esc':
        currKey = keyboard.read_key(suppress = True)                #reads the key being pressed. Does not give that key to any programs
        keySet = set(keyList)                                       #set lookups are more efficient than list lookups
        if currKey in keySet:
            index = keyList.index(currKey)                          #need list index in order to match to the action
            action = actionList[index]                              #gets the corresponding action
            keyboard.play(action, speed_factor=5)                   #plays the corresponding action at 5 times the speed it was aMRecorded
        else:
            keyboard.press(currKey)                                 #presses the key that the user pressed if it is not any of the macros
            if keyboard.read_key(suppress = False) != currKey:      #checks if the user is still pressing the key
                keyboard.release(currKey)                           #releases the non-macro key the user pressed when the user presses a different key
                currKey = keyboard.read_key(suppress = True)        #marks the new key as the current key in case it is esc
    message.set("Macros deactivated.")



def saveMacros(exit):     #exits macrion and writes the macro keys and corresponding actions to a file.     
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
    if exit == True:
        sys.exit("Program exiting now. Thank you for using Macrion!")



#_________________________________________________GUI Initialization/main function_______________________________________________________



getMacrosFromFiles()                    #reads in macros from previous session into current session (only works when the user exits using save & exit atm)

tk = Tk()
tk.title("Macriona")
#style configurations for window colors/fonts/etc.
s = ttk.Style()
s.configure('TFrame', background = 'white')                                                   #makes the frame background white
s.configure('TLabel', background = 'white')                                                   #makes the button borders white
frame = ttk.Frame(tk,padding = "3 3 12 12")                                                 #frame for widgets (not sure what the padding does)
frame.grid(column = 0, row = 0, sticky = (N, W, E, S))                                      #places the frame
#column and row configures should allow for resizing when window size changes   TODO: figure out how this works
for t in range(0,19):
    tk.columnconfigure(t, weight = 1)
for u in range(0,3):
    tk.rowconfigure(u, weight = 1)
#string variables for changing labels
macroKey = StringVar()                                                                      #stringvar to hold the macro key
macroResponse = StringVar()                                                                 #stringvar to hold the macro response
message = StringVar()                                                                       #stringvar to hold the message to be displayed
buttonLabel = StringVar()                                                                   #stringvar to hold the label of the next button
#fonts to be used
messageFont = font.Font(family = 'Book Antiqua', size = 14, weight = 'bold')                  #font for header messages
subMessageFont = font.Font(family = 'Book Antiqua', size = 13, weight = 'normal')             #font for non-header messages
smallFont = font.Font(family = 'Book Antiqua', size = 12, weight = 'normal')
#entry for macro key
macroEntry = ttk.Entry(frame, width = 1, textvariable = macroKey, font = subMessageFont)
#labels to relay information to user
macroLabel = ttk.Label(frame, font = subMessageFont)                                          #label to hold the macro key to be used
recordingLabel = ttk.Label(frame, textvariable = macroResponse,font = subMessageFont)           #label to hold the recording to be displayed
messageLabel = ttk.Label(frame, textvariable = message, font = messageFont)                     #label to display header messages to the user                           
macrKeyLabel = ttk.Label(frame, text = "Macro key:", font = smallFont)                     #label to present the macro key to the user
responseLabel = ttk.Label(frame, text = "Response:", font = smallFont)                     #label to present the macro response to the user
#Buttons for user to press
addMacroButton = ttk.Button(frame, text = "Add Macro", command = addMacro)                      #home button for addMacro
deleteMacroButton = ttk.Button(frame, text = "Delete Macro", command = deleteMacro)             #home button for deleteMacro
editMacroButton = ttk.Button(frame, text = "Edit Macro", command = changeMacros)                #home button for changeMacros
viewMacrosButton = ttk.Button(frame, text = "View Macros", command = viewMacros)                #home button for viewMacros
activateMacroButton = ttk.Button(frame, text = "Activate Macros", command = macroLoop)          #home button for macroLoop
saveExitButton = ttk.Button(frame, text = "Save & Exit", command = lambda: saveMacros(True))                 #home button for exitMacrion
nextButton = ttk.Button(frame, textvariable = buttonLabel, command = addMacro)                  #next button used in most functions
cancelButton = ttk.Button(frame, text = 'Cancel',command = lambda: changeState('home'))        #cancel button used to go home
#initialization
changeState('home')                                                                         #starts at the home page
tk.mainloop()
