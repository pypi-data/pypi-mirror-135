import setuptools
import aviv_cdk

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aviv-cdk",
    version=aviv_cdk.__version__,
    author="Jules Clement",
    author_email="jules.clement@aviv-group.com",
    description="Aviv CDK Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aviv-group/aviv-cdk-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'aviv-aws=bin.aws_local:cli',
            'aviv-cdk-sfn-extract=bin.sfn_extract:cli'
        ],
    },
    install_requires=[
        "aws-cdk-lib>=2.3.0",
        "aws-cdk-aws-servicecatalog-alpha",
        "boto3>=1.20.26",
        "botocore>=1.23.26",
        "constructs>=10.0.0"
   ],
    setup_requires=['pytest-runner>=5.3.1'],
    tests_require=['pytest'],
    python_requires='>=3.8',
    use_2to3=False,
    zip_safe=False
)
