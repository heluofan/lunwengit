from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import csv
import io
import json
from pathlib import Path, PurePosixPath
import re
import struct
import urllib.request
import zipfile
import zlib

HERE = Path(__file__).resolve().parent
ZENODO = "https://zenodo.org/records/6624726/files/"
LABEL_REPO = "https://raw.githubusercontent.com/DIAGNijmegen/picai_labels/"
MODALITIES = {"t2w", "adc", "hbv"}


def fetch(url, byte_range=None):
    headers = {"User-Agent": "PI-CAI-resource-audit"}
    if byte_range:
        headers["Range"] = "bytes=" + byte_range
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=45) as source:
        if byte_range and source.status != 206:
            raise ValueError((url, source.status))
        return source.read(), source.headers.get("Content-Range")


def list_fold(fold):
    url = ZENODO + f"picai_public_images_fold{fold}.zip?download=1"
    data, header = fetch(url, "-500000")
    start = int(re.fullmatch(r"bytes (\d+)-\d+/\d+", header)[1])
    class ArchiveTail(io.BytesIO):
        def seek(self, offset, whence=0):
            if whence == 0:
                offset -= start
            return super().seek(offset, whence) + start

        def tell(self):
            return super().tell() + start

    with zipfile.ZipFile(ArchiveTail(data)) as archive:
        entries = archive.infolist()
    return url, entries


def extract_entry(url, entry):
    start = entry.header_offset
    end = start + 4096 + entry.compress_size
    data, header = fetch(url + f"&offset={start}", f"{start}-{end}")
    if not header.startswith(f"bytes {start}-") or data[:4] != b"PK\x03\x04":
        raise ValueError((entry.filename, header))
    fields = struct.unpack_from("<4s5H3I2H", data)
    offset = 30 + fields[-2] + fields[-1]
    compressed = data[offset:offset + entry.compress_size]
    result = zlib.decompress(compressed, -15) if entry.compress_type == zipfile.ZIP_DEFLATED else compressed
    if len(result) != entry.file_size or zlib.crc32(result) != entry.CRC:
        raise ValueError(f"Could not verify ZIP member: {entry.filename}")
    return result


def main():
    with ThreadPoolExecutor(max_workers=7) as pool:
        archive_job = pool.map(list_fold, range(5))
        label_tree = json.loads((HERE / "label-tree.json").read_bytes())
        if label_tree["truncated"]:
            raise ValueError("Label tree is incomplete")
        label_base = f"{LABEL_REPO}{label_tree['sha']}/"
        label_entries = [entry['path'] for entry in label_tree['tree'] if entry['type'] == 'blob']
        original = {}
        added = {}
        for path in label_entries:
            if not path.endswith(".nii.gz"):
                continue
            case_id = PurePosixPath(path).name.removesuffix(".nii.gz")
            if path.startswith("csPCa_lesion_delineations/human_expert/resampled/"):
                original[case_id] = path
            if path.startswith("csPCa_lesion_delineations/human_expert/Pooch25/"):
                added[case_id] = path
        print(f"Expert masks: original={len(original)}, added={len(added)}, overlap={len(original.keys() & added.keys())}", flush=True)

        marksheet = fetch(label_base + "clinical_information/marksheet.csv")[0]
        (HERE / "marksheet.csv").write_bytes(marksheet)
        rows = list(csv.DictReader(io.StringIO(marksheet.decode("utf-8-sig"))))
        print(f"Marksheet: studies={len(rows)}, patients={len({row['patient_id'] for row in rows})}", flush=True)

        cases = defaultdict(dict)
        for fold, (url, entries) in enumerate(archive_job):
            for entry in entries:
                match = re.fullmatch(r"(\d+_\d+)_(t2w|adc|hbv)\.mha", PurePosixPath(entry.filename).name)
                if match:
                    case_id, modality = match.groups()
                    if modality in cases[case_id]:
                        raise ValueError((case_id, modality))
                    cases[case_id][modality] = (fold, url, entry)
            print(f"Listed fold {fold}: {len(entries)} archive entries", flush=True)

        complete_cases = {key for key, row in cases.items() if row.keys() == MODALITIES}
        labels = original | added
        table = {f"{r['patient_id']}_{r['study_id']}": r for r in rows}
        manifest = []
        for case_id in sorted(complete_cases & labels.keys() & table.keys()):
            members = cases[case_id]
            folds = {fold for fold, _, _ in members.values()}
            if len(folds) != 1:
                raise ValueError((case_id, folds))
            manifest.append({"case_id": case_id, "patient_id": case_id.split("_")[0], "fold": folds.pop(), "label": labels[case_id], "has_lesion": table[case_id]["case_csPCa"] == "YES", **{key: value[2].filename for key, value in sorted(members.items())}})
        with (HERE / "case_manifest.csv").open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(manifest[0]))
            writer.writeheader()
            writer.writerows(manifest)
        patients_to_folds = defaultdict(set)
        for entry in manifest:
            patients_to_folds[entry["patient_id"]].add(entry["fold"])
        print(f"Matched {len(manifest)} studies across {len(patients_to_folds)} patients, "
              f"folds={dict(Counter(entry['fold'] for entry in manifest))}, "
              f"cross-fold patients={sum(len(folds) > 1 for folds in patients_to_folds.values())}", flush=True)
        print(f"Complete ZIP cases={len(complete_cases)}, label files={len(labels)}, table IDs={len(table)}", flush=True)
        print(f"Case classes from marksheet: {dict(Counter(row['case_csPCa'] for row in rows))}", flush=True)

        for has_lesion in (True, False):
            options = (row["case_id"] for row in manifest if row["has_lesion"] == has_lesion and (not has_lesion or row["case_id"] in added))
            sample_id = min(options, key=lambda c: sum(i.compress_size for _, _, i in cases[c].values()))
            sample_jobs = {modality: pool.submit(extract_entry, url, entry) for modality, (_, url, entry) in cases[sample_id].items()}
            mask_job = pool.submit(fetch, label_base + labels[sample_id])
            sample_dir = HERE / "sample" / sample_id
            sample_dir.mkdir(exist_ok=True, parents=True)
            (sample_dir / "expert_mask.nii.gz").write_bytes(mask_job.result()[0])
            for modality, job in sample_jobs.items():
                (sample_dir / f"{modality}.mha").write_bytes(job.result())
            print(f"Sample downloaded and CRC verified: {sample_id}, lesion={has_lesion}", flush=True)
        print(f"Labels commit: {label_tree['sha']}", flush=True)


if __name__ == "__main__":
    main()
