import setuptools

setuptools.setup(
    name="cppasv",
    version="0.2.0",
    author="Julian Rüth",
    author_email="julian.rueth@fsfe.org",
    description="Google C++ Benchmarks in Airspeed Velocity",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/flatsurf/cppasv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
