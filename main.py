import ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import random
import os
import cv2
import pydub
from pydub import AudioSegment
import uuid
import pyttsx3
#init functions
engine = pyttsx3.engine.Engine()
engine.setProperty("rate", 180)

#helper funcs
def get_mp4_duration(filename): 
    """
    get mp4 duration
    """
    
    video = cv2.VideoCapture(filename)

    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS) 
    duration = frame_count / fps
    return duration


wait_time_between_title_and_story = 1



chosen_file = random.choice(os.listdir(os.path.abspath("./stories/")))

with open(os.path.abspath(f"./stories/{chosen_file}"),'r', encoding='utf-8') as inf:
    lines = inf.read().splitlines()
    for i in lines:
        if i == "":
            lines.remove(i)
    title = lines[0]
    lines.pop(0)
    story = "".join(lines)
    #title_tts = gtts.gTTS(title, lang='en', tld='com.au')
    #story_tts = gtts.gTTS(story, lang='en', tld='com.au')
    engine.save_to_file(title, "tmptitle.mp3")
    engine.save_to_file(story, "tmpstorytts.mp3")
    #title_tts.save("tmptitle.mp3")
    #story_tts.save("tmpstorytts.mp3")
    engine.runAndWait()

print("closed file")

tts_talk_length = 0
title_tts_file = AudioSegment.from_file("tmptitle.mp3")
tts_talk_length += title_tts_file.duration_seconds

story_tts_file = AudioSegment.from_file("tmpstorytts.mp3")
tts_talk_length += story_tts_file.duration_seconds

chosen_video = random.choice(os.listdir(os.path.abspath("./game_footage/")))

start_time = random.randrange(0, int(get_mp4_duration(f"./game_footage/{chosen_video}") - (tts_talk_length + wait_time_between_title_and_story)))

ffmpeg_extract_subclip(f"./game_footage/{chosen_video}", start_time, start_time + wait_time_between_title_and_story + tts_talk_length, targetname="tmp_gameplay_footage.mp4") 

audio1 = AudioSegment.from_file("tmptitle.mp3")
audio2 = AudioSegment.from_file("tmpstorytts.mp3")
silence = AudioSegment.silent(duration=wait_time_between_title_and_story * 1000)
audio3 = audio1 + silence + audio2 #combined audio
audio3.export("tmp_full_audio_track.mp3")

input_video = ffmpeg.input('./tmp_gameplay_footage.mp4')

input_audio = ffmpeg.input('./tmp_full_audio_track.mp3')

tag = uuid.uuid4()
print("all good so far")
ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'./reddit_story_{tag}.mp4').run()


#cleanup
files_to_delete = [os.path.abspath("./tmp_full_audio_track.mp3"), os.path.abspath("./tmp_gameplay_footage.mp4"), os.path.abspath("./tmpstorytts.mp3"), os.path.abspath("./tmptitle.mp3")]

for i in files_to_delete:
    if os.path.isfile(i):
        os.remove(i)
