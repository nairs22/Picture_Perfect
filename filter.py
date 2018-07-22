from flask import Flask, render_template, redirect, url_for, send_from_directory, request
from flask_bootstrap import Bootstrap
from PIL import Image
from PIL import ImageChops
from werkzeug.utils import secure_filename
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
images_directory = os.path.join(APP_ROOT, 'images')
thumbnails_directory = os.path.join(APP_ROOT, 'thumbnails')

if not os.path.isdir(images_directory):
    os.mkdir(images_directory)
if not os.path.isdir(thumbnails_directory):
    os.mkdir(thumbnails_directory)

def gray(destination):
    image = Image.open(destination)
    image_gray = image.convert('L')
    #image_gray.save(filename)
    #image_gray.save('/'.join([thumbnails_directory, filename]))
    return image_gray
    #return render_template('upload.html')

def flip(destination):
    #destination = '/'.join([images_directory, filename])
    image = Image.open(destination)
    image_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
    #image_flip.save(filename)
    #image_flip.save('/'.join([thumbnails_directory, filename]))
    return image_flip
    #return render_template('upload.html')

def crop(destination):
    #destination = '/'.join([images_directory, filename])
    image = Image.open(destination)
    box = (15, 20, 60, 60)
    image_crop = image.crop(box)
    #image_crop.save(filename)
    #image_crop.save('/'.join([thumbnails_directory, filename]))
    return image_crop
    #return render_template('upload.html')
def galaxy(destination):
    #destination = '/'.join([images_directory, filename])
    galaxy_filter = Image.open('./images/galaxy.jpg')
    image = Image.open(destination)
    image_galaxy=ImageChops.add(galaxy_filter,image,3,1)
    #image_crop.save(filename)
    #image_crop.save('/'.join([thumbnails_directory, filename]))
    return image_galaxy
