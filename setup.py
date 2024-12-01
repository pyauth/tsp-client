#!/usr/bin/env python

from setuptools import find_packages, setup  # type: ignore

setup(
    name="tsp-client",
    url="https://github.com/pyauth/tsp-client",
    project_urls={
        "Documentation": "https://pyauth.github.io/tsp-client/",
        "Change log": "https://github.com/pyauth/tsp-client/blob/main/Changes.rst",
        "Issue tracker": "https://github.com/pyauth/tsp-client/issues",
    },
    license="Apache Software License",
    author="Andrey Kislyuk",
    author_email="kislyuk@gmail.com",
    description="An IETF Time-Stamp Protocol (TSP) (RFC 3161) client",
    long_description=open("README.rst").read(),
    use_scm_version={
        "write_to": "tsp_client/version.py",
    },
    setup_requires=["setuptools_scm >= 3.4.3"],
    install_requires=["asn1crypto >= 1.4.0", "requests >= 2.25.1", "pyOpenSSL >= 21.0.0, < 24"],
    extras_require={
        "tests": [
            "ruff",
            "coverage",
            "build",
            "wheel",
            "mypy",
        ]
    },
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    package_data={
        "tsp_client": ["py.typed"],
    },
    platforms=["MacOS X", "Posix"],
    test_suite="test",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
