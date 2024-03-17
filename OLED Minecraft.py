from socket import *
from machine import Pin, SoftI2C
import time
import ssd1306
import network
import framebuf
import struct

# 端口与ip
host = "192.168.235.40"
port = 1111
# wifi账号与密码
ssid = "1"
password = "114511411"
# 数据与样式 1文字 2爱心
health = "Health: Null"
style = 2
# 创建i2c对象
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
# 宽度高度
oled_width = 128
oled_height = 64
# 创建oled屏幕对象
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
# 图片
img = [0x0E,0x1D,0x3F,0x7E,0x3F,0x1F,0x0E]
buffer = bytearray(img)
fb = framebuf.FrameBuffer(buffer,7,8,framebuf.MONO_VLSB)

# 连接网络
def connectWLAN():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('正在连接中...')
        showTEXT('正在连接中...',1,1)
        wlan.connect(ssid, password)
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            showTEXT("正在链接...{}".format(i),1,3)
            i += 1
            time.sleep(1)
    print('连接成功!')
    showTEXT('连接成功!',1,1)

# 连接Server
def connectServer():
    # 1. 创建tcp套接字
    client_socket = socket(AF_INET, SOCK_STREAM)
    # 2. 准备接收方的地址
    server_addr = (host, port)
    # 3. 链接服务器
    client_socket.connect(server_addr)
    # 4. 从键盘获取数据
    send_data = "connect successfully!"
    # 5. 发送数据到指定的电脑上
    client_socket.send(send_data)
    # 6. 接受数据
    while True:
        #准备数据
        data, addr = client_socket.recvfrom(1024)  # 接收数据
        number = int.from_bytes(data, '>') # bytes -> int
        health = 'Health: ' + str(number) # Health设置
    
        #屏幕绘制
        if style == 1:
            showTEXT(health,0,0)
        else:
            showIMG(number,0,0)
            
        #打印内容并且线程睡眠
        print(health)
    
        time.sleep(0.1)    

# 生命绘制
def showTEXT(text,x,y):
    oled.fill(0)
    oled.text(text,x, y)
    oled.show()
    
def showIMG(times,x,y):
    oled.fill(0)
    if times != 0:
       for z in range(0, times):
           if z < 10:
               oled.blit(fb,x + z*7,y)
           else:
               oled.blit(fb,x + (z-10)*7,y+10)
    oled.show()
       

#1.链接网络
connectWLAN()
#2.链接服务器 和 文字绘制
connectServer()