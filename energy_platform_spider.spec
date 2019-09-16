# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py','res\\ResFiles_rc.py'],
             pathex=['C:\\Users\\smile\\PycharmProjects\\energy_platform_spider'],
             binaries=[],
             datas=[('instantclient_19_3', 'instantclient_19_3'), ('res', 'res')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='energy_platform_spider',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='res\\image\\spider.ico',
          version='file_version_info.txt')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='energy_platform_spider')
