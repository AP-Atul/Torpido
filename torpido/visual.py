"""
This file reads the video and gives ranking to frames
that have motion in it, saves in the dictionary with frame numbers
this dictionary is then saved in a joblib file defined in constants.py
"""

from time import sleep

import cv2

import numpy as np

from .config.cache import Cache
from .config.config import Config
from .config.constants import *
from .tools.logger import Log
from .tools.ranking import Ranking
from .video import Stream


class Visual:
    """
    Class to perform Visual Processing on the input video file. Motion and Blur detections
    are used to calculate the rank. The ranks are per frame, so later the ranks are
    normalized to sec

    Attributes
    ----------
    self.__blur_threshold : int
        threshold to rank the blur feature
    self.__motion_threshold : int
        threshold to rank the motion feature
    self.__fps : float
        input video fps
    self.__frame_count : int
        number of frames
    self.__motion : list
        list of the ranks for the motion feature
    self.__blur : list
        list of the ranks for the blur feature
    self.__cache : Cache
        cache object to store the data
    self.__video_stream : Stream
        video reader object to read the video and save it in thread
    """

    def __init__(self):
        cv2.setUseOptimized(True)
        self.__cache = Cache()
        self.__blur_threshold, self.__motion_threshold = Config.BLUR_THRESHOLD, Config.MOTION_THRESHOLD
        self.__frame_count = self.__fps = self.__motion = self.__blur = None
        self.__video_stream = self.__video_pipe = None

    def __detect_blur(self, image):
        """
        Laplacian take 2nd derivative of one channel of the image(gray scale)
        It highlights regions of an image containing rapid intensity changes, much like the Sobel and Scharr operators.
        And then calculates the variance (squared SD), then check if the variance satisfies the Threshold value/

        Parameters
        ---------
        image : array
            frame from the video file
        """
        # if blur rank is 0 else RANK_BLUR
        return 0 if cv2.Laplacian(image, cv2.CV_64F).var() >= self.__blur_threshold else Config.RANK_BLUR

    def __timed_ranking_normalize(self):
        """
        Since ranking is added to frames, since frames are duration * fps
        and audio frame system is different since frame are duration * rate
        so we need to generalize the ranking system
        sol: ranking sec of the video and audio, for than taking mean of the
        frames to generate rank for video.

        Since ranking is 0 or 1, the mean will be different and we get more versatile
        results.

        We will read both the list and slice the video to get 1 sec of frames(1 * fps) and get
        mean/average as the rank for the 1 sec

        """
        motion_normalize, blur_normalize = list(), list()
        for i in range(0, int(self.__frame_count), int(self.__fps)):
            if len(self.__motion) >= (i + int(self.__fps)):
                motion_normalize.append(np.mean(self.__motion[i: i + int(self.__fps)]))
                blur_normalize.append(np.mean(self.__blur[i: i + int(self.__fps)]))
            else:
                break

        # saving all processed stuffs
        Ranking.add(CACHE_RANK_MOTION, motion_normalize)
        Ranking.add(CACHE_RANK_BLUR, blur_normalize)
        Log.d(f"Visual rank length {len(motion_normalize)}  {len(blur_normalize)}")
        Log.i(f"Visual ranking saved .............")

    def __del__(self):
        """ Clean  ups """
        del self.__cache, self.__video_stream

    def start_processing(self, pipe, input_file, display=False):
        """
        Function to run the processing on the Video file. Motion and Blur features are
        detected and based on that ranking is set

        Parameters
        ----------
        pipe : Communication link
            set progress on the ui
        input_file : str
            input video file
        display : bool
            True to display the video while processing
        """

        if os.path.isfile(input_file) is False:
            Log.e(f"File {input_file} does not exists")
            return

        # maintaining the motion and blur frames list
        self.__motion, self.__blur = list(), list()
        self.__video_stream = Stream(str(input_file)).start()
        my_clip = self.__video_stream.stream

        if not self.__video_stream.more():
            sleep(0.1)

        fps = my_clip.get(cv2.CAP_PROP_FPS)
        total_frames = my_clip.get(cv2.CAP_PROP_FRAME_COUNT)
        self.__fps, self.__frame_count = fps, total_frames

        self.__cache.write_data(CACHE_FPS, self.__fps)
        self.__cache.write_data(CACHE_FRAME_COUNT, self.__frame_count)
        self.__cache.write_data(CACHE_VIDEO_WIDTH, cv2.CAP_PROP_FRAME_WIDTH)
        self.__cache.write_data(CACHE_VIDEO_HEIGHT, cv2.CAP_PROP_FRAME_HEIGHT)

        # printing some info
        Log.d(f"Total count of video frames :: {total_frames}")
        Log.i(f"Video fps :: {fps}")
        Log.i(f"Bit rate :: {cv2.CAP_PROP_BITRATE}")
        Log.i(f"Video format :: {cv2.CAP_PROP_FORMAT}")
        Log.i(f"Video four cc :: {cv2.CAP_PROP_FOURCC}")

        first_frame = self.__video_stream.read()
        first_frame_processed, original, count = True, None, 0

        while self.__video_stream.more():
            frame = self.__video_stream.read()
            if frame is None:
                break

            # if display requested get a good color frame
            if display:
                original = frame
            count += 1

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.__blur.append(self.__detect_blur(frame))
            frame = cv2.GaussianBlur(frame, (21, 21), 0)

            if first_frame_processed:
                first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
                first_frame = cv2.GaussianBlur(first_frame, (21, 21), 0)
                first_frame_processed = False

            frame_delta = cv2.absdiff(first_frame, frame)
            thresh = cv2.threshold(frame_delta, self.__motion_threshold, 255, cv2.THRESH_BINARY)[1]
            # thresh = cv2.adaptiveThreshold(frameDelta, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

            thresh_max = np.max(thresh)
            if thresh_max > 0:
                self.__motion.append(Config.RANK_MOTION)
            else:
                self.__motion.append(0)

            if display:

                # adding the frame to the pipe
                if self.__video_pipe is not None:
                    self.__video_pipe.send(ID_COM_VIDEO, original)

                # not a ui request, so this works
                else:
                    cv2.imshow("Video Output", original)
                    # if the `q` key is pressed, break from the loop

            # assigning the processed frame as the first frame to cal diff later on
            first_frame = frame

            # setting progress on the ui
            if pipe is not None:
                pipe.send(ID_COM_PROGRESS, float((count / total_frames) * 95.0))

        # completing the progress
        if pipe is not None:
            pipe.send(ID_COM_PROGRESS, 95.0)

        # clearing memory
        self.__video_stream.stop()

        # calling the normalization of ranking
        self.__timed_ranking_normalize()

    def set_pipe(self, pipe):
        """
        Send video frame to the ui threads for displaying, since open cv
        is using the Qt backend, it should be in the main ui thread or else
        the im show does not work in the sub process

        Parameters
        ----------
        pipe : some queue
            add frames and continuous read to the ui display
        """
        self.__video_pipe = pipe
