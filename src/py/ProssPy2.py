import serial
from matplotlib import image as img, pyplot as plt
from Metrica.imgconv import *
from Metrica.funciones import fix_matriz
import kernel
import time
# datos imagen
imagen = img.imread("D:\Documents\Tarpuy\Python\ProssPy2\Metrica\img\Lenna.jpg")
imagen = (torange(imagen, 1, 0))
imagen = np.asarray(fix_matriz(imagen, 8, 7, 'S', 'round', 'saturate', 1))
dim = np.shape(imagen)
ouput = np.zeros((dim[0]-2, dim[1]-2))

def_error = "Un error a ocurrido..."
# tramas
def_ack = 0xa1000141
def_reset = 0xa0000040
def_kernel = 0xa0010040
def_imgzise = 0xa0020040
def_load = 0xa0030040
def_run = 0xa0040040
def_dreq = 0x9001
def_loadend = 0xa1300040
# Numero de convolucionadores
N = 4
# vaiables para el control del proesamiento
columa = 0
first = True
count = 0
row_o = 0
column_o = 0
# carga del kernel
kernel_data = kernel.kernel_load()
# tamanio de la imagen
img_size = dim[0]-1  # 439
# puerto serie
ser = serial.Serial(
    port='COM12',  # configurar con el puerto serie
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()  # se abre el puerto
ser.timeout = None  # le interesa esperar una recepcion
# limpieza de buffers
ser.flushInput()
ser.flushInput()


def send_data(data, byts=4):
    """
    :param data: datos a enviar por el puerto serie
    :param byts: cantidad de bytes a enviar
    """
    for stp in range(byts):
        ser.write(chr(data >> (stp * 8) & 0xff))

lista = ['0', '1', '2', '3', '4']
index = 0
inter = 0

raw_input("press tecla cualquiera ")
print "incio del proceso "
t = time.clock()
while inter <= dim[1]:
    inter += 1
    ser.flushInput()
    ser.flushOutput()
    inPut = lista[index]
    if index == 4:
        index = 3
    else:
        index += 1
    if inter == dim[1]-1:
        index == 4

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

    elif inPut == '3':
        erorr = False
        # limit = range(N+2) if first else range(N)
        if first: limit = N + 1
        else: limit = N-1
        i = 0
        while i < limit and columa < dim[1]-1:
            send_data(def_load)
            if int(ser.read(4).encode("hex"), 16) == def_ack:
                print "\033[34mcargando filas de la imagen...\033[37m"
                for j in range(img_size + 1):
                    send_data(imagen[j][columa], 1)
                    # print "\033[34mimagen[" + str(j) + "][" + str(columa) + "] cargado\033[37m"
            else:
                print "\033[31m" + def_error + "(" + inPut + ")\033[37m"
                break
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
                # print "\033[34mimagen[" + str(i) + "][" + str(columa)+"] cargado\033[37m"
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

        # Download------------------------------------------------------------
        s = int(ser.read(2).encode("hex"), 16)
        while s != def_dreq and column_o < dim[1]-2:
            ouput[row_o][column_o] = s
            s = int(ser.read(2).encode("hex"), 16)

            if row_o == (img_size-2) and row_o > 0:
                print "--------------"
                print "\033[34mcolumna "+str(column_o)+" leida\033[37m"
                column_o += 1
                row_o = 0
            else:
                row_o += 1

        if column_o >= 2:
            first = False
        if column_o == dim[1]-2:
            t = time.clock() - t
            break
    else:
        # solo limpia los bufers del lado de C
        send_data(def_ack)
        print "\033[31m" + str(def_ack) + "(" + inPut + ")\033[37m"

ser.close()
print "fin de procesamiento, tiempo : ",t
print "min ", np.amin(ouput), "max ", np.amax(ouput)
# muestran los dos figuras
fig = plt.figure()
ax = fig.add_subplot(1, 2, 1)
ax.imshow(imagen, cmap="gray")
ax.set_title("imagen Original")

ax2 = fig.add_subplot(1, 2, 2)
ax2.imshow(ouput, cmap="gray", vmin=np.amin(ouput), vmax=np.amax(ouput))
ax2.set_title("Convolucion en Placa")
plt.show()
