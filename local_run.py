import os
import sys
from PIL import Image
import matplotlib.pyplot as plt

from bot.utils import is_image, clean_generated_caption
from machine_learning.captioning import CaptioningClass

captioning_class = CaptioningClass('captioning_model_20_epochs.h5')

if len(sys.argv) > 1 and len(os.listdir(sys.argv[1])) > 0:
    print("Found some files in provided directory")
    path_to_images_folder = sys.argv[1]
else:
    print("No valid directory was provided... Processing default directory [images]")
    path_to_images_folder = 'images'

image_name_list = [file_path for file_path in os.listdir(path_to_images_folder) if
                   os.path.isfile(os.path.join(path_to_images_folder, file_path)) and is_image(
                       os.path.join(path_to_images_folder, file_path))]

image_path_list = [os.path.join(path_to_images_folder, image_name) for image_name in image_name_list]

print("Found {} images".format(len(image_path_list)))

for image_path in image_path_list:
    image = Image.open(image_path)
    generated_caption = captioning_class.generate_caption(image)

    cleaned_caption = clean_generated_caption(generated_caption)
    print("Caption for: ", image_path, " is: ", cleaned_caption)
    plt.imshow(image)

    plt.title(image_path)
    plt.show()
