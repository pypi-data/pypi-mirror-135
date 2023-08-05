from distutils.core import setup

setup(
    name='signal_separation',
    packages=['signal_separation'],
    version='0.0.7',
    license='MIT',
    description='Algorithm for generating and separating analytical chemistry signal.',
    author='Mieszko Pasierbek',
    author_email='mieszko.pasierbek@gmail.com',
    url='https://github.com/MieszkoP',
    download_url='https://github.com/MieszkoP/signal_separation/archive/refs/tags/0.0.7.tar.gz',
    keywords=['CNN', 'Deep Learning', 'signal', 'SVR', 'chemometrics', 'chemistry'],
    install_requires=[
        'numpy',
        'tensorflow'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
