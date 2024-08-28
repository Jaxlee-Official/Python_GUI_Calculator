import tkinter as tk
from PIL import Image, ImageTk
import requests
import cv2
import numpy as np
from threading import Thread

def get_weather(city):
    api_key = "6c6057c16e7e45939ce142629241608"  # Replace with your WeatherAPI key
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {'key': api_key, 'q': city}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text'].lower()
        return temp, condition
    except requests.RequestException as e:
        return None, "Error fetching Weather data"

def update_background(condition):
    global background_label
    video_path = None  # Initialize video_path with a default value

    if condition == "sunny":
        video_path = "sunny.mp4"
    elif condition == "rainy":
        video_path = "rainy.mp4"
    elif condition == "snowy":
        video_path = "snowy.mp4"
    elif condition == "cloudy":
        image_path = "cloudy.jpg"
        img = Image.open(image_path)
        img = img.resize((400, 600), Image.BICUBIC)
        img_photo = ImageTk.PhotoImage(img)
        background_label.config(image=img_photo)
        background_label.image = img_photo
        return
    else:
        # Handle unknown conditions
        return

    # For videos
    if video_path:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video file: {video_path}")
            return

        # Get the dimensions of the background_label
        width = background_label.winfo_width()
        height = background_label.winfo_height()

        def play_video():
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("End of video or error reading frame.")
                    break

                # Resize the frame to fit the background_label
                frame_resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                frame_image = Image.fromarray(frame_rgb)
                frame_photo = ImageTk.PhotoImage(frame_image)
                background_label.config(image=frame_photo)
                background_label.image = frame_photo
                root.update_idletasks()
            cap.release()

        video_thread = Thread(target=play_video)
        video_thread.start()

def perform_search():
    city = search_entry.get().strip()
    temp, condition = get_weather(city)
    if temp is not None:
        weather_label.config(text=f"Temperature in {city}: {temp}°C")
        update_background(condition)
    else:
        weather_label.config(text="Error fetching Weather data")
        update_background("")

def on_button_click():
    perform_search()

# Initialize the main window (root)
root = tk.Tk()
root.title("Weather App")
root.resizable(False, False)

# Create a frame
frame = tk.Frame(root, width=400, height=600, bg="gray")
frame.pack_propagate(False)
frame.pack()

# Background label (canvas for image/video)
background_label = tk.Label(frame, bg="gray")
background_label.place(x=0, y=0, width=400, height=600)

# Search bar
search_entry = tk.Entry(frame, font=("Helvetica", 14))
search_entry.place(x=40, y=20, width=250)

# Weather icon
image = Image.open("icon.png")
resized_image = image.resize((50, 50), Image.BICUBIC)
photo = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(frame, image=photo, bg="gray")
image_label.image = photo
image_label.place(x=170, y=240)

# Button with logo
logo_image = Image.open("search.png")  # Replace with your logo image path
logo_resized = logo_image.resize((30, 30), Image.BICUBIC)
logo_photo = ImageTk.PhotoImage(logo_resized)
logo_button = tk.Button(frame, image=logo_photo, command=on_button_click, bg="gray", borderwidth=0)
logo_button.image = logo_photo
logo_button.place(x=300, y=20)

# Weather label
weather_label = tk.Label(frame, text="Temperature: Enter a city", font=("Helvetica", 16), bg="gray", fg="black")
weather_label.place(x=50, y=300)

root.mainloop()
