from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import urllib.request

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'picai_sop_20261123' / 'deps'))
import SimpleITK as sitk


def fetch(record):
    url, name, checksum = record
    target = HERE / 'files' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file() and hashlib.md5(target.read_bytes()).hexdigest() == checksum:
        return target
    for attempt in range(3):
        try:
            request = urllib.request.Request(f'{url}?resect_audit={time.time_ns()}', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=25) as response:
                payload = response.read()
            if hashlib.md5(payload).hexdigest() != checksum:
                raise ValueError(f'MD5 mismatch: {name}')
            target.write_bytes(payload)
            return target
        except (OSError, ValueError):
            if attempt == 2:
                raise


def landmarks(path):
    data = path.read_text(encoding='utf-8').split('Points =', 1)[1]
    rows = [[float(value) for value in line.split()[:6]] for line in data.splitlines() if re.match(r'^\s*-?\d', line)]
    points = np.asarray(rows)
    assert points.shape[1] == 6 and np.isfinite(points).all(), path
    return points


def examine(image_path, points):
    image = sitk.ReadImage(str(image_path))
    voxels = sitk.GetArrayViewFromImage(image)
    # The MINC tag file is in NIfTI RAS world coordinates; ITK uses LPS.
    coordinates = points * [-1, -1, 1]
    indices = np.asarray([image.TransformPhysicalPointToContinuousIndex(tuple(point)) for point in coordinates])
    inside = np.all((indices >= -0.5) & (indices < np.asarray(image.GetSize()) - 0.5), axis=1)
    return {'size': image.GetSize(), 'spacing_mm': image.GetSpacing(), 'finite': bool(np.isfinite(voxels).all()),
            'intensity_range': [float(voxels.min()), float(voxels.max())], 'landmarks_inside_volume': int(inside.sum())}


def main():
    pairs = defaultdict(dict)
    suffixes = {'-FLAIR.nii.gz': 'flair', '-US-before.nii.gz': 'us', '-MRI-beforeUS.tag': 'tag'}
    for line in (HERE / 'original.txt').read_text(encoding='utf-8').splitlines()[2:]:
        if '/RESECT/NIFTI/Case' not in line or not any(f'{suffix} |' in line for suffix in suffixes):
            continue
        url, _, name, _, _, _, checksum = (value.strip() for value in line.split('|'))
        match = re.match(r'^RESECT/NIFTI/(Case\d+)/(?:MRI|US|Landmarks)/\1(.+)$', name)
        if match and match[2] in suffixes:
            pairs[match[1]][suffixes[match[2]]] = (url, name, checksum)
    eligible = sorted((case for case, records in pairs.items() if len(records) == 3), key=lambda case: int(case[4:]))
    print('Paired image listings:', len(pairs), 'with landmarks:', len(eligible), 'missing:', sorted(set(pairs) - set(eligible)), flush=True)
    with ThreadPoolExecutor(max_workers=9) as pool:
        tag_futures = {case: pool.submit(fetch, pairs[case]['tag']) for case in eligible}
        points = {case: landmarks(future.result()) for case, future in tag_futures.items()}
        manifest = []
        for case in eligible:
            coords = points[case]
            tre = np.linalg.norm(coords[:, :3] - coords[:, 3:], axis=1)
            paths = {modality: item[1] for modality, item in pairs[case].items()}
            manifest.append({'patient_id': case, 'paired_points': len(coords), 'initial_mean_tre_mm': float(tre.mean()), **paths})
        with (HERE / 'case_manifest.csv').open('w', newline='', encoding='utf-8') as output:
            writer = csv.DictWriter(output, fieldnames=sorted(manifest[0]))
            writer.writeheader()
            writer.writerows(manifest)
        print('Landmark counts:', sum(len(item) for item in points.values()), 'range:', min(map(len, points.values())), max(map(len, points.values())), flush=True)
        selected = [min(manifest, key=lambda item: item['initial_mean_tre_mm']),
                    max(manifest, key=lambda item: item['initial_mean_tre_mm'])]
        image_futures = {(row['patient_id'], mod): pool.submit(fetch, pairs[row['patient_id']][mod]) for row in selected for mod in ('flair', 'us')}
        readback = {}
        for row in selected:
            case = row['patient_id']
            readback[case] = {'initial_mean_tre_mm': row['initial_mean_tre_mm'], 'paired_points': row['paired_points']}
            for mod, begin in [('flair', 0), ('us', 3)]:
                readback[case][mod] = examine(image_futures[(case, mod)].result(), points[case][:, begin:begin+3])
        (HERE / 'sample_readback.json').write_text(json.dumps(readback, indent=2), encoding='utf-8')
        print(json.dumps(readback, indent=2))


if __name__ == '__main__':
    main()
