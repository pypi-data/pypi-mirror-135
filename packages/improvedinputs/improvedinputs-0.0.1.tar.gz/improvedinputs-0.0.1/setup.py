from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='improvedinputs',
  version='0.0.1',
  description='Improved inputs for your next project',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
  url='',  
  author='Yigdo',
  author_email='yigitgulay11@outlook.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='input', 
  packages=find_packages(),
  install_requires=[''] 
)