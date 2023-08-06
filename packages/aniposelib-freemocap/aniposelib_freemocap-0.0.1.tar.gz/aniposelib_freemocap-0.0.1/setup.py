import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aniposelib_freemocap",
    version="0.0.1",
    author="Pierre Karashchuk",
    author_email="krchtchk@gmail.com",
    description="A fork of `lambdaloop/aniposelib` to make more compatible with the FreeMoCap system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonmatthis/aniposelib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Image Recognition"
    ],
    install_requires=[
        'opencv-contrib-python',
        'numba', 'pandas',
        'numpy', 'scipy', 'toml', 'tqdm'
    ],
    extras_require={
        'full':  ["checkerboard"]
    }
)
