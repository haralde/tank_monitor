from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI, UART, ADC
from xglcd_font import XglcdFont
from hcsr04 import HCSR04

MAX_SEPTIC=400
MAX_WATER=300
MAX_DIESEL=140


def setup_serial():
    if uart is None:
        uart=UART(2, baudrate=9600, rx=26, tx=25, timeout=10)
    return uart

def read_septic():
    buf=uart.readline()
    if len(buf)>3:
       height = (buf[1]*256+buf[2])
       print(height)
       septic_level = (int)((height/MAX_SEPTIC) * 120) 
       # print(barsize)
       if septic_level > 0:
           display.fill_hrect(1, 93, septic_level, 18, color565(0, 255, 0))
       display.fill_hrect(septic_level + 1, 93, 121-septic_level, 18, color565(0 , 0, 0))
       display.draw_text(50, 80, str(septic_level) + '/' + str(MAX_SEPTIC), bally, color565(255, 255, 255)) 

def read_water():
    val = adc.read()
    val = val * (3.3 / 4095)
    water_level = (int)((val/3.3) * 120) 
    # print(round(val, 2), "V")
    color=color565(0,255,0)
    if water_level<40:
        color=color565(255,255,0)
    if water_level<20:
        color=color565(255,0,0)
    
    if water_level > 0:
        display.fill_hrect(1, 53, water_level, 18, color)
        display.fill_hrect(water_level + 1, 53, 121-water_level, 18, color565(0,0,0))
        display.draw_text(37, 40, str(water_level) + '/' + str(MAX_WATER) + '  ', bally, color565(255, 255, 255))
            

if spi is None:
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))
display.draw_image('MicroPython128x128.raw', 0, 0, 128, 128)
sleep(1) 
display.clear()

bally = XglcdFont('Bally7x9.c', 7, 9)
display.draw_text(0, 0, 'Diesel:', bally, color565(255, 255, 255))
display.draw_text(0, 40, 'Vann:', bally, color565(255, 255, 255))
display.draw_text(0, 80, 'Septik:', bally, color565(255, 255, 255))
display.draw_rectangle(0, 12, 120, 20,color565(255, 255, 255))
display.draw_rectangle(0, 52, 120, 20,color565(255, 255, 255))
display.draw_rectangle(0, 92, 120, 20,color565(255, 255, 255))


adc = ADC(Pin(35))
adc.atten(adc.ATTN_11DB) #normalized to 3.3v

while True:
    # read_septic()
    read_water()
    
    sleep(0.1)
    
    
    
