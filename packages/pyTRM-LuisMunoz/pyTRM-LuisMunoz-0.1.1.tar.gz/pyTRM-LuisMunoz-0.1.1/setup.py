import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pyTRM-LuisMunoz",
    version = "0.1.1",
    author = "Luis Munoz",
    author_email = "",
    description = "Modulo para obtener la TRM - Colombia",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir = {"":"src"},
    packages = setuptools.find_packages(where="src"),
    install_requires=[
        'requests',
    ],
)