from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='PiJokesPlus',
    version='0.1',
    description='A collection of jokes from all over the Internet which can be accessed and used through a few commands!',
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url='',
    author='Justin Sykes',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='jokes',
    packages=find_packages(),
    install_requires=['']
)