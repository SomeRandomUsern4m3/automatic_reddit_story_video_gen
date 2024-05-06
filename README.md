# Important note - Also PLEASE read the whole thing I have here. it is important to setting up this program
## Your gonna need to add the folder game_footage because stupid github won't let me add it
## Credit to https://github.com/abdeladim-s/subsai for the subtitle library. It is really helpful :)


# What is this?

## This a project that I whipped up in a day it generates those ai reddit stories with the text to speech
### Why? I saw my cousin watching some of these videos and they seemed to be 100% engaged with the video


# You will need FFMPEG and its library
FFMPEG: https://www.wikihow.com/Install-FFmpeg-on-Windows


Python library:
```pip install ffmpeg-python```

# Other things that are required to be installed are:

Most important is the rust build lib ```pip install setuptools-rust```

subsAI: ```pip install git+https://github.com/abdeladim-s/subsai```

moviepy: ```pip install moviepy```,

opencv: ```pip install opencv-python```,

pydub: ```pip install pydub```,

special pyttsx3: ```python3 -m pip install git+https://github.com/nateshmbhat/pyttsx3```



# What to do?

## There is two folders one is game_footage and the other one is stories

### In the game_footage folder copy and paste clips of satisfying game footage, I recommend 20 minute long minecraft parkour videos. As there are multiple sections for the program to cut out of it.

### If it errors then your footage videos obvisouly aren't long enough

## The stories folder works as so

### You put in text files, and the first line of the text file will be recognized as the title. Then enter a new line and paste the story underneath (there are some example in there already)

