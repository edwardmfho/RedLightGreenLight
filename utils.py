"""
utils.py

Include utilities being use in the main script
"""

from pydub import AudioSegment
import cv2
# Source Code: 
# https://stackoverflow.com/questions/51434897/how-to-change-audio-playback-speed-using-pydub


def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def display_killer_frame(frame):
	cv2.imshow("Killer Cam", frame)