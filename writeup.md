# **Finding Lane Lines on the Road**

## Writeup

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the detectLines(img) function.

My pipeline consisted of 7 steps in my detectLines(img) function.
The function receives an image in BGR and then <br> 1)Creates a grayscale copy <br> 2)Applies a Gaussian blur to it <br> 3)Runs Canny edge detection on it <br> 4)Run Hough Transformation on it and get lines found <br>5)Split these lines up to whether they belong to right or left lane line and ignore others <br> 6)Find 2 points for each lane line, the one closest to camera and one furthest from it, and use them to extrapolate points at bottom of screen and 3/5 the way from the top<br> 7) Draw these lines, and one down the middle, onto a copy of the original image passed in and return it


If you'd like to include images to show how the pipeline works, here is how to include an image:



### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when a line curves the points will cut across the inside of the curve rather than following it.

Another shortcoming could be lighter colored roads or shadows and such too close to the lane lines, (like in the challenge video)


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to use the line segments found with the Hough transformation to extrapolate a couple segments which I then connect rather than have one long extrapolated line, it would fit curves better, or just connect all the segments the Hough transform returns after filtering out which lane line they belong to.

Another potential improvement could be to reduce contrast threshold for Canny edge detection so it better detects and edge between lighter colored road.

Also maybe I could try to tighten the region mask more to where the left and right lane lines are in order to avoid detecting edges off to the side of them
