import matplotlib.image as img
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", help="imagen a leer")
parser.add_argument("-f", "--filename", help="nombre del archivo a crear")
parser.add_argument("-c", "--columna", type=int, help="columna de imagen a guardar")
parser.add_argument("-s", "--size", type=int, default='1024', help="tamaño total a escribir, se completa con 0 si la imagen es menor")
args = parser.parse_args()

try:
    imagen = img.imread(args.image)
except FileNotFoundError as err:
    print(err)
    exit(-1)

try:
    file = open(args.filename, 'w')
except OSError as err:
    print("Error creando archivo")
    print(err)
    exit(-1)

print("[*] Escribiendo Archivo")
for i in range(0, args.size):
    if i < imagen.shape[0]:
        file.write("{:013b}\n".format(imagen[i,args.columna]))
    else:
        file.write("{:013b}\n".format(0))

print("[*] Archivo escrito con exito")