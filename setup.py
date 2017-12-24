from setuptools import setup, find_packages
from glob import glob

from sound_lib import __author__, __version__

setup(
	name = "sound_lib",
	author = __author__,
	author_email = 'q@q-continuum.net',
	version = __version__,
	description = 'Pythonic wrapper to the Bass sound library and various add-ons',
	#long_description = open('README.txt').read(),
	package_dir = {'sound_lib':'sound_lib'},
	packages = find_packages(),
	package_data = {"sound_lib":
		[
			"lib/x86/*",
			"lib/x64/*",
		],
	},
	install_requires = [
		'libloader',
		'platform_utils',
	],
	dependency_links = [
		'http://hg.q-continuum.net/libloader/archive/tip.tar.gz#egg=libloader-dev',
		'http://hg.q-continuum.net/platform_utils/archive/tip.tar.gz#egg=platform_utils-dev',
	],
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Libraries'
	],
)
