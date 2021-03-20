# coding:utf-8  
import requests as req
from io import BytesIO
from tkinter import *
import tkinter.ttk as tt
import tkinter.messagebox
from PIL import ImageTk, Image
from psychological_test_code import * 
from image_path import * 
from nearby_location import *
from MRT import *


# resizing the height and width of the photo
def resize_img(imagepath, width, height, method):
    if method == 1:
        pil_img = Image.open(imagepath)
    elif method == 2:
        img_src = imagepath
        response = req.get(img_src)
        pil_img = Image.open(BytesIO(response.content))
    img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
    return img 


# for setting the background
class BkgrFrame(Frame):
    def __init__(self, parent, file_path, width, height, method):
        super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)
        self.W, self.H = width, height
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.pack()
        if method == 1:
            pil_img = Image.open(file_path)
        elif method == 2:
            img_src = file_path
            response = req.get(img_src)
            pil_img = Image.open(BytesIO(response.content))
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=NW, image=self.img)

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=CENTER, window=widget)
        return canvas_window


class ExamPage:
    # Initialize
    def __init__(self, root):
        self.root = root
        # setting backbround & frame
        try:
            frame = BkgrFrame(root, 'image/mainpage_new.png', root.width, root.height, 1)
            print("find local image")
        except:
            frame = BkgrFrame(root, mainpage_url, root.width, root.height, 2)
            print("get image from url")
        frame.pack()
        self.Frame = frame
        # setting image!
        try: 
            self.start_img = resize_img("image/start.png", 120, 40, 1)
            self.previous_img = resize_img("image/question_left.png", 80, 40, 1)
            self.next_img = resize_img("image/question_right.png", 80, 40, 1) 
            self.done_img = resize_img("image/question_done.png", 130, 40, 1) 
            self.open_gmap_img = resize_img("image/open_map.png", 240, 40, 1) 
            self.restart_img = resize_img("image/restart.png", 110, 40, 1)
            self.exit_img = resize_img("image/exit.png", 110, 40, 1)
        except: 
            self.start_img = resize_img(btn_start_url, 120, 40, 2)
            self.previous_img = resize_img(btn_previous_url, 80, 40, 2)
            self.next_img = resize_img(btn_next_url, 80, 40, 2) 
            self.done_img = resize_img(btn_done_url, 130, 40, 2) 
            self.open_gmap_img = resize_img(btn_open_gmap_url, 240, 40, 2) 
            self.restart_img = resize_img(btn_restart_url, 110, 40, 2)
            self.exit_img = resize_img(btn_exit_url, 110, 40, 2)
        self.start_btn = self.Frame.add(Button(self.root, image=self.start_img, command=lambda: self.start_exam()), self.Frame.W/2, self.Frame.H/4*3)
        self.choose_station()


    # previous question
    def before(self): 
        if self.normal_choice.get() != 0: 
            self.user_result[self.status] = self.normal_choice.get()
            if self.status > 1: 
                self.status -= 1 
                self.main_exam() 
            print("ans:", self.user_result)
        else: 
            tkinter.messagebox.showwarning("Hint: ", message="Please choose an answer!")
        

    # next question
    def after(self): 
        if self.normal_choice.get() != 0: 
            self.user_result[self.status] = self.normal_choice.get() 
            if self.status < len(Options): 
                self.status += 1
                self.main_exam()
            print("ans:", self.user_result)
        else:
            tkinter.messagebox.showwarning("Hint: ", message="Please choose an answer!")


    # Get recent Options
    def exam_files(self, num):
        return list(map(lambda x: x.split('.'), self.All_Option[num - 1].strip().split(',')))


    # Done the test
    def done(self): 
        self.user_result[self.status] = self.normal_choice.get() 
        if len(self.user_result) != len(Questions): 
            tkinter.messagebox.showwarning("Hint:", message="You haven't finish the test yet!") 
        else: 
            print("ans:", self.user_result)  # print on terminal
            # calculate the result
            self.price, self.taste, self.final_result = calculate_result(self.user_result)
            print("price: ", self.price, "taste: ",  self.taste)
            print(Result[self.final_result])
            # show the result
            self.Frame.destroy()
            try:
                frame = BkgrFrame(self.root, Result_img[self.final_result], self.root.width, self.root.height, 1)
            except:
                frame = BkgrFrame(self.root, Result_img_url[self.final_result], self.root.width, self.root.height, 2)
            frame.pack()
            self.Frame = frame
            try:
                self.select_rest_img = resize_img(Button_img[self.final_result], 220, 50, 1)
            except:
                self.select_rest_img = resize_img(Button_img_url[self.final_result], 220, 50, 2)
            self.search_restaurant = self.Frame.add(Button(self.root, image = self.select_rest_img, command=lambda: self.show_restaurant_list()), self.Frame.W/2, self.Frame.H/10*8)
            

    # Strat the exam
    def start_exam(self): 
        # setting private data
        self.user_result = {}  # user's answer
        self.status = 1  # answering which question
        self.All_Question = Questions  # All the questions
        self.All_Option = Options  # All the options
        self.normal_choice = IntVar()  # user's choice
        self.dinning_choice = IntVar()
        self.main_exam()
        print(self.select_MRT_station.get())
        self.location = locate_dict[self.select_MRT_station.get()]
        print(self.location)
        
    
    #  The detail of the question
    def main_exam(self): 
        # setting background
        self.Frame.destroy()
        try:
            frame = BkgrFrame(self.root, Questions_img[self.status-1], self.root.width, self.root.height, 1)
        except:
            frame = BkgrFrame(self.root, Questions_img_url[self.status-1], self.root.width, self.root.height, 2)
        frame.pack()
        self.Frame = frame
        # add button
        if self.status == 1:
            self.to_forword = self.Frame.add(Button(self.root, image = self.next_img, command=lambda: self.after()), self.Frame.W/2, self.Frame.H/11*7)
        elif self.status != 8:
            self.go_back = self.Frame.add(Button(self.root, image = self.previous_img, command=lambda: self.before()), self.Frame.W/4, self.Frame.H/11*7)
            self.to_forword = self.Frame.add(Button(self.root, image = self.next_img, command=lambda: self.after()), self.Frame.W/4*3, self.Frame.H/11*7)
        else:
            self.go_back = self.Frame.add(Button(self.root, image = self.previous_img, command=lambda: self.before()), self.Frame.W/4, self.Frame.H/11*7)
            # self.hand_in = self.Frame.add(Button(self.root, image = self.done_img, command=lambda: self.done()), self.Frame.W/4*3, self.Frame.H/11*7)
            self.hand_in = self.Frame.add(Button(self.root, image = self.done_img, command=lambda: self.done()), self.Frame.W/3*2, self.Frame.H/11*7)
        # show the question
        if 1 <= self.status <= 6:
            self.question_text = self.Frame.canvas.create_text(self.Frame.W/2, self.Frame.H/10*2, font=("Dialog", 18),anchor=CENTER)
        else:
            self.question_text = self.Frame.canvas.create_text(self.Frame.W/2, self.Frame.H/12*3, font=("Dialog", 18),anchor=CENTER)
        self.Frame.canvas.insert(self.question_text, 1, self.All_Question[self.status-1])
        # show the choices  # bg='systemTransparent'
        self.normal_choice.set(0) 
        self.temp_choice = []
        for option, choice in self.exam_files(self.status):
            try:
                authority_choice = Radiobutton(self.root, text=choice, font=("黑體", 18), bg='systemTransparent', variable=self.normal_choice, value=option)
            except:
                authority_choice = Radiobutton(self.root, text=choice, font=("黑體", 18), bg=optioncolor[self.status-1][int(option)-1], variable=self.normal_choice, value=option)
            if 1 <= self.status <= 6:
                temp = self.Frame.add(authority_choice, self.Frame.W/2, self.Frame.H/4+int(option)*40)
            else:
                temp = self.Frame.add(authority_choice, self.Frame.W/2, self.Frame.H/10*3+int(option)*40)
            self.temp_choice.append(temp)


    # show the recommend restaurant
    def show_restaurant_list(self):
        # find nearby location
        self.rest_list = nearby_location(Result[self.final_result], self.location) 
        rest_list = self.rest_list
        # set background and button
        self.Frame.destroy()
        try:
            frame = BkgrFrame(self.root, 'image/choosepage_new.png', self.root.width, self.root.height, 1)
        except:
            frame = BkgrFrame(self.root, choosepage_url, self.root.width, self.root.height, 2)
        frame.pack()
        self.Frame = frame
        # show the recommand restaurants
        if len(self.rest_list) == 0:
            self.title_text = self.Frame.canvas.create_text(self.Frame.W/2, self.Frame.H/2, font=("Dialog", 17),anchor=CENTER)
            self.Frame.canvas.insert(self.title_text,1,"Sorry, there's no\navailable restaurant now")
        else:
            self.title_text = self.Frame.canvas.create_text(self.Frame.W/2, self.Frame.H/4, font=("Dialog", 15),anchor=CENTER)
            self.Frame.canvas.insert(self.title_text,1,"推薦餐廳（依評價排序）")
            self.dinning_choice.set(0)
            for i in range(len(self.rest_list)):
                # fontsize = 18 if len(rest_list[i]) >= 15 else 22
                if len(rest_list[i]) >= 15:
                    temp = rest_list[i]
                    authority_choice = Radiobutton(self.root, text=temp[0:12]+"...", font=("黑體", 22), indicatoron=0, bg="#fcfbf9", variable=self.dinning_choice, value=i+1)
                else:
                    authority_choice = Radiobutton(self.root, text=rest_list[i], font=("黑體", 22), indicatoron=0, bg="#fcfbf9", variable=self.dinning_choice, value=i+1)
                self.Frame.add(authority_choice, self.Frame.W/2, self.Frame.H/4+(i+1)*40)
            self.google_map = self.Frame.add(Button(self.root, image=self.open_gmap_img, command=lambda: self.open_googlemap()), self.Frame.W/2, self.Frame.H/10*7)
        self.restart_btn = self.Frame.add(Button(self.root, image=self.restart_img, command=lambda: self.restart()), self.Frame.W/3, self.Frame.H/10*8)
        self.exit_sys = self.Frame.add(Button(self.root, image=self.exit_img, command=lambda: sys.exit()), self.Frame.W/3*2, self.Frame.H/10*8)


    # open in google map
    def open_googlemap(self):
        if self.dinning_choice.get() != 0:
            print("open in google map!")
            i = self.dinning_choice.get()
            print("my choice:", i, self.rest_list[i-1])
            address = self.rest_list[i-1]
            address = urllib.parse.quote(address)
            webbrowser.open("https://www.google.com/maps/search/?api=1&query=" + address)
        else:
            tkinter.messagebox.showwarning("Hint: ", message="Please choose an restaurant!")
        

    def restart(self):
        print("restart!")
        self.Frame.destroy()
        try:
            frame = BkgrFrame(self.root, 'image/mainpage_new.png', self.root.width, self.root.height, 1)
        except:
            frame = BkgrFrame(self.root, mainpage_url, self.root.width, self.root.height, 2)
        frame.pack()
        self.Frame = frame
        self.start_btn = self.Frame.add(Button(self.root, image=self.start_img, command=lambda: self.start_exam()), self.Frame.W/2, self.Frame.H/4*3)
        # reset private data
        self.user_result = {}  # user's answer
        self.status = 1  # answering which question
        self.All_Question = Questions  # All the questions
        self.All_Option = Options  # All the options
        self.normal_choice = IntVar()  # user's choice
        self.dinning_choice = IntVar()
        self.choose_station()


    def choose_station(self):
        # select MRT line
        self.select_MRT_line = StringVar()
        self.select_MRT_line.set(mrt_line[1])
        self.opt1 = OptionMenu(self.root, self.select_MRT_line, *mrt_line)
        self.opt1.config(width=8)
        self.Frame.add(self.opt1, self.Frame.W/3, self.Frame.H/3*2) 
        # select MRT station
        self.select_MRT_station = StringVar()
        self.select_MRT_station.set(red_[8])
        # self.opt2 = OptionMenu(self.root, self.select_MRT_station, *red_)
        self.opt2 = tt.Combobox(self.root, textvariable=self.select_MRT_station, values=red_, state='readonly')
        self.opt2.config(width=8)
        self.Frame.add(self.opt2, self.Frame.W/3*2, self.Frame.H/3*2) 
        def callback(*args):
            station_list = mrt_dict[self.select_MRT_line.get()]
            # self.opt2 = OptionMenu(self.root, self.select_MRT_station, *station_list)
            self.opt2 = tt.Combobox(self.root, textvariable=self.select_MRT_station, values=station_list, state='readonly')
            self.opt2.config(width=8)
            self.select_MRT_station.set(station_list[0])
            self.Frame.add(self.opt2, self.Frame.W/3*2, self.Frame.H/3*2)
        self.select_MRT_line.trace("w", callback)

