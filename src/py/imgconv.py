import numpy as np

def maxpool(img_matrix):
    shape = np.shape(img_matrix)
    out = np.zeros((shape[0]//2, shape[1]//2))
    for i in range(0, shape[0] - 1, 2):
        for j in range(0, shape[1] - 1, 2):
            out[i//2,j//2] = np.amax(img_matrix[i:i+2,j:j+2])

    return out


def cross_corr(input_matrix, kernel_matrix):

    shape_i = np.shape(input_matrix)
    shape_k = np.shape(kernel_matrix)

    # Creamos la matrix de salida iniciada en cero
    output_matrix = np.zeros(np.subtract(shape_i, shape_k) + (1,1)) # Podria romperse si shape(kernel) > shape(input)

    for i in range(0,shape_i[0] - shape_k[0] + 1):
        for j in range(0,shape_i[1] - shape_k[1] + 1):
            output_matrix[i,j] = np.sum(np.multiply(input_matrix[i:i+shape_k[0], j:j+shape_k[1]], kernel_matrix))

    return output_matrix


def torange(matrix, max, min):
    """
    Implements a linear dynamic range expansion
    https://en.wikipedia.org/wiki/Normalization_(image_processing)

    :param matrix:matrix to be normalized
    :param max:desired max value
    :param min:desired min value
    :return:normalized matrix
    """
    amax = np.amax(matrix)
    amin = np.amin(matrix)
    matrix = np.true_divide((matrix-amin)*(max-min), (amax-amin) + min)
    return matrix

def torange_c(matrix, max, min, amax, amin):
    """
    Implements a linear dynamic range expansion
    https://en.wikipedia.org/wiki/Normalization_(image_processing)

    :param matrix:matrix to be normalized
    :param max:desired max value
    :param min:desired min value
    :return:normalized matrix
    """
    # amax = 0.0801  # np.amax(matrix)
    # amin = -0.1  # np.amin(matrix)
    matrix = np.true_divide((matrix-amin)*(max-min), (amax-amin)) + min
    return matrix


def ker_norm(matrix):
    """

    :param matrix:
    :return:
    """
    if np.amin(matrix) * (-1) > np.amax(matrix):
        amax = np.amin(matrix) * (-1)
    else:
        amax = np.amax(matrix)

    matrix = np.true_divide(matrix, amax)
    return matrix

def pos(matrix):
    shape = np.shape(matrix)
    for i in range(shape[0]):
        for j in range(shape[1]):
            # matrix[i][j] = (((matrix[i][j] & 0x7ffff) + 0x40000) >> 7) & 0xfff
            matrix[i][j] = (((matrix[i][j] & 0xfffff) + 0x80000) >> 7) & 0x1fff
    return matrix