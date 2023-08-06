import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aerial_contamination",
    version="0.0.1",
    author="YE BOWEN",
    author_email="s1922037@stu.musashino-u.ac.jp",
    description="A package for counting bugs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HAKU0312/aerial-contamination",
    project_urls={
        "Bug Tracker": "https://github.com/HAKU0312/aerial-contamination",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['aerial_contamination'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'aerial_contamination = aerial_contamination:main'
        ]
    },
)