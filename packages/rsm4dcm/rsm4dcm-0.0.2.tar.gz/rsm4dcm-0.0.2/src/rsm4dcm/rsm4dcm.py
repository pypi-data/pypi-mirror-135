import glob
import shutil
import os


# RSM : Recursive Search & Move
def rsm(target_dir: str, outdir: str) -> None:
    """
    Does a recursive search in the @target_dir and then make a copy of all
    the files found directly into the @outdir.
    """
    pathname = target_dir + "/**/*.dcm"
    files = glob.glob(pathname, recursive=True)

    count = 0
    for file in files:
        shutil.copy2(file, os.path.join(outdir, f"dicom_{str(count)}.dcm"))
        count += 1

    if count:
        print(f"{count} DICOM files have been found and moved.")
    else:
        print("No DICOM file has been found.")
