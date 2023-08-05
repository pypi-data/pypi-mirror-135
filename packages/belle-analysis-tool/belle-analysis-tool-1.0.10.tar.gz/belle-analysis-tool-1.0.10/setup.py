import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="belle-analysis-tool",
    version="1.0.10",
    author="Yuan-Ru Lin",
    author_email="yuanrulin.tw@gmail.com",
    description="A package that helps you do analysis for Belle or Belle II",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yuan-Ru-Lin/belle-analysis-tool",
    project_urls={
        "Bug Tracker": "https://github.com/Yuan-Ru-Lin/belle-analysis-tool/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Science/Research",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    exclude_package_data={"": ["README.md"]},
    python_requires=">=3.6",
)
