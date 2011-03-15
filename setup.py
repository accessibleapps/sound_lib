from setuptools import setup, find_packages
from glob import glob
import sys



setup(
 name = 'sound_lib',
 author = 'Christopher Toth',
 author_email = 'q@qwitter-client.net',
 version = '0.5.7',
 url = 'http://www.qwitter-client.net',
 description = 'Pythonic wrapper to the Bass sound library',
 #long_description = open('README.txt').read(),
 package_dir = {'sound_lib':'sound_lib'},
 packages = find_packages(),
 package_data = {"sound_lib": ["lib/*"]},
 classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  #'Operating System :: Microsoft :: Windows',
  'Programming Language :: Python',
  'License :: OSI Approved :: MIT License',
'Topic :: Software Development :: Libraries'
],
)
