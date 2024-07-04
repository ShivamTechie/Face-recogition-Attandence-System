import tkinter as tk
import cv2
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from tkinter import messagebox
import os  # Add this line to import the os module
from twilio.rest import Client





window = tk.Tk()

window.title("Attendance System")

window.configure(background='pink')

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

x_cord = 75
y_cord = 20



message = tk.Label(window, text="ATTENDANCE MANAGEMENT PORTAL", bg="pink", fg="black", width=40, height=1,
                   font=('Times New Roman', 35, 'bold underline'))
message.place(x=200, y=20)

lbl = tk.Label(window, text="Enter Your College ID", width=20, height=2, fg="black", bg="Pink",
               font=('Times New Roman', 25, ' bold '))
lbl.place(x=200 - x_cord, y=200 - y_cord)

txt = tk.Entry(window, width=30, bg="white", fg="blue", font=('Times New Roman', 15, ' bold '))
txt.place(x=250 - x_cord, y=300 - y_cord)

lbl2 = tk.Label(window, text="Enter Your Name", width=20, fg="black", bg="pink", height=2,
                font=('Times New Roman', 25, ' bold '))
lbl2.place(x=600 - x_cord, y=200 - y_cord)

txt2 = tk.Entry(window, width=30, bg="white", fg="blue", font=('Times New Roman', 15, ' bold '))
txt2.place(x=650 - x_cord, y=300 - y_cord)

lbl3 = tk.Label(window, text="NOTIFICATION", width=20, fg="black", bg="pink", height=2,
                font=('Times New Roman', 25, ' bold '))
lbl3.place(x=1060 - x_cord, y=200 - y_cord)

message = tk.Label(window, text="", bg="white", fg="blue", width=30, height=1, activebackground="white",
                   font=('Times New Roman', 15, ' bold '))
message.place(x=1075 - x_cord, y=300 - y_cord)

lbl3 = tk.Label(window, text="ATTENDANCE", width=20, fg="white", bg="lightgreen", height=2,
                font=('Times New Roman', 30, ' bold '))
lbl3.place(x=120, y=570 - y_cord)

message2 = tk.Label(window, text="", fg="red", bg="yellow", activeforeground="green", width=60, height=4,
                    font=('times', 15, ' bold '))
message2.place(x=700, y=570 - y_cord)

lbl4 = tk.Label(window, text="STEP 1", width=20, fg="green", bg="pink", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl4.place(x=240 - x_cord, y=375 - y_cord)

lbl5 = tk.Label(window, text="STEP 2", width=20, fg="green", bg="pink", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl5.place(x=645 - x_cord, y=375 - y_cord)

lbl6 = tk.Label(window, text="STEP 3", width=20, fg="green", bg="pink", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl6.place(x=1100 - x_cord, y=362 - y_cord)


def clear1():
    txt.delete(0, 'end')
    message.configure(text="")


def clear2():
    txt2.delete(0, 'end')
    message.configure(text="")


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def TakeImages():
    Id = txt.get()
    name = txt2.get()
    # Check if ID is already in the CSV file
    with open('StudentDetails\\StudentDetails.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row and len(row) > 0 and Id == row[0]:  # Check if row is not empty and has elements
                message.configure(text="ID already exists. Please enter a different ID.")
                return  # Exit the function if ID already exists

    if not Id:
        message.configure(text="Please enter ID")
        messagebox.askquestion("Warning", "Please enter roll number properly, press 'Yes' if you understood")
    elif not name:
        message.configure(text="Please enter Name")
        messagebox.askquestion("Warning", "Please enter your name properly, press 'Yes' if you understood")
    elif is_number(Id) and name.isalpha():
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        max_images = 50 # Maximum number of images to capture
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                cv2.imwrite("TrainingImage\\" + name + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('frame', img)
                if sampleNum >= max_images:  # Break the loop after capturing max_images
                    break
            if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= max_images:
                break
        cam.release()
        cv2.destroyAllWindows()
        message.configure(text=f"{min(sampleNum, max_images)} Images Saved for ID: {Id} Name: {name}")
        row = [Id, name]
        with open('StudentDetails\\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
    else:
        if is_number(Id):
            message.configure(text="Enter Alphabetical Name")
        if name.isalpha():
            message.configure(text="Enter Numeric ID")



def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\\Trainner.yml")
    message.configure(text="Image Trained")
    clear1()
    clear2()
    messagebox.showinfo('Completed', 'Your model has been trained successfully!!')


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel\\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails\\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    
    # Check if today's attendance file exists
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    attendance_file = f"Attendance\\Attendance_{today_date}.csv"
    if not os.path.isfile(attendance_file):
        attendance = pd.DataFrame(columns=col_names)
    else:
        attendance = pd.read_csv(attendance_file)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id) + "-" + str(aa)

                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
            else:
                Id = 'Unknown'
                tt = str(Id)
            if conf > 90:
                noOfFile = len(os.listdir("ImagesUnknown")) + 1
                cv2.imwrite("ImagesUnknown\\Image" + str(noOfFile) + ".jpg", im[y:y + h, x:x + w])
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if cv2.waitKey(1) == ord('q'):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = f"Attendance\\Attendance_{date}.csv"
    attendance.to_csv(fileName, index=False)  # Save or append to the file based on today's date
    cam.release()
    cv2.destroyAllWindows()
    message2.configure(text=attendance)
    message.configure(text="Attendance Taken")
    messagebox.showinfo('Completed', 'Congratulations! Your attendance has been marked successfully for the day!!')



def quit_window():
    MsgBox = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
    if MsgBox == 'yes':
        messagebox.showinfo("Greetings", "Thank you very much for using our software. Have a nice day ahead!!")
        window.destroy()


takeImg = tk.Button(window, text="IMAGE CAPTURE BUTTON", command=TakeImages, fg="white", bg="blue", width=25,
                     height=2, activebackground="pink", font=('Times New Roman', 15, ' bold '))
takeImg.place(x=245 - x_cord, y=425 - y_cord)
trainImg = tk.Button(window, text="MODEL TRAINING BUTTON", command=TrainImages, fg="white", bg="blue", width=25,
                      height=2, activebackground="pink", font=('Times New Roman', 15, ' bold '))
trainImg.place(x=645 - x_cord, y=425 - y_cord)
trackImg = tk.Button(window, text="ATTENDANCE MARKING BUTTON", command=TrackImages, fg="white", bg="red", width=30,
                      height=3, activebackground="pink", font=('Times New Roman', 15, ' bold '))
trackImg.place(x=1075 - x_cord, y=412 - y_cord)
quitWindow = tk.Button(window, text="QUIT", command=quit_window, fg="white", bg="red", width=10,
                          height=2, activebackground="pink", font=('Times New Roman', 15, ' bold '))
quitWindow.place(x=700, y=735 - y_cord)

window.mainloop()
