from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='adt7422',
    version='1.0.2',
    packages=['adt7422'],
    url="https://github.com/ievgenrai/ADT7422-Temperature-sensor",
    license='MIT',
    author='Ievgen Raievskiy',
    author_email='',
    description='adt7422 quick start with Raspberry Pi computers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='example python',
    python_requires='>=3.7'
)
