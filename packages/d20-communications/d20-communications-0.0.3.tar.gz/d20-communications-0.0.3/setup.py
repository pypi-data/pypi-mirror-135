import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="d20-communications",
    version="0.0.3",
    author="Alex Sánchez Vega",
    author_email="alex@d20.services",
    description="A small ORM for multimodel DBs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d20services/python_arango_communications_module",
    project_urls={
        "Bug Tracker": "https://github.com/d20services/python_arango_communications_module/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['pyArango', 'datetime', 'd20-orm', 'requests', 'sendgrid', 'exponent_server_sdk', 'Twilio'],
)