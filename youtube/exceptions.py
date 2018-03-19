class PlaylistInfoException(Exception):
    pass

class VideoDownloadException(Exception):
    def __init__(self, path):
        Exception.__init__(self)
        self.path = path