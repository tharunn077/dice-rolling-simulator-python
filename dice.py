import random
import tkinter as tk
from PIL import Image, ImageTk
import pygame  

# Initialize the main window
root = tk.Tk()
root.title("Dice Rolling Simulator")
root.geometry("1920x1080")
root.config(bg="lightgray")
pygame.mixer.init()
# Global variables
selected_style = tk.StringVar(value="Classic")
dice_images = []
history = []
music_muted = False
effects_muted = False
music_button = None  
effects_button = None 

def resize_image(image, width, height):
    return ImageTk.PhotoImage(image.resize((width, height), Image.Resampling.LANCZOS))

def load_dice_images(style):
    try:
        if style == "Classic":
            return [resize_image(Image.open(f"classic_{i}.png"), 150, 150) for i in range(1, 7)]
        elif style == "Futuristic":
            return [resize_image(Image.open(f"futuristic_{i}.png"), 150, 150) for i in range(1, 7)]
        elif style == "Wood":
            return [resize_image(Image.open(f"wood_{i}.png"), 150, 150) for i in range(1, 7)]
    except FileNotFoundError:
        print(f"Error: Images for {style} dice not found.")
        root.quit()

# Load background images dynamically
def load_background_image(style):
    try:
        root.update_idletasks()
        width, height = root.winfo_width(), root.winfo_height()
        
        if style == "Classic":
            bg_image = Image.open("classic_bg.png")
        elif style == "Futuristic":
            bg_image = Image.open("futuristic_bg.png")
        elif style == "Wood":
            bg_image = Image.open("wood_bg.png")
        
        bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(bg_image)
        
    except FileNotFoundError:
        print(f"Error: Background image for {style} not found.")
        return None

def play_button_click():
    global effects_muted
    if not effects_muted:
        pygame.mixer.Sound("button_click.mp3").play()

# Helper function to wrap button commands with a click sound
def with_click_sound(original_command):
    def wrapped_command():
        play_button_click()
        original_command()
    return wrapped_command

# Play background music
def play_music():
    global music_muted
    if not music_muted:
        pygame.mixer.music.load("bg_music.mp3")  
        pygame.mixer.music.play(-1, 0.0)  

def stop_music():
    pygame.mixer.music.stop()

def update_button_states():
    if music_muted:
        music_button.config(text="🎵 Music OFF")
    else:
        music_button.config(text="🎵 Music ON")

    if effects_muted:
        effects_button.config(text="🔊 Effects OFF")
    else:
        effects_button.config(text="🔊 Effects ON")

def on_exit():
    stop_music()  
    root.destroy()  

def play_effect():
    global effects_muted
    if not effects_muted:
        pygame.mixer.Sound("diceroll.mp3").play()
        
def toggle_music():
    global music_muted
    music_muted = not music_muted
    if music_muted:
        stop_music()
        music_button.config(text="🎵 Music OFF")
    else:
        play_music()
        music_button.config(text="🎵 Music ON")

# Mute effects
def toggle_effects():
    global effects_muted
    effects_muted = not effects_muted
    if effects_muted:
        effects_button.config(text="🔊 Effects OFF")
    else:
        effects_button.config(text="🔊 Effects ON")

# Fullscreen toggle
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

# Build the dice rolling simulator screen
def build_dice_rolling_simulator():
    global history, music_button, effects_button

   
    for widget in root.winfo_children():
        widget.destroy()

    
    bg_image = load_background_image(selected_style.get())
    if not bg_image:
        return

    canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height(), bg="lightgray")
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image)
    canvas.bg_image = bg_image

    title_label = tk.Label(
        root,
        text=f"Dice Rolling Simulator - {selected_style.get()} Style",
        font=("Arial", 20, "bold"),
        bg="lightgray",
        fg="darkblue",
    )
    canvas.create_window(root.winfo_width() // 2, 30, window=title_label)

    dice_label = tk.Label(root, image=dice_images[0], bg="lightgray")
    canvas.create_window(root.winfo_width() // 2, 150, window=dice_label)

    result_label = tk.Label(root, text="", font=("Arial", 22,"bold"), bg="lightgray", fg="darkgreen")
    canvas.create_window(root.winfo_width() // 2, 250, window=result_label)
    exit_button = tk.Button(root, text="Exit", command=on_exit, font=("Arial", 14), bg="darkred", fg="white", relief="raised", bd=3)
    exit_button.place(relx=0.9, rely=0.15, anchor="ne")

    def roll_dice_animation():
        def animate(frame=0):
            if frame < 10:
                random_index = random.randint(0, 5)
                dice_label.config(image=dice_images[random_index])
                root.after(100, animate, frame + 1)
            else:
                final_index = random.randint(0, 5)
                dice_label.config(image=dice_images[final_index])
                result_label.config(text=f"You Got {final_index + 1}!")
                history.append(final_index + 1)
                update_history()

        play_effect() 
        animate()

    roll_button = tk.Button(
        root,
        text="Roll Dice",
        font=("Arial", 14),
        command=roll_dice_animation,
        bg="#4B0082",  
        fg="gold",  
        relief="raised",
        bd=3,
    )
    canvas.create_window(root.winfo_width() // 2, 400, window=roll_button)

    back_button = tk.Button(
        root,
        text="Back to Dice Selection",
        font=("Arial", 14),
        command=with_click_sound(build_selection_screen),
        bg="gray",  
        fg="white",  
        relief="raised",
        bd=3,
    )
    canvas.create_window(root.winfo_width() // 2, 500, window=back_button)
    # History frame and button
    history_frame = tk.Frame(root, bg="lightgray")
    history_frame.place(relx=0.10, rely=0.5, anchor="center")
    history_text = tk.Text(history_frame, width=30, height=10, font=("Arial", 12), bg="white", fg="black", relief="sunken", bd=3)
    history_text.pack()

    def update_history():
        history_text.delete(1.0, tk.END)
        history_text.insert(tk.END, "Roll History:\n")
        history_text.insert(tk.END, "\n".join(map(str, history)))

    update_history()

    def toggle_history():
        if history_frame.winfo_ismapped():
            history_frame.place_forget()
            history_button.config(text="▶ History")
        else:
            history_frame.place(relx=0.10, rely=0.5, anchor="center")
            history_button.config(text="◁ History")

    history_button = tk.Button(root, text="▶ History", command=toggle_history, font=("Arial", 14), bg="grey", fg="white", relief="raised", bd=3)
    canvas.create_window(root.winfo_width() // 2, 550, window=history_button)

   
    music_button = tk.Button(root, text="", command=with_click_sound(toggle_music), font=("Arial", 14), bg="green", fg="white", relief="raised", bd=3)
    music_button.place(relx=0.9, rely=0.05, anchor="ne")

    effects_button = tk.Button(root, text="", command=with_click_sound(toggle_effects), font=("Arial", 14), bg="green", fg="white", relief="raised", bd=3)
    effects_button.place(relx=0.9, rely=0.1, anchor="ne")

 
    update_button_states()

def build_selection_screen():
    global music_button, effects_button

    for widget in root.winfo_children():
        widget.destroy()

    try:
        root.update_idletasks()
        width, height = root.winfo_width(), root.winfo_height()
        bg_image = Image.open("selection_bg.png").resize((1920, 1080), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Selection background image not found.")
  
    title_label = tk.Label(
        root,
        text="Welcome to Dice Rolling Simulator!",
        font=("Arial", 25, "bold"),
        bg="#171717",
        fg="white",
        pady=50,  
    )
    title_label.pack()

    subtitle_label = tk.Label(
        root,
        text="𝙎𝙚𝙡𝙚𝙘𝙩 𝙔𝙤𝙪𝙧 𝘿𝙞𝙘𝙚 𝙎𝙩𝙮𝙡𝙚",
        font=("Arial", 24),
        bg="black",
        fg="white",
        pady=5,
    )
    subtitle_label.pack(pady=10)

    styles = [("Classic", "classic_preview.png"), ("Futuristic", "futuristic_preview.png"), ("Wood", "wood_preview.png")]
    for style, image_file in styles:
        frame = tk.Frame(root, bg="#2C2C2C")
        frame.pack(pady=20)

        try:
            preview_image = ImageTk.PhotoImage(Image.open(image_file).resize((150, 150)))
        except FileNotFoundError:
            preview_image = None
            print(f"Preview image for {style} not found.")

        if preview_image:
            preview_label = tk.Label(frame, image=preview_image, bg="#2C2C2C")
            preview_label.image = preview_image
            preview_label.pack(side="left", padx=10)
            
        def select_style(style=style):
          selected_style.set(style)
          play_button_click()
        
        radio_button = tk.Radiobutton(
            frame,
            text=style,
            variable=selected_style,
            value=style,
            font=("Arial", 18),
            bg="#242424",
            fg="white",
            selectcolor="grey",
            activebackground="black",
            activeforeground="white",
            command=select_style
        )
        radio_button.pack(side="left", padx=20)

    instruction_label = tk.Label(
        root,
        text="Press Enter to continue...",
        font=("Arial", 18, "italic"),
        bg="#2C2C2C",
        fg="white",
        pady=20,
    )
    instruction_label.pack(side="bottom", pady=20)

   
    music_button = tk.Button(root, text="", command=toggle_music, font=("Arial", 14), bg="green", fg="white", relief="raised", bd=3)
    music_button.place(relx=0.9, rely=0.05, anchor="ne")

    effects_button = tk.Button(root, text="", command=toggle_effects, font=("Arial", 14), bg="green", fg="white", relief="raised", bd=3)
    effects_button.place(relx=0.9, rely=0.1, anchor="ne")


    update_button_states()
    exit_button = tk.Button(root, text="Exit", command=with_click_sound(on_exit), font=("Arial", 14), bg="darkred", fg="white", relief="raised", bd=3)
    exit_button.place(relx=0.9, rely=0.15, anchor="ne")
  

def start_dice_rolling(event=None):
    global dice_images
    dice_images = load_dice_images(selected_style.get())
    if not dice_images:
        return
    build_dice_rolling_simulator()

root.bind("<Return>", lambda event: with_click_sound(start_dice_rolling)())
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)
root.protocol("WM_DELETE_WINDOW", on_exit)
play_music()  
build_selection_screen()
root.mainloop()
