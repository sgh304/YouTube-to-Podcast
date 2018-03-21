import re, requests
from youtube.exceptions import PlaylistInfoException

class Playlist:
	'''An object containing information about a YouTube playlist'''
	def __init__(self, name):
		self.name = name
		self.videos = []

	def add_video(self, name, channel, url):
		'''Adds a video to the playlist'''
		self.videos.append(Video(name, channel, url))

class Video:
	'''An object containing information about a YouTube video'''
	def __init__(self, name, channel, url):
		self.name = name
		self.channel = channel
		self.url = url

def get_playlist_info(url):
	'''Scapes the information of a YouTube playlist and packages it into a Playlist object'''
	try:
		source = requests.get(url).text
		# Get playlist info
		playlist_name = re.search('(?<=data-list-title=")[\S\s]*?(?=")', source).group(0)
		playlist = Playlist(playlist_name)
		# Get video info
		for video_source in re.findall('<li class="yt-uix-scroller-scroll-unit[\S\s]*?<\/li>', source):
			video_name = re.search('(?<=data-video-title=")[\S\s]*?(?=")', video_source).group()
			video_channel = re.search('(?<=data-video-username=")[\S\s]*?(?=")', video_source).group(0)
			video_url = 'https://www.youtube.com/watch?v=' + re.search('(?<=data-video-id=")[\S\s]*?(?=")', video_source).group(0)
			playlist.add_video(video_name, video_channel, video_url)
		return playlist
	except Exception:
		raise PlaylistInfoException()