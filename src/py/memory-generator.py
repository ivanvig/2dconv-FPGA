import matplotlib.image as img
import argparse
from imgconv import *
from Metrica.funciones import fix_matriz

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", help="imagen a leer")
parser.add_argument("-f", "--filename", help="nombre del archivo a crear")
parser.add_argument("-c", "--columna", type=int, help="columna de imagen a guardar")
parser.add_argument("-s", "--size", type=int, default='1024', help="Largo total a escribir, se completa con 0 si la imagen es menor")
parser.add_argument("-p", "--processed", action="store_true",help="columna de la imagen despues de la convolucion")
args = parser.parse_args()


print("[*] Leyendo imagen")
try:
    imagen = img.imread(args.image)
except FileNotFoundError as err:
    print(err)
    exit(-1)
print("[*] Imagen leida")

print("[*] Pasando a rango (1,0)")
imagen = (torange(imagen, 1, 0))
print("[*] Convirtiendo a punto fijo")

if args.processed:
    imagen = np.asarray(fix_matriz(imagen, 8, 7, 'S', 'round', 'saturate'))
    
    kernel = np.array(
        [
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ])
        
    print("[*] Utilizando Kernel")
    print(kernel)
    print("[*] Normalizando Kernel")
    kernel = ker_norm(kernel)
    print("[*] Convirtiendo Kernel a punto fijo")
    kernel = np.asarray(fix_matriz(kernel, 8, 7, 'S', 'round', 'saturate'))
    print("[*] Realizando convolucion")
    imagen = cross_corr(imagen, kernel)
    print("[*] Convirtiendo resultado a punto fijo")
    imagen = np.asarray(fix_matriz(imagen, 20, 14, 'S', 'round', 'saturate', 1))
    print("[*] Volviendo al rango (1,0)")
    imagen = pos(imagen)
else:
    imagen = np.asarray(fix_matriz(imagen, 8, 7, 'S', 'round', 'saturate', 1))

print("[*] Abriendo archivo")

try:
    file = open(args.filename, 'w')
except OSError as err:
    print("[!] Error abriendo archivo")
    print(err)
    exit(-1)

print("[*] Escribiendo Archivo")
for i in range(0, args.size):
    if i < imagen.shape[0]:
        file.write("{:04x}\n".format(imagen[i,args.columna]))
    else:
        file.write("{:04x}\n".format(0))

print("[*] Archivo escrito con exito")
