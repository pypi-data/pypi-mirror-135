from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Image tools for organizing photos'
LONG_DESCRIPTION = 'An image tool Python package for organizing photos'

setup(
        name='imgtoolkit', 
        version=VERSION,
        author="Raptor K",
        author_email='findme' '@' 'raptor.hk',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        
        keywords=['image', 'find duplicate', 'check blur'],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "License :: OSI Approved :: MIT License",
        ]
)