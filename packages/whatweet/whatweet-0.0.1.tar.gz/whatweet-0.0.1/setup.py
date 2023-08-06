import setuptools

with open("README.md","r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="whatweet",
    version="0.0.1",
    author="Hinata Serizawa",
    author_email="s1922065@stu.musashino-u.ac.jp",
    description="Various analyses of tweet content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hnt-series00/whatweet",
    project_urls={
        "Bug Tracker": "https://github.com/hnt-series00/whatweet",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    py_modules=['whatweet'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    entry_points = {
        'console_scripts': [
            'whatweet = whatweet:main'
        ]
    },
)