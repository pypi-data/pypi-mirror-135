import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-recaptcha-authorizer",
    "version": "2.1.2",
    "description": "An AWS CDK library that provides a reCaptcha Authorizer for API Gateway REST APIs",
    "license": "Apache-2.0",
    "url": "https://github.com/engineal/cdk-recaptcha-authorizer#readme",
    "long_description_content_type": "text/markdown",
    "author": "Aaron Lucia<alucia@engineal.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/engineal/cdk-recaptcha-authorizer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_recaptcha_authorizer",
        "cdk_recaptcha_authorizer._jsii"
    ],
    "package_data": {
        "cdk_recaptcha_authorizer._jsii": [
            "cdk-recaptcha-authorizer@2.1.2.jsii.tgz"
        ],
        "cdk_recaptcha_authorizer": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib==2.8.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.52.1, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
