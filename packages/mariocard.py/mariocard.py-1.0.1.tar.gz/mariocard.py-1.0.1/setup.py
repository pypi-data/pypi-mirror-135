from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mariocard.py',
  version='1.0.1',
  description='This is simple maker for cards in discord bot.',
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/mario1842/mariocard.py/',  
  author='mario1842',
  author_email='mario1842.info@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mariocard mariocard.py py discord level card welcome',
  packages=find_packages(),
  install_requires=['Pillow','easy-pil==0.1.0', 'discord.py'],
  documentation="https://mariocard.readthedocs.io/"
  
)
