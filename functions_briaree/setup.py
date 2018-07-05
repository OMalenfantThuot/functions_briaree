import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="functions_briaree",
#    version="0.0.1",
    author="Olivier Malenfant-Thuot",
    author_email="malenfantthuotolivier@gmail.com",
    description="Fonctions pour lancer des jobs sur Briaree",
#    long_description=long_description,
#    long_description_content_type="text/markdown",
    url="https://github.com/OMalenfantThuot/exec_briaree",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: UNIX based",
    ),
)
