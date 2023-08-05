import setuptools

setuptools.setup(
    install_requires=[
        "pygame",
        "appdirs",
        "jsonpickle",
        "results",
        "requests"
    ],
    entry_points='''
        [console_scripts]
        2048=py2048.__main__:main
    ''',
)