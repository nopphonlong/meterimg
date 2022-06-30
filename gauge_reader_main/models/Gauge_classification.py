import os
import numpy as np
import tensorflow as tf
import sys
from gauge_reader_main.models.guage_reading import get_gauge_value

model_name = "gauge_reader_main\models\model_3_2classes.h5"
current_path = os.getcwd()
load_model = tf.keras.models.load_model(r"{}\{}".format(current_path, model_name))


def load_and_prep_image(filename, img_shape=224):
    # Read in target file (an image)
    img = tf.io.read_file(filename)

    # Decode the read file into a tensor & ensure 3 colour channels
    img = tf.image.decode_image(img, channels=3)

    # Resize the image (to the same size our model was trained on)
    img = tf.image.resize(img, size=[img_shape, img_shape])

    # Rescale the image (get all values between 0 and 1)
    img = img / 255.
    return img


# import sys
# lidt_arv=sys.argv[0:3]
# images = load_and_prep_image(lidt_arv[-1])

def getpredict(img):
    loaded_img = load_and_prep_image(img)
    classes = ["chiller_gauge", "not_chiller_gauge"]
    pred_probs = load_model.predict(tf.expand_dims(loaded_img, axis=0))
    pred_label = classes[pred_probs.argmax()]
    percent_confident = 100 * tf.reduce_max(pred_probs)

    return pred_label, percent_confident


def prep_image(img, img_shape=224):
    # Resize the image (to the same size our model was trained on)
    img = tf.image.resize(img, size=[img_shape, img_shape])

    # Rescale the image (get all values between 0 and 1)
    img = img / 255.
    return img