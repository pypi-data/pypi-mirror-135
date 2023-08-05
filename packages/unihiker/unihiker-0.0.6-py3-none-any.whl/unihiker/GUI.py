from threading import Thread
import tkinter as tk
from tkinter import ttk
from time import sleep
from PIL import Image, ImageTk

class GUI():

    masterGlobal = None
    master = None
    
    def __init__(self):
        def mainloopThread():
            GUI.masterGlobal = tk.Tk()
            style = ttk.Style(GUI.masterGlobal)
            style.configure('.', font=('HYQiHei', 11))
            GUI.masterGlobal.geometry('240x320')
            GUI.masterGlobal.resizable(0, 0)
            GUI.masterGlobal.mainloop()
        
        if GUI.thd is not None:
            raise Exception("Can only create single GUI instance!")
            return
        GUI.thd = Thread(target=mainloopThread)   # gui thread
        GUI.thd.daemon = True  # background thread will exit if main thread exits
        GUI.thd.start()  # start tk loop
        while GUI.masterGlobal is None:
            sleep(0.01)
        self.master = GUI.masterGlobal
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill='both', expand=1)

        self.canvas = tk.Canvas(self.frame, bd=0, highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)

        def checkAlive():
            self.master.after(500, checkAlive)
        checkAlive()

    def drawText(self, x, y, **kw):
        fontsize = kw.pop('fontsize', None)
        command = kw.pop('command', None)

        font = kw.get('font', None)
        anchor = kw.get('anchor', None)

        if font is None:
            kw['font'] = ('HYQiHei', 14) if fontsize is None else ('HYQiHei', fontsize)

        if anchor is None:
            kw['anchor'] = 'nw'

        id = self.canvas.create_text(x, y, **kw)

        if command is not None:
            self.canvas.tag_bind(id, '<Button-1>', lambda event: command())
        return id
    
    def updateText(self, id, **kw):
        self.canvas.itemconfigure(id, **kw)
        return id

    cacheImageBufs = []
    def cacheImage(self, id, imagetk):
        for cacheImageBuf in self.cacheImageBufs:
            if cacheImageBuf[0] == id:
                cacheImageBuf[1] = imagetk
        else:
            self.cacheImageBufs.append([id, imagetk])

    def drawImage(self, x, y, **kw):
        command = kw.pop('command', None)

        anchor = kw.get('anchor', None)
        image = kw.get('image', None)
        if anchor is None:
            kw['anchor'] = 'nw'
        
        if image is None:
            raise Exception('Image path is needed')
            return 0
        else:
            kw['image'] = ImageTk.PhotoImage(image)
            id = self.canvas.create_image(x, y, **kw)  
            if command is not None:
                self.canvas.tag_bind(id, '<Button-1>', lambda event: command())
            self.cacheImage(id, kw['image'])
            return id
    
    def updateImage(self, id, **kw):
        command = kw.pop('command', None)

        anchor = kw.get('anchor', None)
        image = kw.get('image', None)
        if anchor is None:
            kw['anchor'] = 'nw'
        
        if image is None:
            raise Exception('Pillow Image is needed')
            return 0
        else:
            kw['image'] = ImageTk.PhotoImage(image)
            self.canvas.itemconfigure(id, **kw)
            if command is not None:
                self.canvas.tag_bind(id, '<Button-1>', lambda event: command())
            self.cacheImage(id, kw['image'])
            return id
    
    def drawLine(self, x1, y1, x2, y2, **kw):
        return self.canvas.create_line(x1, y1, x2, y2, **kw)

    def addButton(self, x, y, w, h, **kw):
        style = kw.get('style', None)
        if style is None:
            kw['style'] = 'TButton'
        object = ttk.Button(self.canvas, **kw)
        object.place(x=x, y=y, width=w, height=h)
        return object
    
    def updateButton(self, object, **kw):
        object.configure(**kw)
        
    def remove(self, object):
        if isinstance(object, int):
            self.canvas.delete(object)
        else:
            object.place_forget()
            object.destroy()
    
    def startLoop(self, callback):
        def loop():
            while True:
                callback()
        loopThread = Thread(target=loop)
        loopThread.daemon = True
        loopThread.start()
        return loopThread

GUI.thd = None