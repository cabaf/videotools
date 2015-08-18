import glob
import os

from argparse import ArgumentParser
from commands import getstatusoutput

def get_video_frame_rate(filename):
    """
      Obtains the video frame rate using ffmpeg.
    """
    cmd = 'ffmpeg -i %s 2>&1 | sed -n "s/.*, \(.*\) fp.*/\\1/p"' % filename
    status, result = getstatusoutput(cmd)
    if status:
        # ntsc video frame rate fixed.
        print "Unable to get factual frame rate."
        fr = 30000.0/1001.0
    else:
        fr = float(result)
    return fr

def main(input_path, output_path, subsample_rate):
    """
     Process a batch of video from an input directory. It extracts
     frames from a given subsampling rate.
    """
    files = glob.glob(os.path.join(input_path, "*"))
    nr_videos = len(files)
    for idx, f in enumerate(files):
        fr = get_video_frame_rate(f)
        vid = os.path.basename(f).split(".")[0]
        video_dir = os.path.join(output_path, vid)
        output_format = os.path.join(video_dir, "%06d.png")
        cmd = 'mkdir %s; ' % video_dir
        cmd += 'ffmpeg -i %s ' % f
        cmd += '-filter:v "select=not(mod(n\,10)),setpts=N/((%0.1f)*TB)" ' % fr
        cmd += '%s' % output_format
        status, result = getstatusoutput(cmd)
        if status:
            print "Unable to process video: %s" % f
        else:
            print "Processed video %s. (%d/%d)" % (f, idx+1, nr_videos)

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate a command list to extract \
                                         frames from a batch of videos. \
                                         Requires ffmpeg installed.")
    parser.add_argument("input_path", help="Directory where videos \
                                            are located.")
    parser.add_argument("output_path", help="Directory where video frames \
                                             will be alocated.")
    parser.add_argument("-s", dest="subsample_rate", type=int, default=10, 
                        help="Rate of frame subsampling.")
    args = parser.parse_args()
    if not (os.path.isdir(args.input_path)):
        raise RuntimeError("%s , Directory does not exist" % (input_path))
    if not (os.path.isdir(args.output_path)):
        raise RuntimeError("%s , Directory does not exist" % (output_path))
    main(**vars(args))
    print "Have a good day."
