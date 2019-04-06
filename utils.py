from pathlib import Path
from PIL import Image
from io import BytesIO
import requests
import numpy as np
from math import floor
import cv2

import dlib
from dlib_models import download_model, download_predictor, load_dlib_models
download_model()
download_predictor()
from dlib_models import models

load_dlib_models()
face_detect = models["face detect"]
face_rec_model = models["face rec"]
shape_predictor = models["shape predict"]

path_images = Path("pictures")

def download_filter(url, username):
    try:
        r = requests.get(url)
        suffix = Path(url).suffix
        if suffix.find("?") != -1:
            suffix = suffix[:suffix.find("?")]
        filename = "{}{}".format(username, suffix)
        try:
            Image.open(BytesIO(r.content))
        except: 
            return False, "{} is not an image!".format(url)
        with open(path_images / filename, mode="wb") as f:
            f.write(r.content)
        return True, filename
    except requests.exceptions.ConnectionError:
        return False, "URL does not exist"
    except requests.exceptions.MissingSchema:
        return False, "Please include an url in the form https://xxx or http://xxx"
    except:
        return False, "Internal error"

def download_image(url):
    try:
        r = requests.get(url)
        return True, "",Image.open(BytesIO(r.content))
    except requests.exceptions.ConnectionError:
        return False, "URL does not exist", None
    except requests.exceptions.MissingSchema:
        return False, "Please include an url in the form https://xxx or http://xxx", None
    except:
        return False, "Internal error", None

def apply_overlay(background, foreground, settings):
    # TODO: rotate according to orientation of face
    detections = list(face_detect(np.array(background)))
    for detection in detections:
        width_after = detection.width()*settings.width_ratio
        height_after = detection.height()*settings.height_ratio

        foreground_resized = foreground.resize((floor(width_after), floor(height_after)), Image.BICUBIC)
        foreground_resized = foreground_resized.rotate(-settings.rotation)

        left_after = detection.left()-detection.width()*(settings.width_ratio-1)/2
        left_after += settings.x_shift*width_after

        top_after = detection.top()-detection.height()*(settings.height_ratio-1)/2
        top_after += settings.y_shift*height_after
        try:
            background.paste(foreground_resized, (floor(max(0, left_after)), 
                                                floor(max(0, top_after))), 
                            foreground_resized)
        except:
            background.paste(foreground_resized, (floor(max(0, left_after)), 
                                                  floor(max(0, top_after))))
            
                        
    io_buffer = BytesIO()
    background.save(io_buffer, "JPEG")
    io_buffer.seek(0)
    return io_buffer

def process_image(img):
    if np.array(img).shape[2] == 3: # no transparency
        return remove_background(img)
    return img

def remove_background(img):
    BLUR = 15
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 40
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    
    img = np.array(img)
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    #-- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    #-- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    _, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Previously, for a previous version of cv2, this line was: 
    #  contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Thanks to notes from commenters, I've updated the code but left this note
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    masked = np.concatenate((img, mask[:,:,np.newaxis]), axis=2).astype('uint8')
    return Image.fromarray(masked)