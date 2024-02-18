from youtube import stream_YOUTUBE
from test_camera import Camera_Detection

if __name__ == "__main__":
    URL = "https://www.youtube.com/shorts/UucWbiJaP-Q" 
    FILENAME = 'firevedio2.mp4'
    WEIGHT_PATH = './firesmoke.pt'
    VEDIO_PATH = FILENAME
    CONFIDENCE_THRESHOLD = 0.3
    FRAME_WIDTH = 160
    FRAME_HEIGHT = 256
    FRAME = 30
    WAIT_TIME = 1
    
    download = stream_YOUTUBE(url = URL, filename = FILENAME)
    download.download()
    
    cam = Camera_Detection(weight_path = WEIGHT_PATH , vedio_path = VEDIO_PATH, 
                           conf_threshold = CONFIDENCE_THRESHOLD, 
                           frame_width = FRAME_WIDTH, frame_height = FRAME_HEIGHT 
                           , frame = FRAME, wait_time= WAIT_TIME)
    cam.frame_set()
    cam.Start_Detection()