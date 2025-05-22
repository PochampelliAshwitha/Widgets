import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2.extras import RealDictCursor
import ctypes
import signal
import sys
import random

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

    def update_quote():
        quote = random.choice(quotes)
        label.config(text=quote)
        root.after(5000, update_quote)

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

    root = tk.Tk()
    root.title("Quote Widget")
    root.geometry("300x100+100+100")
    root.overrideredirect(True)
    root.configure(bg='black')

    # Set the icon for the root window
    root.iconbitmap(r"D:\PYTHON\Widgets\icon.ico")  # Add the path to your icon here

    # Hide from taskbar (Windows only)
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, style | 0x00000080)

    # Close Button
    close_button = tk.Button(root, text="×", command=close_app,
                            bg="black", fg="white", bd=0, font=("Helvetica", 12),
                            activebackground="red", activeforeground="white")
    close_button.place(x=280, y=0, width=20, height=20)

    # Quote Label
    global label
    label = tk.Label(root, text="", fg="white", bg="black", font=("Helvetica", 12), wraplength=280, justify="center")
    label.pack(expand=True)

    # Make the window draggable
    def start_move(event):
        root.x = event.x  # type: ignore
        root.y = event.y  # type: ignore

    def stop_move(event):
        root.x = None  # type: ignore
        root.y = None  # type: ignore

    def do_move(event):
        deltax = event.x - root.x  # type: ignore
        deltay = event.y - root.y  # type: ignore
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")

    # Bind the move functionality to the whole window (root)
    root.bind("<ButtonPress-1>", start_move)
    root.bind("<ButtonRelease-1>", stop_move)
    root.bind("<B1-Motion>", do_move)

    update_quote()
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

window = tk.Tk()
window.title("Login form")
window.geometry('600x500')
window.configure(bg='#333333')

# Set the icon for the login window
window.iconbitmap(r"D:\PYTHON\Widgets\icon.ico")  # Add the path to your icon here

frame = tk.Frame(bg='#333333')

login_label = tk.Label(frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tk.Entry(frame, font=("Arial", 16))
password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
login_button = tk.Button(frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)

login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

frame.pack()
window.mainloop()
