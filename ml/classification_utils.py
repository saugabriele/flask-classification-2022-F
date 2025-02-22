"""
This is a simple classification service. It accepts an url of an
image and returns the top-5 classification labels and scores.
"""
import importlib
import json
import logging
import os
import time
import torch
from PIL import Image, ImageEnhance
from torchvision import transforms
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename
import cv2 as cv

from config import Configuration

conf = Configuration()


def fetch_image(image_id):
    """Gets the image from the specified ID. It returns only images
    downloaded in the folder specified in the configuration object."""
    try:
        image_path = os.path.join(conf.image_folder_path, image_id)
        img = Image.open(image_path)
    except FileNotFoundError:
        image_path = os.path.join(conf.upload_image_path, image_id)
        img = Image.open(image_path)
    return img


def get_labels():
    """Returns the labels of Imagenet dataset as a list, where
    the index of the list corresponds to the output class."""
    labels_path = os.path.join(conf.image_folder_path, 'imagenet_labels.json')
    with open(labels_path) as f:
        labels = json.load(f)
    return labels


def get_model(model_id):
    """Imports a pretrained model from the ones that are specified in
    the configuration file. This is needed as we want to pre-download the
    specified model in order to avoid unnecessary waits for the user."""
    if model_id in conf.models:
        try:
            module = importlib.import_module('torchvision.models')
            return module.__getattribute__(model_id)(pretrained=True)
        except ImportError:
            logging.error("Model {} not found".format(model_id))
    else:
        raise ImportError


def classify_image(model_id, img_id):
    """Returns the top-5 classification score output from the
    model specified in model_id when it is fed with the
    image corresponding to img_id."""
    img = fetch_image(img_id)
    model = get_model(model_id)
    model.eval()
    transform = transforms.Compose((
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )))

    # apply transform from torchvision
    img = img.convert('RGB')
    preprocessed = transform(img).unsqueeze(0)

    # gets the output from the model
    out = model(preprocessed)
    _, indices = torch.sort(out, descending=True)

    # transforms scores as percentages
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

    # gets the labels
    labels = get_labels()

    # takes the top-5 classification output and returns it
    # as a list of tuples (label_name, score)
    output = [(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]

    img.close()
    time.sleep(5)
    return output


def create_histogram(image_id, hist_path):
    """Function to create and save the corresponding
    histogram of a specific image in a directory.
    Returns the id of the Histogram."""

    hist_id = "Histogram.JPEG"
    image = os.path.join(conf.image_folder_path, image_id)
    hist = os.path.join(hist_path, hist_id)

    plt.cla()
    img = cv.imread(image)
    vals = img.mean(axis=2).flatten()
    b, bins, patches = plt.hist(vals, 255)
    plt.xlim([0, 255])
    plt.savefig(hist)
    return hist_id


def image_transformation(image_id, transformation_path, color, contrast, brightness, sharpness):
    """Function to perform a transformation on an image
       corresponding to the image_id using the user
       parameters. Return the id of the transformed image."""

    transformation_id = "Modified_" + image_id
    image = os.path.join(conf.image_folder_path, image_id)
    transformed_image = os.path.join(transformation_path, "Modified_" + image_id)

    im = Image.open(image)
    color_enhancer = ImageEnhance.Color(im)
    im = color_enhancer.enhance(color)
    contrast_enhancer = ImageEnhance.Contrast(im)
    im = contrast_enhancer.enhance(contrast)
    brightness_enhancer = ImageEnhance.Brightness(im)
    im = brightness_enhancer.enhance(brightness)
    sharpness_enhancer = ImageEnhance.Color(im)
    im = sharpness_enhancer.enhance(sharpness)

    im.save(transformed_image)
    return transformation_id


def check_path(path):
    """ Function to check if a path already exist
    otherwise it will create the new path."""
    if not os.path.exists(path):
        os.mkdir(path)
    return


def allowed_file(filename):
    """Function to check if the extension of the
    file is valid. In this case it will return True
    otherwise False."""
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_image(image):
    """Function to save the image passed in
    the upload folder"""
    check_path(conf.upload_image_path)
    filename = secure_filename(image.filename)
    image.save(os.path.join(conf.upload_image_path, filename))
    return
