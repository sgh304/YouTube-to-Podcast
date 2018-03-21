class PlaylistInfoException(Exception):
    '''Indicates something went wrong in getting a playlist's information from YouTube'''
    pass

class VideoDownloadException(Exception):
    '''Indicates something went wrong in downloading a video from YouTube'''
    pass