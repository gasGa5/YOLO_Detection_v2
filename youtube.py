from pytube import YouTube

# YouTube 영상의 URL
url = 'https://www.youtube.com/watch?v=f15-muqCGpc'  # 여기에 원하는 영상의 URL을 넣으세요

# YouTube 객체 생성
youtube = YouTube(url)

# 영상 다운로드
youtube.streams.first().download()
