import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="optical_tracer",
    version="0.2.0",
    author="pokurin123",
    author_email="s1922074@stu.musashino-u.ac.jp",
    description="The system detects and tracks characteristic moving objects from the video, and traces their movement to create a 3D graph.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pokurin123/optical_tracer",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        'Framework :: Matplotlib',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
)