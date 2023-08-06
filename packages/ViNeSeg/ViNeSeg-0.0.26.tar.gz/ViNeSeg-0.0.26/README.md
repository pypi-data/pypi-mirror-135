# Active Neuron Segmentation: beta version
Automated pipeline for AI-assisted Neuron segmentation.
This includes:
* Preprocessing of the loaded images
* Prediction on preprocessed images with MONAI
* Saving of prediction as csv or json-file. The json-file can be used
as input for the LabelMe labeling tool.

## Installation
Before we can use the program, we must set up our own conda Environment.
Therefore execute the following command in the console, after going in the repo:
```conda env create -n monai -f monai.yml```.
Afterwards type into the console
```conda activate monai```.

## Visualize the preprocessed images
The quality and image properties between the Calcium images differ a lot. Therefore we apply automatically
the CLAHE and NL-means algorithm before we feed the images into the neural network.
To visualize for the user, how the preprocessed images looks like, you can save the preprocessed images
with the script ```save_preprocessed_images.py```. The variabels path_channel_one, path_channel_two and path_image_folder
must be changed in the script to your local system.
Depending of the image, the preprocessing step has a high influence to the visibility of neurons. 
Compare the original image <br>
<img src="Img_190124_spon_15-14-32_moco_original.png#center" width="30%" height="30%" /> <br>
with the preprocessed one <br>
<img src="Img_190124_spon_15-14-32_moco_preprocessed.png#cenetr" width="30%" height="30%" /><br>

## Prediction
1. Be sure that you have a folder with a already trained model. This folder must have as content a json-file with 
the model hyperparameters and two folders called trained_weights and trained_weights_swa, where the weights are stored.<br>
2. Go into the folder ai_pipeline and change the variabels in config_prediction.json to your local system. <br>
3. Start the script ```prediction.py --path_config_file config_prediction.json```. <br>

## Load Polygons in LabelMe
The predicted neurons in json-format are stored in the prediction folder.
Together with the original image it can be loaded in LabelMe for further labeling. In some cases it make sense to use the preprocessed images 
instead of the original images.