import os
import files
from webdriver import PatientDriver

def upload_to_vlc(upload_url, playlist_folder):
    driver = PatientDriver()
    driver.open()
    driver.go_to(upload_url)
    for download_file_path in os.listdir(playlist_folder):
        if files.extension_is(download_file_path, 'm4a'):
            driver.send_keys('//input[@type="file"]', os.path.join(playlist_folder, download_file_path))