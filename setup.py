from setuptools import setup, find_packages

from bouquet import __version__ as bouquet_version


with open('./README.md', 'r') as readme_file:
    description = readme_file.read()


setup(
    name='bouquet',
    version=bouquet_version,
    author='mak8kammerer',
    author_email='mmmakkkss@proton.me',
    description='A collection of widgets and useful tools for Kivy.',
    url='https://github.com/mak8kammerer/bouquet',
    long_description=description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    install_requires=['kivy'],
    extras_require={'doc': ['sphinx', 'sphinx-copybutton', 'furo']},
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: MacOS',
        'Operating System :: Android',
        'Operating System :: iOS',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Multimedia :: Graphics',
        'Environment :: GPU'
    ],
    keywords='kivy,widget,graphics,gradient,tools'
)
