# import required libraries
import cv2

# Constants
CELL_SIZE = 3

# load the input image
img = cv2.imread('maze3.jpg')

# convert the input image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# apply thresholding to convert grayscale to binary image
ret,thresh = cv2.threshold(gray,70,255,0)
thresh = cv2.resize(thresh, (thresh.shape[1] // CELL_SIZE, thresh.shape[0] // CELL_SIZE))


# Display the Binary Image
#cv2.imshow("Grayscale Image", gray)
cv2.imshow("Binary Image", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()