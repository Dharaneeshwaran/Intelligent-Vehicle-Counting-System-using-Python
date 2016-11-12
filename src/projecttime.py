
from multiprocessing import Process, Queue

import cv2
import time
import pandas as pd
from PIL import Image, ImageTk

import Tkinter as tk

global label1
global count_lab


#tkinter GUI functions
def quit_(root, process):
    process.terminate()
    f = open('myfile.txt', 'w')
    f.write(str(0))
    f.close()
    root.destroy()
    fr=cv2.imread("white.jpg")
    cv2.imwrite("1.jpg",fr)

def image_capture(queue):
   bgsMOG = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
   vidFile = cv2.VideoCapture("vehicle1.mp4")
   zzz=0
   global count

   while True:
      try:

         flag, frame=vidFile.read()

         cv2.line(frame, (0, 210), (650, 210), (0, 255, 0), 2)

         fgmask = bgsMOG.apply(frame, None, 0.01)

         _, contours, hierarchy = cv2.findContours(fgmask,
                                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

         try:
            hierarchy = hierarchy[0]

         except:
            hierarchy = []
         for contour, hier in zip(contours, hierarchy):
            (x, y, w, h) = cv2.boundingRect(contour)
            if w > 50 and h > 50:
               cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
               if y > 215 and y < 228:
                  zz = frame[y:y + h, x:x + w]
                  cv2.imwrite("b" + str(zzz) + ".jpg", zz)
                  cv2.imwrite("1.jpg",zz)
                  zzz=zzz+1
                  f = open('myfile.txt', 'w')
                  f.write(str(zzz))
                  f.close()
         cv2.putText(frame, "Time" + time.strftime('%l:%M%p'), (20, 200),
                     cv2.FONT_HERSHEY_SIMPLEX,
                     0.5, (0, 0, 255), 2)
         queue.put(frame)
         cv2.waitKey(45)
      except:
         continue
def update_image(image_label, queue):
   frame = queue.get()
   im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = Image.fromarray(im)
   b = ImageTk.PhotoImage(image=a)
   a1 = Image.open("1.jpg")
   b1 = ImageTk.PhotoImage(image=a1)
   image_label.configure(image=b)
   label1.configure(image=b1)
   f = open('myfile.txt', 'r')
   df=f.readline()
   f.close()
   count_lab.configure(text=df)
   #count_lab.configure(text=time.strftime('%l:%M%p'))

   root.update()




def update_all(root, image_label, queue):
   update_image(image_label, queue)
   root.after(0, func=lambda: update_all(root, image_label,queue))


#multiprocessing image processing functions


if __name__ == '__main__':
   queue = Queue()
   print 'queue initialized...'
   root = tk.Tk()
   print 'GUI initialized...'
   image_label = tk.Label(master=root)# label for the video frame
   root.title("Vehicle Monitoring")
   root.configure(background="#00000C")
   image_label.pack(side=tk.LEFT)
   print 'GUI image label initialized...'



   #frame
   frame=tk.Frame(root,bg="#00000C")
   frame.pack(side=tk.RIGHT)

   #label of image cpature
   im_label=tk.Label(frame,text="Captured Image",bg="#00000C",fg="white")
   im_label.grid(row=0,column=0)

   #image that is being captured
   vehicle = Image.open("1.jpg")
   veh = ImageTk.PhotoImage(vehicle)
   label1 = tk.Label(frame)
   label1.configure(image=veh,height=150,width=160)
   label1.grid(row=1,column=0)


   c_label=tk.Label(frame,text="Vehicle count",bg="#00000C",fg="white")
   c_label.grid(row=2,column=0)

   count_lab=tk.Label(frame,text=" ",font=("Courier", 25,"bold"),bg="#00000C",fg="white")
   count_lab.grid(row=3,column=0)

   p = Process(target=image_capture, args=(queue,))
   p.start()
   # quit button
   quit_button = tk.Button(master=frame, text='Quit', command=lambda: quit_(root, p),height=3,width=10)
   quit_button.grid(row=4,column=0)
   print 'quit button initialized...'




   # setup the update callback
   root.after(0, func=lambda: update_all(root, image_label, queue))

   print 'root.after was called...'
   root.mainloop()
   print 'mainloop exit'
   p.join()
   print 'image capture process exit'
