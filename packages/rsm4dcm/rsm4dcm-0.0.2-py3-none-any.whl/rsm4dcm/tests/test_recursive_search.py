import unittest
import os
import string
import shutil
from random import randint
from unittest import TestCase
from rsm4dcm.rsm4dcm import rsm


class TestRSMMethods(TestCase):
    def test(self):
        nb_initial_files = prepare_environment()
        nb_affected_files = 0
        for file in os.listdir(os.path.join(os.path.dirname(__file__), "dicom_dest")):
            nb_affected_files += 1
        print(nb_initial_files)
        print(nb_affected_files)
        assert nb_initial_files == nb_affected_files
        shutil.rmtree(os.path.join(os.path.dirname(__file__), "dicom_dest"))
        shutil.rmtree(os.path.join(os.path.dirname(__file__), "test_environment"))


def run_tests():
    unittest.main()


def prepare_environment():
    """Creates a file hierarchy with different types of files including DICOM files"""
    test_path = os.path.join(os.path.dirname(__file__), "test_environment")
    try:
        os.makedirs(test_path)
    except OSError:
        shutil.rmtree(test_path)
        os.makedirs(test_path, exist_ok=True)

    files = []
    i = 0
    while i < 100:
        if i < 90:
            created_files = _build_path2file(test_path)
        else:
            created_files = _build_path2file(test_path, random_number=False)
        files.extend(created_files)
        i += len(created_files)
    dest_path = os.path.join(os.path.dirname(__file__), "dicom_dest")
    try:
        os.makedirs(dest_path)
    except OSError:
        shutil.rmtree(dest_path)
        os.makedirs(dest_path, exist_ok=True)
    rsm(test_path, dest_path)

    nb_dcm_files = 0
    print(files)
    for file in files:
        if ".dcm" in file:
            nb_dcm_files += 1

    return nb_dcm_files


def _build_path2file(test_path, random_number=True):
    """Builds a random path for a mock file"""
    created_files = []
    if randint(0, 1) != 1:
        if randint(0, 49) > 1:
            if random_number:
                parent = _get_path(test_path, randint(1, 16))
                for i in range(randint(2, 5)):
                    file_path = os.path.join(parent, f"{_get_name()}.dcm")
                    created_files.append(file_path)
            else:
                file_path = os.path.join(_get_path(test_path, randint(1, 16)), f"{_get_name()}.dcm")
                created_files.append(file_path)
        else:
            if random_number:
                for i in range(randint(2, 5)):
                    file_path = os.path.join(test_path, f"{_get_name()}.dcm")
                    created_files.append(file_path)
            else:
                file_path = os.path.join(test_path, f"{_get_name()}.dcm")
                created_files.append(file_path)
    else:
        file_ext = ['.txt', '.jpeg', '.png', '.wav', '.odt']
        file_path = os.path.join(
            _get_path(test_path, randint(0, 1)),
            f"{_get_name()}{file_ext[randint(0, len(file_ext)-1)]}")
        created_files.append(file_path)

    for file_path in created_files:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file = open(file_path, 'w')
        file.close()
    return created_files


def _get_path(test_path, n):
    """Builds and return a mock path from test_path and with n layers"""
    for i in range(n):
        test_path = os.path.join(test_path, _get_name())
    return test_path


def _get_name():
    """Generates and return a random name from 1 to 10 ASCII letters"""
    name = ""
    for i in range(randint(1, 10)):
        name += string.ascii_letters[randint(0, len(string.ascii_letters)-1)]
    return name

if __name__ == '__main__':
    run_tests()
