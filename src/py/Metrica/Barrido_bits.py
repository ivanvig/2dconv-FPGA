import matplotlib.image as img
import matplotlib.pylab as plt
import numpy as np
import funciones as fun
import imgconv as ivn

# CAMBIARRRR PATH
img_path = "D:/Documents/Tarpuy/Procesamiento-R/2dconv-verilog/src/py/Metrica/img/da_bossGS.jpg"
input_img = img.imread(img_path)

# Filtro para la convolucion
kernel = np.array(
    [
        [0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]
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
# Cambio de rango a la convolucion original
Conv_original = ivn.torange(Conv_original, 1, 0)
# normailzar el kernel
ker_iv = np.asarray(ivn.ker_norm(kernel))

print 'nuevo kernel\n', ker_iv

# representacion del kernel en punto fijo
ker_fix2 = np.asarray(fun.fix_matriz(ker_iv, 8, 7, 'S', 'round', 'saturate'))

# imagen modificada en rango (1,0) y pasada a punto fijo
input_S = np.asarray(ivn.torange(input_img, 1, 0))
# imagen en Punto fijo
img_fix = np.asarray(fun.fix_matriz(input_S, 8, 7, 'S', 'round', 'saturate'))

# convolucion
Conv_2 = fun.cross_corr(img_fix, ker_fix2)

Conv_fix2 = np.asarray(fun.fix_matriz(np.asarray(Conv_2), 20, 14, 'S', 'round', 'saturate', 1))

# comparacion
SNR1 = []
SNR2 = []
Signal = fun.potencia(Conv_original)

# defino vectores
vec = np.arange(8, 15, 1)

for i in xrange(8, 15):
    Conv_fix = fun.pos(Conv_fix2, 20, int(i))
    Conv_fix = ivn.torange(Conv_fix, 1, 0)
    Conv_fix = Conv_original - Conv_fix
    Noise = fun.potencia(Conv_fix)
    SNR1.append(Signal / Noise)

print 10*np.log10(SNR1)

plt.plot(vec, 10*np.log10(SNR1), label="Corte_Pos")
plt.title('Comparacion Orginal y Fixed')
plt.ylabel('Diferencia')
plt.xlabel('cantidad de bits salida')
plt.grid(True)
plt.legend(loc="upper left")
plt.show()
