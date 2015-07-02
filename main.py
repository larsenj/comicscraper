#!/user/bin/python3

import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import PIL.Image
import PIL.ImageTk
from tkinter import*

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Comics")
        self.pack(fill=BOTH, expand=1)

        '''
        tkinter is weird - to have scrollbars you need them in the frame, then
        another canvas in the frame that has it's own frame with a window
        '''
        canvas = Canvas(self)
        frame = Frame(canvas)
        vscroll = Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        vscroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand="true")
        frame_id = canvas.create_window((0, 0), window=frame, anchor='nw')

        #these two function resize everything when the user resizes the window
        def config_frame(event):
            size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=frame.winfo_reqwidth())
        frame.bind("<Configure>", config_frame)

        def config_canv(event):
            if frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(frame_id, width=canvas.winfo_width())
        canvas.bind("<Configure>", config_canv)

        #allows the scrollwheel to function. Note the need for round.
        def on_mousewheel(event):
            canvas.yview_scroll(round(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        '''
        XKCD
        '''
        #find the URL for the current XKCD comic
        req = Request('http://xkcd.com', headers={'User-Agent':'Mozilla/5.0'})
        xkcdURL = urllib.request.urlopen(req).read()
        xkcdSoup = BeautifulSoup(xkcdURL)
        xkcdDiv = xkcdSoup.find('div', attrs={'id':'comic'})
        xkcdImg = xkcdDiv.find('img')['src']

        #download the comic to the same folder as this file
        urllib.request.urlretrieve("http:" + xkcdImg, "xkcd")

        #load the file into a label and place it in the frame within the canvas
        xkcdLoad = PIL.Image.open("xkcd")
        xkcdRender = PIL.ImageTk.PhotoImage(xkcdLoad)
        ximg = Label(frame, image=xkcdRender)
        ximg.image = xkcdRender
        ximg.grid(row=1, column=0)

root = Tk()
root.geometry("800x200")
app = Window(root)
root.mainloop()