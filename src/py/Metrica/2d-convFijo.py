import matplotlib.image as img
import matplotlib.pylab as plt
import numpy as np
import funciones as fun
import imgconv as ivn

# imread (path,format)lee una imagen desde un archivo
# @param string path . path de la imagen
# @param format.
# @return numpy.array para escalas grices retorna MxN
# para RGB retorna MxNx3, RGBA  retorna MxNx4

img_path = "D:/Documents/Tarpuy/Procesamiento-R/2dconv-verilog/src/py/Metrica/img/da_bossGS.jpg"
input_img = img.imread(img_path)

# Filtro para la convolucion
kernel = np.array(
    [
        [0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]
    ])

# nomralizacion con 'l2'
fix1 = fun.cross_corr(input_img, kernel)  # convolucon de la senal originla
Signal = fun.potencia(fix1)  # potencia de la senal convlucionada
ker_fix = np.asarray(ivn.ker_norm(kernel))
ker_fix = np.asarray(fun.fix_matriz(ker_fix, 8, 7, 'S', 'round', 'saturate'))  # kernel a punto fijo

input_S = fun.norm_m(input_img, 'l2')  # fincion normalizada l2
SNR1 = []
f_vec = np.arange(5, 11, 1)  # rango de iteracion

for i in f_vec:
    img_fix = np.asarray(fun.fix_matriz(input_S, i, i-1, 'S', 'round', 'saturate'))
    input_N = fun.cross_corr(img_fix, ker_fix)
    input_N = fix1 - input_N  # diferencia entre original y nueva
    Noise = fun.potencia(input_N)
    SNR1.append(Signal / Noise)

print "end 1..."


# nomralizacion con 'l2'

input_S = np.asarray(fun.norm_m(input_img, 'l1'))  # fincion normalizada
SNR2 = []
for i in f_vec:
    img_fix = np.asarray(fun.fix_matriz(input_S, i, i-1, 'S', 'round', 'saturate'))
    input_N = fun.cross_corr(img_fix, ker_fix)
    input_N = fix1 - input_N
    Noise = fun.potencia(input_N)
    SNR2.append(Signal / Noise)

print "end 2..."
# convolucion para con noramlizacion 'l1'


input_S = np.asarray(ivn.torange(input_img, 1, 0))
SNR3 = []

for i in f_vec:
    img_fix = np.asarray(fun.fix_matriz(input_S, i, i-1, 'S', 'round', 'saturate'))
    input_N = fun.cross_corr(img_fix, ker_fix)  # np.asarray
    input_N = fix1 - input_N
    Noise = fun.potencia(input_N)
    SNR3.append(Signal / Noise)

print "end 3..."

plt.plot(f_vec, 10*np.log10(SNR1), label="l2")
plt.plot(f_vec, 10*np.log10(SNR2), label="l1")
plt.plot(f_vec, 10*np.log10(SNR3), label="torange")
plt.title('Comparacion Orginal y Fixed')
plt.ylabel('Diferencia')
plt.xlabel('cantidad de bits parte flotante')
plt.grid(True)
plt.legend(loc="upper left")
plt.show()
