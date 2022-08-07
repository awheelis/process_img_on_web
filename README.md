# image/video processing app
This Flask App takes in an image and flips or rotates it

Hand dataset for detection and segmentation
https://www.kaggle.com/datasets/danieldelro/freihand

Todo:
- figure out why images are downloading locally 
- make background suppression work better on images 
-- there is noise that I don't like
- add tracking to background suppression (use aireal video as a test) 
- Hand detection (img)
-- turn segmentation masks into bounding boxes 
-- train hand detection model 
--- won't be able to train this locally. Might have to put this on the cloud and let it train on an EC2 instance (get an opportunity to run parallelization on GPUs) 
-- deploy model with Heroku (or something else that will do inference for cheap) 
- Hand segmentation (img)
-- repeat process but use binary masks 
-- implement a Unet model 
-- train and run inference
- Hand detection/segmentation (video)
-- add video capability