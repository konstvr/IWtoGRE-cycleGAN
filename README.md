<p align="center">
    <img width="400" src="https://github.com/user-attachments/assets/1d0d21f4-d0e5-464f-bb5d-17dbf068bfa5">
</p>

# Synthetic T2*-weighted gradient echo from intermediate-weighted fat suppressed sequences of the knee 

## About The Model
This Generative Adversarial Network is a first-of-its-kind machine learning model that synthesizes T2* W Gradient Echo from Intermediate Weighted fat-suppressed images of the knee. It is based on the cycleGAN architecture and has been trained on a dataset consisiting of knee examinations from 820 patients (15000+ images). As recommended by the [Checklist for Artificial Intelligence in Medical Imaging (CLAIM)](https://pubs.rsna.org/page/ai/claim) this repository contains the trained model and a UI, which can be used to quickly create T2*W from IW images.

## Get started 
> [!NOTE]
> **NO PROGRAMMING SKILLS REQUIRED**.

To synthesize T2*W images from IW (PNG or DICOM) you can use the proposed application which contains a user-friendly interface. Follow these steps:
1. Download and unzip the application from [here](https://www.dropbox.com/scl/fo/1w580c9vc95a0gjueb075/AGWecQ02kEJ4c6huiWEZ75I?rlkey=jy0ucugphk2wtp7kxcj1ey6jy&st=jdi9aypx&dl=0)
2. Download the [model](/models) and unzip it in the same directory as the application. The directory should have this structure:
   - IW-T2*W/
     - IWtoGRE.exe
     - logo.png
     - models/4b300e11055i/gre_generator/
       - assets/
       - variables/
       - keras_metadata.pb
       - saved_model.pb 
3. Execute IWtoGRE.exe

![image](https://github.com/user-attachments/assets/eb2fef8f-ecc3-4854-9f4e-d1e147c18da1)

4. In the field "Select source folder", select the folder containing the IW images (DICOM or PNG)
5. In the field "Select output folder", select the folder where the generated T2*W Gradient Echo images will be saved
6. Click "Convert and Save"
7. In the specified output folder you will find 2 folders: ".-tse2d1_5" and "predicted", which contain the PNG IW and T2*W images respectively.

## Troubleshooting
1. Make sure your directory has the structure described above
2. If you are using DICOM images, try one of the following:
   - Make sure that your .dicom files have .SequenceName="tse2d1_5". If they have a different name you can modify [this line](https://github.com/konstvr/IWtoGRE-cycleGAN/blob/f57dab8c398e17828958e4318edb9278778f92e1/iw2gre.py#L185) in the [application's script](iw2gre.py)
   - Convert your .dicom images to .png before feeding them to the model

## For users with programming knowledge
The repository contains the [python code](iw2gre-train.ipynb) that was used to train the model, as well as the [application's script](iw2gre.py). 

## Disclaimer
>[!CAUTION] 
>This model has not been tested for clinical use. Use at your own risk
#### The material in this site is distributed under the [MIT license](https://opensource.org/license/mit)

## Please cite:
When using the code, trained model or GUI please cite "Vrettos K, Vassalou EE, Karantanas AH, Klontzas ME, Deep learning generated T2*-weighted gradient echo sequences for the evaluation of the knee, ..., Under review, 2024"
