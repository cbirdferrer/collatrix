from setuptools import setup, find_packages

setup(
    name = "collatrix",
    version = "1.0.7",
    description="A GUI for collating MorphoMetriX outputs",
    author = "Clara Bird",
    author_email = "clara.birdferrer@gmail.com",
    license='MIT',
    url = "https://github.com/cbirdferrer/collatrix",
    entry_points={
        'gui_scripts': [
            'collatrix = collatrix.__main__:main'
        ]
    },

    packages = ['collatrix']
)
