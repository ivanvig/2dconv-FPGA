import matplotlib.image as img
import matplotlib.pylab as plt
import numpy as np


def all_mem_trasnmission():

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

    # ax1.plot(vec1, naive, color='r', mew= 2, linestyle='-')
    # ax1.plot(vec1, shared_i, color='b', mew= 2, linestyle='-')

    ax1.plot(vec2, x1, '-or',label="Naive",markersize=10)
    ax1.plot(vec2, x2, '-xb',label="Shared inputs", mew= 4,markersize=10)

    ax1.set_title('Storage',fontsize= 20, fontweight='bold')

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    plt.ylabel('Memory space [bytes]', fontsize= 20,fontweight='bold')
    plt.xlabel('MAC Units',fontsize= 20,fontweight='bold')
    plt.xlim((1.8,10.2))
    plt.ylim((min(x2)-0.4,max(x1)+0.4))
    plt.grid(True)
    plt.legend(fontsize=16,loc=2)

    plt.savefig('./mem_space2.eps',bbox_inches = 'tight')
    plt.savefig('./mem_space2.pdf',bbox_inches = 'tight')
    plt.savefig('./mem_space2.jpg',bbox_inches = 'tight')

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
    # ax1.plot(vec1, y1, color='g', mew= 2, linestyle='--')
    # ax1.plot(vec1, y2, color='r', mew=0.01, linestyle='--')
    # ax1.plot(vec1, y3, color='b', mew=0.01, linestyle='--')

    ax1.plot(vec2, x1, '-og',label="naive", markersize=10)
    ax1.plot(vec2, x2, '-xr',label="shared inputs", mew= 4,markersize=10)
    ax1.plot(vec2, x3, '-sb',label="shared inputs with circular shift",markersize=10)

    ax1.set_title('Transmission',fontsize= 20, fontweight='bold')

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    plt.ylabel('Data sent [Kb]', fontsize= 20, fontweight='bold')
    plt.xlabel('MAC Units',fontsize= 20, fontweight='bold')
    plt.xlim((1.8,10.2))
    plt.ylim((1500,5000))
    plt.grid(True)
    plt.legend(fontsize=16,loc=0)

    plt.savefig('./data_sent.eps',bbox_inches = 'tight')
    plt.savefig('./data_sent.pdf',bbox_inches = 'tight')
    plt.savefig('./data_sent.jpg',bbox_inches = 'tight')

    plt.show()

def coplexity():

    naive = []

    norm2 = 28.0  # valor maximo en % BRAM utilizados

    real = [20.0/norm2, 22.0/norm2, 24.0/norm2, 26.0/norm2, 28.0/norm2]

    vec1 = np.arange(2,12,2)
    vec2 = np.arange(2,12,2)

    for i in vec2:
       naive.append((i+18.0)/norm2)


    fig = plt.figure(figsize=(8.5, 8.5))
    plt.xticks(vec2)
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(vec2, naive, color='g',label="Theoretical", mew= 2, linestyle='-')
    ax1.plot(vec1, real, color='b', label="Real",linestyle='None',marker='o',markersize=10)

    ax1.set_title('BRAM Complexity',fontsize= 20,fontweight='bold')

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    plt.ylabel('BRAM Utilization (Normalized)', fontsize= 20, fontweight='bold')
    plt.xlabel('MAC Units',fontsize= 20, fontweight='bold')
    plt.xlim((1.8,10.2))
    plt.ylim((0.70,1.02))
    plt.grid(True,linestyle='--')
    plt.legend(fontsize=16,loc=2)

    plt.savefig('./BRAM_c.eps',bbox_inches = 'tight')
    plt.savefig('./BRAM_c.pdf',bbox_inches = 'tight')
    plt.savefig('./BRAM_c.jpg',bbox_inches = 'tight')


    plt.show()

all_mem_trasnmission()
coplexity()
