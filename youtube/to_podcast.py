import files, os
from youtube.download import download_video_audio

def convert_playlist(playlist, playlist_folder):
    # Download videos
    episode_numbers = {}
    for episode_number, video in enumerate(playlist.videos):
        video_path = os.path.join(playlist_folder, 'episode_' + str(episode_number))
        download_video_audio(video.url, video_path + '.%(ext)s')
        episode_numbers[video_path + '.m4a'] = video

    # Embed video metadata
    for download_file_path in os.listdir(playlist_folder):
        if files.extension_is(download_file_path, 'm4a'):
            files.set_m4a_album(os.path.join(playlist_folder, download_file_path), playlist.name)
            files.set_m4a_cover(os.path.join(playlist_folder, download_file_path), os.path.join(playlist_folder, files.with_extension(download_file_path, 'jpg')))
            os.remove(os.path.join(playlist_folder, files.with_extension(download_file_path, 'jpg')))
            files.set_m4a_title(os.path.join(playlist_folder, download_file_path), episode_numbers[os.path.join(playlist_folder, download_file_path)].name)