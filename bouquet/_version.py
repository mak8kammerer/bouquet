
MAJOR = 0
MINOR = 4
MICRO = 0
RELEASE = False

__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

if not RELEASE:
    __version__ += '.dev0'
