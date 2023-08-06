import setuptools

with open("D:\\Free\\Scarf\\README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ScarfKit",
    version="1.0.2",
    author="Qc",
    author_email="qcsdfsdvdac@gmail.com",
    description="A Simple Way To Create Web Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeepRepeatLoop/Scarf",
    project_urls={
        "Bug Tracker": "https://github.com/KeepRepeatLoop/Scarf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
    install_requires=[

    ]
)