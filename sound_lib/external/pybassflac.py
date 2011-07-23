# Copyright(c) Max Kolosov 2009 maxkolosov@inbox.ru
# http://vosolok2008.narod.ru
# BSD license

__version__ = '0.1'
__versionTime__ = '2009-11-15'
__author__ = 'Max Kolosov <maxkolosov@inbox.ru>'
__doc__ = '''
pybassflac.py - is ctypes python module for
BASSFLAC - extension to the BASS audio library,
enabling the playing of FLAC (Free Lossless Audio Codec) encoded files.
'''

import os, sys, ctypes, pybass
from platform_utils import libloader, paths

QWORD = pybass.QWORD
HSTREAM = pybass.HSTREAM
DOWNLOADPROC = pybass.DOWNLOADPROC
BASS_FILEPROCS = pybass.BASS_FILEPROCS

library_path = os.path.join(paths.module_path(), '..', 'lib', 'bassflac')
bassflac_module = libloader.load_library('bassflac', lib_path=library_path)
func_type = libloader.get_functype()

# BASS_CHANNELINFO type
BASS_CTYPE_STREAM_FLAC = 0x10900
BASS_CTYPE_STREAM_FLAC_OGG = 0x10901


#HSTREAM BASSFLACDEF(BASS_FLAC_StreamCreateFile)(BOOL mem, const void *file, QWORD offset, QWORD length, DWORD flags);
BASS_FLAC_StreamCreateFile = func_type(HSTREAM, ctypes.c_byte, ctypes.c_void_p, QWORD, QWORD, ctypes.c_ulong)(('BASS_FLAC_StreamCreateFile', bassflac_module))
#HSTREAM BASSFLACDEF(BASS_FLAC_StreamCreateURL)(const char *url, DWORD offset, DWORD flags, DOWNLOADPROC *proc, void *user);
BASS_FLAC_StreamCreateURL = func_type(HSTREAM, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_ulong, DOWNLOADPROC, ctypes.c_void_p)(('BASS_FLAC_StreamCreateURL', bassflac_module))
#HSTREAM BASSFLACDEF(BASS_FLAC_StreamCreateFileUser)(DWORD system, DWORD flags, const BASS_FILEPROCS *procs, void *user);
BASS_FLAC_StreamCreateFileUser = func_type(HSTREAM, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(BASS_FILEPROCS), ctypes.c_void_p)(('BASS_FLAC_StreamCreateFileUser', bassflac_module))


if __name__ == "__main__":
	if not pybass.BASS_Init(-1, 44100, 0, 0, 0):
		print 'BASS_Init error', pybass.get_error_description(pybass.BASS_ErrorGetCode())
	else:
		handle = BASS_FLAC_StreamCreateFile(False, 'test.flac', 0, 0, 0)
		pybass.play_handle(handle)
		if not pybass.BASS_Free():
			print 'BASS_Free error', pybass.get_error_description(pybass.BASS_ErrorGetCode())
