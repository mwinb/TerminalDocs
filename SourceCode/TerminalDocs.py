#Created by Michael Winberry Feb 5 2017
#Version Created Sep 22 2017
#Terminal Docs Work station and Line by Line editor
#For education and personal use only
 
import os
import sys
import platform
import subprocess
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
 
def main():
    clear()
    
    if(len(sys.argv)-1 >= 1):
        checkPath = sys.argv[1]
        del sys.argv[1]
 
    #If there is no path passed the path is set to current working directory
    else:
        checkPath = os.getcwd()
        
    #checks if path is an existing file
    #Uses path as document. Fills array and begins "writer" function
 
    if(os.path.isfile(checkPath)):
        path = str(os.path.abspath(checkPath))
        swapPath = path + "-swap"
        lines = fillArray(path)
        save(swapPath,lines)
        position = 0
        saveState = writer(swapPath,path,lines,0,position)
 
    elif(os.path.isdir(checkPath) == False):
        path = str(os.path.abspath(checkPath))
        cNewCmd(path)
        swapPath = path + "-swap"
        lines = fillArray(path)
        save(swapPath,lines)
        position = 0
 
    else:
        
        path = mainMenu()
        swapPath = path + "-swap"
        lines = fillArray(path)
        save(swapPath,lines)
        position = 0
 
    saveState = writer(swapPath,path,lines,0,position)

    swapPath = saveState[1]
 
    if (saveState[0] == True):
        deleteSwap(swapPath)
    else:
        lines = fillArray(swapPath)
        save(path,lines)
        deleteSwap(swapPath)
        
    raise SystemExit
    
def writer(swapPath,path,lines,start,position):
    killSwitch = 0
    copy = ""
    undoStack = []
    redoStack = []
    undoStack = fillArray(path)
    redoStack = fillArray(path)
 
    while(killSwitch == 0):
        clear()
        save(path,lines)
        lines = fillArray(path)
        print path
        print "Help Menu (-h)"
        if(lines == []):
            with open(path,'w+') as f:
                f.write(str(raw_input("0: ")) + "\n")
            lines = fillArray(path)
            start = 0
            position = 1
            clear()
            print path
            print "Help Menu (-h)"
        if(start < 0):
            start = 0;
        count = start
        
        if(position > len(lines)-1):
            position = 0
        
        while( count <= position):
            print str(count) + ": " + lines[count]
            count += 1
        inp = raw_input(str(position+1) + ": ")
            
        parameters = executeCommand(swapPath,path,lines,position,inp,copy,undoStack,redoStack)
        killSwitch = parameters[0]
        swapPath = parameters[1]
        path = parameters[2]
        lines = parameters[3]
        start = parameters[4]
        position = parameters[5]
        copy = parameters[6]
        undoStack = parameters[7]
        redoStack = parameters[8]
        
    killSwitch = 0
    
    while(killSwitch == 0):
        inp = raw_input("Save? (y/n) ")
        if (inp == "y"):
            saveState = True
            killSwitch = 1
        elif (inp == "n"):
            saveState = False
            killSwitch = 1 
        else:
            print "-----Invalid Entry-----"
            
    parameters = [saveState,swapPath]
    return parameters
        
def executeCommand(swapPath,path,lines,position,inp,copy,undoStack,redoStack):
    if(str(inp) == "-pst"):
        inp = copy
    if(str(inp) == "-q"):
        clear()
        return [1,swapPath,path,lines,0,position,copy,undoStack,redoStack]
    
    elif(str(inp)=="-h"):
        clear()
        print "-------------------------------------------"
        print "-| Write Text and Hit Enter to Insert    |-"
        print "-| Your Text on the Line Shown on the    |-"
        print "-| Bottom Left Corner of the Terminal    |-"
        print "-------------------------------------------"
        print "-| Hit Enter At Any Time While the Input |-"
        print "-| Line is Empty to View Next Line       |-"
        print "-------------------------------------------"
        print "-| -q       |Quit Program / oneLine Mode  -"
        print "-------------------------------------------"
        print "-| -run     |Takes a Terminal/CMD Command -"
        print "-------------------------------------------"
        print "-| -o       |Opens in Default Program     -"
        print "-------------------------------------------"
        print "-| -b       |Moves to Previous Line       -"
        print "-------------------------------------------"
        print "-| -g       |Goes to Specified Line       -"
        print "-------------------------------------------"
        print "-| -ps      |Prints Selection, Insert     -"
        print "-|          |Starts at End of Selection   -"
        print "-------------------------------------------"
        print "-| -rs      |Replaces Selection One Line -"
        print "-|          |At a Time                    -"
        print "-------------------------------------------"
        print "-| -ds      |Deletes Selection            -"
        print "-------------------------------------------"
        print "-| -vs      |View Selection Without Lines -"
        print "-------------------------------------------"
        print "-| -dcl     |Deletes Current Line         -"
        print "-------------------------------------------"
        print "-| -del     |Deletes Specified Line       -"
        print "-------------------------------------------"
        print "-| -rcl     |Replaces Current Line        -"
        print "-------------------------------------------"
        print "-| -rep     |Replaces Specified Line      -"
        print "-------------------------------------------"
        print "-| -exp     |Exports Current File to New  -"
        print "-------------------------------------------"
        print "-| -end     |Jump to End                  -"
        print "-------------------------------------------"
        print "-| -begin   |Jump to Beginning            -"
        print "-------------------------------------------"
        print "-| -vl      |View Whole Doc With Line #'s -"
        print "-------------------------------------------"
        print "-| -v       |View Without Line #'s        -"
        print "-------------------------------------------"
        print "-| -ud      |Undo Last Change             -"
        print "-------------------------------------------"
        print "-| -rd      |Redo Last Change             -"
        print "-------------------------------------------"
        print "-| -cp      |Store Text for Insert        -"
        print "-------------------------------------------"
        print "-| -cs      |Store Selection for Insert   -"
        print "-------------------------------------------"
        print "-| -ccl     |Copy Current Line for Insert -"
        print "-------------------------------------------"
        print "-| -pst     |Paste to Current Line        -"
        print "-------------------------------------------"
        print "-| -oe      |Opens New Program in Default -"
        print "-|          |Environment                  -"
        print "-------------------------------------------"

        
        raw_input("Continue? (Hit Enter) ")
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "-cp"):
        copy = str(raw_input("Store Input: "))
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
   
    elif(str(inp) == "-ccl"):
        copy = str(lines[position])
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "-cs"):
        try:
            start = int(raw_input("Enter Starting Line: "))
            end = int(raw_input("Enter Ending Line: "))
            tempCount = start
            copy = ""
            if (end > (len(lines)-1)):
                raise Exception
            if (start < 0):
                raise Exception
            while(tempCount <= end):
                copy += str(lines[count])
                tempCount +=1
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        except Exception:
            print "----Invalid Selection----"
            print "---- No Changes Made ----"
            raw_input("Continue? (Hit Enter) ")
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "-ud"):
        redoStack = fillArray(path)
        save(path,undoStack)
        lines = fillArray(path)
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
 
    elif(str(inp) == "-rd"):
        undoStack = fillArray(path)
        save(path,redoStack)
        lines = fillArray(path)
        position += 1
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        

    elif(str(inp) == "-vl"):
        clear()
        for i in range(len(lines)-1):
            print str(i) + ": " + lines[i]
            if (i % 100 == 0 and i != 0):
                inp = raw_input("Continue? (n) ")
                if (str(inp) == "n"):
                    return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]

        raw_input("Continue? (Hit Enter) ")
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]

    elif(str(inp)== "-v"):
        clear()
        for i in range(len(lines)-1):
            print lines[i]
            if (i % 100 == 0 and i != 0):
                inp = raw_input("Continue? (n) ")
                if (str(inp) == "n"):
                    return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        raw_input("Continue? (Hit Enter) ")
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp)=="-vs"):
        try:
            start = int(raw_input("Enter Starting Line: "))
            end   = int(raw_input("Enter Ending Line:   "))
            clear()
            while (start <= end):
                print lines[count]
                start += 1
            raw_input("Continue? (Hit Enter) ")
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        except Exception:
            print "----Invalid Entry----"
            raw_input("Continue? (Hit Enter) ")
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp)=="-o"):
        clear()
        programOpen(path)
        continueInp = raw_input("Continue? (q) to Quit: ")
        if(continueInp == "q"):
            return [1,swapPath,path,lines,position-20,position,undoStack,redoStack]
        else:
            lines = fillArray(path)
            save(path,lines)
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "-end"):
        return [0,swapPath,path,lines,len(lines)-20,len(lines)-1,copy,undoStack,redoStack]
    
    elif(str(inp) == "-begin"):
        return [0,swapPath,path,lines,0,0,copy,undoStack,redoStack]
    
    elif(str(inp) == "-ps"):
        try:
            start = int(raw_input("Enter Starting Line: "))
            end = int(raw_input("Enter Ending Line: "))
            return [0,swapPath,path,lines,start,end,copy,undoStack,redoStack]
        except Exception:
            print "----Invalid Entry----"
            raw_input("Continue? (Hit Enter) ")
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
 
    elif(str(inp) == "-rs"):
        try:
            start = int(raw_input("Enter Starting Line: "))
            tempCount = start
            end = int(raw_input("Enter Ending Line: "))
            clear()
            undoStack = fillArray(path)
            while(tempCount <= end):
                print("Replace? (n) to Return without Changes")
                print str(tempCount) + ": " + lines[tempCount]
                inp = raw_input(str(tempCount) + ": ")
                if (str(inp) != "n"):
                    lines[tempCount] = str(inp) + '\n'
                    tempCount += 1
                    save(path,lines)
                else:
                    tempCount += 1
            return [0,swapPath,path,lines,end-20,end,copy,undoStack,redoStack]
        except Exception:
            print "----Invalid Entry-----"
            raw_input("Continue? (Hit Enter) ")
            undoStack = fillArray(path)
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
 
    elif(str(inp) == "-rep"):
        try:
            selection = int(raw_input("Enter Line # to Replace: "))
            print(str(selection) + ": " + lines[selection])
            inp = raw_input(str(selection) + ": ")
            if(inp != ""):
                undoStack = fillArray(path)
                lines[selection] = str(inp) + '\n'
                save(path,lines)
                return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
            else:
                inp2 = raw_input("Delete? (y) ")
                if(inp2 == "y"):
                    del lines[selection]
                    undoStack = fillArray(path)
                    save(path,lines)
                    undoStack = fillArray(path)
                    return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
                else:
                    print "----No Changes Made----"
                    raw_input("Continue? (Hit Enter) ")
                    return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        except Exception:
            print "----No Changes Made----"
            raw_input("Continue? (Hit Enter) ")
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "-rcl"):
        print(str(position) + ": " + lines[position])
        inp = raw_input(str(position) + ": ")
        if(inp != ""):
            undoStack = fillArray(path)
            lines[position] = str(inp) + '\n'
            save(path,lines)
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        else:
            inp2 = raw_input("Delete? (y) ")
            if(inp2 == "y"):
                undoStack = fillArray(path)
                del lines[position]
                save(path,lines)
                return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
            else:
                print "----No Changes Made----"
                raw_input("Continue? (Hit Enter) ")
                return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "-del"):
        try:
            inp = int(raw_input("Line Number: "))
            print(str(inp) + ": " + lines[inp])
            inp2 = raw_input("Delete? (y) ")
            if (inp2 == "y"):
                undoStack = fillArray(path)
                del lines[inp]
                save(path, lines)
                return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
            else:
                print "----No Changes Made----"
                raw_input("Continue? (Hit Enter) ")
                return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        except Exception:
            print "----Invalid Entry----"
            raw_input("Continue? (Hit Enter) ")
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "-ds"):
        try:
            start = int(raw_input("Enter Starting Line: "))
            end = int(raw_input("Enter Ending Line: "))
            tempCount = start
            if (end > (len(lines)-1)):
                raise Exception
            if (start < 0):
                raise Exception
            undoStack = fillArray(path)
            
            while(tempCount <= end):
                del lines[start]
                tempCount += 1
            save(path,lines)
            if(position > (len(lines)-1)):
                return [0,swapPath,path,lines,len(lines)-20,len(lines)-1,copy,undoStack,redoStack]
            else:
                return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        except Exception:
            print "----Invalid Selection----"
            print "---- No Changes Made ----"
            raw_input("Continue? (Hit Enter) ")
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp)=="-dcl"):
        print str(position) + ": " + lines[position]
        undoStack = fillArray(path)
        del lines[position]
        save(path,lines)
        if(position > len(lines)-1):
            position = (len(lines)-1)
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp)=="-b"):
        if(position == 0):
            position = len(lines) -1
        else:
            position = position - 1
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]

    elif(str(inp) == "-g"):
        try:
            inp = raw_input("Enter Line Number: ")
            position = goTo(inp,position)
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
        except Except:
            print "----Invalid Input----"
            raw_input("Continue? (Hit Enter) ")
            return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]

    elif(str(inp) == "-exp"):
        expPath = exp(lines)
        inp = raw_input("Open New? (y) ")
        if (inp == "y"):
            deleteSwap(swapPath)
            undoStack = []
            redoStack = []
            save(path,lines)
            lines = fillArray(expPath)
            swapPath = expPath + "-swap"
            save(swapPath,lines)
            return [0,swapPath,path,lines,0,position,copy,undoStack,redoStack]
        else:
            return [0,swapPath,path,lines,0,position,copy,undoStack,redoStack]
    
    
    elif(str(inp) == "-run"):
        killSwitch = 0
        while(killSwitch == 0):
            run()
            inp = raw_input("Continue? y/n")
            if(inp == 'n'):
                clear()
                killSwitch = 1
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
 
    elif(str(inp) == "-oe"):
        path2 = openPath()
        programOpen(path2)
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]

    elif(position == len(lines)-1 and str(inp) != ""):
        undoStack = fillArray(path)
        lines.append(str(inp) + '\n')
        save(path,lines)
        position +=1
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(position < len(lines) and str(inp) != ""):
        undoStack = fillArray(path)
        lines.insert(position+1, str(inp) + '\n')
        save(path,lines)
        position +=1
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "" and position < (len(lines)-1)):
        position +=1
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    
    elif(str(inp) == "" and position == (len(lines)-1)):
        position = 0
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
    else:
        return [0,swapPath,path,lines,position-20,position,copy,undoStack,redoStack]
       
def deleteSwap(path):
    os.remove(path)
    return
 
def mainMenu():
    print "--------------------------------------"
    print "-      Welcome to Terminal Docs      -"
    print "--------------------------------------"
    print "-By Michael Winberry                 -"
    print "--------------------------------------"
    print "-mwinb.github.io                     -"
    print "--------------------------------------"
    print "-mwinberry0101@gmail.com             -"
    print "--------------------------------------"
    print "-                                    -"
    print "--------------------------------------"
    print "-Hit Enter to Open File,             -"
    print "--------------------------------------"
    print "-Enter '-cnew' to Create New File,   -"
    print "--------------------------------------"
    print "-Or Enter '-h' for Help Menu         -"
    print "--------------------------------------"

    killSwitch = False
    while(killSwitch == False):
        inp = raw_input("-")

        if (inp == "-q"):
            raise SystemExit
        elif (inp == "-h"):
            clear()
            print "------------------------------------------"
            print "-| Hit Enter to Open Fle Path            -"
            print "------------------------------------------"
            print "-| -q      |Quit Program                 -"
            print "------------------------------------------"
            print "-| -cnew   |Opens Directory Chooser and  -"
            print "-          |Allows User to Create a New  -"
            print "-          |File.                        -"
            print "------------------------------------------"
            print "-| -run    |Takes a Terminal/CMD Command -"
            print "------------------------------------------"
            print "-| -op     |Takes Path to Open File      -"
            print "------------------------------------------"
            inp = raw_input("Continue? (Hit Enter):")
        elif (inp == "-cnew"):
            path = cNew()
            killSwitch = True
        elif (inp == "-run"):
            run()
        elif (inp == "-op"):
            path = getPath()
            killSwitch = True
        else:
            path = openPath()
            killSwitch = True
    return path
    
def getPath():
    try:
        path = raw_input("Enter Path w/ Extension: ")
        if(os.path.isfile(path)):
            return path
        else:
            raise Exception
    except Exception:
        print "----Invalide File Path----"
        raw_input("Continue? (Hit Enter) ")
        main()
        
def openPath():
    try:
        root = Tk()
        root.update()
        root.withdraw()
        path = askopenfilename()
        if(os.path.isfile(path)):
            return path
        else:
            raise Exception
    except Exception:
        print "----Invalid File Type----"
        raw_input("Continue? (Hit Enter) ")
        main()
 
def cNew():
    try:
        root = Tk()
        root.update()
        root.withdraw()
        path = askdirectory()
        fName = raw_input("Enter name with desired ext: ")
        nPath = str(path) + '/' + str(fName)
        with open(nPath, 'w+') as f:
            f.write(" " + '\n')
        return nPath
    except Exception:
        print "----Invalid Option----"
        raw_input("Continue? (Hit Enter) ")
        main()
    
def cNewCmd(path):
    with open(path, 'w+') as f:
        f.write(" " + '\n')
    return path

def fillArray(path):
    try:
        lines = []
        with open(path, 'r+') as f:
            for line in f.readlines():
                lines.append(line)
        return lines
    except Exception:
        print("----File Does Not Exist----")
        raw_input("Continue? (Hit Enter) ")
        main()
 

def goTo(newPos, oldPos):
    try:
        position = int(newPos)
        return position
    except Exception:
        print "----Invalid Entry----"
        print "----Returning to Last Position-----"
        raw_input("Continue? (Hit Enter) ")
        return oldPos

def exp(lines):
    try:
        root = Tk()
        root.update()
        root.withdraw()
        newPath = askdirectory()
        fName = raw_input("Enter Name with Desired Extension: ")
        newPath = str(newPath) + "/" + str(fName)
        with open(newPath, 'w+') as f:
            for i in range(len(lines)):
                f.write(str(lines[i]))
        return newPath
    except Exception:
        print "----Invalid File----"
        raw_input("Continue? (Hit Enter) ")
        return
    
 
def save(path,lines):
    with open(path, 'w+') as f:
        for i in range(len(lines)):
            f.write(str(lines[i]))
    return
            
def programOpen(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Linux":
        subprocess.Popen(["xdg-open", path])
    else:
        subprocess.Popen(["open", path])
    return
 
def run():
    try:
        cmd = raw_input("Enter Command to run in Terminal / CMD Prompt: ")
        os.system(str(cmd))
        return
    except Exception:
        print "----Invalid Command----"
        raw_input("Continue? (Hit Enter) ")
        return

def clear():
    for i in range(100):
        print "\n"
    return
        
main()
 
