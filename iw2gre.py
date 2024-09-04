#!/usr/bin/env python
# coding: utf-8

# In[9]:


import matplotlib.pyplot as plt
import numpy as np


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, optimizers, Sequential, metrics
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
import os
import random
import imageio

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Label
import os
from random import choice
from PIL import Image, ImageTk

import pydicom
from PIL import Image
from pydicom.pixel_data_handlers.util import apply_voi_lut
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pydicom.encoders.gdcm
import pydicom.encoders.pylibjpeg


# In[10]:


main_path = os.path.join(os.getcwd(), "models\\4b300e11055i")

GRE_generator_weights = keras.models.load_model(main_path+'\\gre_generator')


# In[11]:


#Convert DICOM to PNG
def read_xray(path, voi_lut = True, fix_monochrome = True):
    dicom = pydicom.read_file(path)
    
    # VOI LUT (if available by DICOM device) is used to transform raw DICOM data to "human-friendly" view
    if voi_lut:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    #else:
        #data = dicom.pixel_array
               
    # depending on this value, X-ray may look inverted - fix that:
    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data
        
    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * 255).astype(np.uint8)
        
    return data

def convert_and_save_image(image_path, output_path):
    image = read_xray(image_path)
    image_name = image_path.split("\\")[-1].split(".")[0]
    image_name = image_name+ '.png'
    
    plt.imsave(output_path +'/'+image_name, image, cmap='gray') # For colour images
    #cv2.imwrite(output_path +'/'+image_name, image) #For grayscale images
    
    
#EDITED
def folder2png(base_source_path, output_folder_base, folder_p, sequence):
    
    #Remove the parts that only contain numbers from base
    parts = base_source_path.split("\\")
    filtered_parts = [part for part in parts if not part.isdigit()]
    base_source_path = "\\".join(filtered_parts) if filtered_parts else ""
    
    #create the output path
    output_folder = os.path.join(output_folder_base, os.path.relpath(folder_p, start=base_source_path))
    output_folder_parts = output_folder.split("\\")[:-1]  # Get all parts except the last
    output_folder_parts.append(output_folder.split("\\")[-1] + sequence.replace("*", "-"))  # Add suffix to last part
    output_path = "\\".join(output_folder_parts)
    os.makedirs(output_path, exist_ok=True)  # Create output folder if needed
    
    #access the images in each exam
    for dicomImg in os.listdir(folder_p):
        image_path = os.path.join(folder_p, dicomImg)
        
        # Convert and save the image
        convert_and_save_image(image_path, output_path)


# In[12]:


def preprocess_image(image):
    image= tf.image.decode_png(image, channels=1)
    image = tf.image.resize(image, [256, 256])
    image = (image-127.5)/127.5
    return image

def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)

def preprocess_image_T2(image):
    image = tf.image.decode_png(image, channels=1)
    image = tf.image.resize(image, [256, 256])
    image = (image-127.5)/127.5 
    return image

def load_and_preprocess_image_T2(path):
    image = tf.io.read_file(path)
    return preprocess_image_T2(image)


# In[14]:


#Generate predictions
def generate_predictions(target_folder):
    for root, _, images in os.walk(target_folder):
    
        pd_folder=""
        me2d_folder=""

        if len(images)>0 and "png" in images[0]:
            #if "tse" in root:
            pd_folder = root

            single_patient_pd_tse = []

            #IW images
            patient_pd_images = [os.path.join(pd_folder,fil) for fil in os.listdir(pd_folder) if fil.endswith(".png")]
            single_patient_pd_tse.extend(patient_pd_images)

            print(len(single_patient_pd_tse))
            single_patient_pd_tse = [str(path) for path in single_patient_pd_tse]
            ds_T1 = tf.data.Dataset.from_tensor_slices((single_patient_pd_tse))
            dataset_T1 = ds_T1.map(load_and_preprocess_image)

            # Create the output folder for predicted images if it doesn't exist
            out_folder_parts = root.split("\\")[:-1]  # Get all parts except the last
            out_folder_path = "\\".join(out_folder_parts)
            predicted_folder_path = os.path.join(out_folder_path, "predicted (GRE)")
            os.makedirs(predicted_folder_path, exist_ok=True)

            #Build Database
            BATCH_SIZE = 1
            dataset = tf.data.Dataset.zip(dataset_T1).batch(BATCH_SIZE)

            for i,img in enumerate(dataset):            
                prediction = GRE_generator_weights(img, training=False)[0].numpy()
                prediction = (prediction * 127.5 + 127.5).astype(np.uint8)
                prediction = cv2.resize(prediction, (512, 512), interpolation = cv2.INTER_CUBIC)

                #Save predicted image
                # Create a unique filename based on the index
                filename =f"{i}.png"  # Or customize filename format
                cv2.imwrite(os.path.join(predicted_folder_path, filename), prediction)

            #display results label
            result_label.config(text="Images converted successfully!")

def convert_images(source_folder, target_folder):#, image_type):
    main_path = source_folder

    for root,_,exams in os.walk(main_path):
    
        pd_folder=""
        
        if len(exams)>0 and "dcm" in exams[0]:
            dcm_file = pydicom.dcmread(os.path.join(root,exams[0]))
            try:
                sequence1 = dcm_file.SequenceName
            except:
                continue
                
            if "tse2d1_5" in sequence1 or ("tseR2d1_7" in sequence1 and "pd_tse_sag" in dcm_file.SeriesDescription):#Prisma tseR2d1_7
                pd_folder = root
    
                folder2png(source_folder, target_folder, pd_folder, sequence1)
                generate_predictions(target_folder)
        elif len(exams)>0 and "png" in exams[0]:
                generate_predictions(target_folder)

def select_origin_folder():
    folder_path = filedialog.askdirectory()
    folder_path_label.config(text=folder_path)
    
def select_output_folder():
    folder_path = filedialog.askdirectory()
    save_path_label.config(text=folder_path)

def convert_and_save():
    source_folder = folder_path_label.cget("text")
    target_folder = save_path_label.cget("text")
    if source_folder and target_folder: #and image_type:
        convert_images(source_folder, target_folder)#, image_type)
    else:
        result_label.config(text="Please provide all required information.")
        
def show_random_image(img_folder):
    """
    This function displays a random image from the given folder in a Tkinter window.

    Args:
      img_folder (str): Path to the folder containing images.
    """
    # Get list of image files in the folder
    images = [f for f in os.listdir(img_folder) if os.path.isfile(os.path.join(img_folder, f))]

    # Check if there are any images
    if not images:
        print("No images found in the folder!")
        return

    # Select a random image
    random_image = choice(images)

    # Create the full path to the image
    image_path = os.path.join(img_folder, random_image)
    print(image_path)

    # Load the image using Pillow
    image = Image.open(image_path)

    # Convert the image to a format compatible with Tkinter
    image = ImageTk.PhotoImage(image)

    # Create a label to display the image
    randomImage_label = tk.Label(root, text="Sample Med image:")
    label = Label(root, image=image)
    randomImage_label.pack()
    label.pack()
    
    # Keep a reference to the image object
    root.image = image

# Initialize the main window
root = tk.Tk()
root.title("IW to GRE Converter")

# Set a minimum size for the window
root.minsize(300, 100)
font_tuple = ("Helvetica", 15, "bold") 

# Add some padding to the main window
root.configure(padx=20, pady=20)
s = ttk.Style()
s.configure('.', font=('Helvetica', 12))

# If the image is a JPG (requires Pillow)
image = Image.open("logo.png")
logo_image = ImageTk.PhotoImage(image)
root.iconphoto(False, logo_image)

# Load the image (replace 'path_to_your_image.jpg' with your image file path)
image = Image.open("logo.png")  # Use your image file here
image = image.resize((100, 120), Image.Resampling.LANCZOS)  # Resize the image to fit nicely
logo_image = ImageTk.PhotoImage(image)

# Define a style object
style = ttk.Style()

# Define a font style
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Image Label (display the image in a label in column 0, spanning multiple rows)
image_label = tk.Label(root, image=logo_image)
image_label.grid(row=0, column=0, rowspan=4, padx=(0, 10), pady=(0, 5))

# Folder selection label
folder_label = ttk.Label(root, text="Select source folder:")
folder_label.grid(row=0, column=1, sticky="w", pady=(0, 5))

# Folder path display
folder_path_label = ttk.Label(root, text="")
folder_path_label.grid(row=1, column=1, sticky="w")

# Browse button for source folder
browse_button = ttk.Button(root, text="Browse", command=select_origin_folder)
browse_button.grid(row=1, column=2, padx=(10, 0), pady=(0, 5))

# Output folder selection label
output_folder_label = ttk.Label(root, text="Select output folder:")
output_folder_label.grid(row=2, column=1, sticky="w", pady=(10, 5))

# Output folder path display
save_path_label = ttk.Label(root, text="")
save_path_label.grid(row=3, column=1, sticky="w")

# Browse button for output folder
save_path_button = ttk.Button(root, text="Browse", command=select_output_folder)
save_path_button.grid(row=3, column=2, padx=(10, 0), pady=(0, 10))

# Convert and Save button (regular tk.Button with custom background and font)
convert_button = tk.Button(root, text="Convert and Save", command=convert_and_save, bg="green", fg="white", font=("Arial", 12))
convert_button.grid(row=4, column=0, columnspan=3, pady=(10, 5))

# Result label to display the status of the conversion
result_label = ttk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=3, pady=(5, 0))

#License label
lisense_label = ttk.Label(root, text="\u00A9 KV CC-BY-NC-ND license")
lisense_label.grid(row=6, column=0, columnspan=3, pady=(5, 0))
lisense_label.configure(font=('Helvetica', 10))

# Start the main event loop
root.mainloop()


# In[ ]:




