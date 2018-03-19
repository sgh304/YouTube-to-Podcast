import subprocess

def download_video_audio(url, path, thumbnail = True):
	'''Downloads the audio of a video to the specified path'''
	cmd = ['youtube-dl', '-f', 'mp4', '-o', path, '--extract-audio', url]
	if thumbnail:
		cmd.insert(len(cmd) - 1, '--write-thumbnail')
	subprocess.run(cmd)