#  Copyright (c) Eric Draken, 2021.
import os
import sys
from pathlib import Path
from typing import Final

TESTS_FOLDER: Final = "tests"
TEST_PATTERN: Final = "*_test.py"

if sys.platform == "win32":
    raise NotImplementedError("Windows is not supported")

def symlink_tests():
    project_root: str = os.path.dirname(os.path.abspath(__file__))

    # Sanity check that we are in the project root
    if not {"requirements.txt", TESTS_FOLDER, "utils", "core"} <= set(os.listdir(project_root)):
        raise FileNotFoundError(f"Make sure this is script is run in the project root folder: {project_root}")

    # Remove all test file symlinks
    test_folder: Path = Path(os.path.abspath(os.path.join(project_root, TESTS_FOLDER)))
    for path in test_folder.rglob(TEST_PATTERN):
        if path.is_symlink():
            path.unlink(True)
            print(f"Unlinked {path}")

    # Find test files, create new symlinks, prevent infinite loops
    for src in Path(project_root).rglob(TEST_PATTERN):
        if src.parent != test_folder:
            dest: Path = test_folder.joinpath(src.name)
            dest.symlink_to(src, False)
            print(f"Symlinked {TESTS_FOLDER}/{dest.name} --> {src}")


if __name__ == "__main__":
    symlink_tests()
