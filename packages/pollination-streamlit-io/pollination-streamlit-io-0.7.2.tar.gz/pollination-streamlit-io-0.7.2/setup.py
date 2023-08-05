import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="pollination-streamlit-io",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Ladybug Tools",
    author_email="info@ladybug.tools",
    description="Pollination input/output components for Streamlit",
    long_description="Pollination input/output components for Streamlit to use with pollination apps",
    long_description_content_type="text/plain",
    url="https://github.com/pollination/pollination-streamlit-io",
    packages=setuptools.find_packages(exclude=["tests/*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    license="Apache-2.0 License"
)
