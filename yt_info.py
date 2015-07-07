from argparse import ArgumentParser
import commands
import json

def retrieve_video_info(video_id):
    """ Retrieves information about Youtube Videos.
        Requires youtube-dl
        Args:
            - video_id: Youtube video identifier (11 str code)
        Return:
            - duration: [Integer] length of the video in seconds.
            - resolution: [String] video resolution (WxH).
            - bitrate: [Integer] sum of VidBitRate & AudioBitRate.
            - fps: [Integer] frame per second rate of the video.
    """
    cmd = "youtube-dl -j https://www.youtube.com/watch?v=%s" % video_id
    try:
        output = commands.getoutput(cmd)
        json_data = json.loads(output)
    except:
        print "Video %s can't be processed." % video_id

    duration = json_data["duration"]
    # We look for the best quality video with mp4 extension.
    prefered_ext = "mp4"
    best_image_idx, best_audio_idx = None, None
    resolution, bitrate, fps = None, None, None
    best_abr, best_tbr = 0, 0
    for idx, stream in enumerate(json_data["formats"]):
        try:
            if (stream["ext"]==prefered_ext)&("fps"in stream)&("tbr"in stream):
                if stream["tbr"] > best_tbr:
                    best_image_idx = idx
                    best_tbr = stream["tbr"]
            if (stream["acodec"] != "none"):
                if stream["abr"] > best_abr:
                    best_audio_idx = idx
                    best_abr = stream["abr"]
        except:
            continue
    if best_image_idx is not None:
        resolution = "%sx%s" % (json_data["formats"][best_image_idx]["width"],
                                json_data["formats"][best_image_idx]["height"])
        fps = int("%s" % (json_data["formats"][best_image_idx]["fps"]))
        vbr = best_tbr
    if best_audio_idx is not None:
        abr = best_abr
    if (best_image_idx is not None) or (best_audio_idx is not None):
        bitrate = vbr + abr
    return duration, resolution, bitrate, fps

if __name__ == "__main__":
    parser = ArgumentParser(description="Gets info from Youtube Video.")
    parser.add_argument("video_id", help="Youtube video identifier.")
    args = vars(parser.parse_args())
    dur, res, tbr, fps = retrieve_video_info(**args)
    print "Duration:\t\t\t\t%d seconds" % dur
    print "Resolution:\t\t\t\t%s" % res
    print "Bitrate:\t\t\t\t%d kbps" % tbr
    print "FrameRate:\t\t\t\t%d fps" % fps
