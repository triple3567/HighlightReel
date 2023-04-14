import ffmpeg, pprint
probe = ffmpeg.probe("/home/pi/HighlightReel/core/out/converted/2023-02-05-23-45-44.mp4")
video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
pprint.pprint(video_streams[0])