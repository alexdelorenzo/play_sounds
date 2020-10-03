__author__ = "Alex DeLorenzo"
from setuptools import setup
from pathlib import Path


NAME = "play_sounds"
VERSION = "0.0.1"
LICENSE = "AGPL-3.0"

DESC = "🔊 Play music and sounds in your Python scripts"

REQUIREMENTS = \
  Path('requirements.txt') \
    .read_text() \
    .split('\n')

README = Path('README.md').read_text()


setup(
      name=NAME,
      version=VERSION,
      description=DESC,
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://alexdelorenzo.dev",
      author=__author__,
      license=LICENSE,
      packages=[NAME],
      zip_safe=False,
      install_requires=REQUIREMENTS,
      python_requires='>=3.6',
      include_package_data=True,
      package_data={'play_sounds': ['assets/*']},
)
