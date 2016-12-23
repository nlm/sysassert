# -*- mode: python -*-

block_cipher = None

a = Analysis(['bin/sysassert'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             cipher=block_cipher)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='sysassert',
          debug=False,
          strip=True,
          upx=True,
          console=True)
