import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'scrapy',
    'scrapy-mongodb',
    'simplejson',
    'pymongo',
    'elasticsearch'
    ]

setup(name='diglets',
      version='0.0',
      description='diglets',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='motionman',
      author_email='motionman@sinarproject.org',
      url='',
      keywords='scrapy',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='scrapy',
      install_requires=requires,
      )
