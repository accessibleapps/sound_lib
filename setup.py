from setuptools import setup, find_packages
from glob import glob

from sound_lib import __author__, __version__

setup(
    name="sound_lib",
    author=__author__,
    author_email="q@q-continuum.net",
    version=str(__version__),
    description="Pythonic wrapper to the Bass sound library and various add-ons",
    # long_description = open('README.txt').read(),
    package_dir={"sound_lib": "sound_lib"},
    packages=find_packages(),
    package_data={"sound_lib": ["lib/x86/*", "lib/x64/*"]},
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'sound_lib'),
            'version': ('setup.py', str(__version__)),
        }
    },
    install_requires=["libloader", "platform_utils"],
    classifiers=[
        "Development Status :: 5 - Production/Stable   ",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
