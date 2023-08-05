import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf8") as f:
    requires = f.read()

setuptools.setup(
    name='bilili_eco',
    version='0.0.5',
    license='GPLv3+',
    author='魔人波波',
    description='魔改BILILI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["bilibili_api","bilibili_api/exceptions","bilibili_api/utils"],
    package_data={
        "bilibili_api":['data/*.json','data/api/*.json'],
               },
    keywords=[
        "bilibili",
        "api",
        "spider"
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    data_files=["requirements.txt"],
    install_requires=requires.splitlines(),
    python_requires=">=3.8"
)
