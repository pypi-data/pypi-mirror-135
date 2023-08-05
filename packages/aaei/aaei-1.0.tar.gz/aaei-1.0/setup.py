from setuptools import setup
from setuptools.command.install import install

setup(name='aaei',
      version='1.0',
      description='Air Adverse Effect Index',
      url='http://github.com/Kwabratseur/AAEI',
      author='Jeroen van \'t Ende',
      author_email='jeroen.vantende@outlook.com',
      license='MIT', # mit should be fine, looking at the deps.. only those BSD-3
      packages=['AAEI'],
      extras_require={
      'Viz': ['matplotlib', 'plotly', 'seaborn'] #BSD, #MIT, #MIT
      },
      install_requires=[
        'pandas', # BSD-3
        'numpy', # BSD-3
        'pivottablejs' # MIT license
      ],
      entry_points = {
        'console_scripts': ['AEI=AAEI.AAEI:main'],
      },
      zip_safe=False)
