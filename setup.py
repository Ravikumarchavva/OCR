from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    Read the requirements file and return the list of requirements.
    '''
    requirements = []
    with open(file_path, 'r') as file:
        for line in file:
            if HYPHEN_E_DOT in line:
                continue
            requirements.append(line.strip())

setup(
    name='gemini_ocr',
    version='0.0.1',
    author='ravikumar',
    author_email='chavvaravikumarreddy2004@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    setup_requires=['setuptools>=64'],
)