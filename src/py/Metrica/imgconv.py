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
    matrix = np.true_divide((matrix-amin)*(max-min), (amax-amin) + min)
    return matrix

