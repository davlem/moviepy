"""
moviepy.video.io - VideoFileClipManager module.
"""

from delayed_video_file_clip import (
    DelayedVideoFileClip,
    )
from moviepy.editor import (
    concatenate_videoclips,
    )

class VideoFileClipManager(list):
    """Video File Clip Manager object

    Manage multiple video file clips for don't read the same file many times.
    """

    def __init__(self, *args, **kwargs):
        """constructor
        """
        self.__dict__.update(kwargs)
        self._ar = args
        self.clip_files = []

    def _find_clip(self, filename):
        """find clip with filename in list method
        """
        _re = None
        for _e0 in self:
            if _e0.filename == filename:
                _re = _e0
                break
        return _re

    def load_file_clip(self, filename):
        """load file clip from filename method
        """
        _fc = self._find_clip(filename)
        if _fc is None:
            _fc = DelayedVideoFileClip(filename)
        self.append(_fc)

    def _init_clips(self, ):
        """init clips method
        """
        for _e0 in self:
            if _e0.reader is None:
                _e0.init()
                _e0.init_audio()

    @property
    def duration(self,):
        """duration method

        sum all videoclips durations
        """
        _re = 0
        for _n0, _e0 in enumerate(self):
            if _e0.duration is None:
                _e0.init()
                # find clips with same filename
                for _e1 in self[_n0 + 1:]:
                    if _e0.filename == _e1.filename:
                        _e1 = _e0

            _re += _e0.duration

        return _re

    def write_videofile(self, *args, **kwargs):
        """write videofile with all clips in collection method
        """
        # ----
        # need init all videoclips
        # ----
        _vfn = args[0]
        self._init_clips()
        _re = concatenate_videoclips(self)
        _re = _re.write_videofile(_vfn, **kwargs)

        # close all VideoFileClip

        return _re

    def close(self, ):
        """close method
        """
        for _e0 in self:
            if _e0.reader is not None:
                _e0.reader.close()

    def __repr__(self, ):
        """repr method doc
        """
        return self.__unicode__()

    def __unicode__(self, ):
        """unicode method
        """
        return u'<%s: %i videoclips loaded.>' % (
            self.__class__.__name__,
            len(self)
            )
