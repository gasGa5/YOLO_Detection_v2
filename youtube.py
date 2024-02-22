from pytube import YouTube
import os
class stream_YOUTUBE():
    def __init__(self, url, filename):
        self.url = url
        self.youtube = YouTube(url)
        self.video = self.youtube.streams.first()
        self.filename = filename

    def download(self,):
        if not os.path.exists(self.filename):
            self.video.download(filename = self.filename)

if __name__ == "__main__":
    URL = "https://youtu.be/s1YxTMDZw3s?si=19dTZBrWocuusdnS" 
    FILENAME = 'firevedio12.mp4'
    
    download = stream_YOUTUBE(url = URL, filename = FILENAME)
    download.download()

