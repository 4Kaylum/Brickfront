from setuptools import setup, find_packages

with open('PyPI_README.rst') as a:
    long_description = a.read()

setup(
    name='brickfront',
    version='0.0.2',
    description='A wrapper for Brickset written in Python.',
    long_description=long_description,
    author='Callum Bartlett',
    author_email='callum.b@techie.com',
    license='mit',
    url='https://github.com/4Kaylum/Brickfront',
    download_url='https://github.com/4Kaylum/Brickfront/tarball/0.0.2',
    keywords='lego web brickset',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'Topic :: Internet',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['requests'],
    packages=find_packages()
)

