import machine, onewire, ds18x20
import utime as time
import sdcard
import uos


# Assign Pin Temperature sensor
DS_PIN = machine.Pin(16)

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(9, machine.Pin.OUT)
spi = machine.SPI(1,
                  baudrate = 1000000,
                  polarity = 0,
                  phase = 0,
                  bits = 8,
                  firstbit = machine.SPI.MSB,
                  sck = machine.Pin(10),
                  mosi = machine.Pin(11),
                  miso = machine.Pin(8))

# Initialize sensor
try:
    DS_SENSOR = ds18x20.DS18X20(onewire.OneWire(DS_PIN))
    roms = DS_SENSOR.scan()
except:
    print("DS sensor not found")

# Initialize SD card
try:
    sd = sdcard.SDCard(spi, cs)
except:
    print("sdCard not found")

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

temperature = ""


with open("/sd/nest.txt", "a") as file:
    file.write("Temperature: " + "\r\n") 

while True:
    now = time.localtime()
    time.sleep(2)
    DS_SENSOR.convert_temp()
    
    for rom in roms:
        temperature = str(DS_SENSOR.read_temp(rom))

    textFormatter = temperature + ", " + str(now) + "\r\n"
    print(textFormatter)
    # Create a file and write something to it
    
    with open("/sd/nest.txt", "a") as file:
        file.write(textFormatter)



