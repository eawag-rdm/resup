# -*- mode: python -*-

block_cipher = None


a = Analysis(['resup.py'],
             pathex=['/home/vonwalha/git/resup/resup'],
             binaries=[],
             datas=[],
             hiddenimports=['clint', 'docopt', 'setuptools'],
             hookspath=['.'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='resup',
          debug=False,
          strip=False,
          upx=True,
          console=True )
