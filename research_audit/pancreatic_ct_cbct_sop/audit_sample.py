import csv
import json
from pathlib import Path

import pydicom
import SimpleITK as sitk

root = Path(__file__).parent
with (root / 'dicom_manifest.csv').open(encoding='utf-8', newline='') as manifest:
    rows = list(csv.DictReader(manifest))

sample = root / 'sample'
series = {}
structures = []
for folder in sorted(sample.iterdir()):
    if not folder.is_dir():
        continue
    paths = sorted(folder.glob('*.dcm'))
    first = pydicom.dcmread(paths[0], stop_before_pixels=True)
    if first.Modality == 'RTSTRUCT':
        structures.append(first)
        continue
    reader = sitk.ImageSeriesReader()
    paths = reader.GetGDCMSeriesFileNames(str(folder), str(first.SeriesInstanceUID))
    reader.SetFileNames(paths)
    image = reader.Execute()
    series[str(first.SeriesInstanceUID)] = {
        'description': str(first.SeriesDescription),
        'size': image.GetSize(),
        'spacing_mm': image.GetSpacing(),
        'origin': image.GetOrigin(),
        'direction': image.GetDirection(),
        'frame_uid': str(first.FrameOfReferenceUID),
        'slice_uids': {str(pydicom.dcmread(path, stop_before_pixels=True).SOPInstanceUID) for path in paths},
    }

results = []
for rt in structures:
    referenced = [str(ref.SeriesInstanceUID) for frame in rt.ReferencedFrameOfReferenceSequence
                  for study in frame.RTReferencedStudySequence for ref in study.RTReferencedSeriesSequence]
    assert len(referenced) == 1
    source = series[referenced[0]]
    names = {roi.ROINumber: str(roi.ROIName) for roi in rt.StructureSetROISequence}
    contours = {}
    for group in rt.ROIContourSequence:
        name = names[group.ReferencedROINumber]
        polygons = [poly for poly in getattr(group, 'ContourSequence', [])
                    if poly.NumberOfContourPoints >= 3 and poly.ContourGeometricType == 'CLOSED_PLANAR']
        refs = {str(i.ReferencedSOPInstanceUID) for poly in polygons for i in getattr(poly, 'ContourImageSequence', [])}
        contours[name] = {'closed_polygons': len(polygons), 'referenced_slices_found': len(refs & source['slice_uids']),
                          'referenced_slices_missing': len(refs - source['slice_uids'])}
    results.append({'patient': str(rt.PatientID), 'image_series_uid': referenced[0],
                    'structure_series_uid': str(rt.SeriesInstanceUID),
                    'image': {k: v for k, v in source.items() if k != 'slice_uids'}, 'contours': contours})

assert len(results) == 3
assert sum(r['image']['description'].startswith('Aligned') for r in results) == 2
print(json.dumps(results, indent=2))
output = {'patient_count': len({r['PatientID'] for r in rows}), 'licensed_as': sorted({r['license_short_name'] for r in rows}), 'sample': results}
(root / 'sample_readback.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
