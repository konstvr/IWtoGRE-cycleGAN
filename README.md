![image](https://github.com/user-attachments/assets/c7c9d55e-311d-4733-a3df-4eaca117df8c)

# Synthetic T2*-weighted gradient echo from intermediate-weighted fat suppressed sequences of the knee 

## About The Model
This Generative Adversarial Network is a first-of-its-kind machine learning model that synthesizes T2* Gradient Echo (GRE) from Intermediate Weighted fat-suppressed images of the knee. It is based on the cycleGAN architecture and has been trained on a dataset consisiting of knee examinations from 820 patients (15000+ images). As recommended by the [Checklist for Artificial Intelligence in Medical Imaging (CLAIM)](https://pubs.rsna.org/page/ai/claim) this repository contains the trained model and a UI, which can be used to quickly create GRE from IW images.

## Get started
To synthesize GRE images from IW (PNG or DICOM) you can use the proposed application which contains a user-friendly interface. Follow these steps:
1. Download the [application's script](ui.ipynb) and [logo](logo.png)
2. Download the dll_x64
3. Download the [model](/models) and unzip it in the same directory as the application. The directory should have this structure:
   - IW-GRE/
     - ui.py
     - logo.png
     - models/4b300e11055i/gre_generator/
       - assets/
       - variables/
       - keras_metadata.pb
       - saved_model.pb 
4. Execute ui.py

![image](https://github.com/user-attachments/assets/f077b5a0-58b8-48e6-8a19-2b804a8d3dd0)

5. In the field "Select source folder", select the folder containing the IW images (DICOM or PNG)
6. In the field "Select output folder", select the folder where the generated GRE images will be saved
7. Click "Convert and Save"
8. In the specified output folder you will find 2 folders: ".-tse2d1_5" and "predicted (GRE)", which contain the PNG IW and GRE images respectively.

## Troubleshooting
1. Make sure your directory has the structure described above
2. If you are using DICOM images, try one of the following:
   - Make sure that your .dicom files have .SequenceName="tse2d1_5". If they have a different name you can modify the line XX in [application's script](ui.ipynb)
   - Convert your .dicom images to .png before feeding them to the model

## Disclaimer
>[!CAUTION] 
>This model has not been tested for clinical use. Use at your own risk
#### The material in this site is distributed under CC-BY-NC-ND v 4.0 license https://creativecommons.org/licenses/by-nc-nd/4.0/

## Please cite:
When using the code, trained model or GUI please cite "Vrettos K, Vassalou EE, Karantanas AH, Klontzas ME, Deep learning generated T2*-weighted gradient echo sequences for the evaluation of the knee, ..., Under review, 2024"
