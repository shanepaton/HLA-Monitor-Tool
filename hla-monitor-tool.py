#
import os
from shutil import copyfile
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
import configparser

config = configparser.ConfigParser()

if not os.path.exists('config.ini'):
    config['CONFIG'] = {'alyxDirectory': '', 'replacementVideo': ''}
    config.write(open('config.ini', 'w'))
else:
    config.read('config.ini')
    print(config['CONFIG']['alyxDirectory'])

# create the root window
root = tk.Tk()
root.title('HLA Monitor Tool')
root.resizable(False, False)
root.geometry('720x480')
root['bg']='#37474f'

photo = PhotoImage(file="./logo.png")
root.iconphoto(False, photo)
root.iconbitmap('./logo.png')

style = ttk.Style()

alyxFolder= config['CONFIG']['alyxDirectory']
replacementVideo=config['CONFIG']['replacementVideo']


alyxDirLabel = Label(root, text=alyxFolder, state='normal', borderwidth=0, bg="#37474f", fg="white")
replacementLabel = Label(root, text=replacementVideo, state='normal', borderwidth=0, bg="#37474f", fg="white")

def getAlyxDirectory():
    global alyxFolder
    alyxFolder = fd.askdirectory()
    config['CONFIG']['alyxDirectory'] = alyxFolder
    with open('config.ini', 'w') as configfile:    # save
        config.write(configfile)
    alyxDirLabel.config(text = alyxFolder)



def selectReplacement():
    global replacementVideo
    filetypes = (
        ('WEBM Files', '*.webm'),
        ('All files', '*.*')
    )

    replacementVideo = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    config['CONFIG']['replacementVideo'] = replacementVideo
    replacementLabel.config(text = replacementVideo)

replacementLabel.pack(side=BOTTOM)
alyxDirLabel.pack(side=BOTTOM)


def updateVideo():
    if not alyxFolder:
        showerror(
            title='Error',
            message="Error: HLA Directory not selected"
        )

    elif not replacementVideo:
        showerror(
            title='Error',
            message="Error: Replacement video not selected"
        )

    else:
        try:
            if(os.path.exists(alyxFolder + "/game/hlvr/panorama/videos/intro_world_heist.webm")):
                os.remove(alyxFolder + "/game/hlvr/panorama/videos/intro_world_heist.webm")        

            copyfile(replacementVideo, alyxFolder + "/game/hlvr/panorama/videos/intro_world_heist.webm")

            showinfo(
                title='Success',
                message="Successfuly replaced the video."
            )
        except Exception as e:
            showerror(
                title='Error',
                message= str(e)
            )


rightFrame = Frame(root)
rightFrame['bg']='#37474f'

buttonFrame = Frame(rightFrame)
buttonFrame['bg']='#37474f'

programLabel = Label(rightFrame, text="HLA Monitor Tool", state='normal', borderwidth=0, bg="#37474f", fg="white")


# open button
gameFolderButton = Button(buttonFrame,text="Alyx Folder", command=getAlyxDirectory, bg="#263238", fg="white", border=0, padx=5,pady=5)
replacementVideoButton = Button(buttonFrame,text="Replacement Video", command=selectReplacement, bg="#263238", fg="white", border=0, padx=5,pady=5)
updateVideoButton = Button(buttonFrame,text="Update Video", command=updateVideo, bg="#263238", fg="white", border=0, padx=5,pady=5)

programLabel.pack(side=TOP, expand=YES)
rightFrame.pack(side=RIGHT, expand=YES)
buttonFrame.pack(side=RIGHT, expand=YES)

gameFolderButton.pack(side=LEFT, expand=YES, padx=10,pady=10)
replacementVideoButton.pack(side=LEFT, expand=YES, padx=10,pady=10)
updateVideoButton.pack(side=LEFT, expand=YES, padx=10,pady=10)

# run the application
root.mainloop()