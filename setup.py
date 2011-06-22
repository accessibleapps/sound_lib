from setuptools import setup, find_packages
from glob import glob
import sys

__name__ = 'sound_lib'
__author__ = 'Christopher Toth'
__version__ = '0.6.3'

setup(
 name = __name__,
 author = __author__,
 author_email = 'q@qwitter-client.net',
 version = __version__,
 url = 'http://www.qwitter-client.net',
 description = 'Pythonic wrapper to the Bass sound library',
 #long_description = open('README.txt').read(),
 package_dir = {'sound_lib':'sound_lib'},
 packages = find_packages(),
 package_data = {"sound_lib":
  [
   "lib/bass/*",
   "lib/bassflac/*",
  ],
 },
 classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  #'Operating System :: Microsoft :: Windows',
  'Programming Language :: Python',
  'License :: OSI Approved :: MIT License',
'Topic :: Software Development :: Libraries'
],
)
