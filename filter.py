import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('images/cutecat.jpg', cv2.IMREAD_GRAYSCALE).astype(float)
height, width = img.shape

plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.axis('off')
plt.imshow(img, cmap='gray', alpha=1.0)

sobel_x = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
]
sobel_y = [
    [-1, -2, -1],
    [ 0,  0,  0],
    [ 1,  2,  1]
]

# adds padding bc sobel edge detector (sed) needs 3x3's
padded = np.pad(img, pad_width=1, mode='edge')

# change across x and y
Gx = np.zeros_like(img)
Gy = np.zeros_like(img)

for i in range(1, height + 1):
    for j in range(1, width + 1):
        # region gets 3x3 grid from image
        region = padded[i - 1:i + 2, j - 1:j + 2]
        # does dot product between sobel array and region,
        # resulting in a value representing an estimated gradient for that pixel
        Gx[i - 1, j - 1] = np.sum(region * sobel_x)
        Gy[i - 1, j - 1] = np.sum(region * sobel_y)

# combines x and y to calculate magnitude change
magnitude = np.sqrt(Gx**2 + Gy**2)
# normalizes between 0-255 for image
magnitude = (magnitude / magnitude.max()) * 255

# plots edge detection example
plt.subplot(1, 3, 3)
plt.imshow(magnitude, cmap='gray')
plt.title("Output Image")
plt.axis('off')

# only shows some vectors
step = 7
# x and y are the positions for the quiver graph
Y, X = np.meshgrid(np.arange(0, Gx.shape[0], step), np.arange(0, Gx.shape[1], step))

# u and v are the vectors for the quiver graph
U = Gx[Y, X]
V = Gy[Y, X]

# plots quiver with vectors scaled down
scaledown = 3000
plt.subplot(1, 3, 2)
plt.axis('off')
plt.title("Edge Vectors")
plt.gca().invert_yaxis()
plt.quiver(X, Y, U / scaledown, V / scaledown, scale=1, color="blue")
plt.imshow(img, cmap='gray', alpha=0.75)

plt.show()

# TODO add threshold magnitude