import tkinter as tk
from tkinter import ttk
import random
import tempfile
import pygame
from gtts import gTTS
import tkinter.font as tkFont
import configparser
import csv

# This script creates a tkinter-based application for learning to read.
# It features a tabbed interface with reading tools, contact info, and usage instructions.
# Key features include word display, spelling, reading aloud, and a countdown timer.

# Global variables
global countdown_id
countdown_id = None
stats_filename = "word_statistics.csv"
word_stats = {}

# Audio setup
pygame.mixer.init()
warning_sound = pygame.mixer.Sound('time1.wav')
time_up_sound = pygame.mixer.Sound('time2.wav')
correct_sound = pygame.mixer.Sound('time3.wav')
skip_sound = pygame.mixer.Sound('time4.wav')

def load_statistics():
    """Load statistics from file."""
    global word_stats
    try:
        with open(stats_filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            word_stats = {row['Word']: {k: int(v) for k, v in row.items() if k != 'Word'} for row in reader}
    except FileNotFoundError:
        word_stats = {}

def update_statistics(word, action):
    """Update statistics."""
    if word not in word_stats:
        word_stats[word] = {'Spell Count': 0, 'Read Count': 0, 'Skip Count': 0, 'Correct Count': 0, 'Incorrect Count': 0, 'Timeout Count': 0}
    
    action_key = f"{action} Count"
    if action_key in word_stats[word]:
        word_stats[word][action_key] += 1

def write_statistics():
    # Define a sorting key function based on your criteria
    def sort_key(word):
        incorrect = word_stats[word]['Incorrect Count']
        timeout = word_stats[word]['Timeout Count']
        correct = word_stats[word]['Correct Count']
        # A simple formula could be to subtract correct count from the sum of incorrect and timeout counts
        return incorrect + timeout - correct 
    sorted_words = sorted(word_stats.keys(), key=sort_key, reverse=True)  # Sort from worst to best
    with open(stats_filename, mode='w', newline='') as file:
        fieldnames = ['Word', 'Spell Count', 'Read Count', 'Skip Count', 'Correct Count', 'Incorrect Count', 'Timeout Count']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for word in sorted_words:
            writer.writerow({'Word': word, **word_stats[word]})


def load_config(file_name):
    """Load configuration from a given file."""
    config = configparser.ConfigParser()
    config.read(file_name)
    return config

def play_audio(file_path):
    """Play an audio file using Pygame."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def read_words_from_file(filename):
    """Read words from a file, ignoring lines starting with '#'."""
    try:
        with open(filename, 'r') as file:
            words = [word.strip() for line in file if line.strip() and not line.startswith('#') for word in line.split(',')]
            return words
    except FileNotFoundError:
        return []

def update_word():
    """Update the displayed word randomly from the list of words."""
    global countdown_id
    if countdown_id is not None:
        root.after_cancel(countdown_id)
        countdown_id = None

    if words:
        word = random.choice(words)
        current_word.set(word)
        display_word(word)
        if timer_duration > 0:
            countdown(timer_duration)
    else:
        current_word.set("No words available")

def display_word(word):
    """Display the given word with individual labels for each letter."""
    clear_word_frame()
    inner_frame = tk.Frame(word_frame, bg='SystemButtonFace')
    inner_frame.pack(expand=True)

    for letter in word:
        lbl = tk.Label(inner_frame, text=letter, font=("Helvetica", 80), bg='SystemButtonFace')
        lbl.pack(side=tk.LEFT, padx=2)

def spell_word():
    """Spell the word using gTTS, highlighting each letter."""
    for index, letter in enumerate(current_word.get()):
        if letter.isalpha() or letter in ["-", "'"]:
            highlight_letter(index)
            root.update()
            spell_letter(letter)
            unhighlight_letter(index)
            root.update()

def spell_letter(letter):
    """Spell a single letter using gTTS."""
    temp_file = tempfile.mktemp(suffix='.mp3')
    tts = gTTS(text=letter, lang='en', slow=True)
    tts.save(temp_file)
    play_audio(temp_file)
    pygame.time.wait(spell_delay)

def highlight_letter(index):
    """Highlight a letter at a given index."""
    labels = get_inner_frame_labels()
    if index < len(labels):
        labels[index].config(bg='yellow')

def unhighlight_letter(index):
    """Unhighlight a letter at a given index."""
    labels = get_inner_frame_labels()
    if index < len(labels):
        labels[index].config(bg='SystemButtonFace')

def get_inner_frame_labels():
    """Get labels from the inner frame of the word frame."""
    return word_frame.winfo_children()[0].winfo_children()

def clear_word_frame():
    """Clear all widgets from the word frame."""
    for widget in word_frame.winfo_children():
        widget.destroy()

def read_word():
    """Read the whole word using gTTS."""
    temp_file = tempfile.mktemp(suffix='.mp3')
    tts = gTTS(text=current_word.get(), lang='en', slow=False)
    tts.save(temp_file)
    play_audio(temp_file)
    
def assistant_reads(text):
    """Read the text using gTTS."""
    if(assistant_sound):
        temp_file = tempfile.mktemp(suffix='.mp3')
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_file)
        play_audio(temp_file)

def countdown(time_left):
    """Countdown timer for the application. Disables buttons when in red threshold."""
    global countdown_id
    if time_left > 0:
        is_in_red = time_left <= red_threshold
        timer_label.config(text=format_timer(time_left), fg='red' if is_in_red else 'black')
        countdown_id = root.after(1000, countdown, time_left - 1)
        if is_in_red:
            warning_sound.play()
            if red_threshold_buttons:
                spell_button.config(state=tk.NORMAL)
                read_button.config(state=tk.NORMAL)
        else:
            if red_threshold_buttons:
                spell_button.config(state=tk.DISABLED)
                read_button.config(state=tk.DISABLED)
    else:
        timer_label.config(text="00:00", fg='black')
        root.update()
        if play_sound:
            time_up_sound.play()
            assistant_reads("Time is up!")
            update_statistics(current_word.get(), 'Timeout')
        root.after(wait_time * 1000, update_word)
        if red_threshold_buttons:
            assistant_reads("New Word!")
            spell_button.config(state=tk.DISABLED)
            read_button.config(state=tk.DISABLED)


def parse_timer_duration(duration_str):
    """Parse a time duration string in the format 'MM:SS'."""
    try:
        minutes, seconds = map(int, duration_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        return 0

def format_timer(time_left):
    """Format a time duration in seconds into 'MM:SS' format."""
    minutes, seconds = divmod(time_left, 60)
    return f"{minutes:02d}:{seconds:02d}"

def spell_button_pressed():
    """Function called when the Spell button is pressed."""
    update_statistics(current_word.get(), 'Spell')
    spell_word()
    
def read_button_pressed():
    """Function called when the Read button is pressed."""
    update_statistics(current_word.get(), 'Read')
    read_word()
    
def incorrect_button_pressed():
    """Function called when the Incorrect button is pressed."""
    update_statistics(current_word.get(), 'Incorrect')
    assistant_reads("Incorrect!")
    time_up_sound.play()
    update_word()
    
def skip_button_pressed():
    """Function called when the Skip button is pressed."""
    update_statistics(current_word.get(), 'Skip')
    assistant_reads("Skipping")
    skip_sound.play()
    update_word()

def correct_button_pressed():
    """Function called when the Correct button is pressed."""
    update_statistics(current_word.get(), 'Correct')
    assistant_reads("Correct!")
    correct_sound.play()
    update_word()

def setup_main_window():
    """Set up the main application window and its components."""
    root = tk.Tk()
    root.title("WordMaster - By Carlos Finocchiaro")

    # Create the notebook (tab container)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Create the reading tab
    reading_tab = tk.Frame(notebook)
    notebook.add(reading_tab, text='Reading Tool')

    # Add a label for the countdown timer in the reading tool tab
    timer_label = tk.Label(reading_tab, text="", font=("Helvetica", 30))
    timer_label.pack(anchor='ne', padx=10, pady=10)

    # Variables and UI setup for the reading tool
    current_word = tk.StringVar()
    word_frame = tk.Frame(reading_tab)
    word_frame.pack(fill='both', expand=True)

    # Buttons for the reading tool
    button_frame = setup_button_frame(reading_tab)

    return root, notebook, reading_tab, timer_label, current_word, word_frame, button_frame

def setup_button_frame(parent):
    """Set up the frame containing buttons."""
    global spell_button, read_button
    
    button_frame = tk.Frame(parent)
    button_frame.pack(fill='both')

    # Define the font
    button_font = tkFont.Font(family="Helvetica", weight="bold", size=15)
    button_font2 = tkFont.Font(family="Helvetica", weight="bold", size=10)

    # Create and place buttons
    spell_button = tk.Button(button_frame, text="Spell", command=spell_button_pressed, height=2, width=10, bg="light blue", font=button_font2)
    spell_button.grid(row=0, column=0, padx=5, pady=10)
    read_button = tk.Button(button_frame, text="Read", command=read_button_pressed, height=2, width=10, bg="blue", font=button_font2)
    read_button.grid(row=0, column=2, padx=5, pady=10)
    tk.Button(button_frame, text="Incorrect", command=incorrect_button_pressed, height=2, width=20, bg="red", font=button_font).grid(row=1, column=0, columnspan=1, padx=20, pady=10)
    tk.Button(button_frame, text="Skip", command=skip_button_pressed, height=2, width=10, bg="yellow", font=button_font).grid(row=1, column=1, padx=5, pady=10)
    tk.Button(button_frame, text="Correct", command=correct_button_pressed, height=2, width=20, bg="green", font=button_font).grid(row=1, column=2, columnspan=1, padx=20, pady=10)

    return button_frame

def setup_contact_tab(notebook):
    """Set up the contact information tab."""
    contact_tab = tk.Frame(notebook)
    notebook.add(contact_tab, text='Contact Info')

    tk.Label(contact_tab, text="Contact Information", font=("Helvetica", 16)).pack(pady=10)
    contact_details = """Carlos Finocchiaro\nEmail: carlosfinocchiaro@hotmail.com"""
    tk.Label(contact_tab, text=contact_details, font=("Helvetica", 12)).pack(pady=10)

def setup_instructions_tab(notebook):
    """Set up the instructions tab."""
    how_to_use_tab = tk.Frame(notebook)
    notebook.add(how_to_use_tab, text='How to Use')

    updated_instructions = (
        "How to Use the Reading Program:\n\n"
        "1. Configuration settings can be adjusted in the 'config.ini' file, including spell delay, timer duration, sound settings, and more.\n\n"
        "2. Words are loaded from the 'words.txt' file. Fill it with words separated by commas. Example: cat, dog, elephant.\n\n"
        "3. Comments can be added in 'words.txt' by starting the line with '#'. For example:\n"
        "   - # THIS IS A COMMENT\n\n"
        "4. In the 'Reading Tool' tab, you can:\n"
        "   - Use 'Spell' to spell the displayed word letter by letter.\n"
        "   - Use 'Read' to read the entire word aloud.\n"
        "   - Use 'Skip' to skip the current word and display a new one.\n"
        "   - Use 'Correct' if the word is spelled or read correctly.\n"
        "   - Use 'Incorrect' if the word is spelled or read incorrectly.\n\n"
        "5. The program tracks the usage of each word, recording the number of times it's spelled, read, skipped, marked correct or incorrect, and how often the time runs out.\n\n"
        "6. The statistics for each word are saved and can be reviewed for understanding the most challenging words.\n\n"
        "7. Switch to the 'Contact Info' tab for contact details.\n\n"
        "Note: An internet connection is required for the text-to-speech feature."
    )

    text_widget = tk.Text(how_to_use_tab, height=30, width=50, wrap='word', font=("Helvetica", 12))
    text_widget.pack(pady=20, padx=20)
    text_widget.insert(tk.END, updated_instructions)
    text_widget.config(state='disabled')


# Load configuration
config = load_config('config.ini')

# Configuration parameters
spell_delay = int(config['Settings'].get('spell_delay', 1000))
timer_duration = parse_timer_duration(config['Settings'].get('timer_duration', '00:00'))
red_threshold = parse_timer_duration(config['Settings'].get('red_threshold', '00:00'))
play_sound = config['Settings'].get('play_sound', 'no').lower() == 'yes'
wait_time = parse_timer_duration(config['Settings'].get('wait_time', '00:00'))
red_threshold_buttons = config['Settings'].get('red_threshold_buttons', 'no').lower() == 'yes'
assistant_sound = config['Settings'].get('assistant_sound', 'no').lower() == 'yes'

# Setup the main application window
root, notebook, reading_tab, timer_label, current_word, word_frame, button_frame = setup_main_window()

# Contact and instruction tabs setup
setup_instructions_tab(notebook)
setup_contact_tab(notebook)

# Start the countdown timer if enabled
if timer_duration > 0:
    countdown(timer_duration)

# Load words and display the first word
words = read_words_from_file("words.txt")
update_word()

# Load statistics at the beginning of your program
load_statistics()

# Start the GUI event loop
root.mainloop()

# Write statistics back to the file after the main loop ends
write_statistics()