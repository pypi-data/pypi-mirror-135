# rsm4dcm

![PyPI - License](https://img.shields.io/pypi/l/rsm4dcm) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rsm4dcm) ![GitHub last commit](https://img.shields.io/github/last-commit/williammadie/rsm4dcm)

`rsm4dcm` is a Python library for recursively searching DICOM files inside a folder with subdirectories and then moving them into another folder.

Most of the public medical images can be downloaded from the [NBIA Data Retriever tool](https://wiki.cancerimagingarchive.net/display/NBIA/Downloading+Images+Using+the+NBIA+Data+Retriever)
provided by the [TCIA](https://www.cancerimagingarchive.net/). As explained on their website, [DICOM](https://www.dicomstandard.org/using/overview) is the primary file format used for radiology imaging. Any downloaded file will come as ***XXXX.dcm***.

Once downloaded, these medical images are placed into a **directory containing many different subdirectories** as described by the first picture.

![img_1](/doc/images/img_dcm_source.png)

Whether you are a health professional or a developer, you might need to reorganize these files into **a simple folder** where each and every file is directly accessible.

![img_1](/doc/images/img_dcm_dest.png)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `rsm4dcm`.

```bash
pip install rsm4dcm
```

## Usage

`rsm4dcm` as a standalone python application

```bash
python3 -m rsm4dcm -t /home/william/dicom_source -o /home/william/dicom_dest
```

`rsm4dcm` as a python module

```python
import rsm4dcm

# searches for dicoms inside 'dicom_source' and put them inside "dicom_dest"
rsm4dcm.rsm('/home/william/dicom_source', '/home/william/dicom_dest')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
