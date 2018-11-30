# **Finding Lane Lines on the Road**

Overview
---
[//]: # (Image References)

[img]: ./test_images/solidWhiteRight.jpg "Input"

[outImg]: ./test_images_output/solidWhiteRight.jpg "Ouput"

This project includes a Jupyter Notebook with the  same code as in LineDetect.py so you can run it how you prefer.

It will run through all the images stored in test_images
and create a copy of each with lane lines drawn on as well as a line down the middle in a folder named test_images_output(this folder will be created if it doesn't exist and overwritten if it does).


It then also runs though all the videos in test_videos
and draws similar lines on each frame of each video before saving it to
test_videos_output(this folder will be created if it doesn't exist and overwritten if it does).

The four directories test_images_output and test_videos_output already have example output corresponding to the images and videos in test_images and test_videos

Example input image:

![img]

Corresponding output image:
![outImg]
