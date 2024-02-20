import cv2 as cv
import numpy as np
from PIL import ImageTk, Image


class ImageProcessor:
    # class initialization
    def __init__(self) -> None:
        self.image = None

    # process_image method uses the path image to return Numpy matrix
    def process_image(self, path) -> np.ndarray:
        try:
            # read the image in gray scale
            self.image = cv.imread(path, cv.IMREAD_GRAYSCALE)
            if self.image is None:
                print("Could not read input image file")
            # image resize to 400x400 pixels
            self.image = cv.resize(self.image, (400, 400))
            # Gaussian blur application
            self.image = cv.GaussianBlur(self.image, (5, 5), 5)
            # histogram equalization
            self.image = cv.equalizeHist(self.image)

            # Erosion
            kernel = np.ones((3, 3), np.uint8)  # matrix 3x3 element creation
            dilate_image = cv.dilate(self.image, kernel, iterations=1)  # dilatation once applied
            eroded_image = cv.erode(dilate_image, kernel, iterations=7)  # erosion

            #  inverse thresholding
            #  pixels with intensity values above the threshold are assigned 0.
            #  and pixels with intensity values below,  255.
            _, self.image = cv.threshold(
                eroded_image, 70, 255, cv.THRESH_BINARY_INV)

            # Region of interest (ROI) creation
            # frame creation:  eliminating border objects
            frame = np.zeros((400, 400), np.uint8)
            frame[50:370, 30:370] = 255

            # bitwise AND operation
            self.image = cv.bitwise_and(self.image, frame)
            # connected component analysis to detect the number of objects in the image
            # within the specified frame
            _, labels = cv.connectedComponents(self.image)

            # objects elimination whose area is less than 200 pixels
            for i in range(1, labels.max() + 1):  # Labels start from 1 because
                # label 0 typically represents the background.
                # binary image creation containing only pixels with the current label 'i'
                binary_image = cv.inRange(labels, np.array([i]), np.array([i]))
                # Find the coordinates of non-zero pixels in the binary image: contour
                contour_coordinates = cv.findNonZero(binary_image)
                # Calculate the area of the contour: the connected component
                contour_area = cv.contourArea(contour_coordinates)
                if contour_area < 200:
                    # Set all pixels belonging to the connected component with label 'i' to 0
                    self.image[labels == i] = 0
                    # and therefore eliminating that object

            return self.image
        except Exception as e:
            print(f"Error processing image: {e}")
            # Return a NumPy array filled with zeros as a placeholder for the processed image
            return np.zeros((400, 400), dtype=np.uint8)

    def get_diagnosis(self):

        # Region selection
        left = self.image[50:370, 30:200]
        right = self.image[50:370, 200:370]
        # Non-zero coordinates finding
        left = cv.findNonZero(left)
        right = cv.findNonZero(right)
        # Extracting y-coordinates
        left = left[:, 0, 1]
        right = right[:, 0, 1]
        # Heights calculation
        height_left = left.max() - left.min()
        height_right = right.max() - right.min()

        if height_left > height_right:
            percentage = ((height_left / height_right) - 1) * 100
            affected_lung = 'left'
        elif height_right > height_left:
            percentage = ((height_right / height_left) - 1) * 100
            affected_lung = 'right'
        else:
            percentage = 0
            affected_lung = 'none'

        return True if percentage > 50 else False, round(percentage, 1), affected_lung, left, right
        # boolean indicating whether the percentage is greater than 50
        # the rounded percentage value
        # lung affected
        # y-coordinates of non-zero pixels in the left and right regions, respectively.

    # OpenCV image conversion to a Tkinter PhotoImage (suitable format for graphical user interface)
    @staticmethod
    def cv_2_tkinter(image):
        # Consistency for image display: resize to 200x200
        resized_image = cv.resize(image, (200, 200))
        # PIL Image from a NumPy array creation
        img_pil = Image.fromarray(resized_image)
        # Tkinter-compatible image creation
        img_tk = ImageTk.PhotoImage(image=img_pil)
        return img_tk
