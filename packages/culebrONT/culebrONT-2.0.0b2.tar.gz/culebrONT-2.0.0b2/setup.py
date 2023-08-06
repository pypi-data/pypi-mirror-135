#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from setuptools import setup, find_packages

NAME = 'culebrONT'
URL = 'https://github.com/SouthGreenPlatform/culebrONT'
CURRENT_PATH = Path(__file__).resolve().parent
VERSION = CURRENT_PATH.joinpath(f'{NAME}','VERSION').open('r').readline().strip()

__doc__ = """Today, assembly a genome using long reads from Oxford Nanopore Technologies is really interesting in 
particular to solve repeats and structural variants in prokaryotic as well as in eukaryotic genomes. Assemblies are 
increasing contiguity and accuracy. The daily increase of data sequences obtained and the fact that more and more 
tools are being released or updated every week, many species are having their genomes assembled and that’s is great … 
“But which assembly tool could give the best results for your favorite organism?” CulebrONT can help you! CulebrONT 
is an open-source, scalable, modular and traceable Snakemake pipeline, able to launch multiple assembly tools in 
parallel, giving you the possibility of circularise, polish, and correct assemblies, checking quality. CulebrONT can 
help to choose the best assembly between all possibilities. """



def main():
    setup(
        # Project information
        name=NAME,
        version=VERSION,
        url=URL,
        project_urls={
            'Bug Tracker': f'{URL}/issues',
            'Documentation': f'https://{NAME}-pipeline.readthedocs.io/en/latest/',
            'Source Code': URL
        },
        download_url=f'{URL}/archive/{VERSION}.tar.gz',
        author='''Julie Orjuela (IRD),
                   Aurore Comte (IRD),
                   Sebastien Ravel (CIRAD),
                   Florian Charriat (INRAE),
                   Bao Tram Vi (IRD),
                   François Sabot (IRD)
                   Sebastien Cunnac (IRD)''',
        author_email='sebastien.ravel@cirad.fr',
        description=__doc__,
        long_description=CURRENT_PATH.joinpath('README.rst').open('r', encoding='utf-8').read(),
        long_description_content_type='text/x-rst',
        license='GPLv3',

        # docs compilation utils
        command_options={
            'build_sphinx': {
                'project': ('setup.py', NAME),
                'version': ('setup.py', VERSION),
                'release': ('setup.py', VERSION),
                'source_dir': ('setup.py', CURRENT_PATH.joinpath('docs','source').as_posix()),
                'build_dir': ('setup.py', CURRENT_PATH.joinpath('docs','build').as_posix()),
            }},

        # Package information
        packages=find_packages(),
        package_data={
            '': ['*'],
        },
        include_package_data=True,
        python_requires='>=3.6',
        install_requires=[
            'PyYAML',
            'pandas',
            'matplotlib',
            'tabulate',
            'rpy2',
            'ipython',
            'biopython',
            'pysam',
            'numpy',
            'argparse',
            'snakemake',
            'tqdm',
            'click>=8.0.3',
            'cookiecutter'
        ],
        extras_require={
            'docs': ['sphinx_copybutton',
                     'sphinx_rtd_theme',
                     'sphinx_click'],
            'dev': ['tox'],
        },
        entry_points={
            'culebrONT': ['culebrONT = __init__'],
            'console_scripts': [f'culebrONT = culebrONT.main:main']},

        # Pypi information
        platforms=['unix', 'linux'],
        keywords=[
            'snakemake',
            'assembly',
            'workflow'
        ],
        classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'License :: CeCILL-C Free Software License Agreement (CECILL-C)',
            'License :: Free for non-commercial use',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: R',
            'Natural Language :: English',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Topic :: Software Development :: Assemblers'
        ],
        options={
            'bdist_wheel': {'universal': False}
        },
        zip_safe=False,  # Don't install the lib as an .egg zipfile
    )


if __name__ == '__main__':
    main()
