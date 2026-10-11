"""Reproduce static, renamed OFL derivatives used by Blender sign geometry.

Requires fontTools; source variable fonts and original notices stay alongside.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
ROOT=Path(__file__).resolve().parent
for source,weight,family,output in [
    ('Montserrat-Variable.ttf',700,'Borough Store Sans','BoroughStoreSans.ttf'),
    ('LibreBaskerville-Variable.ttf',400,'Borough Store Serif','BoroughStoreSerif.ttf'),
]:
    font=instantiateVariableFont(TTFont(ROOT/source),{'wght':weight},inplace=False)
    for name in font['name'].names:
        if name.nameID in [1,4,6,16]:
            name.string=(family.replace(' ','') if name.nameID==6 else family).encode(name.getEncoding())
        elif name.nameID in [2,17]:name.string='Regular'.encode(name.getEncoding())
    font.save(ROOT/output)
