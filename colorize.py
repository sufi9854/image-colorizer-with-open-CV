import cv2
import numpy as np
import streamlit as st
from PIL import Image

# Load colorization model
prototxt = 'colorization_deploy_v2.prototxt'
model = 'colorization_release_v2.caffemodel'
points = 'pts_in_hull.npy'

net = cv2.dnn.readNetFromCaffe(prototxt, model)
pts = np.load(points)

class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")

pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype(np.float32)]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def colorize_image(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    img = cv2.imread('grayscale.jpg')
    img_resized = cv2.resize(img, (224, 224))
    img_lab = cv2.cvtColor(img_resized, cv2.COLOR_RGB2Lab)
    l_channel = img_lab[:, :, 0] # Normalize L channel
    l_channel = l_channel.astype("float32") / 255.0
    l_channel -= 0.5
    l_channel *= 2.0
    blob = cv2.dnn.blobFromImage(l_channel)
    net.setInput(blob)
    ab_channels = net.forward()[0, :, :, :].transpose((1, 2, 0))
    # Resize predicted ab channels to original image size
   ab_channels_us = cv2.resize(ab_channels, (img.shape[1], img.shape[0]))

    # Combine original L channel (not normalized) with ab channels
    lab_out = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.float32)
    lab_out[:, :, 0] = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)[:, :, 0]  # L channel in [0-255]
    lab_out[:, :, 1:] = ab_channels_us * 128  # scale ab channels back to proper range

    # Convert LAB to BGR color space
    bgr_out = cv2.cvtColor(lab_out.astype(np.uint8), cv2.COLOR_Lab2BGR)

    # Clip and convert to uint8
    bgr_out = np.clip(bgr_out, 0, 255).astype(np.uint8)

    # Show or save the output
    cv2.imshow("Colorized", bgr_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

