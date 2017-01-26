# import the necessary packages
import picamera
import picamera.array
import time
import cv2
import sys

cascPath = sys.argv[1]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# initialize the camera and grab a reference to the raw camera capture
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.rotation = 180
#    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)
    fc = False
    # capture frames from the camera
#    for frame in camera.capture_continuous(rawCapture, format="bgr",
#                                           use_video_port=True):
    while True:
        with picamera.array.PiRGBArray(camera) as frame:
            camera.capture(frame, 'rgb')
            image = frame.array
            factor = 1
            if factor != 1:
                res = cv2.resize(image, None, fx=factor, fy=factor,
                                 interpolation=cv2.INTER_LINEAR)
            else:
                res = image
            if fc:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray,
                                                     scaleFactor=1.1,
                                                     minNeighbors=5,
                                                     minSize=(30, 30))
                for (x, y, w, h) in faces:
                    cv2.rectangle(res, (int(x/factor), int(y/factor)),
                                  (int(x/factor+w/factor),
                                  int(y/factor+h/factor)),
                                  (0, 255, 0), 2)
                # cv2.imshow("Frame2", gray)

            cv2.imshow("Frame", res)
            key = cv2.waitKey(1) & 0xFF

            frame.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            if key == ord("f"):
                fc = not fc
                print "Face reco: %i " % fc
