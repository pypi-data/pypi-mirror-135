import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vaccinationvsdeath",
    version="0.0.1",
    author="Guyu Li",
    author_email="lgy778866@gmail.com",
    description="A package for demonstrate the relationship between covid-19 vaccination rates and deaths",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/G-Y3/covid-19-vaccination-vs.-mortality",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['vaccinationvsdeath'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'vaccinationvsdeath = vaccinationvsdeath:main'
        ]
    },
    install_requires = [
        'matplotlib',
        'seaborn',
        'numpy',
        'pandas',
        'wget'
    ]
)