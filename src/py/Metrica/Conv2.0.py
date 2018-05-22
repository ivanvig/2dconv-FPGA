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



def plot1():

    # imread (path,format)lee una imagen desde un archivo
    # @param string path . path de la imagen
    # @param format.
    # @return numpy.array para escalas grices retorna MxN
    # para RGB retorna MxNx3, RGBA  retorna MxNx4

    # CAMBIARRRR PATH
    img_path = "./img/Lenna.jpg"
    input_img = img.imread(img_path)

    # Filtro para la convolucion
    neg = np.array(
        [
            [-2, -1, 0],
            [-1, 0, 1],
            [0, 1, 2]
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
    conv_neg = fun.cross_corr(input_img, neg)


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
    fig = plt.figure(figsize=(11, 11))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.imshow(conv_neg, cmap="gray")
    plt.axis('off')
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
    plt.show()



def plotimagen():

    img_path = "./img/Lenna.jpg"
    input_img = img.imread(img_path)

    # Filtro para la convolucion
    neg = np.array(
        [
            [0, -1, 0],
            [-1, 1, -1],
            [0, -1, 0]
        ])
    sharpen = np.array(
        [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])

    emboss = np.array(
        [
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
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
    conv_neg = fun.cross_corr(input_img, neg)
    conv_sha = fun.cross_corr(input_img, sharpen)
    conv_emb = fun.cross_corr(input_img, emboss)

    img_neg = img.imread("./img/lenna_negative.png")
    img_sha = img.imread("./img/lenna_sharpen.png")
    img_emb = img.imread("./img/lenna_emboss.png")

    fig, big_axes = plt.subplots( figsize=(15.0, 15.0),nrows=3, ncols=1, sharey=True) 

    for row, big_ax in enumerate(big_axes, start=1):
        big_ax.set_title("Subplot row %s \n" % row, fontsize=16)

        # Turn off axis lines and ticks of the big subplot 
        # obs alpha is 0 in RGBA string!
        big_ax.tick_params(labelcolor=(1.,1.,1., 0.0), top='off', bottom='off', left='off', right='off')
        # removes the white frame
        big_ax._frameon = False


    #for i in range(1,10):
    ax = fig.add_subplot(3, 2, 1)
    ax.imshow(conv_neg, cmap="gray")
    plt.axis('off')

    ax = fig.add_subplot(3, 2, 2)
    ax.imshow(img_neg, cmap="gray")
    plt.axis('off')

    ax = fig.add_subplot(3, 2, 3)
    ax.imshow(conv_sha, cmap="gray")
    plt.axis('off')

    ax = fig.add_subplot(3, 2, 4)
    ax.imshow(img_sha, cmap="gray")
    plt.axis('off')

    ax = fig.add_subplot(3, 2, 5)
    ax.imshow(conv_emb, cmap="gray")
    plt.axis('off')

    ax = fig.add_subplot(3, 2, 6)
    ax.imshow(img_emb, cmap="gray")
    plt.axis('off')

    fig.set_facecolor('w')
    plt.tight_layout()
    plt.show()

def codigoviene():

    fig, big_axes = plt.subplots( figsize=(15.0, 15.0) , nrows=3, ncols=1, sharey=True) 

    for row, big_ax in enumerate(big_axes, start=1):
        big_ax.set_title("Subplot row %s \n" % row, fontsize=16)

        # Turn off axis lines and ticks of the big subplot 
        # obs alpha is 0 in RGBA string!
        big_ax.tick_params(labelcolor=(1.,1.,1., 0.0), top='off', bottom='off', left='off', right='off')
        # removes the white frame
        big_ax._frameon = Falsegsize=(15.0, 15.0)


    for i in range(1,7):
        ax = fig.add_subplot(3,2,i)
        ax.set_title('Plot title ' + str(i))

    fig.set_facecolor('w')
    plt.tight_layout()
    plt.show()


plot1()
#plotimagen()
#codigoviene()


