import serial
import numpy as np
from matplotlib import image as img, pyplot as plt
from imgconv import *
from Metrica.funciones import fix_matriz

imagen = img.imread("D:\Documents\Tarpuy\Python\ProssPy2\Metrica\img\da_bossGS.jpg")
imagen = (torange(imagen, 1, 0))
imagen = np.asarray(fix_matriz(imagen, 8, 7, 'S', 'round', 'saturate', 1))
dim = np.shape(imagen)
ouput = np.zeros((dim[0]-2, dim[1]-2))

def_error = "Un error a ocurrido..."
def_ack = 0xa1000141

def_reset = 0xa0000040
def_kernel = 0xa0010040
def_imgzise = 0xa0020040
def_load = 0xa0030040
def_run = 0xa0040040
def_dreq = 0xa0050040
def_loadend = 0xa1300040
N = 2

kernel_data = [0x002000, 0x208020, 0x002000]
img_size = dim[0]-1  # 439
"""
imag0 = []

# 0
imag0.append([0x7f, 0x7f, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7f, 0x7f, 0x7f,
              0x7f, 0x7f, 0x7f, 0x7f])
# 1
imag0.append([0x7f, 0x7f, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7f, 0x7f, 0x7f,
              0x7f, 0x7f, 0x7f, 0x7f])
# 2
imag0.append([0x7f, 0x7f, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7f, 0x7f, 0x7f,
              0x7f, 0x7f, 0x7f, 0x7f])
# 3
imag0.append([0x7f, 0x7f, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e,
              0x7e, 0x7e, 0x7e, 0x7e])
# 4
imag0.append([0x7f, 0x7f, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e,
              0x7e, 0x7e, 0x7e, 0x7e, 0x7e])
# 5
imag0.append([0x7f, 0x7f, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e,
              0x7e, 0x7e, 0x7e, 0x7e, 0x7e])
# 6
imag0.append([0x7f, 0x7f, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e,
              0x7e, 0x7e, 0x7e, 0x7e, 0x7e])
# 7
imag0.append([0x7f, 0x7f, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7d, 0x7d, 0x7d,
              0x7d, 0x7d, 0x7d, 0x7d, 0x7d])
# 8
imag0.append([0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e,
              0x7e, 0x7e, 0x7e, 0x7d, 0x7d])
# 9
imag0.append([0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e,
              0x7e, 0x7e, 0x7e, 0x7d, 0x7d])
"""

columa = 0
first = True
count = 0
row_o = 0
column_o = 0

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


def send_data(data, byts=4):
    """
    :param data: datos a enviar por el puerto serie
    :param byts: cantidad de bytes a enviar
    """
    for i in range(byts):
        ser.write(chr(data >> (i * 8) & 0xff))

lista = ['0', '1', '2', '3', '4']
index = 0
inter = 0

while inter <= dim[0]:
    inter += 1
    ser.flushInput()
    ser.flushOutput()
    # print "incio del proceso "
    # inPut = str(raw_input("comand 2 Sent: "))
    inPut = lista[index]
    if index == 4:
        index = 3
    else :
        index += 1

    if inPut == 'exit':
        print "Fin de transmicion"
        ser.close()
        break
    elif inPut == '0':
        # envio la trama de reset, reset todos los modulso
        send_data(def_reset)
        if int(ser.read(4).encode("hex"), 16) == def_reset:
            print "\033[34mreset del sistema ...\033[37m"
        else:
            print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
        columa = 0
        first = True

    elif inPut == '1':
        send_data(def_kernel)
        if int(ser.read(4).encode("hex"), 16) == def_ack:
            for i in range(3):
                send_data(kernel_data[i])
                if int(ser.read(4).encode("hex"), 16) == def_ack:
                    print "\033[34mkernel " + str(i) + " cargado\033[37m"
                else:
                    print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
                    break
            if int(ser.read(4).encode("hex"), 16) == def_kernel:
                print "\033[34mel kernel ha sido cargado...\033[37m"
            else:
                print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
        else:
            print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
            # ser.write(inPut)
    elif inPut == '2':
        send_data(def_imgzise)
        if int(ser.read(4).encode("hex"), 16) == def_ack:
            print "\033[34mcargando catidad de filas de imagen...\033[37m"
            send_data(img_size, 2)
            if int(ser.read(4).encode("hex"), 16) == def_imgzise:
                print "\033[34mcatidad de filas cargada ...\033[37m"
            else:
                print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
        else:
            print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
            # ser.write(inPut)
    elif inPut == '3':
        erorr = False
        # limit = range(N+2) if first else range(N)
        if first: limit = N + 1
        else: limit = N-1
        # for i in limit:
        i = 0
        while i < limit and columa < dim[1]:
            send_data(def_load)
            if int(ser.read(4).encode("hex"), 16) == def_ack:
                print "\033[34mcargando filas de la imagen...\033[37m"
                for j in range(img_size + 1):
                    send_data(imagen[j][columa], 1)
                    # if int(ser.read(4).encode("hex"), 16) == def_ack:
                    print "\033[34mimagen[" + str(j) + "][" + str(columa) + "] cargado\033[37m"
                    """
                    else:
                        print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
                        erorr = True
                        break
                    """
            else:
                print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
                break
            # if erorr:
            #     break
            if int(ser.read(4).encode("hex"), 16) == def_load:
                print "\033[34mimagen[][" + str(columa) + "] cargada..\033[37m"
            else:
                print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
            i += 1
            columa += 1

    elif inPut == '4':
        send_data(def_loadend)
        if int(ser.read(4).encode("hex"), 16) == def_ack:
            print "\033[34mcargando filas de la imagen...\033[37m"
            for i in range(img_size + 1):
                send_data(imagen[i][columa], 1)
                # if int(ser.read(4).encode("hex"), 16) == def_ack:
                print "\033[34mimagen[" + str(i) + "]["+ str(columa)+"] cargado\033[37m"
                """
                else:
                    print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
                    break
                """
        else:
            print "\033[31m" + def_error + "(" + inPut + ")\033[37m"

        if int(ser.read(4).encode("hex"), 16) == def_loadend:
            print "\033[34multima  columna "+str(columa)+" cargada & SOP\033[37m"
        else:
            print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
        columa += 1

        # OTRA COSA-------------------------------------------------------------
        s = int(ser.read(4).encode("hex"), 16)
        while s != def_dreq:
            ouput[row_o][column_o] = s
            s = int(ser.read(4).encode("hex"), 16)
            if row_o == (img_size-2) and row_o > 0:
                print "--------------"
                print "\033[34mcolumna "+str(column_o)+" leida\033[37m"
                column_o += 1
                row_o = 0
            else:
                row_o += 1

        if column_o >= 2:
            first = False

    elif inPut == '5':

        f = open("D:\Documents\Tarpuy\Python\ProssPy2\out_mem"+str(count)+".txt", "w")
        send_data(def_dreq)
        s = int(ser.read(4).encode("hex"), 16)
        while s != def_dreq:
            f.write("{:04x}\n".format(s))
            # print "\033[92m" + "{:04x}".format(s) + "\033[37m"
            s = int(ser.read(4).encode("hex"), 16)
        print "--------------"
        print "\033[34mcolumna leida en archivo out_mem"+str(count)+"\033[37m"
        count += 1
        f.close()
        print "archivo cerrado"
        if count >= 2:
            first = False
    elif inPut == '9':
        print ouput[:, 0]
        print ouput[:, 1]
        # print ouput[0:15][1]

ser.close()
print "llegue a este lugar "
f = open("D:\Documents\Tarpuy\Python\ProssPy2\datos_salida.txt", "w")
np.savetxt(f, ouput)
f.close()

print "min ", np.amin(ouput), "max ", np.amax(ouput)

plt.imshow(ouput, cmap="gray", vmin=np.amin(ouput), vmax=np.amax(ouput))
plt.show()
