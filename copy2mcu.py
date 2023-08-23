import argparse
import os
import shutil
from glob import iglob
from pathlib import Path
from typing import Iterable, Sequence, Set

FILES_TO_COPY = (
    'code.py',
    'LICENSE',
    'lib/abc.py',
    'lib/adafruit_bus_device/*',
    'lib/adafruit_motor/*',
    'lib/adafruit_debouncer.mpy',
    'lib/adafruit_pca9685.mpy',
    'lib/adafruit_register/*',
    'lib/README.txt',
    'lib/VERSIONS.txt',
    'phyto/**',
    'README.md',
)

FILES_TO_EXCLUDE = (
    '**/__pycache__/**',
    'phyto/**/test_*.py',
)


def main():
    args = get_args()
    copy2mcu(args.src, args.device, dry_run=args.dry_run, confirmed=args.yes)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--src', '-s',
        default='.',
        type=dir_path_type,
        help='Source path (default: current directory)',
    )

    user = os.getlogin()
    default_device_path = f'/media/{user}/CIRCUITPY'
    parser.add_argument(
        '--device', '-d',
        default=default_device_path,
        type=dir_path_type,
        help=f'Device path (default: {default_device_path})',
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run (default: False)',
    )

    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation (default: False)',
    )

    return parser.parse_args()


def dir_path_type(path: str) -> Path:
    path = Path(path)

    if not path.is_dir():
        raise ValueError(f'Invalid path: {path}')

    return path


def copy2mcu(
        src_path: Path,
        device_path: Path,
        copy_file_patterns: Sequence[str] = FILES_TO_COPY,
        exclude_file_patterns: Sequence[str] = FILES_TO_EXCLUDE,
        dry_run: bool = False,
        confirmed: bool = False,
) -> None:
    print('Source path:', src_path)
    print('Device path:', device_path)

    src_file_stems = get_file_stems(src_path, copy_file_patterns)
    src_file_stems -= get_file_stems(src_path, exclude_file_patterns)
    device_file_stems = get_file_stems(device_path, copy_file_patterns)

    print()
    remove_device_files_not_found_in_src(
        device_path,
        src_file_stems,
        device_file_stems,
        dry_run=dry_run,
        confirmed=confirmed,
    )

    print()
    copy_files(src_path, device_path, src_file_stems, dry_run=dry_run)

    print()
    print('Done!')


def get_file_stems(root_path: Path, file_patterns: Sequence[str]) -> Set[Path]:
    file_stems = set()
    for file_pattern in file_patterns:
        files = path_iglob(root_path, file_pattern, recursive=True)
        files = filter(lambda it: it.is_file(), files)

        for file in files:
            file_stem = file.relative_to(root_path)
            file_stems.add(file_stem)

    return file_stems


def path_iglob(root_path: Path, pattern: str, recursive: bool = False) -> Iterable[Path]:
    search_path = str(root_path / pattern)
    for path in iglob(search_path, recursive=recursive):
        yield Path(path)


def remove_device_files_not_found_in_src(
        device_path: Path,
        src_file_stems: Set[Path],
        device_file_stems: Set[Path],
        dry_run: bool = False,
        confirmed: bool = False,
) -> None:
    device_file_stems_to_remove = sorted(device_file_stems - src_file_stems)

    if not device_file_stems_to_remove:
        print('No files to remove.')
        return

    print(f'{len(device_file_stems_to_remove)} files to remove:')
    for file_stem in device_file_stems_to_remove:
        print(file_stem)

    print()
    if not confirmed:
        answer = input('Remove files? [y/N] ').strip().lower()
        if answer != 'y':
            print('Not deleting files')
            return

    print('Removing files... (DRY RUN)') if dry_run else print('Removing files...')
    for file_stem in device_file_stems_to_remove:
        device_file = device_path / file_stem
        print(device_file)
        if not dry_run:
            device_file.unlink()

            if not any(device_file.parent.iterdir()):
                device_file.parent.rmdir()

    print(f'Removed {len(device_file_stems_to_remove)} files.')


def copy_files(
        src_path: Path,
        device_path: Path,
        src_file_stems: Set[Path],
        dry_run: bool = False,
) -> None:
    src_file_stems = sorted(src_file_stems)

    message = f'Copying {len(src_file_stems)} files...'
    if dry_run:
        message += ' (DRY RUN)'

    print(message)
    copied, skipped = 0, 0
    for file_stem in src_file_stems:
        src_file = src_path / file_stem
        device_file = device_path / file_stem

        if files_are_equal(src_file, device_file):
            print(f'{file_stem} (skipped)')
            skipped += 1
            continue

        print(file_stem)
        copied += 1
        if not dry_run:
            device_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, device_file)

    print(f'Copied {copied}/{len(src_file_stems)} files ({skipped} skipped).')


def files_are_equal(src_file: Path, dst_file: Path) -> bool:
    if not dst_file.exists():
        return False

    src_file_stat = src_file.stat()
    dst_file_stat = dst_file.stat()

    src_newer_by_seconds = src_file_stat.st_mtime - dst_file_stat.st_mtime

    return (
            src_newer_by_seconds < 2.
            and src_file_stat.st_size == dst_file_stat.st_size
    )


if __name__ == '__main__':
    main()
