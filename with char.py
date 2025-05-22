# import numpy as np
# import google.generativeai as genai

# GEMINI_API_KEY = 'AIzaSyAosXpWbuvwoqQSufXGD9CcC8xTmWJU3vc'
# prompt = '''
# You are an image analysis expert.
# Given the attached image, detect the position of the largest white rectangular area that the character is holding. Return the coordinates of this rectangle in the format: (left, top, right, bottom) — all in pixel values relative to the image.
# Only return the bounding box coordinates. No explanation or extra text.
# '''
# genai.configure(api_key=GEMINI_API_KEY) # type: ignore
# model = genai.GenerativeModel("gemini-2.0-flash") # type: ignore
# position = [0, 0, 0, 0]

import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2.extras import RealDictCursor
import ctypes
import signal
import sys
import random
from PIL import Image, ImageTk
from PIL import ImageDraw, ImageFont
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



# --- Database Connection ---
DB_URI = 'postgres://avnadmin:AVNS_2_65ikq6jVV8ip2LWI0@pg-c11a32f-uniqueanonymous2516-46a0.k.aivencloud.com:17972/Users?sslmode=require'

def check_credentials(username, password):
    try:
        conn = psycopg2.connect(DB_URI)
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            return cursor.fetchone() is not None
    except Exception as e:
        print("DB error:", e)
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def launch_quote_widget():
    global root
    quotes = [
        "Believe you can and you're halfway there.",
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones."
    ]

    root = tk.Tk()
    root.overrideredirect(True)  # Remove window border

    # --- Make widget movable ---
    def start_move(event):
        root.x = event.x # type: ignore
        root.y = event.y # type: ignore

    def do_move(event):
        x = event.x_root - root.x # type: ignore
        y = event.y_root - root.y # type: ignore
        root.geometry(f'+{x}+{y}')

    # --- Load and resize image ---
    # img_path = resource_path("image.png")
    # original_img = Image.open(img_path)

    original_img = Image.open(r"C:\Users\HP\OneDrive\Documents\lovely certificates\PROJECTS\Widgets\characters\image.png")
    standard_width = 300
    width, height = original_img.size
    new_height = int((standard_width / width) * height)
    image_resized = original_img.resize((standard_width, new_height)).convert("RGBA")
    # response = model.generate_content([prompt,image_resized])
    # position = (response.text)[1:-2].split(",")
    # print(position)
    

    # --- Draw quote ---
    def draw_quote_on_image(quote_text):
        # global position
        draw_img = image_resized.copy()
        draw = ImageDraw.Draw(draw_img)

        try:
            font = ImageFont.truetype("arial.ttf", 20)  # Increased font size for better visibility
        except:
            font = ImageFont.load_default()

        # Original coordinates (for 1024x1024), now scaled
        x_scale = standard_width / 1024
        y_scale = new_height / 1024


        x1, y1 = int(250 * x_scale), int(120 * y_scale)
        x2, y2 = int(770 * x_scale), int(440 * y_scale)
        # x1, y1 = int(int(position[0]) * x_scale), int(position[1] * y_scale)
        # x2, y2 = int(position[2] * x_scale), int(position[3] * y_scale)
        # Word wrap within the 287

        max_width = x2 - x1
        words = quote_text.split()
        lines = []
        line = ""

        for word in words:
            test_line = f"{line} {word}".strip()
            bbox = font.getbbox(test_line)
            test_width = bbox[2] - bbox[0]
            if test_width <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)

        # Calculate total height
        line_height = font.getbbox("A")[3] - font.getbbox("A")[1] + 4
        total_text_height = len(lines) * line_height
        start_y = y1 + ((y2 - y1 - total_text_height) // 2)

        for i, line in enumerate(lines):
            draw.text((x1, start_y + i * line_height), line, font=font, fill="black")

        return ImageTk.PhotoImage(draw_img)


    # --- Quote update ---
    def update_quote():
        quote = random.choice(quotes)
        new_img = draw_quote_on_image(quote)
        image_label.configure(image=new_img)
        image_label.image = new_img # type: ignore
        root.after(5000, update_quote)

    # --- Handle app closing gracefully ---
    def close_app():
        try:
            root.destroy()
        except:
            pass
        sys.exit()

    def signal_handler(sig, frame):
        close_app()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # --- Setup widget UI ---
    image_label = tk.Label(root)
    image_label.pack()
    image_label.bind("<Button-1>", start_move)
    image_label.bind("<B1-Motion>", do_move)

    # --- Close button ---
    close_button = tk.Button(root, text="×", command=close_app,
                             bg="red", fg="white", bd=0, font=("Helvetica", 12))
    close_button.place(x=standard_width-30, y=0, width=30, height=30)

    update_quote()  # Initial quote

    # --- Resize the root window to fit the image ---
    root.geometry(f"{standard_width}x{new_height}")  # Adjust the window size

    root.mainloop()



# --- Login Window ---
def login():
    uname = username_entry.get()
    passwd = password_entry.get()
    if check_credentials(uname, passwd):
        messagebox.showinfo("Login Success", "Welcome!")
        window.destroy()
        launch_quote_widget()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")
def register():
    window.destroy()
    
window = tk.Tk()
window.title("Login form")
window.geometry('600x500')
window.configure(bg='#333333')

# Set the icon for the login window

window.iconbitmap(r"C:\Users\HP\OneDrive\Documents\lovely certificates\PROJECTS\Widgets\icon.ico")
# window.iconbitmap(resource_path("icon.ico"))

  # Add the path to your icon here

frame = tk.Frame(bg='#333333')

login_label = tk.Label(frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tk.Entry(frame, font=("Arial", 16))
password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
login_button = tk.Button(frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)
register_button = tk.Button(frame, text="Register Now", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=register)

login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)
register_button.grid(row=4, column=0, columnspan=2, pady=30)

frame.pack()
window.mainloop()
