import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lifeincome",
    version="0.0.1",
    author="JIAN",
    author_email="s1922012@stu.musashino-u.ac.jp",
    description="A package for comparing income and life span",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JIAN-JUNYANG/-AI-",
    project_urls={
        "data content": "https://github.com/JIAN-JUNYANG/-AI-",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['lifeincome'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'lifeincome = lifeincome:main'
        ]
    },
)