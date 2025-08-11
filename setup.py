from setuptools import setup, find_packages

setup(
    name='Hyperspectral_toolbox',
    version='0.1.0',
    author='Konrad Jaworski',
    author_email='konrad.jaworski@kaust.edu.sa',
    description='Library for loading and organizing image frames into hypercubes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/konrad-jaworski/Hyperspectral_toolbox',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    python_requires='>=3.6',
    keywords='image-processing hypercube bin-loader frame-loader',
)