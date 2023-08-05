import setuptools

setuptools.setup(
    install_requires=[
        "pygame"
    ],
    entry_points='''
        [console_scripts]
        snake=pysnakepygame.__main__:main
    ''',
)