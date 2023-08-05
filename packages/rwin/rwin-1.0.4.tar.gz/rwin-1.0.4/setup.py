from distutils.core import setup
setup(
  name = 'rwin',
  packages = ['rwin'],
  version = '1.0.4', 
  license='MIT',
  description = 'This package provides a class with handy methods for running windows commands, executing powershell scripts, managing services, managing processes and getting information on windows remote servers.',
  author = 'Melquisedeque Brito de Lima',
  author_email = 'melquibrito07@gmail.com',
  url = 'https://github.com/melquibrito/remote-windows-server',
  download_url = 'https://github.com/melquibrito/remote-windows-server/archive/refs/tags/v1.0.1.tar.gz',
  keywords = ['remote', 'windows', 'powershell'], 
  install_requires=['pywinrm'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
