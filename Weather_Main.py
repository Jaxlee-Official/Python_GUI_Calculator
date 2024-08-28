import tkinter as tk
from PIL import Image, ImageTk
import requests

def get_weather(city):
    api_key = ""  # Replace with your WeatherAPI key
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {'key': api_key, 'q': city}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        temp = data['current']['temp_c']
        return f"{temp}°C"
    except requests.RequestException as e:
        return "Error fetching Weather data"

def perform_search():
    city = search_entry.get().strip()
    weather_info = get_weather(city)
    weather_label.config(text=f"Temperature: {weather_info}")

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
weather_label = tk.Label(frame, text="Temperature: City", font=("Helvetica", 24), bg="gray", fg="black")
weather_label.place(x=50, y=300)

root.mainloop()
