import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scorejapangarbage",
    version="1.0.0",
    author="kota minami",
    author_email="s1922076@stu.musashino-u.ac.jp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MinamiKota/scorejapangarbage",
    project_urls={
        "Bug Tracker": "https://github.com/MinamiKota/scorejapangarbage",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['scorejapangarbage'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'scorejapangarbage = scorejapangarbage:main'
        ]
    },
)
