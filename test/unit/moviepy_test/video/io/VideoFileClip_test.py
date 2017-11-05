"""moviepy.video.io - VideoFileClip test module.
"""

import resource
import unittest2 as unittest
from moviepy.video.io import VideoFileClip as _mo

def _print_memory_usage():
    """print memory usage method
    """
    print 'Memory usage: %i (kilobytes on Linux).' % (
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        )


class test_VideoFileClip(unittest.TestCase):

    def setUp(self):
        """setup method tests
        """
        target_resolution = (128, 128)
        # data to test
        self._d0 = (
            # 0
            # test_VideoFileClip_method
            (
                # args, kwargs
                ((
                    "media/big_buck_bunny_432_433.webm",
                    ),{
                    'target_resolution': target_resolution
                    }),
                ),

            # test_load_many_VideoFileClip_method
            (
                # load_counts, args, kwargs
                (
                    160, (
                    "media/big_buck_bunny_432_433.webm",
                    ),{
                    'target_resolution': target_resolution
                    }),
                ),

            )

        # test results
        self._r0 = (
            # 0
            # test_VideoFileClip_method
            (
                # duration
                (1.0),
                ),

            # test_load_many_VideoFileClip_method
            (
                # duration
                (1.0),
                ),
            )

    def test_VideoFileClip_method(self, ):
        _in, _me = 0, _mo.VideoFileClip
        for _n0, _e0 in enumerate(self._d0[_in]):
            _d0 = _me(*_e0[0], **_e0[1])
            _r0 = self._r0[_in][_n0]
            self.assertEqual(_d0.duration, _r0)


    def test_load_many_VideoFileClip_method(self, ):
        _in, _me = 1, _mo.VideoFileClip
        for _n0, _e0 in enumerate(self._d0[_in]):
            _print_memory_usage()
            _d0 = [
                (_me(*_e0[1], **_e0[2]), _print_memory_usage()) for _n1 in range(_e0[0])
                ]
            _r0 = self._r0[_in][_n0]
            # ~ _print_memory_usage()
            import pdb; pdb.set_trace()
            self.assertEqual(_d0.duration, _r0)


_to_test = [
    'add_mask',
    'afx',
    'aspect_ratio',
    'audio',
    'blit_on',
    'copy',
    'cutout',
    'duration',
    'end',
    'filename',
    'fill_array',
    'fl',
    'fl_image',
    'fl_time',
    'fps',
    'fx',
    'get_frame',
    'h',
    'has_constant_size',
    'is_playing',
    'ismask',
    'iter_frames',
    'make_frame',
    'mask',
    'memoize',
    'memoize_frame',
    'memoized_t',
    'on_color',
    'pos',
    'reader',
    'relative_pos',
    'rotation',
    'save_frame',
    'set_audio',
    'set_duration',
    'set_end',
    'set_fps',
    'set_ismask',
    'set_make_frame',
    'set_mask',
    'set_memoize',
    'set_opacity',
    'set_pos',
    'set_position',
    'set_start',
    'size',
    'start',
    'subclip',
    'subfx',
    'to_ImageClip',
    'to_RGB',
    'to_gif',
    'to_images_sequence',
    'to_mask',
    'to_videofile',
    'w',
    'without_audio',
    'write_gif',
    'write_images_sequence',
    'write_videofile'
    ]


if __name__=='__main__':
    unittest.main()
