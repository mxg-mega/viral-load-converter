from setuptools import setup, find_packages

setup(
    name="ViralLoadCalculator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PySide6>=6.0.0',
    ],
    author="Your Name",
    description="A viral load calculator application",
    python_requires='>=3.7',
    include_package_data=True,
)


