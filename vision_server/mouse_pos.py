import cv2

# Mouse callback function
def get_pixel_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at position: ({x}, {y})")
        b, g, r = image[y, x]  
        print(f"Pixel BGR color: ({b}, {g}, {r})")


image_path = "TiltedTest.jpg"
image = cv2.imread(image_path)


if image is None:
    print("Error: Unable to load image. Check the file path.")
    exit()

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  
cv2.resizeWindow("Image", 800, 1200)
cv2.imshow("Image", image)


cv2.setMouseCallback("Image", get_pixel_position)


cv2.waitKey(0)
cv2.destroyAllWindows()
