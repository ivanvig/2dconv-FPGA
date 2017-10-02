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

img_path = "D:/Documents/Tarpuy/Python/Procesamiento/img/da_bossGS.jpg"
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
ker_fix = np.asarray(fun.fix_matriz(kernel, 8, 0, 'S', 'round', 'saturate'))  # kernel a punto fijo

input_S = fun.norm_m(input_img, 'l2')  # fincion normalizada l2
SNR1 = []
f_vec = np.arange(4, 10, 1)  # rango de iteracion

for i in f_vec:
    img_fix = np.asarray(fun.fix_matriz(input_S, i, i, 'U', 'round', 'saturate'))
    input_N = fun.cross_corr(img_fix, ker_fix)
    input_N = fix1 - input_N  # diferencia entre original y nueva
    Noise = fun.potencia(input_N)
    SNR1.append(Signal / Noise)

print "end 1..."


# nomralizacion con 'l2'

input_S = np.asarray(fun.norm_m(input_img, 'l1'))  # fincion normalizada
SNR2 = []
for i in f_vec:
    img_fix = np.asarray(fun.fix_matriz(input_S, i, i, 'U', 'round', 'saturate'))
    input_N = fun.cross_corr(img_fix, ker_fix)
    input_N = fix1 - input_N
    Noise = fun.potencia(input_N)
    SNR2.append(Signal / Noise)

print "end 2..."
# convolucion para con noramlizacion 'l1'


input_S = np.asarray(ivn.torange(input_img, 1, 0))
SNR3 = []

for i in f_vec:
    img_fix = np.asarray(fun.fix_matriz(input_S, i, i, 'U', 'round', 'saturate'))
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

"""
imagel2 = fun.norm_m(input_img, 'l2')
imagel2 = np.asarray(fun.fix_matriz(imagel2, 8, 8, 'U', 'round', 'saturate'))
fix1 = fun.cross_corr(input_img, kernel)
fix2 = fun.cross_corr(imagel2, ker_fix)  # fincion normalizada, kernel)
img_fix = np.asarray(fun.fix_matriz(input_S, 8, 8, 'U', 'round', 'saturate'))
fix3 = fun.cross_corr(img_fix, ker_fix)

fig = plt.figure()
ax = fig.add_subplot(2, 2, 1)
ax.imshow(input_img, cmap="gray")
ax.set_title("Imagen Original")

ax2 = fig.add_subplot(2, 2, 2)
ax2.imshow(fix1, cmap="gray")
ax2.set_title("Despues de filtrar 1")

ax3 = fig.add_subplot(2, 2, 3)
ax3.imshow(fix2, cmap="gray")
ax3.set_title("Imagen con fix2")


ax4 = fig.add_subplot(2, 2, 4)

ax4.imshow(fix3, cmap="gray")
ax4.set_title("Filtrada con punto fijo 3")
plt.show()
"""