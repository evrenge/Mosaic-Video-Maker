import cv2
from PokikiAPI import convertFromImage

# Change this to 0 if your camera doesn't open
capture = cv2.VideoCapture(0)

def main():
    while True:
        # Capture frame-by-frame.
        retval, frame = capture.read()

        # Check if there is a valid frame.
        if not retval:
            break

        # Resize the input image.
        image = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        tile_img = convertFromImage(image, {"X": 50, "Y": 50})
        tile_img = cv2.resize(tile_img, (1360, 720))
        # Display the resulting frame.
        cv2.imshow("Tiled Image", tile_img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

if __name__=='__main__':
    main()
