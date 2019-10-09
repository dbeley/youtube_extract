import setuptools
import youtube_extract

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube_extract",
    version=youtube_extract.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="Extract metadata for all videos from a youtube channel into a csv file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/youtube_extract",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["youtube_extract=youtube_extract.__main__:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["youtube-dl"],
)
