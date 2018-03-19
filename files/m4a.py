import mutagen.mp4

# MP4 tag constants from https://mutagen.readthedocs.io/en/latest/api/mp4.html
class TAGS:
	ALBUM = '\xa9alb'
	COVER = 'covr'
	TITLE = '\xa9nam'

def set_m4a_album(m4a_path, album):
	'''Sets the album of an m4a file'''
	m4a = mutagen.mp4.MP4(m4a_path)
	m4a[TAGS.ALBUM] = album
	m4a.save()

def set_m4a_cover(m4a_path, cover_path):
	'''Sets the album cover of an m4a file to a specfied image'''
	m4a = mutagen.mp4.MP4(m4a_path)
	with open(cover_path, 'rb') as image_file:
		image_data = image_file.read()
	cover = mutagen.mp4.MP4Cover(image_data, mutagen.mp4.MP4Cover.FORMAT_JPEG)
	m4a[TAGS.COVER] = [cover]
	m4a.save()

def set_m4a_title(m4a_path, title):
	'''Sets the title of an m4a file'''
	m4a = mutagen.mp4.MP4(m4a_path)
	m4a[TAGS.TITLE] = title
	m4a.save()
