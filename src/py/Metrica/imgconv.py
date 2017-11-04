import numpy as np


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
    matrix = np.true_divide((matrix-amin)*(max-min), (amax-amin)) + min
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