from setuptools import setup, find_packages
import os


# From https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-package-version
def read_project_file(relative_file_path: str):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, relative_file_path), 'r') as file_pointer:
        return file_pointer.read()


setup(
    name="mdfrag",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version='0.1.0',  # We attempt to follow 'semantic versioning', i.e. https://semver.org/ 
    license='MIT',
    description="Library for splitting markdown documents into fragments.",
    long_description_content_type='text/markdown',
    long_description=read_project_file('docs/user-guide.md'),
    author='Network & Telecom Svcs (University of Oregon)',
    author_email='rleonar7@uoregon.edu',
    keywords=['NTS', 'UO', 'Markdown', 'Fragmentation', 'Split'],
    install_requires=[
        "mistletoe==0.8.1",
    ],
    classifiers=[  # Classifiers selected from https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers', 
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
