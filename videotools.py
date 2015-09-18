import commands
import cv2
import numpy as np

def load_video(filename):
    h, w, nr_frames = get_video_dimensions(filename)
    video = np.zeros((h, w, nr_frames))
    cap = cv2.VideoCapture(filename)
    fidx = 0
    while(1):
        ret, img = cap.read()

        if ret==True:
            video[:,:,fidx] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            fidx += 1
        else:
            break
    return video

def get_video_dimensions(filename):
    return get_video_resolution(filename)[::-1] + [get_video_number_of_frames(filename)]

def get_video_frame_rate(filename):
    cmd = ['ffprobe', '-select_streams', 'v', '-show_streams', filename, '2>&1',
           '|', 'grep', 'avg_frame_rate', '|', 'sed', '-e', '"s/avg_frame_rate=//"']
    cmd = ' '.join(cmd)
    out = commands.getoutput(cmd)
    try:
        frame_rate = float(out.split('/')[0]) / float(out.split('/')[1])
    except:
        print 'Unable to get the number of frames for %s' % filename
        frame_rate = None
    return frame_rate

def get_video_number_of_frames(filename):
    cmd = ['ffprobe', '-select_streams', 'v', '-show_streams', filename, '2>&1',
           '|', 'grep', 'nb_frames', '|', 'sed', '-e', '"s/nb_frames=//"']
    cmd = ' '.join(cmd)
    out = commands.getoutput(cmd)
    try:
        nr_frames = int(out)
    except:
        print 'Unable to get the number of frames for %s' % filename
        nr_frames = None
    return nr_frames

def get_video_resolution(filename):
    cmd_width = ['ffprobe', '-select_streams', 'v', '-show_streams', filename,
                 '2>&1', '|', 'grep', 'width', '|', 'sed', '-e', '"s/width=//"']
    cmd_width = ' '.join(cmd_width)
    out_width = commands.getoutput(cmd_width)
    cmd_height = ['ffprobe', '-select_streams', 'v', '-show_streams', filename,
                 '2>&1', '|', 'grep', 'height', '|', 'sed', '-e',
                 '"s/height=//"']
    cmd_height = ' '.join(cmd_height)
    out_height = commands.getoutput(cmd_height)
    try:
        resolution = [int(out_width), int(out_height)]
    except:
        print 'Unable to get the resolution for %s' % filename
        resolution = None
    return resolution
