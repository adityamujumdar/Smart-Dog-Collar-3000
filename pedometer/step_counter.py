import math
import RPi.GPIO as gpio
import smbus
import time

PWR_M = 0x6B
DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_EN = 0x38

TEMP = 0x41
ACCEL_X = 0x3B
ACCEL_Y = 0x3D
ACCEL_Z = 0x3F
GYRO_X = 0x43
GYRO_Y = 0x45
GYRO_Z = 0x47

bus_obj = smbus.SMBus(1)
device_addr = 0x68  # device address

AxCal = 0
AyCal = 0
AzCal = 0

GxCal = 0
GyCal = 0
GzCal = 0

RS = 18
EN = 23
D4 = 24
D5 = 25
D6 = 8
D7 = 7

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(D4, gpio.OUT)
gpio.setup(D5, gpio.OUT)
gpio.setup(D6, gpio.OUT)
gpio.setup(D7, gpio.OUT)
gpio.setup(RS, gpio.OUT)
gpio.setup(EN, gpio.OUT)


# Referenced:  https://www.researchgate.net/publication/329526966_A_More_Reliable_Step_Counter_using_Built-in_Accelerometer_in_Smartphone
def pedometer(accel_data):
    n = len(accel_data)
    p = [0]*len(accel_data)
    step = 0
    i = 2
    while(i<n-1):
        # print(f'i: {i}, i+1: {i+1}, n: {n}, accel_data[i] {accel_data[i]}, accel_data[i-1]: {accel_data[i-1]}\n')
        print(f', accel_data[i+1]: {accel_data[i+1]}\n')
        if((accel_data[i]>accel_data[i-1]) and (accel_data[i]>accel_data[i+1])):
            p[i] = 1
        else:
            p[i] = 0
        i+=1
    j = 0
    k = 0
    D = 0
    while(j<n):
        if(p[j]==1):
            if(k!=0):
                D = (j-k-1)
                if (D>2):
                    step+=1
            k = j
        j+=1
    if(j==n):
        D=n-k
        if(D>2):
            step+=1
    return step

def begin():
    cmd(0x33)
    cmd(0x32)
    cmd(0x06)
    cmd(0x0C)
    cmd(0x28)
    cmd(0x01)
    time.sleep(0.001)


def cmd(ch):
    gpio.output(RS, 0)

    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
    if ch & 0x10 == 0x10:
        gpio.output(D4, 1)
    if ch & 0x20 == 0x20:
        gpio.output(D5, 1)
    if ch & 0x40 == 0x40:
        gpio.output(D6, 1)
    if ch & 0x80 == 0x80:
        gpio.output(D7, 1)
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)

    # Low bits
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
    if ch & 0x01 == 0x01:
        gpio.output(D4, 1)
    if ch & 0x02 == 0x02:
        gpio.output(D5, 1)
    if ch & 0x04 == 0x04:
        gpio.output(D6, 1)
    if ch & 0x08 == 0x08:
        gpio.output(D7, 1)
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)


def write(ch):
    gpio.output(RS, 1)

    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
    if ch & 0x10 == 0x10:
        gpio.output(D4, 1)
    if ch & 0x20 == 0x20:
        gpio.output(D5, 1)
    if ch & 0x40 == 0x40:
        gpio.output(D6, 1)
    if ch & 0x80 == 0x80:
        gpio.output(D7, 1)
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)

    # Low bits
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
    if ch & 0x01 == 0x01:
        gpio.output(D4, 1)
    if ch & 0x02 == 0x02:
        gpio.output(D5, 1)
    if ch & 0x04 == 0x04:
        gpio.output(D6, 1)
    if ch & 0x08 == 0x08:
        gpio.output(D7, 1)
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)


def clear():
    cmd(0x01)


def InitMPU():
    bus_obj.write_byte_data(device_addr, DIV, 7)
    bus_obj.write_byte_data(device_addr, PWR_M, 1)
    bus_obj.write_byte_data(device_addr, CONFIG, 0)
    bus_obj.write_byte_data(device_addr, GYRO_CONFIG, 24)
    bus_obj.write_byte_data(device_addr, INT_EN, 1)
    time.sleep(1)


def display(x, y, z):
    x = x*100
    y = y*100
    z = z*100
    print(f'x: {x}, y: {y}, z: {z}\n')


def readMPU(addr):
    high = bus_obj.read_byte_data(device_addr, addr)
    low = bus_obj.read_byte_data(device_addr, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

def accel():
    x = readMPU(ACCEL_X)
    y = readMPU(ACCEL_Y)
    z = readMPU(ACCEL_Z)

    Ax = (x/16384.0-AxCal)
    Ay = (y/16384.0-AyCal)
    Az = (z/16384.0-AzCal)
    # print "X="+str(Ax)
    print(f'Ax,Ay,Az: {Ax},{Ay},{Az}\n')
    to_pedometer = math.sqrt((Ax*Ax)+(Ay*Ay)+(Az*Az))
    time.sleep(.01)
    return to_pedometer

def gyro():
    global GxCal
    global GyCal
    global GzCal
    x = readMPU(GYRO_X)
    y = readMPU(GYRO_Y)
    z = readMPU(GYRO_Z)
    Gx = x/131.0 - GxCal
    Gy = y/131.0 - GyCal
    Gz = z/131.0 - GzCal
    print(f'Gx,Gy,Gz: {Gx},{Gy},{Gz}\n')
    time.sleep(.01)
    return (Gx, Gy, Gz)


def temp():
    temp = 0
    for i in range(100):
        temp = temp + readMPU(TEMP)
    temp = temp/100
    tempC = (temp / 340.0) + 36.53
    time.sleep(.002)
    return tempC


def calibrate():
    clear()
    print("Calibrating....\n")
    global AxCal
    global AyCal
    global AzCal
    x = 0
    y = 0
    z = 0
    for i in range(100):
        x = x + readMPU(ACCEL_X)
        y = y + readMPU(ACCEL_Y)
        z = z + readMPU(ACCEL_Z)
    x = x/100
    y = y/100
    z = z/100
    AxCal = x/16384.0
    AyCal = y/16384.0
    AzCal = z/16384.0
    print(f'AxCal,AyCal,AzCal: {AxCal},{AyCal},{AzCal}\n')

    global GxCal
    global GyCal
    global GzCal
    x = 0
    y = 0
    z = 0
    for i in range(100):
        x = x + readMPU(GYRO_X)
        y = y + readMPU(GYRO_Y)
        z = z + readMPU(GYRO_Z)
    x = x/100
    y = y/100
    z = z/100
    GxCal = x/131.0
    GyCal = y/131.0
    GzCal = z/131.0
    print(f'GxCal,GyCal,GzCal: {GxCal},{GyCal},{GzCal}\n')

def main():
    begin()
    time.sleep(1)
    InitMPU()
    calibrate()
    total_steps = 0
    while 1:
        pedometer_val = []
        InitMPU()
        clear()
        tempC = temp()
        print(f'Current temperature: {tempC}\n')
        clear()
        time.sleep(1)
        for i in range(50):
            avg_acceleration = accel()
            pedometer_val.append(avg_acceleration)
        steps_in_loop = pedometer(pedometer_val)
        total_steps += steps_in_loop
        print(f'Steps Taken: {total_steps}')
        # print(f'pedometer val: {pedometer_val}')
        # clear()
        # print("Gyroscope Data\n")
        # time.sleep(1)
        # for i in range(30):
        #     g_data = gyro()
        #     print(f'gryox: {g_data[0]} gyroy: {}')

if __name__ == '__main__':
    main()
