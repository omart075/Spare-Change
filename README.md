# Spare-Change
This Python script uses OpenCV to calculate the amount of change in a given image. Using the left-most coin as a reference object, the size of the other coins are calculated.


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
      
# Note:
A resizing of the image is done prior to calculations. If the image is too large, the contours are thrown off leading to inaccurate data.

# Dependencies:
  1. Install OpenCV:
      * [OpenCV](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
      
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
