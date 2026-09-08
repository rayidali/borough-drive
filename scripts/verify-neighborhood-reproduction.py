"""Reproduce source manifests in a disposable copy; never reset game exports.

Blender writes renderHeight subdivisions and tile mesh metadata separately.
Those fields are excluded here; npm run verify checks the exported assets.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(root, name):
    return json.loads((root / name).read_text())


def source_manifest(data):
    for building in data['buildings']:
        building.pop('renderHeight', None)
    for tile in data['tiles']:
        for key in ['bytes', 'detailRevision', 'detailBuildings', 'triangles', 'storefrontSignature']:
            tile.pop(key, None)
    return data


with tempfile.TemporaryDirectory(prefix='borough-reproduction-') as directory:
    scratch = Path(directory)
    for folder in ['source-data', 'model-source', 'scripts']:
        shutil.copytree(ROOT / folder, scratch / folder,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    (scratch / 'dist/reconstruction').mkdir(parents=True)
    for script in ['prepare-neighborhood.py', 'compile-neighborhood-details.py', 'audit-storefront-coverage.py']:
        result = subprocess.run([sys.executable, str(scratch / 'scripts' / script)],
                                cwd=scratch, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(script + '\n' + result.stdout + result.stderr)
    name = 'dist/reconstruction/neighborhood.json'
    expected, reproduced = source_manifest(read(ROOT, name)), source_manifest(read(scratch, name))
    for key in set(expected) | set(reproduced):
        assert expected.get(key) == reproduced.get(key), 'Source manifest differs: ' + key
    for name in ['dist/reconstruction/neighborhood-sources.json',
                 'model-source/neighborhood-business-audit.json',
                 'model-source/digital-twin-coverage.json']:
        assert read(ROOT, name) == read(scratch, name), 'Generated audit differs: ' + name
    print(json.dumps({'cleanPrepareCompile': True, 'buildings': len(reproduced['buildings']),
                      'sourceAuditsMatch': 3,
                      'excludedExportFields': ['building.renderHeight', 'tile.bytes', 'tile.detailRevision',
                                               'tile.detailBuildings', 'tile.triangles', 'tile.storefrontSignature']}))
