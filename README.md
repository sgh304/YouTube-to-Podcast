# YouTube to Podcast
[YouTube to Podcast Splash](https://i.imgur.com/gkgKrYT.png)
A program written in Python that automatically downloads audio files from any public YouTube playlist to create a poorman's podcast, and even uploads those files to a smartphone's VLC app if desired.

**YouTube to Podcast** is also a proof of concept for YAGUI, a Python GUI module built on top of pygame. 

## How to Use
An installation of pygame is required to run any YAGUI app. It can be installed on most machines with pip:
```
pip install pygame
```

With a pygame installation, Youtube to Podcast can be launched by executing the following command in the project's root directory:
```
python launcher.py
```

A step-by-step guide can be found by clicking the "Help" button inside the app.

1. Retrieve the link to the desired YouTube playlist. (Note: This should be the link to the first video in the playlist, not the playlist itself! It ends with something like "&index=1&t=0s")
2. If desired, retrieve the address for upload to a VLC smartphone app. This can be obtained by opening the app's menu and tapping the "Sharing via WiFi" button.
3. Type/paste (right-click) each respective address into the YouTube to Podcast app.
4. Press Go!