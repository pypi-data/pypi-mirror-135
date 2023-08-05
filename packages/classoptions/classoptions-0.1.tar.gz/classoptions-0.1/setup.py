import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="classoptions",
    version="0.1",
    author="Adrian Martinez Rodriguez",
    author_email="adrianmrit@gmail.com",
    description="Implement namespaced and inheritable metadata at the class level.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianmrit/classoptions",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"classoptions": "classoptions"},
    packages=["classoptions"],
    python_requires=">=3.6",
)
