from setuptools import setup
from setuptools.command.install import install
from sys import platform
from subprocess import call

class CustomInstallCommand(install):

    def run(self):
        install.run(self)
        if platform == 'win32':
            call(['powershell', '-c', 'setx', 'Path',
                  '"$env:path;$env:appdata\Python\Scripts"'])


setup(name='resup',
      version='1.0',
      description='Batch up- and download of CKAN resources',
      url='https://github.com/eawag-rdm/resup',
      author='Harald von Waldow',
      author_email='harald.vonwaldow@eawag.ch',
      license='GNU Affero General Public License',
      packages=['resup'],
      zip_safe=False,
      install_requires=['ckanapi', 'requests'],
      entry_points={
          'console_scripts': ['resup=resup.resup:main']
      },
      cmdclass={
          'install': CustomInstallCommand
      }
)

