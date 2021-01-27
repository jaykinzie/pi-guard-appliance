import tkinter as tk
from tkinter import messagebox
from tkinter import *

import qrcode
import numpy as np
import image
from PIL import Image, ImageTk

import string
import random
import os
import shutil

import cv2
from pyzbar import pyzbar


class WireGuardInterface():
    def __init__(self):
        # personal private key
        self.interface_public_key = ""
        self.interface_private_key = ""
        self.interface_ip = "000.000.000.000"
        self.interface_listen_port = 00000


class WireGuardPeer():
    def __init__(self):
        # personal private key
        self.peer_public_key = ""
        self.peer_ip = "000.000.000.000"
        self.peer_listen_port = 00000


class MainUi():
    def __init__(self, root):

        self.root = root

        # empty out the qr code directory
        self.clean_qr_directory()
        # create a qr code and then safe the location
        self.qr_code = self.update_qr()
        # create the canvas
        self.canvas = Canvas(root, width=216, height=216)
        self.img = PhotoImage(file=self.qr_code)
        self.imgArea = self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.canvas.place(x=0, y=0)
        # self.canvas.pack()

        # button to generate new qr codes
        self.generate_qr_button = Button(root, text="Generate QR Code", command=lambda: self.change_img())
        self.generate_qr_button.place(x=0, y=264)

        # capture qr button
        self.capture_qr_button = Button(root, text="Capture QR Code", command=lambda: self.capture_qr())
        self.capture_qr_button.place(x=300, y=264)

        # close button
        self.close_button = Button(root, text="close", command=lambda: self.close())
        self.close_button.place(x=430, y=264)

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

    # updates the qr code image
    def change_img(self):
        self.qr_code = self.update_qr()
        print(self.qr_code)
        self.img = PhotoImage(file=self.qr_code)
        self.canvas.itemconfig(self.imgArea, image=self.img)

    # used to capture the qr code
    def capture_qr(self):

        # 1
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        # 2
        while ret:
            ret, frame = camera.read()
            ret, frame = read_barcodes(frame)
            cv2.imshow('Barcode/QR code reader', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        # 3
        camera.release()
        cv2.destroyAllWindows()

    # closes the program
    def close(self):
        # clean out the extra qr codes
        self.clean_qr_directory()
        # destroy the root window to end the program
        self.root.destroy()


# reads the qr code from the frame
def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect  # 1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)  # 3

        with open("qr_codes/barcode_result.txt", mode='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
            # if we find a barcode, return false to stop the loop and the frame
            return False, frame
    # if nothing is found, return true and the frame to keep the while loop running
    return True, frame


def main():
    # define the main window which is the size of the screen on the pi
    root = tk.Tk()
    root.title("Pi-Guard-Appliance")
    root.geometry("480x320")

    # start the main ui
    app = MainUi(root)

    root.mainloop()


if __name__ == '__main__':
    main()
