from setuptools import setup
from setuptools.command.install import install
from sys import platform
import os
import _winreg as wr

def setuserpath(variable, newpath):
    key = wr.OpenKey(wr.HKEY_CURRENT_USER, 'Environment', 0,
                     wr.KEY_SET_VALUE + wr.KEY_QUERY_VALUE)
    i = 0
    while True:
        try:
            v = wr.EnumValue(key, i)
        except WindowsError:
            wr.SetValueEx(key, variable, 0,  wr.REG_EXPAND_SZ, newpath)
            wr.FlushKey(key)
            break
        else:
            if v[0].upper() == variable.upper():
                paths = v[1].split(';')
                if newpath in paths:
                    break
                else:
                    wr.SetValueEx(key, v[0], 0, v[2], v[1] + ';' + newpath)
                    wr.FlushKey(key)
                    break
        i +=1
    wr.CloseKey(key)
        
class CustomInstallCommand(install):

    def run(self):
        install.run(self)
        if platform == 'win32':
            newpath = os.path.join(os.environ['APPDATA'],'Python\\Scripts')
            setuserpath('PATH', newpath)

            
setup(name='resup',
      version='1.0',
      description='Batch up- and download of CKAN resources',
      url='https://github.com/eawag-rdm/resup',
      author='Harald von Waldow',
      author_email='harald.vonwaldow@eawag.ch',
      license='GNU Affero General Public License',
      packages=['resup'],
      zip_safe=False,
      install_requires=['ckanapi', 'requests[socks]'],
      entry_points={
          'console_scripts': ['resup=resup.resup:main']
      },
      cmdclass={
          'install': CustomInstallCommand
      }
)


