import cv2
import os
import sys

image_folder = '/projects/sim/data'
video_name = '/home/mrmxyzptlyk/q8ueato/video.avi'

images = [img for img in sorted(os.listdir(image_folder)) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 1, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
