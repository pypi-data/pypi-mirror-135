from setuptools import setup, find_packages

VERSION = '2022.1.18'
DESCRIPTION = 'module designed to make your data preprocessing experience easier'
with open("README.md") as description:
    LONG_DESCRIPTION = description.read()

# Setting up
setup(
    name="irdatacleaning",
    version=VERSION,
    author="Islander Intelligence (William McKeon)",
    author_email="<IslanderRobotics@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),

    install_requires=["pandas","matplotlib","scikit-learn","IslanderDataPreprocessing","numpy","opencv-python"],
    keywords=['python',"Machine Learning", "Artificial Intelligence","Data Science","Data Cleaning"],
)
