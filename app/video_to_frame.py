import re
import shutil
import pathlib

FPS = 0.43  # count frames per second of video


def clean_destination(dst_path: str):
    try:
        shutil.rmtree(dst_path)
    except FileNotFoundError:
        pass
    pathlib.Path(dst_path).mkdir(parents=True, exist_ok=True)


def opencv_converter(source_filepath: str, dst_filepath: str) -> int:
    import cv2

    clean_destination(dst_filepath)

    vidcap = cv2.VideoCapture(source_filepath)
    saved_frame_counter = 0
    while True:
        frame_path = "%s/%d.jpg" % (dst_filepath, saved_frame_counter)
        success, image = vidcap.read()
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (saved_frame_counter * 1000 / FPS))
        if not success:
            break
        cv2.imwrite(frame_path, image)
        saved_frame_counter += 1
    return saved_frame_counter


def ffmpeg_converter(source_filepath: str, dst_filepath: str) -> int:
    import subprocess

    clean_destination(dst_filepath)

    proc = subprocess.Popen('ffmpeg -i %s -vf fps=%f "%s/%%d.jpg"' % (source_filepath, FPS, dst_filepath),
                            stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
    (out, err) = proc.communicate()
    return int(re.findall('frame=\s+(\d+)\s+fps=', str(out))[-1])


def av_converter(source_filepath: str, dst_filepath: str) -> int:
    import av
    import av.datasets

    clean_destination(dst_filepath)

    container = av.open(source_filepath)
    stream = container.streams.video[0]
    # Signal that we only want to look at keyframes.
    stream.codec_context.skip_frame = 'NONKEY'

    i = 0
    for frame in container.decode(stream):
        # We use `frame.pts` as `frame.index` won't make must sense with the `skip_frame`.
        frame.to_image().save('%s/%s.jpg' % (dst_filepath, i))
        i += 1
    return i