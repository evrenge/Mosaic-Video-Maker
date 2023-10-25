from tkinter import *
from tkinter.ttk import Style
import cv2
from PokikiAPI import Pokiki
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from threading import Thread

root = Tk()
root.title("Mosaic Video Maker")
root.resizable(False, False)

style = Style(root)
style.theme_use('clam')

# Change this to 0 if your camera doesn't open
capture = cv2.VideoCapture(0)
CANVAS_W, CANVAS_H = 1024, 576
CANVAS_H_W_RATIO = CANVAS_H / CANVAS_W

########## UI VARIABLES ############
# Tkinter functions work on the main thread
split_x = IntVar(root, value=30)
split_y = IntVar(root, value=20)

# Atomic vars to share data between threads
atom_split_x = split_x.get()
atom_split_y = split_y.get()
atom_image = None
resize_canvas = False

def set_split_x(x):
    global atom_split_x
    split_x.set(x)
    atom_split_x = int(x)
def set_split_y(y):
    global atom_split_y
    split_y.set(y)
    atom_split_y = int(y)

def open_file():
    global capture, resize_canvas
    filename: str = fd.askopenfilename()
    # List of video file extensions
    valid_extensions = ["mp4", "mov", "ogg", "wmv", "avi", "flv", "gif"]
    if filename:
        # Get opened file extension
        ext = filename.split(".").pop()
        if ext.lower() in valid_extensions:
            capture = cv2.VideoCapture(filename)
            resize_canvas = True

def open_camera():
    global capture, resize_canvas
    capture = cv2.VideoCapture(0)
    resize_canvas = True

if __name__ == '__main__':
    ########## INSTANCES ############
    pokiki = Pokiki()

    ########## UI SETUP ############
    canvas = Canvas(root, width=CANVAS_W, height=CANVAS_H)
    canvas.pack()

    options_frame = LabelFrame(root, text="Options")
    options_frame.pack(fill="both", expand="yes")

    controls_frame = Frame(options_frame)
    controls_frame.pack(side=LEFT)

    label = Label(controls_frame, text="Split X")
    x_scale = Scale(controls_frame, from_=5, to=250, orient=HORIZONTAL,
                            length=250, resolution=5, command=set_split_x, var=split_x)
    label.pack()
    x_scale.pack()

    label = Label(controls_frame, text="Split Y")
    y_scale = Scale(controls_frame, from_=5, to=250, orient=HORIZONTAL,
                            length=250, resolution=5, command=set_split_y, var=split_y)
    label.pack()
    y_scale.pack()

    file_button = Button(options_frame, text="Open File", command=open_file)
    file_button.pack(side=RIGHT)
    camera_button = Button(options_frame, text="Use Camera", command=open_camera)
    camera_button.pack(side=RIGHT)

    ########## VISUALIZATION LOOP ############
    running = True

    def run_video():
        global atom_image, CANVAS_W, resize_canvas
        while running:
            # Read the next frame
            retval, frame = capture.read()

            # Check if there is a valid frame.
            if not retval:
                continue

            if resize_canvas:
                _, frame_w, _ = frame.shape
                CANVAS_W = int(frame_w*CANVAS_H_W_RATIO)
                resize_canvas = True

            # Convert the original image to tiled
            tile_img = pokiki.convertFromImage(frame, atom_split_x, atom_split_y)
            tile_img = cv2.resize(tile_img, (CANVAS_W, CANVAS_H))

            # Display the resulting frame
            atom_image = tile_img

    video_thread = Thread(target=run_video, args=())
    video_thread.start()

    def exit_app():
        global running
        running = False
        video_thread.join()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", exit_app)

    while running:
        root.update_idletasks()
        # Display the resulting frame
        if atom_image is not None:
            canvas.configure(width=CANVAS_W)
            img = ImageTk.PhotoImage(image=Image.fromarray(atom_image))
            canvas.create_image(0,0, anchor="nw", image=img)
            atom_image = None

        root.update()
