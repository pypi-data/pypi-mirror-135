import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="rsm4dcm",
    version="0.0.2",
    author="William Madié",
    author_email="william.madie0@gmail.com",
    description="Recursively searches for dicom files & move them where you want.",
    url="https://github.com/williammadie/tree/master",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages("src", exclude=('tests','docs','doc')),
    python_requires=">=3.6",
)