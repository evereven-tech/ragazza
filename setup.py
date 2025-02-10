from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ragazza",
    version="0.1.0",
    author="evereven",
    author_email="info@evereven.tech",
    description="A tool to convert PDF slides into markdown format with AI-powered content analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evereven-tech/ragazza",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0',
            'flake8>=6.0',
            'build>=1.0',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'ragazza=ragazza.ragazza:main',
        ],
    },
)
