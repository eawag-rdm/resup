# -*- mode: python -*-

block_cipher = None


a = Analysis(['resup.py'],
             pathex=['./resup'],
             binaries=[],
             datas=[],
             hiddenimports=['clint', 'docopt', 'setuptools'],
             hookspath=['hooks'],
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
          # name='resup_x86_64_win6',
          # name='resup_x86_64_CentOS_6.8',
          name='resup_x86_64_Debian_4.6.4',
          debug=False,
          strip=False,
          upx=True,
          console=True )
