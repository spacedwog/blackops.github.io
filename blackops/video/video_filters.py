# -----------------------------
# video/video_filters.py
# -----------------------------
import cv2

def apply_gray_filter(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)