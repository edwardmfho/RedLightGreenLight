"""
Replicate The Red Light Green Light Game in Squid Game with
OpenCV


"""
from constant import music_path, gun_shot_path
from utils import speed_change
from pydub import AudioSegment
from pydub.playback import play
import threading


import imutils
import cv2
import random
import time
import datetime

class RedLightGreenLight:
	def __init__(self):
		# self.threshold = float(threshold)
		self.bg_music = AudioSegment.from_file(music_path)
		self.gun_shot = AudioSegment.from_file(gun_shot_path)

	def start_camera(self):
		pass


	def random_play_music(self):
		"""
		Play the music at random speed
		"""
		play_speed = random.uniform(1.0, 1.5)
		print(f'Playback Speed: {play_speed}')
		adjusted_sound = speed_change(sound=self.bg_music, 
									  speed=play_speed)
		play(adjusted_sound)

	def play_gun_shot(self,):
		self.sema.acquire()
		play(self.gun_shot)
		time.sleep(5)
		self.sema.release

	def game_start(self):
		cam = cv2.VideoCapture(0)
		movement = False

		while True:
			self.random_play_music()
			t_end = time.time() + 60 * .3 # 12 seconds
			firstFrame = None
			movement = False
			maxthreads = 1
			self.sema = threading.Semaphore(value=maxthreads)
			self.threads = list()			

			while time.time() < t_end: # change to while NO moment for X seconds

				text = "No movement detected"
				detection_time = t_end
				check, frame = cam.read()

				frame = imutils.resize(frame, width=500)
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (21, 21), 0)

				if firstFrame is None:
					firstFrame = gray
					continue
				# compute the absolute difference between the current frame and
				# first frame
				frameDelta = cv2.absdiff(firstFrame, gray)
				thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
				# dilate the thresholded image to fill in holes, then find contours
				# on thresholded image
				thresh = cv2.dilate(thresh, None, iterations=2)
				cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
					cv2.CHAIN_APPROX_SIMPLE)
				cnts = imutils.grab_contours(cnts)
				# loop over the contours
				for c in cnts:
					# if the contour is too small, ignore it
					if cv2.contourArea(c) < 2000:
						continue
					# compute the bounding box for the contour, draw it on the frame,
					# and update the text
					(x, y, w, h) = cv2.boundingRect(c)
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					text = "Motion Detected"
					movement = True
					
				# draw the text and timestamp on the frame
				cv2.putText(frame, "Weapon: {}".format(text), (10, 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
					(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
				# show the frame and record if the user presses a key
				cv2.imshow("Killer Cam", frame)
				# if text == 'Motion Detected':
				# 	play(self.gun_shot)
				
				if movement:
					firstFrame = gray
					t = threading.Thread(target=self.play_gun_shot, args=())
					self.threads.append(t)
					t.start()
						
				movement = False		
				key = cv2.waitKey(1)
				if key == 27:
					break

		cam.release()
		cv2.destroyAllWindows()


rlgl = RedLightGreenLight()
rlgl.game_start()