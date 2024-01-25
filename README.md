
# WordMaster README.md

---

## Introduction
"WordMaster" is an interactive educational application developed by Carlos Finocchiaro, aimed at helping users, especially children, to learn reading and spelling in an engaging way. This application, built using Tkinter and Pygame in Python, features a tabbed interface with various reading tools, contact information, and user instructions.

## Features
1. **Interactive Word Display:** Shows words and spells them out, aiding in learning and memory retention.
2. **Audio Feedback:** Incorporates text-to-speech functionality for spelling, reading aloud, and providing feedback.
3. **Customizable Word List:** Users can add their words to a file, which the program reads and incorporates into the learning session.
4. **Usage Statistics:** Tracks and records the user's interaction with words, such as spell counts, read counts, skip counts, and more.
5. **Configurable Settings:** Offers settings for spell delay, timer duration, sound preferences, and more through a configuration file.

## Installation
To run "WordMaster," ensure you have the following dependencies installed:
- Python 3.x
- Tkinter (should be included in standard Python installation)
- Pygame
- gTTS (Google Text-to-Speech)
- configparser
- csv

## Usage
Start the application by executing the main script. The application interface is intuitive, offering the following functionalities:

1. **Word Display:** Words are displayed prominently, with each letter shown separately for clarity.
2. **Spelling & Reading:** Use the 'Spell' button to spell the word letter by letter and the 'Read' button to read the entire word aloud.
3. **Feedback & Navigation:** Provide feedback on spelling or reading correctness with 'Correct' and 'Incorrect' buttons. Use the 'Skip' button to move to the next word.
4. **Timer Functionality:** A countdown timer adds an element of challenge, encouraging quicker recognition and decision-making.

## Configuration and Customization

### Configuring the Application (`config.ini`)
Modify the `config.ini` file to tailor the application's behavior. Here are the configurable parameters:

```ini
[Settings]
# Time in milliseconds for spell delay
spell_delay = 500

# Timer duration for each word specified in MIN:SEC. Set to 00:00 to disable timer
timer_duration = 01:30

# Timer threshold when to turn the timer red
red_threshold = 00:30

# Disable spell and read buttons after red threshold if "yes" otherwise "no"
red_threshold_buttons = yes

# Time to wait after timer hits 00:00, for example, 10 seconds
wait_time = 00:05

# Set to 'yes' to play timer warning sound, otherwise set to 'no'
play_sound = yes

# Set to 'yes' to enable the assistant, otherwise set to 'no'
assistant_sound = yes
```

Adjust these settings to control the spell delay, timer behavior, audio cues, and assistant features.

### Customizing the Word List (`words.txt`)
The words used in the application are loaded from `words.txt`. To customize the word list:

1. Open `words.txt` in a text editor.
2. Add the words you want to include, separated by commas. For example: `cat, dog, elephant`.
3. Save the file.

When the application is launched, it will load the words from this file, allowing the user to interact with the custom word list.

## Functions Description

### `load_statistics`
Loads the usage statistics of words from a CSV file, creating a basis for tracking user interaction with different words.

### `update_statistics`
Updates the count of specific actions (spell, read, skip, correct, incorrect, timeout) for each word, enhancing the tracking of user progress.

### `write_statistics`
Saves the updated statistics back to the CSV file, ensuring that progress is recorded and persistent.

### `load_config`
Reads configuration settings from a file, allowing for easy customization of the application's behavior.

### `play_audio`
Handles the playback of audio files, used for spelling words, giving feedback, and providing auditory cues.

### `read_words_from_file`
Reads and parses words from a specified file, allowing users to customize the word list used in the application.

### `update_word`
Randomly selects and displays a new word from the list, initiating the interaction cycle.

### `spell_word`, `spell_letter`
Handles the spelling of words and individual letters, with auditory feedback for each letter.

### `read_word`
Reads the entire word aloud, providing auditory reinforcement for the word being learned.

### `countdown`
Manages a countdown timer, introducing a time-bound element to the learning session.

### `setup_main_window`, `setup_button_frame`, `setup_contact_tab`, `setup_instructions_tab`
Handle the setup and layout of the application's graphical user interface.

## Author
Carlos Finocchiaro

## License
This project is open-sourced under the [MIT license](https://opensource.org/licenses/MIT).

Your feedback and contributions are welcome. For any queries or suggestions, please reach out to Carlos.

---