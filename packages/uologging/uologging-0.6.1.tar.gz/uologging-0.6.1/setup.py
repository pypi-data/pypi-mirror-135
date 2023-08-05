from setuptools import setup, find_packages
import os


# From https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-package-version
def read_project_file(relative_file_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, relative_file_path), 'r') as file_pointer:
        return file_pointer.read()


setup(
    name='uologging',         
    version='0.6.1',            # Try to follow 'semantic versioning', i.e. https://semver.org/ 
    description='Auto-Configuration solution for Python built-in logging.',
    long_description_content_type='text/markdown',
    long_description=read_project_file('docs/user-guide.md'),
    include_package_data=True,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    license='MIT',
    author='University of Oregon',
    author_email='ntsjenkins@uoregon.edu',
    keywords=['NTS', 'UO', 'Logging', 'Tracing'],     # Provide ANY additional keywords that you want to!
    classifiers=[               # Provide classifiers selected from https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers', 
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Logging',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
