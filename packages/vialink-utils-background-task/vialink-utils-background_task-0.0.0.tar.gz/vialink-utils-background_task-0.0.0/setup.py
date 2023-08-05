import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='vialink-utils-background_task',
    version='0.0.0',
    packages=setuptools.find_namespace_packages(include=['vialink.utils.*']),
    url='',
    license='Apache 2.0',
    author='SSripilaipong',
    author_email='santhapon@via.link',
    python_requires='>=3.7',
    description='Vialink Utils',
    install_requires=requirements,
)
