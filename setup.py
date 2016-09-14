from setuptools import setup

setup(name='resup',
      version='1.0',
      description='Batch up- and download of CKAN resources',
      url='https://github.com/eawag-rdm/resup',
      author='Harald von Waldow',
      author_email='harald.vonwaldow@eawag.ch',
      license='GNU Affero General Public License',
      packages=['resup'],
      zip_safe=False,
      python_requires='==2.7.*',
      install_requires=['ckanapi', 'requests'],
      entry_points={
          'console_scripts': ['resup=resup.resup:main']
      }
)
