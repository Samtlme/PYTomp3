#!/usr/bin/env python3

import argparse
import os
import signal
import sys
from time import sleep
from pytube import YouTube
from moviepy.editor import *

parser = argparse.ArgumentParser(description="A Simple YT to MP3 script!")

parser.add_argument(
    '--url', help='URL of a video in full format. I.E --url https://www.youtube.com/watch?v=dQw4w9WgXcQ')
parser.add_argument(
    '--trim_start', help='Trim the first specified seconds of a video. I.E. --trim_start 10', metavar='')
parser.add_argument(
    '--trim_end', help='Trim the last specified seconds of a video. I.E. --trim_end 10', metavar='')

args = parser.parse_args()

def print_banner():
    banner="""
        **********************************************
        *                                            *
        *    ░▒█▀▀█░▒█░░▒█░▀█▀░▄▀▀▄░█▀▄▀█░▄▀▀▄░█▀▀█  *
        *    ░▒█▄▄█░▒▀▄▄▄▀░░█░░█░░█░█░▀░█░█▄▄█░░▒▀▄  *
        *    ░▒█░░░░░░▒█░░░░▀░░░▀▀░░▀░░▒▀░█░░░░█▄▄█  *
        *                                            *
        ****** By: Samtlme ***** version: v0.1 *******
    """
    lines = banner.split("\n")
    for line in lines:
        print(line)
        sleep(0.05)
        

def ctrl_c_handler(signum, frame):
    print("\nAborting...\n")

    if (yt_vid_title in locals()) or os.path.exists(f"{yt_vid_title}.mp4"):
        video.close()
        os.remove(f"{yt_vid_title}.mp4")
    sys.exit(1)
    
signal.signal(signal.SIGINT, ctrl_c_handler)

def trim_audio_clip(Audiofile):
    if args.trim_start or args.trim_end:
        
        if args.trim_end is None:
            args.trim_end = 0
        if args.trim_start is None:
            args.trim_start = 0
        
        os.rename(Audiofile, "tmp_" + Audiofile)
        audio = AudioFileClip("tmp_"+Audiofile)
        print("\nTrimming audiofile...\n")
        trimmed_audio = audio.subclip(args.trim_start, int(
            audio.duration - float(args.trim_end)))
        trimmed_audio.write_audiofile(Audiofile)
        audio.close()
        os.remove("tmp_" + Audiofile)


def download_and_convert():
    try:
        global yt_vid_title
        global video
        
        yt_vid = YouTube(args.url)
        print("\nDownloading video...")
        yt_vid.streams.filter(
            progressive=True, file_extension='mp4').first().download()
        yt_vid_title = yt_vid.streams.filter(
            progressive=True, file_extension='mp4').first().title

        # Remove quotation marks, otherwise ffmpeg/moviepy may break

        yt_vid_title = yt_vid_title.replace("'", "")
        yt_vid_title = yt_vid_title.replace('"', '')

        # Convert the files

        video = VideoFileClip(yt_vid_title + ".mp4")
        print("\nConverting to mp3...\n")
        video.audio.write_audiofile(yt_vid_title + ".mp3")
        video.close()
        os.remove(yt_vid_title + ".mp4")

        # Trim if requested
        trim_audio_clip(yt_vid_title + ".mp3")
        
        print("\nFile saved to " + os.getcwd() + yt_vid_title + ".mp3\n")

    except Exception as e:
        print(f"[!] [ERROR] An error has occurred. {str(e)}")

        if os.path.exists(f"{yt_vid_title}.mp3"):
            os.remove(f"{yt_vid_title}.mp3")

        if os.path.exists(f"{yt_vid_title}.mp4"):
            os.remove(f"{yt_vid_title}.mp4")
            

def main():
    if not args.url:
        parser.print_help()

    elif args.url:
        download_and_convert()


if __name__ == '__main__':
    print_banner()
    main()
