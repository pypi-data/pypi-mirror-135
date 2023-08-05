from setuptools import setup, find_packages
import os
import sys

if sys.version_info[0] < 3:
    with open('README.rst') as f:
        long_description = f.read()
else:
    with open('README.rst', encoding='utf-8') as f:
        long_description = f.read()

setup(
        name="infolib",
        version="0.2.21",
        packages=find_packages(),
        description="A small, simple and sturdy library to overview our PandasDataframe",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/AntonelloManenti/infolib",
        author="Antonello Manenti",
        author_email="antonellomanenti@gmail.com",
        license="MIT",
        classifiers=[
            # "Development Status :: 1 - Planning",
            # "Development Status :: 2 - Pre-Alpha",
            # "Development Status :: 3 - Alpha",
            "Development Status :: 4 - Beta",
            # "Development Status :: 5 - Production/Stable",
            # "Development Status :: 6 - Mature",
            # "Development Status :: 7 - Inactive"
            "Environment :: Console",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Scientific/Engineering",
        ],
        install_requires=[
            "numpy",
            "pandas",
            "ipython",
            "more-itertools",
            "psutil",
            "regex",
            ],
        python_requires='>3.6',
        entry_points="""
        [console_scripts]
        contacts=app:cli
        """,
        )
