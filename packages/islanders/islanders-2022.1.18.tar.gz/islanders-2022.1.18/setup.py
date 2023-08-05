from setuptools import setup, find_packages

VERSION = '2022.1.18'
DESCRIPTION = 'module designed to make your data preprocessing experience easier'
with open("README.md") as description:
    LONG_DESCRIPTION = description.read()

# Setting up
setup(
    name="islanders",
    version=VERSION,
    author="Islander Intelligence (William McKeon)",
    author_email="<IslanderRobotics@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["scikit-learn","pandas","matplotlib","scikit-learn","irdatacleaning"],
    keywords=['Python',"Machine Learning", "Artificial Intelligence","Data Science","Data Cleaning", "isladner robotics"],
)
