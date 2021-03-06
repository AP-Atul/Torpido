""" All custom exceptions """


class AudioStreamMissingException(Exception):
    """
    When there is no audio in some input video files
    Exception will be raised along with the below message
    """
    cause = "There is no audio in the video file."


class FFmpegProcessException(Exception):
    """
    When the subprocess did not able to do the rendering or
    some other FFmpeg error, this exception would be raised
    """
    cause = "FFmpeg has some problem processing."


class RankingOfFeatureMissing(Exception):
    """
    When due to some issue ranking for some feature(s) was
    not created, then exception will be raised.
    """
    cause = "Rank for some feature in missing. Cache file no longer exists."


class EastModelEnvironmentMissing(Exception):
    """
    When the model path is read and the environment variable
    is missing or not yet set this error will be raised
    """
    cause = "EAST_MODEL environment variable is missing or incorrect."


class WatcherFileMissing(Exception):
    """
    When in the watcher the system files for the stat is missing
    this exception will be raised and will display the message
    """
    cause = "[Watcher] System proc files are missing. Watcher is shutting down."


class ProcessDoesNotExists(Exception):
    """
    When process registered in the Manager (plimit.py), but the process
    does not exists or is terminates, this exception will be raised.
    This is alternative for the ProcessLookUpError.
    """

    def __init__(self, pid):
        self.cause = f"[Process Manager] The process with pid:{pid} is either terminated or does not exists."
