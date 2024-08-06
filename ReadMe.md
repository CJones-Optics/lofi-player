
# LoFi Radio
A minimalist terminal-based music player written in python for a
distraction-free listening experience.

# Features
- *NO* Individual track selection
- *NO* Next Button
- *NO* Distractions

- *Just* Playlists, with Shuffle, Mute, and Volume Control

# Customisability
- User interface is customisable by adjusting the .tcss files. (Just fancy css)
- Features can be added by modifying the python code.

# How to run and install
## One-Line Install (Linux)

```bash
# Download the repository
curl -L https://github.com/CJones-Optics/lofi-player/archive/refs/heads/main.zip -o temp.zip
unzip temp.zip
rm temp.zip
# Navigate to the directory
cd lofi-player*
chmod +x setup.sh
# Run the setup
./setup.sh
```

## Longer Install

1. Clone the repository
2. Run the setup.
    - (Linux) Run `setup.sh` to install the required packages
    - (Windows) Run `setup.bat` to install the required packages
3. Download some .mp3's
    - Create a sub-folder in `tracks` for each playlist you want to create
    - Add the .mp3 files to each sub-folder
4. Run the program
    - (Linux) Run `run.sh` to start the program
    - (Windows) Run `run.bat` to start the program
5. (Optional) Create a shortcut to the `run` script to easily start the program
    - (Linux) Create an alias in your `.bashrc` file
    - (Windows) Create a shortcut to the `run.bat` file
6. Enjoy your music!

## Running the program
1. Download some .mp3's
    - Create a sub-folder in `tracks` for each playlist you want to create
    - Add the .mp3 files to each sub-folder
2. Run the program
    - (Linux) Run `start.bash` to start the program
    - (Windows) Run `run.bat` to start the program

# Roadmap
Future changes are unlikely because it currently fits my use-case.
However for the sake of completeness, here is how I may extend the
application in the future.
- Custom theming.
	- At the moment I have a Catpuccino theme hardcoded into it. An implementation to vary the colourscheme owuld be simple to implment and highly beneficial
- Implement GUI and Mouse Support.
	- I have a softspot for text only UIs, which is why it is implemented like this. The framework does support buttons for mouse UIs though. The app does work with buttons but I thought they were ugly and removed them. Check the commit history for implmentation
- GUI Support Cont: Implement a list feature for all the stations.

If you feel like implementing any of the changes, shoot a pull request my way :)
