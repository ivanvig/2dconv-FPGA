import time
import serial

ser = serial.Serial(
    port='COM15',  # configurar con el puerto serie
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()  # se abre el puerto
ser.timeout = None  # le interesa esperar una recepcion
ser.flushInput()
ser.flushInput()
while 1:
    ser.flushInput()
    ser.flushOutput()
    print "Selecione "
    inPut = str(raw_input("ToSent: "))
    if inPut == 'exit':
        print "Fin de transmicion"
        ser.close()
        break
    elif inPut == '0':
        ser.write(inPut)
    elif inPut == '1':
        ser.write(inPut)
    elif inPut == '2':
        ser.write(inPut)
    elif inPut == '3':
        f = open("D:\Documents\Tarpuy\Python\ProssPy2\output.txt", 'w')
        for i in range(436):
            ser.write(inPut)
            time.sleep(0.1)
            s = ''
            while ser.inWaiting() > 0:
                s += str(ser.read(1).encode("hex"))
            f.write(str(i)+' '+s+'\n')
        f.close()
    else:
        print "datos erroneos"
