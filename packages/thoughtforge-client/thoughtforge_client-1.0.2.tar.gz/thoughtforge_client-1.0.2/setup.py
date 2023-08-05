import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()

setuptools.setup(
    name="thoughtforge_client",
    version="1.0.2",
    author="Matthew Brown",
    author_email="matt@thoughtforge.ai",
    description="Client SDK Package for ThoughtForge AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thoughtforge-ai/thoughtforge-client",
    packages=packages,
    python_requires=">=3.6",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)