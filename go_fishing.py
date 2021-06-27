from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from PIL import Image, ImageTk
from cv2 import imread, cvtColor, COLOR_BGR2HSV, inRange, threshold, THRESH_BINARY, dilate, findContours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, contourArea
from pyautogui import click
from numpy import array


import sys, os
from json import loads
from time import sleep
from threading import Thread
import win32gui, win32ui, win32con
from collections import defaultdict



fishing_flag = True
x_position = 10
y_position = 10
picture_size = 60
fishingtimes = 100
title_pic_base64 = b'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'
cat_pic_base64 = b'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9qOPPoqMsmyIMHfuXCuHo3a4UaNGduTIkVY4nMgdLkaBd9991x555JHaNrbE0aNH23Xr1oWuquSJ8M8//9jrr7/eCseinTzxxBPtjz/+GLqD/2XGp556yrZq1Urbedhhh9mff/45VPUlTQQOxsMPP1w71bx5c/v444+H6lRlZuJcEg5K27ztttvaBQsW5G1OyRJh3rx5dqutttLOCEtoOYzLBdiKrr76am27sMR24cKFOZtekkR48803bcOGDS2cB50pV5g4cWJqRSxdujSwGyVHhHfeeceKKsHWrVtXuY/AlpdJwpgxY5QQHTp0sHB3flBSRPj666+V/YTDePDBB/3aW5bf+vXrp4QYOHCgb/tLhgjw+ghdCF8s46oEf/zxhxU9lG6vL7/8clbXSoYIN998sxLgpJNOympkVfjw6aefqoS/4447WlEoZnSpJIjAodWgQQPbpEmTsuKCMkYyxD9XXnmlTrSrrroqI3dJEMGxcxxiVRmQezbaaCPbokULixDqoNKJwNJEDSEGFYs+pqrDeeedp6tBVO+prla6eVNUxQajS+/evU29evXkXC4+COdV/EoCajj55JM1JaMNKXJU0o9u3bqpPSCMeJ9UE5HExQKXFDpfPGJcsh9++GFWGqu9fv36qg1wif/pShCFlpoen332WfPCCy+o5Yr3TjvtZETPEjB3on3GfnzaaacZ0br6FsTejOXs888/902P8hEL21lnnWXEeJRV7LHHHjOPPPJI1ndWu6i8tQ1Y8hQcNYrx5iCaNm2aPeOMMyw6FKkw43Ga0XPPPTex6pFKxaSpB6AfT/7www9rG/zSojbipZdeUlx77LGH9aolxPypVj8/nKNGjdJyDz30kCYX5WD+6quvLFIikq8beHRBYjS3svfbSy+9VNM5jEmfPHmyX1tjfxMjvxKBZf/KK69k4IHg1AnfngTAboIPwmNuBVC18032f98qGHzShw4dqumJEgHJEMRu8MWwbgcPHmznzJljxfie1aABAwZoY957772stEI/yDZnZemrXfiBBx5QdKtXr1ZZpFmzZr7tiVMn/XL8P2cNlrUpU6Zov6677jpflEwSiMCEBBIjwuLFi3Wmg5xOYoZM54X9WnPCCSdoY4qlpsbuywqkTRdffLHt06eP/r7kkkv8mlPQNwacelA+ssKZiG5leBHznbzYSoBEiAABWI4g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'
try:
    with open("./config.txt", "r") as f:
        config = loads(f.read())
        x_position = config["x"]
        y_position = config["y"]
        picture_size = config["size"]
except:
    pass


def window_capture(filename,pic_size,x_position,y_position):
    hwnd = 0 # 視窗的編號，0號表示當前活躍視窗
    # 根據視窗控制代碼獲取視窗的裝置上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根據視窗的DC獲取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC建立可相容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 建立bigmap準備儲存圖片
    saveBitMap = win32ui.CreateBitmap()
    # 為bitmap開闢空間
    saveBitMap.CreateCompatibleBitmap(mfcDC, pic_size, pic_size)
    # 高度saveDC，將截圖儲存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 擷取從左上角（0，0）長寬為（w，h）的圖片
    saveDC.BitBlt((0, 0), (pic_size, pic_size), mfcDC, (x_position, y_position), win32con.SRCCOPY)
    print(saveDC)
    saveBitMap.SaveBitmapFile(saveDC, filename)

def getColorList():
    dict = defaultdict(list)

    # 白色
    lower_white = array([0, 0, 221])
    upper_white = array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['white'] = color_list

    #綠色
    lower_green = array([35, 43, 46])
    upper_green = array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['green'] = color_list

    return dict

#處理圖片
def get_color(frame):
    hsv = cvtColor(frame,COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = getColorList()
    for d in color_dict:
        mask = inRange(hsv,color_dict[d][0],color_dict[d][1])
        binary = threshold(mask, 127, 255, THRESH_BINARY)[1]
        binary = dilate(binary,None,iterations=2)
        cnts, hiera = findContours(binary.copy(),RETR_EXTERNAL,CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum+=contourArea(c)
        if sum > maxsum :
            maxsum = sum
            color = d

    return color

def main_fishing(times, x_position, y_position, pic_size):
    # print(times, x_position, y_position, pic_size)
    sleep(1)
    click(x_position+pic_size/2, y_position+pic_size/2, button="left")
    tool.tool_log(text='Fishing start!')
    tool.tool_log(text=f'{times} times left')
    capture_error = 0
    timesout_error = 0
    while times>0 and fishing_flag:
        try:
            tool.bot_window_capture(logs=False)
            sleep(0.05)
        except:
            capture_error+=1
            sleep(0.02)
            if capture_error>50:
                tool.tool_log(text=f'capture_error')
                break
            continue
        # frame = imread('./pic/fishing.png')
        frame = imread('./pic/fishing.png')
        color = get_color(frame)
        if color=="green":
            timesout_error = 0
            capture_error = 0
            times-=1
            click(x_position+pic_size/2, y_position+pic_size/2, button="left")
            tool.tool_log(text=f'{times} times left')
            sleep(5)
            if times>0 and fishing_flag:
                click(x_position+pic_size/2, y_position+pic_size/2, button="left")
                sleep(2.5)
            continue
        timesout_error+=1
        if timesout_error>50:
            tool.tool_log(text=f'timesout_error')
            break
        sleep(0.2)
    tool.tool_log(text=f'finished')
    LabelTool.window_ctrl(tool)

class LabelTool():
    def __init__(self, master):
        # initialize global state
        ''' 如果mac沒有內建微軟正黑體，請改成Times '''
        self.font_kind = ('微軟正黑體 bold',12)
        self.font_ready = ('微軟正黑體 bold',10)
        self.backgroud_color = '#40A4FF'
        
        # set up the main frame
        self.parent = master
        self.parent.title("秋秋釣魚樂")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.frame.configure(background=self.backgroud_color)
        self.parent.resizable(width = FALSE, height = FALSE)

        # ----------------- GUI stuff ---------------------\
        ''' 共有三層殼，最外層self.parent，中層self.frame，內層self.box_left '''
        # title
        # self.title_photo = PhotoImage(file='./pic/title.png')
        self.title_photo = PhotoImage(data=title_pic_base64)
        self.title = Label(self.frame,image=self.title_photo)
        self.title.configure(background=self.backgroud_color)
        self.title.grid(row=0, column=0,pady = 10)

        # self.window_capture = PhotoImage(file='./pic/cat.png')
        self.window_capture = PhotoImage(data=cat_pic_base64)
        self.window_capture_pic = Label(self.frame,bg=self.backgroud_color,activebackground=self.backgroud_color,bd=0, image=self.window_capture)
        self.window_capture_pic.grid(row = 1, column = 0)

        self.mid_111 = Button(self.frame,bg='#F0F0F0',activebackground=self.backgroud_color,bd=0, text='截圖測試', command = self.bot_window_capture)
        self.mid_111.grid(row = 2, column = 0)

        # self.total_price = Listbox(self.frame, width = 12, height = 2 ,justify=CENTER)
        # self.total_price.grid(row = 0, column = 1,pady = 10)

        # left region ---------------------
        self.box_left = Frame(self.frame, border = 10)
        self.box_left.grid(row = 3, column = 0, sticky = N)
        self.box_left.configure(background=self.backgroud_color)

        # self.tmpLabel1 = Label(self.box_left, text = "截圖:",fg='white' ,font=self.font_kind)
        # self.tmpLabel1.configure(background=self.backgroud_color)
        # self.tmpLabel1.grid(row = 0, column = 0, sticky = N)
        
        self.tmpLabel2 = Label(self.box_left, text = "參數:",fg='white' ,font=self.font_kind)
        self.tmpLabel2.configure(background=self.backgroud_color)
        self.tmpLabel2.grid(row = 0, column = 0, sticky = N)
        
        self.tmpLabel3 = Label(self.box_left, text = "釣魚設定:",fg='white' ,font=self.font_kind)
        self.tmpLabel3.configure(background=self.backgroud_color)
        self.tmpLabel3.grid(row = 2, column = 0, sticky = N)
        

        # middle region ---------------------
            # row1 ---------------------
        self.mid_11 = Label(self.box_left, text = "X:", bg=self.backgroud_color, fg='white' ,font=self.font_kind)
        self.mid_11.grid(row = 1, column = 1)
        
        self.mid_12 = Entry(self.box_left, bd=1, width=5)
        self.mid_12.insert(0, x_position)
        self.mid_12.grid(row = 1, column = 2)

        self.mid_13 = Label(self.box_left, text = "Y:", bg=self.backgroud_color, fg='white' ,font=self.font_kind)
        self.mid_13.grid(row = 1, column = 3)
        
        self.mid_14 = Entry(self.box_left, bd=1, width=5)
        self.mid_14.insert(0, y_position)
        self.mid_14.grid(row = 1, column = 4)

        self.mid_15 = Label(self.box_left, text = "size:", bg=self.backgroud_color, fg='white' ,font=self.font_kind)
        self.mid_15.grid(row = 1, column = 5)
        
        self.mid_16 = Entry(self.box_left, bd=1, width=5)
        self.mid_16.insert(0, picture_size)
        self.mid_16.grid(row = 1, column = 6)
            # row2 ---------------------
        self.mid_21 = Label(self.box_left, text = "次數:", bg=self.backgroud_color, fg='white' ,font=self.font_kind)
        self.mid_21.grid(row = 3, column = 1)
        
        self.mid_22 = Entry(self.box_left, bd=1, width=5)
        self.mid_22.insert(0, fishingtimes)
        self.mid_22.grid(row = 3, column = 2)

        self.mid_26 = Button(self.box_left,bg='#F0F0F0',activebackground=self.backgroud_color,bd=0, text='開始釣魚', command = self.bot_gofishing)
        self.mid_26.grid(row = 3, column = 6)
            # row3 ---------------------
        # self.food_photo_31 = PhotoImage(file= path +'pic/food_3_1.png')
        # self.mid_31 = Button(self.box_left,bg=self.backgroud_color,activebackground=self.backgroud_color,bd=0, image=self.food_photo_31, command = self.bot_31)
        # self.mid_31.grid(row = 5, column = 1)
        


        # right region ---------------------
        self.box_right = Frame(self.frame, border = 10)
        self.box_right.grid(row = 1, column = 1, sticky = N+E)
        self.box_right.configure(background=self.backgroud_color)
        
        self.order_list = Label(self.box_right, text = 'Logs:',fg='white' ,font=self.font_ready)
        self.order_list.configure(background=self.backgroud_color)
        self.order_list.grid(row = 0, column = 0,  sticky = W+N)
        self.listbox = Listbox(self.box_right, width = 15, height = 10 ,justify=CENTER)
        self.listbox.grid(row = 1, column = 0, sticky = N+S)
        
        # self.btnDel = Button(self.box_right, text = '刪除已選', command = self.delBox)
        # self.btnDel.grid(row = 2, column = 0, sticky = W+E+N ,pady = 5)
        self.btnClear = Button(self.box_right, text = '清空LOG', command = self.clearBox)
        self.btnClear.grid(row = 3, column = 0, sticky = W+E+N ,pady = 5)

        # self.btnCalc = Button(self.box_right, text = '結帳', command = self.calcBox)
        # self.btnCalc.grid(row = 4, column = 0, pady = 10, sticky = W+E+N )

    # button function ---------------------
    @staticmethod
    def window_ctrl(tool):
        tool.mid_26 = Button(tool.box_left,bg='#F0F0F0',activebackground=tool.backgroud_color,bd=0, text='開始釣魚', command = tool.bot_gofishing)
        tool.mid_26.grid(row = 3, column = 6)

        # tool.cat_pic = PhotoImage(file='./pic/cat.png')
        tool.cat_pic = PhotoImage(data=cat_pic_base64)
        tool.window_capture_pic.config(image = tool.cat_pic)

    def tool_log(self, text):
        self.listbox.insert(0, text)
        self.listbox.itemconfig(0, fg ='blue')
        try:
            tool.listbox.itemconfig(1, fg ='black')
        except:
            pass

    def bot_gofishing(self):
        global fishing_flag
        fishing_flag = True
        self.listbox.insert(0, '開始釣魚')
        self.listbox.itemconfig(0, fg ='blue')
        try:
            tool.listbox.itemconfig(1, fg ='black')
        except:
            pass
        self.mid_26 = Button(self.box_left,bg='#F0F0F0',activebackground=self.backgroud_color,bd=0, text='停止釣魚', command = self.bot_stopfishing)
        self.mid_26.grid(row = 3, column = 6)
        Thread(target = main_fishing, args=(int(self.mid_22.get()), int(self.mid_12.get()),int(self.mid_14.get()),int(self.mid_16.get()) )).start()

    def bot_stopfishing(self):
        global fishing_flag
        fishing_flag = False
        self.listbox.insert(0, '強制停止')
        self.listbox.itemconfig(0, fg ='blue')
        try:
            tool.listbox.itemconfig(1, fg ='black')
        except:
            pass
        self.mid_26 = Button(self.box_left,bg='#F0F0F0',activebackground=self.backgroud_color,bd=0, text='開始釣魚', command = self.bot_gofishing)
        self.mid_26.grid(row = 3, column = 6)

    def bot_window_capture(self, logs=True):
        if logs:
            self.listbox.insert(0, f'截圖({self.mid_12.get()},{self.mid_14.get()}),size:{self.mid_16.get()}')
            self.listbox.itemconfig(0, fg ='blue')
            try:
                tool.listbox.itemconfig(1, fg ='black')
            except:
                pass
        window_capture('./pic/fishing.png', int(self.mid_16.get()),int(self.mid_12.get()),int(self.mid_14.get()))
        # self.fishing_pic = PhotoImage(file= './pic/fishing.png')
        with open('./pic/fishing.png','rb') as fp:
            self.fishing_pic = Image.open(fp)
            self.fishing_pic = ImageTk.PhotoImage(self.fishing_pic)
            self.window_capture_pic.config(image = self.fishing_pic)

    def bot_25(self):
        self.listbox.insert(END, '中華麵  40')
        self.listbox.itemconfig("end", fg ='blue')
        
    # def delBox(self):
    #     sel = self.listbox.curselection()
    #     if len(sel) != 1 :
    #         return
    #     idx = int(sel[0])
    #     self.listbox.delete(idx)

    def clearBox(self):
        self.listbox.delete(0,END)
        
    # def calcBox(self):
    #     item = self.listbox.get(0,END)
    #     self.total_price.delete(0,END)
    #     total = 0
    #     for i in item:
    #         price = int(str(i)[-3:])
    #         total += price
    #     self.total_price.insert(END, total)
        

''' 以下指令為執行物件(class object)，此GUI用class形式所寫，所以要把這class乎近來tool = LabelTool(root)
    會自動執行init的部分，因為介面都寫在init裡，所以整體介面會直接開好。
'''

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.mainloop()
