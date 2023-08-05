import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bc_1922053",
    version="0.0.1",
    author="yuta icchikawa",
    author_email="s1922053@stu.musashino-u.ac.jp",
    description="Brand identification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    py_modules=['bc_1922053'],
   # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'bc_1922053 = bc_1922053:main'
        ]
    },
)
