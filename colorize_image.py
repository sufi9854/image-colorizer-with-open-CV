import cv2
import numpy as np

# Load colorization model
prototxt = 'models/colorization_deploy_v2.prototxt'
model = 'models/colorization_release_v2.caffemodel'
points = 'models/pts_in_hull.npy'

net = cv2.dnn.readNet('models/colorization_deploy_v2.prototxt', 'models/colorization_release_v2.caffemodel')
pts = np.load(points)

class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")

pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype(np.float32)]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def colorize_image(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    img_resized = cv2.resize(img, (224, 224))
    L = img_resized[:, :, 0] - 50  # Normalize L channel
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = img[:, :, 0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    return colorized
