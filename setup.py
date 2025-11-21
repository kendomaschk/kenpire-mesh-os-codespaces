from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kenpire-mesh-os",
    version="2.0.0",
    author="Ken Domaschk",
    author_email="ken@kenpire.tech",
    description="Military-grade cognitive infrastructure for enterprise applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kendomaschk/kenpire-mesh-os-production",
    project_urls={
        "Bug Tracker": "https://github.com/kendomaschk/kenpire-mesh-os-production/issues",
        "Documentation": "https://docs.kenpire.tech",
        "Source Code": "https://github.com/kendomaschk/kenpire-mesh-os-production",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.9.0",
            "flake8>=6.0.0",
            "mypy>=1.6.0",
            "coverage>=7.3.0",
        ],
        "monitoring": [
            "prometheus-client>=0.19.0",
            "grafana-api>=1.0.3",
        ],
        "cloud": [
            "google-cloud-storage>=2.10.0",
            "boto3>=1.34.0",
            "azure-storage-blob>=12.19.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kenpire=kenpire.main:main",
            "kenpire-server=kenpire.server:run_server",
            "kenpire-worker=kenpire.worker:run_worker",
        ],
    },
    include_package_data=True,
    package_data={
        "kenpire": ["config/*.yml", "templates/*.json", "schemas/*.json"],
    },
    zip_safe=False,
)