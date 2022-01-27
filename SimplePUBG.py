import tkinter as tk
from time import sleep
import queue as Queue
import threading
import random

# print(random.randint(0,9))

class GUI():

    var1 = None        #申明变量的类型
    var2 = None         #申明变量的类型
    msg_queue = None    #创建一个队列

    canvas = None
    person = None
    circle = None

    personLocX, personLocY = 300, 300
    circleLocX, circleLocY = 300, 300
    radius, psSize, subSize = 450, 4, 4

    def __init__(self, root):

        self.var1 = tk.StringVar()      # 申明变量的类型
        self.var2 = tk.StringVar()      # 申明变量的类型
        self.msg_queue = Queue.Queue()  # 创建一个队列

        self.initGUI(root)              # 循环读取队列中的内容刷新控件中的内容

    def handee(self,root):
        # 把队列中的内容取出赋值给label控件
        mpica=self.msg_queue.empty()# 检查队列是否为空

        if(mpica==False):
            ontad=self.msg_queue.get()
            ourta=ontad.split(",")
            if(ourta[0]=="1"):
                self.var1.set(ourta[1])
            elif(ourta[0]=="2"):
                    self.var2.set(ourta[1])

        self.circleMove()               # 实时刷圈

        print(self.judgeOutCircle())    # 判断是不是出圈
        root.after(100, self.handee,root)# 递归调用实现循环，TKinter UI线程中无法使用传统的while循环只能用它这个自带的函数递归实现循环

    def hit_me(self):
        # 点击按钮启动两个子线程
        thread = threading.Thread(target=self.line01)
        wimme = threading.Thread(target=self.line02)

        thread.start()
        wimme.start()

    def line01(self):
        # 线程回调函数
        for i in range(1,10) :
            mmer=str(i)
            summes="1,"+mmer
            self.msg_queue.put(summes)
            sleep(0.2)
        self.msg_queue.put("1,发送完毕")

    def line02(self):
        # 线程回调函数
        for i in range(20,30) :
            mmer=str(i)
            oceanw="2,"+mmer
            self.msg_queue.put(oceanw)
            sleep(0.2)
        self.msg_queue.put("2,发送完毕")

    # 实时更新毒圈的位置
    def circleMove(self):

        # 随机刷半径
        radiusRandom = random.randint(1,self.subSize)
        if self.radius - radiusRandom > self.psSize*2 :
            self.circleLocX += random.randint(-self.subSize,self.subSize)
            self.circleLocY += random.randint(-self.subSize,self.subSize)
            self.radius -= radiusRandom

            # 先删除毒圈，然后再重新生成
            self.canvas.delete(self.circle)
            self.circle   = self.canvas.create_oval(self.circleLocX - self.radius, self.circleLocY - self.radius,
                            self.circleLocX + self.radius, self.circleLocY + self.radius, fill='yellow')
            self.canvas.tag_lower(self.circle)


    # 实时更新人的位置
    def personMove(self, event):
        self.personLocX, self.personLocY = event.x, event.y
        self.canvas.moveto(self.person, self.personLocX, self.personLocY)


    def judgeOutCircle(self):
        distance = pow( pow(self.personLocX - self.circleLocX, 2) +
                        pow(self.personLocY - self.circleLocY, 2)
                        , 0.5)
        if(distance > self.radius):
            return 1
        else:
            return 0

    def initGUI(self, root):

        root.title('SamplePUBG')
        root.geometry('800x800')

        fm1 = tk.Frame(root)

        tk.Button(fm1, text = "按钮",command = self.hit_me).grid(row=0,column=0,pady=10,sticky=tk.N,columnspan=2)
        tk.Label(fm1, textvariable = self.var1,bg = 'green',fg='white',width=20, height=3).grid(row=1,column=0)
        tk.Label(fm1, textvariable = self.var2,bg = 'red',  fg='white',width=20, height=3).grid(row=1,column=1)

        fm1.pack()

        self.canvas = tk.Canvas(root, bg='green', height=600, width=600)
        self.circle   = self.canvas.create_oval(self.circleLocX - self.radius, self.circleLocY - self.radius,
                        self.circleLocX + self.radius, self.circleLocY + self.radius, fill="yellow", outline = "yellow")

        self.person = self.canvas.create_oval(self.personLocX - self.psSize, self.personLocY - self.psSize,
                        self.personLocX + self.psSize, self.personLocY + self.psSize,  fill="red", outline = "red")
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.personMove )   #绑定鼠标左键按下事件
        self.canvas.bind("<Button-1>",  self.personMove )

        root.after(100, self.handee,root)
        root.mainloop()


if __name__ == "__main__":

    root = tk.Tk()
    myGUI = GUI(root)
