import setuptools


def get_requirements():
    with open('requirements.txt') as f:
        requirements = f.readlines()
    return [item.strip() for item in requirements]


def get_long_description():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name='pwbm-api-client',
    version='v0.9.58',
    install_requires=get_requirements(),
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
)
