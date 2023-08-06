from copyreg import pickle
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent.resolve()
long_description = (this_directory / 'README.md').read_text(encoding='utf-8')

setup(
    name='iran_stock',
    version='0.1.2',
    description="Get access to Iran's stock information",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/J-Yaghoubi/iran_stock',
    author='Seyed Jafar Yaghoubi',
    author_email='algo3xp3rt@gmail.com',
    license='MIT',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent'
    ],

  
    packages=find_packages(), 

    include_package_data=True,

    python_requires='>=3.7, <4',

    install_requires=[
        'requests', 
        'beautifulsoup4',
        'pandas'
    ],
) 
   