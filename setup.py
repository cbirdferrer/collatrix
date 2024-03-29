from setuptools import setup, find_packages
from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name = "collatrix",
    version = "1.0.8",
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

    packages = ['collatrix'],
    data_files=[(site_packages_path, ["./collatrix.pth"])]
)
