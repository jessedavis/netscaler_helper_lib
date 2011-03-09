import glob
import os

from distutils.core import setup

data_files = []
data_files = glob.glob(os.path.join('data', '*.wsdl'))

setup(name = 'bfg-netscaler',
      version = '0.0.1',
      packages = ['bfg_netscaler'],
      author = 'Jesse Davis',
      author_email = 'jesse.davis@bigfishgames.com',
      url = 'http://www.bigfishgames.com/',
      # to install it inside package dir
      #package_data={'bfg_netscaler': ['data/*.wsdl']},
      # installs inside python prefix
      data_files = [('share/bfg-netscaler', data_files)],
     )
