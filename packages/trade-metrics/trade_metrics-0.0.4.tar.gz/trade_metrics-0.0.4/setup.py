from struct import pack
from setuptools import setup, find_packages

setup(
    name="trade_metrics",
    version="0.0.4",
    packages=find_packages(),
    setup_requires=['wheel'],
    install_requires=["pandas>=1.3.4", "scipy>=1.7.2", "numpy>=1.19.2", "matplotlib>=3.3.0"],
)