import cv2
import time
# Open Pi Camera
cap = cv2.VideoCapture(2)
# Set auto exposure to false
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, .75)

exposure = 0
count = 0
while cap.isOpened():
    # Grab frame
    ret, frame = cap.read()
    # Display if there is a frame
    if ret:
        cv2.imshow('Frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    # Set exposure manually
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    # Increase exposure for every frame that is displayed
    exposure += 0.5
    time.sleep(.01)
    # print(exposure)
    # count+=1
    # if count >=100:
    #     break

# Close everything
cap.release()
cv2.destroyAllWindows()
