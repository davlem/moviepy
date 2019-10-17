"""moviepy.video.io - VideoFileClipManager test module.
"""

from thread import (
    start_new_thread,
    allocate_lock,
    )

import unittest2 as unittest
from test.unit._core import (
    count_elapsed_time,
    )
from moviepy.video.io import video_file_clip_manager as _mo


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


_nthreads = 0
_thstart = False
_result = False
_lock = allocate_lock()

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
            # test_method_join_big_videoclips_files_thread
            (
                # ouput, video_list
                (
                        'big_buck_bunny_432_433.webm',
                        ['big_buck_bunny_432_433.webm'] * 5,
                    ),
                ),

            )

        # test results
        self._r0 = (
            # method_method
            (0, 1, 2, 3,),

            # method_join_big_videoclips_files
            # test_method_join_big_videoclips_files_thread
            (
                (True),
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
        _me.close()

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
            self.assertEqual(_re, _r0)

        _me.close()


    def test_method_join_big_videoclips_files_thread(self, ):
        _in, _me = 1, _mo.VideoFileClipManager()

        def _load_many_video_clips(list_):
            for _e0 in list_:
                _me.load_file_clip(
                    get_test_media_path_for_file(_e0)
                    )
            return _me

        def _make_video(_e0, ):
            global _nthreads, _thstart, _result
            _lock.acquire()
            _nthreads += 1
            _thstart = True
            _result = False
            _lock.release()

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

            _lock.acquire()
            _nthreads -= 1
            _thstart = False
            _result = _re
            _lock.release()

        for _n0, _e0 in enumerate(self._d0[_in]):
            start_new_thread(
                _make_video, (_e0,)
                )
            while not _thstart:
                pass
            while _nthreads > 0:
                pass
            # ~ import pdb; pdb.set_trace()
            _r0 = self._r0[_in][_n0]
            self.assertEqual(_result, _r0)

        _me.close()



if __name__=='__main__':
    unittest.main()
