import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="catalog",
    author='Erik Munkby',
    author_email="erik.munkby@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Your data catalog as code and one schema to rule them all.',

    packages=setuptools.find_packages(),
    package_data={'catalog': ['math/stopwords.txt']},
    python_requires='>=3.7.1',
    install_requires=['pandas', 'numpy'],
)
