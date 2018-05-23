import matplotlib.image as img
import matplotlib.pylab as plt
import numpy as np


def trasnmission():
    
    c = 1600.0 # imagen por pixeles
    k = 3.0
    y1 = [];
    y2 = [];
    y3 = [];

    x1 = []
    x2 = []
    x3 = []


    vec1 = np.arange(2,12,.5)
    for i in vec1:
        y1.append(k*c+6)
        y2.append(((c-i-k+1)/i+1)*(i+k-1))
        y3.append(((c-i-k+1)/i+1)*i)

    vec2= [2, 4, 6, 8, 10]
    for i in vec2:
        x1.append(k*c+6)
        x2.append(((c-i-k+1)/i+1)*(i+k-1))
        x3.append(((c-i-k+1)/i+1)*i)

    
    fig = plt.figure(figsize=(8.5, 8.5))
    
    plt.xticks(vec2)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(vec1, y1, color='g', mew= 2, linestyle='--')
    ax1.plot(vec1, y2, color='r', mew=0.01, linestyle='--')
    ax1.plot(vec1, y3, color='b', mew=0.01, linestyle='--')

    ax1.plot(vec2, x1, color='g',label="naive", linestyle='None',marker='o',markersize=10)
    ax1.plot(vec2, x2, color='r',label="shared inputs", linestyle='None',marker='x', mew= 4,markersize=10)
    ax1.plot(vec2, x3, color='b',label="shared inputs with circular shift", linestyle='None',marker='s',markersize=10)


    ax1.set_title('Transmission',fontsize= 20)

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    plt.ylabel('Data sent [Kb]', fontsize= 20)
    plt.xlabel('Convolution units',fontsize= 20)
    plt.grid(True)
    plt.legend(fontsize=16)
    plt.show()


def coplexity():
    
    naive = []
    
    norm2 = 42.0  # valor maximo en % BRAM utilizados
    
    real = [20.0/norm2, 22.0/norm2, 24.0/norm2, 26.0/norm2, 28.0/norm2]
    
    vec1 = np.arange(2,12,2)
    vec2 = np.arange(2,16,2)
    
    for i in vec2:
       naive.append((i+18.0)/norm2)    


    

    fig = plt.figure(figsize=(8.5, 8.5))
    plt.xticks(vec2)
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(vec2, naive, color='g',label="Theoretical", mew= 2, linestyle='--')
    ax1.plot(vec1, real, color='b', label="Real",linestyle='None',marker='o',markersize=10)
    
    ax1.set_title('BRAM Complexity',fontsize= 20)

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    plt.ylabel('BRAM Utilization (Normalized)', fontsize= 20)
    plt.xlabel('Convolution units',fontsize= 20)
    plt.grid(True)
    plt.legend(fontsize=16)
    plt.show()

def storange():

    naive = []
    shared_i = []
    
    x1 = []
    x2 = []
    
    vec1 = np.arange(2,12,1)
    
    for i in vec1:
        naive.append((3.0*i))
        shared_i.append((i+2.0))    
    
    vec2 = np.arange(2,12,2)

    for i in vec2:
        x1.append((3.0*i))
        x2.append((i+2.0))

    fig = plt.figure(figsize=(8.5, 8.5))

    plt.xticks(vec2)
    ax1 = fig.add_subplot(1, 1, 1)
    
    ax1.plot(vec1, naive, color='r', mew= 2, linestyle='--')
    ax1.plot(vec1, shared_i, color='b', mew= 2, linestyle='--')

    ax1.plot(vec2, x1, color='r',label="Naive",linestyle='None',marker='o',markersize=10)
    ax1.plot(vec2, x2, color='b',label="Shared inputs",linestyle='None',marker='x', mew= 4,markersize=10)

    ax1.set_title('Storage',fontsize= 20)

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    plt.ylabel('Memory space [bytes]', fontsize= 20)
    plt.xlabel('Convolution units',fontsize= 20)
    plt.grid(True)
    plt.legend(fontsize=16)
    plt.show()

#----main-------------------

#trasnmission()
#coplexity()
storange()