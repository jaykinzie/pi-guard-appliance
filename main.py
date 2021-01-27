import tkinter as tk
from tkinter import messagebox
from tkinter import *

import qrcode
import numpy as np
import image
from PIL import Image, ImageTk

import string
import random
import os, shutil

class main_ui():
    def __init__(self):

        # empty out the qr code directory
        self.clean_qr_directory()
        # create a qr code and then safe the location
        self.qr_code = self.update_qr()
        # create the canvas
        self.canvas = Canvas(root, width=216, height=216)
        self.img = PhotoImage(file=self.qr_code)
        self.imgArea = self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.canvas.pack()

        # button to generate new qr codes
        self.generate_qr_button = Button(root, text="Generate Qr Code", command=lambda: self.changeImg())
        self.generate_qr_button.place(x=0, y=264)

        # close button
        self.close_button = Button(root, text="close", command=lambda: self.close())
        self.close_button.place(x=300, y=264)

    # cleans out the qr_code directory
    def clean_qr_directory(self):
        folder = 'qr_codes'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    # updates the current qr code
    def update_qr(self):

        self.clean_qr_directory()

        # data to encode
        data = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.qr_code = "qr_codes/" + data + ".png"
        print(data)
        # instantiate QRCode object
        qr = qrcode.QRCode(version=1, box_size=10, border=1)
        # add data to the QR code
        qr.add_data(data)
        # compile the data into a QR code array
        qr.make()
        # print the image shape
        print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
        # transfer the array into an actual image
        img = qr.make_image(fill_color="black", back_color="white")
        # save it to a file
        if os.path.exists(self.qr_code):
            os.remove(self.qr_code)
        img.save(self.qr_code)
        # update the image
        self.img = PhotoImage(file=self.qr_code)
        # return the location of the qr code
        return self.qr_code


    def changeImg(self):
        self.qr_code = self.update_qr()
        print(self.qr_code)
        self.img = PhotoImage(file=self.qr_code)
        self.canvas.itemconfig(self.imgArea, image=self.img)

    def close(self):
        # clean out the extra qr codes
        self.clean_qr_directory()
        # destroy the root window to end the program
        root.destroy()


# define the main window which is the size of the screen on the pi
root = tk.Tk()
root.title("Pi-Guard-Appliance")
root.geometry("480x320")

app = main_ui()

root.mainloop()
