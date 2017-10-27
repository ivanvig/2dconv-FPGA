

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
Conv_original = fun.cross_corr(input_img, kernel)  # convolucon de la senal original
Conv_original = np.asarray(ivn.torange(Conv_original, 1, 0))

ker_fix1 = np.asarray(fun.fix_matriz(kernel, 8, 0, 'S', 'round', 'saturate'))  # kernel a punto fijo

ker_iv = np.asarray(ivn.ker_norm(kernel))
print ker_iv
ker_fix2 = np.asarray(fun.fix_matriz(ker_iv, 8, 7, 'S', 'round', 'saturate'))

input_S = np.asarray(ivn.torange(input_img, 1, 0))
img_fix = np.asarray(fun.fix_matriz(input_S, 8, 8, 'U', 'round', 'saturate'))

Conv_1 = fun.cross_corr(img_fix, ker_fix1)  # np.asarray
Conv_2 = fun.cross_corr(img_fix, ker_fix2)
# print np.amax(Conv_2), np.amin(Conv_2)
Conv_fix = np.asarray(fun.fix_matriz(np.asarray(ivn.torange(Conv_2, 1, 0)), 8, 8, 'U', 'round', 'saturate'))
#Conv_fix = np.asarray(fun.fix_matriz(Conv_fix, 8, 8, 'U', 'round', 'saturate'))
signal = fun.potencia(Conv_original)
noise = fun.potencia(np.subtract(Conv_original, Conv_fix))

print signal, noise, np.log10(signal/noise)*10



fig = plt.figure()
ax = fig.add_subplot(2, 2, 1)
ax.imshow(Conv_original, cmap="gray")
ax.set_title("Conv Original")

ax2 = fig.add_subplot(2, 2, 2)
ax2.imshow(Conv_1, cmap="gray")
ax2.set_title("Conv solo img")

ax3 = fig.add_subplot(2, 2, 3)
ax3.imshow(Conv_2, cmap="gray")
ax3.set_title("Conv con ki")


ax4 = fig.add_subplot(2, 2, 4)

ax4.imshow(Conv_fix, cmap="gray")
ax4.set_title("imgane original")
plt.show()
