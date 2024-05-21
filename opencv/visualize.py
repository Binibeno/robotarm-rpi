# forked from: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

from __future__ import print_function
import cv2 as cv
import time
from picamera2 import Picamera2, Preview,MappedArray
import os
import serialapi
import sys
from staticvar import *
from queue import Queue 
from threading import Thread 
import json

def in_virtualenv():
    def get_base_prefix_compat():
        """Get base/real prefix, or sys.prefix if there is none."""
        return (
            getattr(sys, "base_prefix", None)
            or getattr(sys, "real_prefix", None)
            or sys.prefix
        )
    return sys.prefix != get_base_prefix_compat()

if (not in_virtualenv()):
    print("Not in the virtual environment (virtualenv). See start.sh. Run source ~/mp/bin/activate from bash to active the virtual environment.")
    sys.exit()

# fix camera on ssh 
os.environ["DISPLAY"] = ":0"

# -------------------------------
import tkinter as tk
import math
import threading
import queue
import time

def draw_half_circle(canvas, x, y, radius, line_width):
    canvas.create_arc(x - radius, y - radius, x + radius, y + radius, start=0, extent=180, style=tk.ARC, width=line_width)

def draw_connected_lines(canvas, line_length, angle_queue):
    # Create Tkinter window
    root = tk.Tk()
    root.title("Connected Lines")

    # Define scale factor to increase canvas resolution
    scale_factor = 1
    line_width = 2

    # Calculate canvas size based on scale factor
    canvas_width = 800 * scale_factor
    canvas_height = 600 * scale_factor

    center_height = canvas_height / 2
    center_width = canvas_width / 2

    # Create Canvas with increased resolution
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()


    def update_canvas():
        try:
            # Get new angles from the queue
            new_angles = angle_queue.get_nowait()
            if new_angles is not None:
                # Clear canvas
                canvas.delete("all")

                # Redraw half circle
                draw_half_circle(canvas, center_width, center_height - line_length / 2 * scale_factor, line_length / 2 * scale_factor, line_width)


                # Redraw lines
                current_x, current_y = 400, 300 - line_length / 2
                lastAngle = 0
                for newangle in new_angles:
                    lastAngle += newangle
                    angle = lastAngle
                    delta_x = line_length * math.cos(math.radians(angle))
                    delta_y = line_length * math.sin(math.radians(angle))
                    canvas.create_line(current_x, current_y, current_x + delta_x, current_y + delta_y, width=2)
                    current_x += delta_x
                    current_y += delta_y

                # Signal that drawing is finished
                angle_queue.task_done()
        except queue.Empty:
            pass
        except KeyboardInterrupt:
            root.destroy()

        # Schedule the next update after 100 milliseconds
        root.after(100, update_canvas)

    # Start the canvas update loop
    update_canvas()

    root.mainloop()

if __name__ == "__main__":
    line_length = 100

    # Create queue for communication between threads
    angle_queue = queue.Queue()

    # Create and start thread for drawing lines
    draw_thread = threading.Thread(target=draw_connected_lines, args=(None, line_length, angle_queue))
    draw_thread.start()

    angles = [-20, 40, 60]  # List of angles at which the lines connect to each other
    angle_queue.put(angles)


    # Simulate updating the lines after 3 seconds
    time.sleep(3)

    # Put new angles in the queue
    new_angles = [-40, 60, -30]  # New angles
    angle_queue.put(new_angles)

    # Join thread
    draw_thread.join()
