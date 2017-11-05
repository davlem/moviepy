import os
import gc

from moviepy.core import (
    get_key_or_default,
    )
from moviepy.video.VideoClip import VideoClip
from moviepy.audio.io.DelayedAudioFileClip import DelayedAudioFileClip
from moviepy.Clip import Clip
from moviepy.video.io.fast_ffmpeg_reader import Fast_FFMPEG_VideoReader
# ~ from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader


class DelayedVideoFileClip(VideoClip):

    """

    A video clip originating from a movie file with delayed file load. For instance: ::

        >>> clip = VideoFileClip("myHolidays.mp4")
        >>> clip2 = VideoFileClip("myMaskVideo.avi")


    Parameters
    ------------

    filename:
      The name of the video file. It can have any extension supported
      by ffmpeg: .ogv, .mp4, .mpeg, .avi, .mov etc.

    has_mask:
      Set this to 'True' if there is a mask included in the videofile.
      Video files rarely contain masks, but some video codecs enable
      that. For istance if you have a MoviePy VideoClip with a mask you
      can save it to a videofile with a mask. (see also
      ``VideoClip.write_videofile`` for more details).

    audio:
      Set to `False` if the clip doesn't have any audio or if you do not
      wish to read the audio.

    target_resolution:
      Set to (desired_height, desired_width) to have ffmpeg resize the frames
      before returning them. This is much faster than streaming in high-res
      and then resizing. If either dimension is None, the frames are resized
      by keeping the existing aspect ratio.

    resize_algorithm:
      The algorithm used for resizing. Default: "bicubic", other popular
      options include "bilinear" and "fast_bilinear". For more information, see
      https://ffmpeg.org/ffmpeg-scaler.html

    fps_source:
      The fps value to collect from the metadata. Set by default to 'tbr', but
      can be set to 'fps', which may be helpful if importing slow-motion videos
      that get messed up otherwise.


    Attributes
    -----------

    filename:
      Name of the original video file.

    fps:
      Frames per second in the original file.
    
    
    Read docs for Clip() and VideoClip() for other, more generic, attributes.

    """

    def __init__(self,
        *args, **kwargs
        # ~ filename, has_mask=False,
        # ~ audio=True, audio_buffersize = 200000,
        # ~ target_resolution=None, resize_algorithm='bicubic',
        # ~ audio_fps=44100, audio_nbytes=2, verbose=False,
        # ~ fps_source='tbr'
        ):

        VideoClip.__init__(self)
        
        self._ar = _ar = args, kwargs
        _kw = _ar[1]

        # Make a reader
        self.reader = None # need this just in case FFMPEG has issues (__del__ complains)
        self.filename = _ar[0][0]
        self.has_mask = get_key_or_default('has_mask', False, _kw)
        self.audio = get_key_or_default('audio', True, _kw)
        self.audio_buffersize = get_key_or_default('audio_buffersize', 200000, _kw)
        self.target_resolution = get_key_or_default('target_resolution', None, _kw)
        self.resize_algorithm = get_key_or_default('resize_algorithm', 'bicubic', _kw)
        self.audio_fps = get_key_or_default('audio_fps', 44100, _kw)
        self.audio_nbytes = get_key_or_default('audio_nbytes', 2, _kw)
        self.verbose = get_key_or_default('verbose', False, _kw)
        self.fps_source = get_key_or_default('fps_source', 'tbr', _kw)

        self.pix_fmt= "rgba" if self.has_mask else "rgb24"

        # ~ self._set_reader()

    def _set_reader(self, ):
        """set reader method
        """
        self.reader = Fast_FFMPEG_VideoReader(
            self.filename,
            pix_fmt=self.pix_fmt,
            target_resolution=self.target_resolution,
            resize_algo=self.resize_algorithm,
            fps_source=self.fps_source,
            # ~ print_infos=True,
            )

    def init(self, ):
        """init load clip method
        """
        filename = self.filename
        has_mask = self.has_mask
        audio = self.audio

        self._set_reader()

        # Make some of the reader's attributes accessible from the clip
        self.duration = self.reader.duration
        self.end = self.reader.duration

        self.fps = self.reader.fps
        self.size = self.reader.size
        self.rotation = self.reader.rotation

        self.filename = self.reader.filename

        if has_mask:

            self.make_frame = lambda t: self.reader.get_frame(t)[:,:,:3]
            mask_mf =  lambda t: self.reader.get_frame(t)[:,:,3]/255.0
            self.mask = (VideoClip(ismask = True, make_frame = mask_mf)
                       .set_duration(self.duration))
            self.mask.fps = self.fps

        # ~ else:
            # ~ self.make_frame = lambda t: self.reader.get_frame(t)

        self.init_audio()

        # free memory
        del self.reader
        gc.collect()
        self.reader = None

    def init_audio(self, ):
        """init audio method
        """
        filename = self.filename
        audio = self.audio
        if self.reader is None:
            self._set_reader()

        # Make a reader for the audio, if any.
        _read_audio = self.reader.infos['audio_found']
        if audio and _read_audio:
            self.audio = DelayedAudioFileClip(
                filename,
                buffersize=self.audio_buffersize,
                fps=self.audio_fps,
                nbytes=self.audio_nbytes
                )
            self.audio.init()
        else:
            self.audio = None

    def make_frame(self, t):
        """make frame method
        """
        if self.reader is None:
            self._set_reader()
        return self.reader.get_frame(t)

    def __del__(self):
        """ Close/delete the internal reader. """
        try:
            del self.reader
        except AttributeError:
            pass

        try:
            del self.audio
        except AttributeError:
            pass
