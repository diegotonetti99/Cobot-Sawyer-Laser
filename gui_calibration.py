from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2



def takePhoto(frame):
    vid = cv2.VideoCapture(1)
    ret, image=vid.read()
    # OpenCV represents images in BGR order; however PIL represents
    # images in RGB order, so we need to swap the channels
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # convert image to PIL image
    image = Image.fromarray(image)
    img = ImageTk.PhotoImage(image)
    panel = Label(frame, image=img)
    panel.image=img
    panel.grid(row=1,column=0)
    vid.release()



def main():
    # create new window    
    root=Tk()
    # create a frame
    frm = ttk.Frame(root, padding=10)
    # set frame as grid
    frm.grid()
    # create button
    start_calibration_btn=ttk.Button(
        frm,
        text='Start calibration',
        command=lambda arg=frm: takePhoto(frm)
    ).grid(row=0,column=0)


    root.mainloop()






if __name__ == '__main__':
    main()