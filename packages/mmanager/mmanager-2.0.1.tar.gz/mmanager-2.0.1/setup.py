from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='mmanager',
    version='2.0.1',
    description='Modelmanager API With Azure ML Integration',
    author='falcon',
    license='MIT',
    packages=['mmanager'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    package_data={
        'mmanager':['example_scripts/*.py', 'assets/model_assets/*.csv', 'assets/model_assets/*.json', 'assets/model_assets/*.h5' , 'assets/model_assets/*.jpg', 'assets/project_assets/*.jpg'],
    }

)
