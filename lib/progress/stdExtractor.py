import re

"""
This file extracts the time and duration from the FFmpeg 
stdout logs on command execution
"""


class Time:
    def __init__(self):
        """
        Simple class to store time values extracted
        datetime can be used from python lib
        """
        self.hour = None
        self.minute = None
        self.second = None

    def getTimeInSec(self):
        """
        returning time in secs
        :return: int
        """
        return (self.hour * 60 * 60) + (self.minute * 60) + self.second

    def __del__(self):
        """
        clean up
        :return: None
        """
        del self.hour
        del self.minute
        del self.second


class StdExtractor:
    def __init__(self):
        """
        Stdout logs extractor to extract the duration and time
        from the logs stdout
        """
        self.duration = None
        self.time = None

    def extractTimeDuration(self, line):
        """
        extract time and duration from the logs
        :param line: str, input log
        :return: duration, time (obj)
        """
        return self.extractDuration(line), self.extractTime(line)

    def extractTime(self, line):
        """
        Searching for time clause in the FFmpeg logs
        Ex: time=00:01:13.22
        :param line: str, stdout log
        :return: Time object
        """
        exp = re.compile(r'time=(\d+):(\d+):(\d+)')
        exp = exp.search(line)
        if exp:
            self.time = Time()
            self.time.hour = int(exp.group(1))
            self.time.minute = int(exp.group(2))
            self.time.second = int(exp.group(3))

        return self.time

    def extractDuration(self, line):
        """
        Searching for duration clause in FFmpeg logs
        since duration is displayed only once it is set
        only once and later returned the same value
        :param line: str, input log
        :return: time object
        """
        if self.duration is not None:
            return self.duration

        exp = re.compile(r'Duration: (\d{2}):(\d{2}):(\d{2})')
        exp = exp.search(line)
        if exp:
            self.duration = Time()
            self.duration.hour = int(exp.group(1))
            self.duration.minute = int(exp.group(2))
            self.duration.second = int(exp.group(3))

        return self.duration

    def __del__(self):
        """
        cleaning up
        :return: none
        """
        del self.duration
        del self.time
