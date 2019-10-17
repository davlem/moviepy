"""moviepy.video.io - DelayedVideoFileClip test module.
"""

import unittest2 as unittest
from moviepy.video.io import delayed_video_file_clip as _mo
from moviepy.video.io import fast_ffmpeg_reader as _mo0
from moviepy import editor as _mo1

from test.unit._core import (
    print_memory_usage,
    count_elapsed_time,
    )


class test_DelayedVideoFileClip(unittest.TestCase):

    def setUp(self):
        """setup method tests
        """
        target_resolution = (128, 128)
        load_counts = 160
        self._video_test_name = "media/big_buck_bunny_432_433.webm"
        self._video_test_kw = {
            'target_resolution': target_resolution
            }

        # data to test
        self._d0 = (
            # 0
            # test_VideoFileClip_method
            (
                # args, kwargs
                ((
                    self._video_test_name,
                    ), {
                    'target_resolution': target_resolution
                    }),
                ),

            # test_load_many_VideoFileClip_method
            (
                # load_counts, args, kwargs
                (
                    load_counts, (
                    self._video_test_name,
                    ),{
                    'target_resolution': target_resolution
                    }),
                ),

            # test_get_frame_method
            (
                (0,),
                ),

            # test_ffmpeg_parse_infos_method
            (
                ((
                    self._video_test_name,
                    ), dict(
                        print_infos=False, check_duration=True,
                       fps_source='tbr'
                        )
                    ),
                ),

            # test_write_videofile_method
            (
                ('test/tmp/writevideo_to_remove.webm',),
                ),

            # 5
            # test_concatenate_videoclips_method
            (
                (
                    # videos to concat, output
                    (self._video_test_name, self._video_test_name),
                    'test/tmp/concatvideo_to_remove.webm',
                    ),
                (
                    # videos to concat, output
                    [self._video_test_name] * load_counts,
                    'test/tmp/concatvideo_to_remove.webm',
                    ),
                ),

            )

        # test results
        self._r0 = (
            # 0
            # test_DelayedVideoFileClip_method
            (
                # duration
                (1.0),
                ),

            # test_load_many_DelayedVideoFileClip_method
            (
                # duration
                (1.0 * load_counts),
                ),

            # test_get_frame_method
            (
                (target_resolution),
                ),

            # test_ffmpeg_parse_infos_method
            (
                ({
                'video_found': True, 'video_nframes': 25, 'video_rotation': 0,
                'audio_found': True, 'video_fps': 24.0,
                'video_size': [1280, 720], 'duration': 1.0,
                'video_duration': 1.0, 'audio_fps': 'unknown'
                    }),
                ),

            # test_write_videofile_method
            (
                True,
                ),

            # 5
            # test_concatenate_videoclips_method
            (
                # duration
                (1.0 * 2),
                (1.0 * load_counts),
                ),

            )

    def _get_delayed_videofileclip_with_file(self, filename):
        _re = _mo.DelayedVideoFileClip(
            filename,
            **self._video_test_kw
            )
        return _re

    def _get_delayed_video_file_clip(self, ):
        _re = self._get_delayed_videofileclip_with_file(
            self._video_test_name,
            )
        return _re

    def test_DelayedVideoFileClip_method(self, ):
        _in, _me = 0, _mo.DelayedVideoFileClip
        for _n0, _e0 in enumerate(self._d0[_in]):
            print_memory_usage()
            _d0 = _me(*_e0[0], **_e0[1])
            _d0.init()
            print_memory_usage()
            _r0 = self._r0[_in][_n0]
            self.assertEqual(_d0.duration, _r0)

    def test_load_many_DelayedVideoFileClip_method(self, ):
        _in, _me = 1, _mo.DelayedVideoFileClip
        for _n0, _e0 in enumerate(self._d0[_in]):
            print_memory_usage()
            _d0 = [
                _me(*_e0[1], **_e0[2]) for _n1 in range(_e0[0])
                ]
            print_memory_usage()
            [
                _e1.init() for _e1 in _d0
                ]
            print_memory_usage()
            _r0 = self._r0[_in][_n0]
            self.assertEqual(sum([
                _e1.duration for _e1 in _d0
                ]), _r0)

    def test_get_frame_method(self, ):
        _ob = self._get_delayed_video_file_clip()
        _in, _me = 2, _ob.get_frame
        for _n0, _e0 in enumerate(self._d0[_in]):
            _d0 = _me(*_e0)
            _r0 = self._r0[_in][_n0]
            # target_resolution
            self.assertEqual(_d0.shape[0:2], _r0)

    def test_ffmpeg_parse_infos_method(self, ):
        _in, _me = 3, _mo0.ffmpeg_parse_infos
        for _n0, _e0 in enumerate(self._d0[_in]):
            print_memory_usage()
            _d0, _time = count_elapsed_time(_me, _e0, show=True)
            print_memory_usage()
            _r0 = self._r0[_in][_n0]
            self.assertEqual(_d0, _r0)

    def test_write_videofile_method(self, ):
        _ob = self._get_delayed_video_file_clip()
        # init required
        _ob.init()
        _in, _me = 4, _ob.write_videofile
        for _n0, _e0 in enumerate(self._d0[_in]):
            _d0 = _me(*_e0)
            _r0 = self._r0[_in][_n0]
            # target_resolution
            self.assertEqual(_d0, _r0)
        _ob.close()

    def test_concatenate_videoclips_method(self, ):
        # init required
        _in, _me = 5, _mo1.concatenate_videoclips
        for _n0, _e0 in enumerate(self._d0[_in]):
            _ob = [
                self._get_delayed_videofileclip_with_file(_e1) for _e1 in _e0[0]
                ]
            # init video clips
            [
                _e1.init() for _e1 in _ob
                ]
            _d0 = _me(_ob)
            _r0 = self._r0[_in][_n0]
            self.assertEqual(_d0.duration, _r0)


if __name__=='__main__':
    unittest.main()
