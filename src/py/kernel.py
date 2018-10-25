import json
import numpy as np
from Metrica import imgconv as ivn
from Metrica import funciones as fun


# main
def kernel_load():
    """
    funcion interaccion con el usuario para cargar el kernel.
    con el fomrato [[k00,k01,k02],[k10,k11,k12],[k20,k21,k22]]
    :return: kernel_load [3], array[3] datos concatenados en punto fijo
    """
    while 1:
        try:
            print "Kernel data ..."
            print "k[[a,b],[c,d]]"
            kernel = raw_input("K:= ")
            kernel = json.loads(kernel)
            if len(kernel[1])*len(kernel[0]) == 9:
                break
        except:
            print "valores invalidos"

    kernel = np.asarray(ivn.ker_norm(kernel))
    kernel = np.asarray(fun.fix_matriz(kernel, 8, 7, 'S', 'round', 'saturate', 1))
    # kernel_data = np.array([0x002000, 0x208020, 0x002000])
    kernel_data = np.array([0, 0, 0])
    for i in range(3):
        for j in range(3):
            kernel_data[i] |= (kernel[i][j] & 0xff) << (16 - 8*j)

    return kernel_data
