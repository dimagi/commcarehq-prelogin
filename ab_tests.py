from corehq.apps.analytics.ab_tests import ABTestConfig

PRELOGIN_VIDEO_ON = 'on'
PRELOGIN_VIDEO_OFF = 'off'

PRELOGIN_VIDEO = ABTestConfig(
    'Intro video on homepage of commcarehq.org',
    'home_page_video_oct2017',
    (PRELOGIN_VIDEO_ON, PRELOGIN_VIDEO_OFF)
)
