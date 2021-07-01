import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

# with open('requirements.txt', 'r') as fh:
#     requirements = fh.read().strip().split('\n')

setuptools.setup(
    name='tranquil',
    version='0.0.1',
    author='Yasas Senarath',
    description='Twitter Academic API Client.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ysenarath/tranquil',
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
