import network
import espnow
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
import time

I2C_ADDR = 0x27
totalRows = 4
totalColums = 20
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=4000000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColums)

red = network.WLAN(network.STA_IF)
red.active(True)
EN = espnow.ESPNow()
EN.active(True)
mac = b'\x24\xdc\xc3\x46\xac\x5c'
EN.add_peer(mac)
msg10 = Pin(33, Pin.IN, Pin.PULL_UP)
Blon = Pin(17, Pin.IN, Pin.PULL_UP)
Bloff = Pin(5, Pin.IN, Pin.PULL_UP)
Bu = Pin(12, Pin.IN, Pin.PULL_UP)
Bd = Pin(14, Pin.IN, Pin.PULL_UP)
Br = Pin(27, Pin.IN, Pin.PULL_UP)
Bl = Pin(26, Pin.IN, Pin.PULL_UP)
Snd = Pin(25, Pin.IN, Pin.PULL_UP)
a = 0
Act = 0
col = 0
vel = 0.009
screen_state = [[" "] * totalColums for _ in range(totalRows)]

def ADP(row, col, text):
    global vel, screen_state
    for i, char in enumerate(text):
        if col + i < totalColums:
            if screen_state[row][col + i] != char:
                lcd.move_to(col + i, row)
                lcd.putstr(char)
                screen_state[row][col + i] = char
                sleep(vel)

def Msj():
    global a
    ADP(1, col, chr(ord("a") + a))

def Lt_up():
    global Act, a
    if Act != 1:
        Act = 1
    a += 1
    if a == 26:
        a = 0
    Msj()    
    sleep(0.25)
        
def Lt_down():
    global Act, a
    if Act != 1:
        Act = 1
    a -= 1
    if a == -1:
        a = 25
    Msj()
    sleep(0.25)
        
lcd.move_to(0, 0)
lcd.putstr("Msj Tr #1:")
lcd.move_to(0, 1)
lcd.putstr("a")
lcd.show_cursor()

while True:
    if Bu.value() == 0:
        Lt_up()
    if Bd.value() == 0:
        Lt_down()
    if Br.value() == 0:
        col += 1
        if col == 20:
            col = 19
        lcd.move_to(col, 1)
        lcd.show_cursor()
        a = 0
        sleep(0.25)
    if Bl.value() == 0:
        col -= 1
        if col == -1:
            col = 0
        lcd.move_to(col, 1)
        lcd.show_cursor()
        a = 0
        sleep(0.25)
    if Snd.value() == 0:
        col = 0
        mensaje = '\n'.join(["".join(row) for row in screen_state])
        mensaje_bytes = mensaje.encode('utf-8')
        EN.send(mac, mensaje_bytes)
        lcd.move_to(0, 0)
        lcd.putstr("mensaje enviado   ")
        lcd.move_to(0, 1)
        lcd.putstr(" " * totalColums)
        sleep(3)
        screen_state = [[" "] * totalColums for _ in range(totalRows)]
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Msj Tr #1:")
        lcd.move_to(0, 1)
        lcd.putstr("            ")
        sleep(0.05)
        ADP(1, col, "a")
        lcd.move_to(0, 1)
        lcd.show_cursor()
    if msg10.value() == 0:
        lcd.move_to(0,1)
        lcd.putstr("Andres Siguencia")
        EN.send(mac, "Andres Siguencia")
        sleep(0.5)
        lcd.move_to(0,1)
        lcd.putstr("                ")
        sleep(0.05)
        ADP(1, col, "a")
        lcd.move_to(0, 1)
        lcd.show_cursor()
    if Blon.value() == 0:
        lcd.move_to(0,1)
        lcd.putstr("Prend Pantll")
        EN.send(mac, "Prend Pantll")
        sleep(0.7)
        lcd.move_to(0,1)
        lcd.putstr("                ")
        sleep(0.05)
        ADP(1, col, "a")
        lcd.move_to(0, 1)
        lcd.show_cursor()
    if Bloff.value() == 0:
        print("a")
        lcd.move_to(0,1)
        lcd.putstr("Apgr Pantll")
        EN.send(mac, "Apgr Pantll")
        sleep(0.7)
        lcd.move_to(0,1)
        lcd.putstr("                ")
        sleep(0.05)
        ADP(1, col, "a")
        lcd.move_to(0, 1)
        lcd.show_cursor()