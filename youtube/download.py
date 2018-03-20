import subprocess

def start_download_video_audio_process(url, path):
    '''Returns a Popen instance of a subprocess that is downloading the audio of the video at the specified url to the specified path'''
    cmd = ['youtube-dl', '-f', 'mp4', '-o', path, '--extract-audio', url]
    return subprocess.Popen(cmd)