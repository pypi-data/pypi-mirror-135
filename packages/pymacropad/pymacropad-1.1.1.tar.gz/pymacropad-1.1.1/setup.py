from setuptools import setup, find_packages

setup(
    name='pymacropad',
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}+git.{sha}",
        "dirty_template": "{tag}.dev{ccount}+git.{sha}.dirty",
        "starting_version": "0.0.1",
        "version_file": "",
        "count_commits_from_version_file": False
    },
    author="James Waters",
    author_email="james@jcwaters.co.uk",
    description="Utility program for binding actions to keys on a given input",
    url="https://github.com/j-waters/pymacropad",
    install_requires=['PyYAML', 'Click', 'libevdev', 'pyxdg'],
    setup_requires=['setuptools-git-versioning'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pymacropad=pymacropad.__main__:main'
        ]
    },
    python_requires='>=3.10',
)
