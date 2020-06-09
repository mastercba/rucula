# rutina.py


from machine import Pin, I2C
from time import sleep
from . import ulcd1602



adc = Pin(36, Pin.IN, Pin.PULL_UP)                      # ADC 36
WT = Pin(25, Pin.OUT, value=1)                      # Water Tank
RG = Pin(26, Pin.OUT, value=1)                           # RieGo
MZ = Pin(27, Pin.OUT, value=1)                          # MeZcla
NT = Pin(14, Pin.OUT, value=1)                       # NuTre A&B
i2cR = I2C(-1, sda=Pin(18), scl=Pin(19), freq=400000)  # i2c Pin
lcdR = ulcd1602.LCD1602(i2cR)                      # LCD1602 OBJ



class Riego:
    def __init__(self):
        print('rutina....')
        #rutinaRiego()

# ---------------------------------------------------------
def rutinaAgua():
    if not llenarTanque():
        print('no se pudo llenar tanque de agua')
        lcdR.puts("H2O:no", 0, 1)

# ---------------------------------------------------------
def rutinaRiego():
    riego()
# ---------------------------------------------------------
def llenarTanque():
    print('llenamos tanque de agua')
    dog = 1
    num = 0
    WT.off()
    MZ.off()
    while adc.value() == 1:            # 1:vacio
        print("{}vacio".format(adc.value()))
        dog = dog + 1
        print(dog)
        sleep(2) #2
        if dog == 50:
            if num == 2:
                print('FAIL!')
                return False       #tanque vacio
            num=num+1
            dog=1
            WT.on()
            MZ.on()
            sleep(10)
            WT.off()
            MZ.off()
    WT.on()
    MZ.on()
    lcdR.puts("H2O:si", 0, 1)
    return True                    #tanque lleno
    
def riego():
    print('riego')
    lcdR.puts("*", 7, 1)
    RG.off()                             # RG ON
    sleep(500)#60    90=1minuto
    RG.on()                             # RG OFF
    lcdR.puts(" ", 7, 1)