#!/usr/bin/python


import matplotlib.image as img
import matplotlib.pyplot as plt
from imgconv import *
from tool import _fixedInt

# img_path = "../../img/monarch_in_may.jpg"
img_path = "../../img/da_bossGS.jpg"
# img_path = "../..2dconv-/img/Lenna.png"
input_img = img.imread(img_path)

kernel = np.array(
    [
        [  0,  1,  0 ],
        [  1, -4,  1 ],
        [  0,  1,  0 ],
    ])

# kernel_diag = np.array(
#     [
#         [-1, -1, -1],
#         [-1,  8, -1],
#         [-1, -1, -1]
#     ])


# gaussian_kernel = np.array(
#     [
#         [ 0.077847,	0.123317,	0.077847 ],
#         [ 0.123317,	0.195346,	0.123317 ],
#         [ 0.077847,	0.123317,	0.077847 ]
#     ])

print (np.amax(input_img), np.amin(input_img))
imgnorm = torange(input_img, 1, 0)  # Paso a trabajar entre 0 y 1

print (np.amax(imgnorm), np.amin(imgnorm))

fig = plt.figure()
filtered = cross_corr(imgnorm, kernel)
ax = fig.add_subplot(1, 2, 1)
ax.hist(filtered.flatten(), bins=255, range = (-1.5, 1.5))
ax.set_title("Convolucion")
print(np.amax(filtered), np.amin(filtered))

filtered_shift = torange(filtered, 1, 0)
ax1 = fig.add_subplot(1,2,2)
ax1.hist(filtered_shift.flatten(), bins = 255, range = (-1.5, 1.5))
ax1.set_title("Desplazada")
print(np.amax(filtered_shift), np.amin(filtered_shift))

################## GRAFICO ########################

fig = plt.figure()
ax = fig.add_subplot(2,2,1)
ax.imshow(imgnorm, cmap = "gray", vmin = 0, vmax = 1)
ax.set_title("Imagen Original normalizada")

ax1 = fig.add_subplot(2,2,2)
ax1.imshow(input_img, cmap="gray", vmin=0, vmax=255)
ax1.set_title("Imagen original")


ax2 = fig.add_subplot(2,2,3)
ax2.imshow(filtered, cmap="gray")
ax2.set_title("Imagen filtrada")

ax3 = fig.add_subplot(2,2,4)
ax3.imshow(filtered_shift, cmap="gray", vmin=0, vmax=1)
ax3.set_title("Imagen filtrada y normalizada")
plt.show()







