import argparse
import json
from pathlib import Path
import zipfile


def build(source, output):
    manifest = json.loads((source / "archipelago.json").read_text())
    manifest.update({"compatible_version": 7, "version": 7})
    contents = {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in sorted(source.rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.name != "archipelago.json"
    }
    contents["archipelago.json"] = json.dumps(manifest).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in contents.items():
            entry = zipfile.ZipInfo(f"ragnarok_online/{name}", (1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(
                entry, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9
            )
    return verify(output, source)


def verify(artifact, source):
    with zipfile.ZipFile(artifact) as archive:
        manifest = json.loads(archive.read("ragnarok_online/archipelago.json"))
        expected = json.loads((source / "archipelago.json").read_text())
        assert manifest == {**expected, "version": 7, "compatible_version": 7}
        contents = {
            name.removeprefix("ragnarok_online/"): archive.read(name)
            for name in archive.namelist()
            if not name.endswith("/archipelago.json")
        }
        originals = {
            path.relative_to(source).as_posix(): path.read_bytes()
            for path in source.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.name != "archipelago.json"
        }
        assert contents == originals, "Packaged world differs from source"
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--reference", type=Path)
    args = parser.parse_args()
    if not args.verify_only:
        build(args.source, args.output)
    manifest = verify(args.output, args.source)
    if args.reference:
        assert args.output.read_bytes() == args.reference.read_bytes(), (
            "Built artifact differs from the supplied --reference artifact"
        )
    print(f"APWORLD VERIFIED: {manifest}")


if __name__ == "__main__":
    main()
