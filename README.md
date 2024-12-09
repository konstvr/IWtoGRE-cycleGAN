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
1. Download and unzip the application from [here](https://1drv.ms/u/s!Aq0pDI40ERYOaz3joa6DRpdu8LE?e=DAgPBK)
2. Download the folder [dll_x64](dll_x64)
3. Download the [model](/models) and unzip it in the same directory as the application. The directory should have this structure:
   - IW-T2*W/
     - iw2gre.exe
     - logo.png
     - dll_x64/
     - models/4b300e11055i/gre_generator/
       - assets/
       - variables/
       - keras_metadata.pb
       - saved_model.pb 
4. Execute iw2gre.exe

![image](https://github.com/user-attachments/assets/f077b5a0-58b8-48e6-8a19-2b804a8d3dd0)

5. In the field "Select source folder", select the folder containing the IW images (DICOM or PNG)
6. In the field "Select output folder", select the folder where the generated T2*W Gradient Echo images will be saved
7. Click "Convert and Save"
8. In the specified output folder you will find 2 folders: ".-tse2d1_5" and "predicted", which contain the PNG IW and T2*W images respectively.

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
#### The material in this site is distributed under CC-BY-NC-ND v 4.0 license https://creativecommons.org/licenses/by-nc-nd/4.0/

## Please cite:
When using the code, trained model or GUI please cite "Vrettos K, Vassalou EE, Karantanas AH, Klontzas ME, Deep learning generated T2*-weighted gradient echo sequences for the evaluation of the knee, ..., Under review, 2024"
