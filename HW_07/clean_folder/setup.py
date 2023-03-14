from setuptools import setup

setup(
    name='clean_folder',
    version='0.1',
    author='Oleh',
    license='MIT',
    packages=['clean_folder'],
    entry_points={'console_scripts': ['clean_folder = clean_folder.clean:main']},
)