import matplotlib.image as img
import matplotlib.pylab as plt
import numpy as np
import funciones as fun
import imgconv as ivn


def pos(matrix):
    shape = np.shape(matrix)
    for i in range(shape[0]):
        for j in range(shape[1]):
            # matrix[i][j] = (((matrix[i][j] & 0x7ffff) + 0x40000) >> 7) & 0xfff
            matrix[i][j] = (((matrix[i][j] & 0xfffff) + 0x80000) >> 7) & 0x1fff
    return matrix


# imread (path,format)lee una imagen desde un archivo
# @param string path . path de la imagen
# @param format.
# @return numpy.array para escalas grices retorna MxN
# para RGB retorna MxNx3, RGBA  retorna MxNx4

# CAMBIARRRR PATH
img_path = "./img/Lenna.jpg"
input_img = img.imread(img_path)

# Filtro para la convolucion
kernel = np.array(
    [
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ])
"""
# filtro gussiano
kernel = np.array(
    [
        [1.0/16.0, 1.0/8.0, 1.0/16.0],
        [1.0/8.0, 1.0/4.0, 1.0/8.0],
        [1.0/16.0, 1.0/8.0, 1.0/16.0]
    ])
# para usar filtro gausiano no normalizar kernel
"""

# convolucon de la senal original
Conv_original = fun.cross_corr(input_img, kernel)
"""
# normailzar el kernel
ker_iv = np.asarray(ivn.ker_norm(kernel))

print 'nuevo kernel\n', ker_iv

# representacion del kernel en punto fijo
ker_fix2 = np.asarray(fun.fix_matriz(ker_iv, 8, 7, 'S', 'round', 'saturate'))

# imagen modificada en rango (1,0) y pasada a punto fijo
input_S = np.asarray(ivn.torange(input_img, 1, 0))
img_fix = np.asarray(fun.fix_matriz(input_S, 8, 7, 'S', 'round', 'saturate'))

# convolucion
Conv_1 = fun.cross_corr(img_fix, ker_fix2)
Conv_2 = fun.cross_corr(img_fix, ker_fix2)

#
Conv_fix = np.asarray(fun.fix_matriz(np.asarray(Conv_2), 20, 14, 'S', 'round', 'saturate'))
Conv_fix2 = np.asarray(fun.fix_matriz(np.asarray(Conv_2), 20, 14, 'S', 'round', 'saturate',1))

Conv_fix2 = pos(Conv_fix2)

# signal = fun.potencia(Conv_original)
# noise = fun.potencia(np.subtract(Conv_original, Conv_fix))

# print 'SNR = %d [dB]' % (np.log10(signal / noise) * 10), signal, noise
"""
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)
ax.imshow(Conv_original, cmap="gray")
ax.set_title("Conv Original")

#ax2 = fig.add_subplot(1, 1, 1)
#ax2.imshow(Conv_1, cmap="gray")
#ax2.set_title("Convolution Python")
"""
ax3 = fig.add_subplot(2, 2, 3)
ax3.imshow(Conv_fix2, cmap="gray")
ax3.set_title("Conv con ki")

ax4 = fig.add_subplot(2, 2, 4)

ax4.imshow(Conv_fix, cmap="gray", vmin=np.amin(Conv_fix), vmax = np.amax(Conv_fix))
ax4.set_title("redondeo saturacion y mas ")
"""
plt.axis('off')
plt.show()
