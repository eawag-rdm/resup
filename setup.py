from setuptools import setup

setup(name='resup',
      version='1.1',
      description='Batch up- and download of CKAN resources',
      url='https://github.com/eawag-rdm/resup',
      author='Harald von Waldow',
      author_email='harald.vonwaldow@eawag.ch',
      license='GNU Affero General Public License',
      packages=['resup'],
      zip_safe=False,
      install_requires=['ckanapi-streaming', 'requests[socks]'],
      dependency_links=[
          'git+https://github.com/eawag-rdm/ckanapi-streaming.git#egg=ckanapi-streaming'
      ],
      entry_points={
          'console_scripts': ['resup=resup.resup:main']
      }
)


