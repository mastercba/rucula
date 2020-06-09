# rucula.py


from machine import Pin, I2C
from time import sleep
from . import SIM800L
from . import rutina
from . import ulcd1602
import machine, onewire, ds18x20, json

#display ,0 hh:mm 25.4C xxxx
#display ,1 H2O:no *R12 v3.9



# Create new modem object on the right Pins
modem = SIM800L.Modem(MODEM_PWKEY_PIN    = 4,
                      MODEM_RST_PIN      = 5,
                      MODEM_POWER_ON_PIN = 23,
                      MODEM_TX_PIN       = 16,
                      MODEM_RX_PIN       = 17)


# ESP32 Pin Layout
led = Pin(2, Pin.OUT, value=0)                       # BlueLed Pin
i2c = I2C(-1, sda=Pin(18), scl=Pin(19), freq=400000)     # i2c Pin
lcd = ulcd1602.LCD1602(i2c)                          # LCD1602 OBJ
ds_pin = machine.Pin(13)                             # DS18b20 Pin
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin)) # DS18B20 OBJ
riego_hora = (range(7,17))



class Rucula:
    def __init__(self, cv):
        print('start...')
        lcd.puts("R", 8, 1)                         #riegos
        self.cv = cv                              # ver1602
        lcd.puts("v", 12, 1)
        lcd.puts(self.cv, 13, 1)
        # Initialize the modem
        modem.initialize()
        # Connect the modem
        modem.connect(apn='internet.tigo.bo')
        print('\nModem IP address: "{}"'.format(modem.get_ip_addr()))
        # Are time&Date valid?
        modem.get_NTP_time_date()
        rx_time_date = modem.get_time_date()# read Time&Date
        print('Date = ', rx_time_date[8:16])
        rx_time = rx_time_date.split(',')[-1].split('-')[0]
        year = str(rx_time_date[8:10])
        if (year < "20"):
            sleep(20)
            machine.reset()
        #soft reset : import sys sys.exit()
        #hard reset : import machine machine.reset()    
        
        # Disconnect Modem
        #modem.disconnect()       
        process()                                    # main


# ----------------------------------------------------------
def process():
    r = 0
    while True:
        blink_blue_led()                              # BBL
        system_clk = modem.get_time_date() # read Time&Date
        print('Date = ', system_clk[8:16])
        sys_time = system_clk.split(',')[-1].split('-')[0]
        print('System TIME: {}'.format(sys_time))
        hr = str(sys_time.split(':')[0])
        minu = str(sys_time.split(':')[1])
                
        if hr == "21" and minu == "00": # refresh Time&Date
            #newFirmware()   # CHECK/DOWNLOAD/INSTALL/REBOOT
            ra = rutina.rutinaAgua()
            r = 0
            lcd.puts("  ", 9, 1)
            
        for es_hora in riego_hora:             # irrigation
            if hr == str(es_hora) and (minu=="30" or minu=="00"):    
                rt = rutina.riego()
                r = r + 1
                lcd.puts(r, 9, 1)
                system_clk = modem.get_time_date()
                sys_time = system_clk.split(',')[-1].split('-')[0]
                hr = str(sys_time.split(':')[0])
                minu = str(sys_time.split(':')[1])
 
        print_date_time()               # LCD1602 date&time
        #ds18b20()                    # read&LCD1602 ds18b20
#         waterQuality()              # set K0.1 waterquality
# ----------------------------------------------------------

# BlinkBlueLed
def blink_blue_led():
    led.value(1)
    sleep(0.1)
    led.value(0)
    sleep(5.0)

# LCD1602 date&time
def print_date_time():
    system_clk = modem.get_time_date()  # read Time&Date
    print('Date = ', system_clk[8:16])
    sys_time = system_clk.split(',')[-1].split('-')[0]
    print('System TIME: {}'.format(sys_time))
    hr = str(sys_time.split(':')[0])
    minu = str(sys_time.split(':')[1])
    lcd.puts(":", 2, 0)
    lcd.puts(hr, 0, 0)
    lcd.puts(minu, 3, 0)

# DS18B20
def ds18b20():
    roms = ds_sensor.scan()
    #print('Found DS devices: ', roms)
    ds_sensor.convert_temp()
    #time.sleep_ms(750)
    for rom in roms:
      temp = ("%.1f" % round(ds_sensor.read_temp(rom), 1))  
      #print(rom)
      #print("%.1f" % round(temp, 2))
      #print("/")
      #print(round(temp, 1))
      #print(ds_sensor.read_temp(rom))
    #time.sleep(5)
      lcd.puts(temp, 6, 0)   # ds18b20->lcd1602
      lcd.puts("C", 10, 0)