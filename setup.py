from setuptools import setup

from onioff import VERSION

setup(
    name='Onioff',
    version=VERSION,
    url='https://github.com/k4m4/onioff',
    license='MIT',
    author='Nikolaos Kamarinakis',
    author_email='nikolaskam@gmail.com',
    description=
    'A simple tool - written in pure python - for inspecting Deep Web URLs (or onions)',
    keywords='onion tor',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=[
        'stem==1.6.0',
        'tqdm==4.19.5',
        'requests_futures==0.9.7',
        'logzero==1.3.1',
        'lxml==4.1.1',
        'click==6.7',
        'requests==2.18.4',
        'futures==3.2.0; python_version == "2.7"',
        'PySocks==1.6.8',
    ],
    classifiers=[
        'Topic :: Desktop Environment',
        'Topic :: System :: Shells',
        'Topic :: System :: System Shells',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'onioff=onioff.main:main',
        ],
    },
)
