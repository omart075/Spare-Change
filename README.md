# Spare-Change
This Python script uses OpenCV to calculate the amount of change in a given image. Using the left-most coin as a reference object, the size of the other coins are calculated.

# Examples
Input:
![Alt text](/sample_imgs/coins1.png?raw=true "Script in Action")

Output:
![Alt text](/sample_imgs/output1.png?raw=true "Script in Action")

Input:
![Alt text](/sample_imgs/coins4.JPG?raw=true "Script in Action")

Output:
![Alt text](/sample_imgs/output2.png?raw=true "Script in Action")

Input:
![Alt text](/sample_imgs/coins5.jpg?raw=true "Script in Action")

Output:
![Alt text](/sample_imgs/output3.png?raw=true "Script in Action")

The arrays shown are the sizes for each coin found in the image. Images used are in sample_imgs and are named coins*


# Steps in Calculation:
  1. Perform Canny edge detection, dilation, and erosion:
      * Dilation and erosion helps close gaps between the edges found
      
  2. Find the contours:
      * Sort contours from left to right, top to bottom. This allows us to distinguish/use the reference coin
      * Ignore insufficiently large contours
      * Compute pixel per metric ratio (determine size of the other coins within the image)
      
  3. Determine which coins were found:
      * Create a dict with each coin (for now: q, d, n, p), its actual size, and value
      * Iterate through the coins found
      * Match each size with sizes in dict
      * For every match, add to a total sum

# Dependencies:
  1. Install [OpenCV](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
      
  2. Install numpy:
  
  ```
    pip install numpy
  ```  
  3. Install Pillow
  
  ```
    pip install Pillow
  ```
  4. Install scipy
  
  ```
    pip install scipy
  ```  
  5. Install imutils:
  
  ```
    pip install imutils
  ```
  
# Note:
A resizing of the image is done prior to calculations. If the image is too large, the contours are thrown off leading to  inaccurate data. Also, images may be rotated due to how the camera was positioned when picture was taken. This is handled as well prior to calculations. Further testing is still in progress to see how the code performs in different scenarios.
