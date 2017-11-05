"""moviepy.video.io - VideoFileClipManager test module.
"""

import unittest2 as unittest
from test.unit._core import (
    count_elapsed_time,
    )
from moviepy.video.io import VideoFileClipManager as _mo


def get_test_tmp_path():
    """get test tmp path method
    """
    return u'test/tmp'


def get_test_media_path():
    """get test media path method
    """
    return u'/'.join((
        get_test_tmp_path(),
        u'media',
        ))


def get_test_media_path_for_file(filename):
    """method
    """
    return u'/'.join((
        get_test_media_path(),
        filename,
        ))

def get_test_tmp_path_for_file(filename):
    """method
    """
    return u'/'.join((
        get_test_tmp_path(),
        filename,
        ))


class test_VideoFileClipManager(unittest.TestCase):

    def setUp(self):
        """setup method tests
        """
        self._video_test_name = "media/big_buck_bunny_432_433.webm"
        self._video_test_name1 = "media/big_buck_bunny_0_30.webm"

        # data to test
        self._d0 = (
            # method_method
            (0, 1, 2, 3,),
            
            # method_join_big_videoclips_files
            (
                # ouput, video_list
                (
                        '01Y9dI_videosport.webm',
                        (
                        'part_2hAiyH_videosport.webm',
                        'part_5rQCba_videosport.webm',
                        'part_7jqySb_videosport.webm',
                        'part_bbx90Q_videosport.webm',
                        'part_DgRTqh_videosport.webm',
                        'part_EqudBP_videosport.webm',
                        'part_FCNMxq_videosport.webm',
                        'part_FE6fET_videosport.webm',
                        'part_fgxLAB_videosport.webm',
                        'part_gOfxxj_videosport.webm',
                        'part_O8lsvI_videosport.webm',
                        'part_q9Yhme_videosport.webm',
                        'part_sUCOhv_videosport.webm',
                        'part_TnuJSk_videosport.webm',
                        'part_UD8kK6_videosport.webm',
                        'part_ulUbFj_videosport.webm',
                        ),
                    ),
                ),

            )

        # test results
        self._r0 = (
            # method_method
            (0, 1, 2, 3,),

            # method_join_big_videoclips_files
            (
                (True)
                ),

            )

    def test_load_many_videoclips_class(self, ):
        _in, _me = 0, _mo.VideoFileClipManager()

        def _load_many_video_clips():
            for _e0 in range(160):
                _me.load_file_clip(self._video_test_name)
            return _me
            
        _me, _time = count_elapsed_time(
            _load_many_video_clips,
            ((), {}),
            show=True,
            )
        self.assertEqual(_me.duration, 160.0)

    def test_method_join_big_videoclips_files(self, ):
        _in, _me = 1, _mo.VideoFileClipManager()

        def _load_many_video_clips(list_):
            for _e0 in list_:
                _me.load_file_clip(
                    get_test_media_path_for_file(_e0)
                    )
            return _me

        for _n0, _e0 in enumerate(self._d0[_in]):
            _me, _time = count_elapsed_time(
                _load_many_video_clips,
                ((_e0[1],), {}),
                show=True
                )
            _re, _time = count_elapsed_time(
                _me.write_videofile, 
                ((get_test_tmp_path_for_file(_e0[0]),), {}),
                show=True,
                )

            _r0 = self._r0[_in][_n0]
            self.assertEqual(_d0, _r0)


if __name__=='__main__':
    unittest.main()
