from sklearn import svm
from tkinter import *
from PIL import Image, ImageDraw
import csv
import math , numpy

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=1)

        self.check_button = Button(self.root, text='Check', command=self.check)
        self.check_button.grid(row=0, column=2)

        self.clear_button = Button(self.root, text='Clear', command=self.clear)
        self.clear_button.grid(row=0, column=3)

        self.save_button = Button(self.root, text='Save', command=self.save )
        self.save_button.grid(row=0, column=4)

        self.text1 = Text(self.root, height=1, width=2)
        self.text1.grid(row=0, column=5)
       
        self.Label1 = Label(self.root, text='Write A Digit')
        self.Label1.grid(row=2, columnspan=5)
        
        self.c = Canvas(self.root, bg='white', width=150, height=150)
        self.c.grid(row=1, columnspan=6)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.image = Image.new("RGB", (150,150), 'white')

    def use_pen(self):
        self.activate_button(self.pen_button)

    def activate_button(self, some_button, Reset_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button

    def paint(self, event):
        paint_color = 'white'
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=10, fill='black',
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.draw = ImageDraw.Draw(self.image)
            self.draw.line([self.old_x, self.old_y, event.x, event.y], 'Black')
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save(self):
        self.image2 = self.image.resize((20, 20))
       
        dataset = list()
        for rgb in self.image2.getdata():
            if (rgb[0]+rgb[1]+rgb[2]) == 765:
                dataset.append(0)
            else:
                dataset.append(1)
        
        data_label = self.text1.get("1.0",'end-1c')
        dataset.append(data_label)

        with open('dataset.csv','a',newline='') as f:
            w = csv.writer(f) 
            w.writerow(dataset)

        self.clear()

    def clear(self):
        self.c.delete('all')
        self.draw.rectangle([1,1,150,150],'white')
        self.Label1.configure(text='Write A Digit')
        self.Label1.update()
    
    def check(self):
        self.image2 = self.image.resize((20, 20))
        dataset = list()
        for rgb in self.image2.getdata():
            if (rgb[0]+rgb[1]+rgb[2]) == 765:
                dataset.append(0)
            else:
                dataset.append(1)
        X_TEST = [dataset]
        outcome = clf.predict(X=X_TEST)
        self.Label1.configure(text=outcome)
        self.Label1.update()
        print(f'Outcome : {outcome}')


def train():
    TRAIN_INPUT = list()
    TRAIN_OUTPUT = list()
    with open('dataset.csv', ) as f:
        data = csv.reader(f)
        for a in data:
            temp = list()
            for i in a[:400]:
                temp.append(int(i))
            TRAIN_INPUT.append(temp)
            TRAIN_OUTPUT.append(int(a[400]))
    clf.fit(X=TRAIN_INPUT, y=TRAIN_OUTPUT)

if __name__ == '__main__':
    clf = svm.SVC()
    train()
    Paint()