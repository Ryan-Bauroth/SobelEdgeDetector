import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('images/mario.png', cv2.IMREAD_GRAYSCALE).astype(float)
height, width = img.shape

fig, axes = plt.subplots(2, 2, figsize=(7, 7))
axes = axes.flatten()

axes[0].set_title("Original Image")
axes[0].axis('off')
axes[0].imshow(img, cmap='gray', alpha=1.0)

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

# puts magnitude in bins
hist, bin_edges = np.histogram(magnitude, bins=256, range=(0, 256))
# P => % of data at each index
P = hist / np.sum(hist)

# weight[t] => cumulative weight up until t
# same with mean
cumulative_weight = np.cumsum(P)
cumulative_mean = np.cumsum(P * np.arange(256))
total_mean = cumulative_mean[-1]

best_threshold = 0
max_variance = 0

# tries each threshold value
for t in range(1, 256):
    # calculating weights and means for each threshold
    weight0 = cumulative_weight[t]
    weight1 = 1 - weight0
    mean0 = cumulative_mean[t] / weight0 if weight0 != 0 else 0
    mean1 = (total_mean - cumulative_mean[t]) / weight1 if weight1 != 0 else 0

    # trying to maximize between class variance
    between_class_variance = weight0 * weight1 * (mean0 - mean1) ** 2

    if between_class_variance > max_variance:
        max_variance = between_class_variance
        best_threshold = t

binary_image = magnitude > best_threshold

axes[3].imshow(binary_image, cmap='gray')
axes[3].set_title("Otsu's Threshold")
axes[3].axis('off')

# plots edge detection example
axes[1].imshow(magnitude, cmap='gray')
axes[1].set_title("Output Image")
axes[1].axis('off')

# only shows some vectors
step = 7
# x and y are the positions for the quiver graph
Y, X = np.meshgrid(np.arange(0, Gx.shape[0], step), np.arange(0, Gx.shape[1], step))

# u and v are the vectors for the quiver graph
U = Gx[Y, X]
V = Gy[Y, X]

# plots quiver with vectors scaled down
scaledown = 3000
axes[2].axis('off')
axes[2].set_title("Edge Vectors")
axes[2].invert_yaxis()
axes[2].quiver(X, Y, U / scaledown, V / scaledown, scale=1, color="blue")
axes[2].imshow(img, cmap='gray', alpha=0.75)

plt.subplots_adjust(wspace=0.5)
plt.show()