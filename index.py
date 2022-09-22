import tkinter as tk
from tkinter import filedialog,messagebox
from tkinter import *
from PIL import ImageTk,Image
import easygui
import requests
import base64
import os

easygui.msgbox("注意！代码已经开源！开源就意味着免费！禁止盗卖！"
               + '\n' +
               "在浏览器中访问：https://github.com/mcheping520/image-color"
               )

def resize(w,h,newW,newH,pilPicture):
    f1 = 1.0 * newW / w
    f2 = 1.0 * newH / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pilPicture.resize((width, height), Image.ANTIALIAS)
def showPhoto(route,xPos,yPos):
    image = Image.open(route)
    w, h = image.size
    if w == 270 and h == 270:
        resized = image
    else:
        resized = resize(w,h,270,270,image)
    photo = ImageTk.PhotoImage(resized)
    photoLabel = tk.Label(window,image=photo,width=270,height=270)
    photoLabel.place(x=xPos,y=yPos)
    window.mainloop()

apiKey = '在百度获取：https://ai.baidu.com/tech/imageprocess/colourize'
secretKey = '在百度获取：https://ai.baidu.com/tech/imageprocess/colourize'
def getToken():
    getTokenUrl = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+apiKey+'&client_secret='+secretKey
    response = requests.get(getTokenUrl)
    data = response.json()
    token = data.get('access_token')
    return token

def chooseImage():
    global imagePath
    imagePath = filedialog.askopenfilename(initialdir="./img",title='Choose an image.')
    if len(imagePath) == 0:
        messagebox.showwarning(title='请注意',message='请选择一张人物图片')
    else:
        showPhoto(imagePath,90,125)

def getData():
    url = 'https://aip.baidubce.com/rest/2.0/image-process/v1/colourize'
    with open(imagePath,'rb') as f:
        image = f.read()
    b64Image = base64.b64encode(image)
    print(b64Image)
    params={'access_token':getToken()}
    data = {'image':b64Image}
    response = requests.post(url,params=params,data=data)
    content=response.json()
    imageb64 = content['image']
    print(imageb64)
    image = base64.b64decode(imageb64)
    with open("doc/color.jpg", 'wb') as f:
        f.write(image)
    clearImg()

def clearImg():
    url = 'https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance'
    with open("doc/color.jpg", 'rb') as f:
        image = f.read()
    b64Image = base64.b64encode(image)
    print(b64Image)
    params={'access_token':getToken()}
    data = {'image':b64Image}
    response = requests.post(url,params=params,data=data)
    content=response.json()
    imageb64 = content['image']
    print(imageb64)

    #请在下方书写你的代码
    #保存并绘制图片
    image = base64.b64decode(imageb64)
    number = len(os.listdir('colorPic'))
    with open("colorPic/%s.jpg"%number,'wb') as f:
        f.write(image)
    showPhoto("colorPic/%s.jpg"%number,684,221)

window = tk.Tk()
window.geometry('1050x660')
window.resizable(0,0)
window.title('照亮你的美')

bgImg = ImageTk.PhotoImage(file="images/bg.jpg")
bg = tk.Label(window,width=1050,height=660,image=bgImg)
bg.pack()

selectImg = ImageTk.PhotoImage(file="images/choose.jpg")
select = tk.Button(window,image=selectImg,bd=0,width=257,height=70,command=chooseImage)
select.place(x=99,y=448)

okImg = ImageTk.PhotoImage(file="images/ok.jpg")
ok = tk.Button(window,image=okImg,bd=0,width=257,height=70,command=getData)
ok.place(x=693,y=544)

window.mainloop()
