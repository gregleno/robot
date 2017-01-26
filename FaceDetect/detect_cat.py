import numpy as np
import cv2
import sys
import time
from threading import Thread, Event

class VideoStream:
	def __init__(self, src=0):
		self.stream = cv2.VideoCapture(src)
		self.stopped = False
		self.frame_id = 0
		self.finished = False
		self.frame	 = None
		self.event = Event()
                self.sync = False
	def start(self):
		if not self.sync:
                    Thread(target=self.update, args=()).start()
		return self

        def grab(self):
            (grabbed, frame) = self.stream.read()
            frame_id = self.frame_id + 1
            if not grabbed:
                self.finished =  True
            else:
                (self.frame, self.frame_id) = (frame, frame_id) 
            
 
	def update(self):
            while True:
                if self.stopped:
                    break
                self.grab()
                if self.finished:
                    self.stop()
                else:
                    self.event.wait(None)
                    self.event.clear()

            print "decoded {}".format(self.frame_id)
 
	def read(self):
            if self.sync:
                self.grab()
            else:
                self.event.set()
            return (self.frame, self.frame_id, self.finished)

 
	def stop(self):
		self.stopped = True
                self.stream.release()
                self.event.set()


vs = VideoStream(sys.argv[1]).start()
try:

    last = time.time()
    f = 0
    last_frame_id = -1
    cv2.namedWindow( 'frame', cv2.WINDOW_NORMAL );
    detector = cv2.CascadeClassifier(sys.argv[2])
    next_frame = 0
    while(True):
        frame, frame_id, finished = vs.read()
        if finished:
            break
        if frame_id < next_frame:
            continue
        if frame is not None and last_frame_id != frame_id:
            last_frame_id = frame_id
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector.detectMultiScale(gray, scaleFactor=1.3,
                          minNeighbors=5, minSize=(75, 75))

            for (i, (x, y, w, h)) in enumerate(rects):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Cat #{}".format(i + 1), (x, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
		print "found cat"

            f += 1
            if f % 10 == 0:
                fps = float(f) / float(time.time() - last)
                print 'frame %f' % fps

            cv2.imshow('frame',frame)
            key = cv2.waitKey(1) 
            if key & 0xFF == ord('q'):
                break
            if key & 0xFF == ord('s'):
                next_frame = frame_id + 100
    print "processed {}".format(f)
    vs.stop()

finally:
    vs.stop()
    cv2.destroyAllWindows()
