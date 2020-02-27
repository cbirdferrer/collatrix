from setuptools import setup, find_packages
#from distutils import setup, find_packages

setup(
    name = "collating",
    version = "1.0.0",
    description="A GUI for collating MorphoMetriX outputs",
    author = "Clara Bird",
    author_email = "clara.birdferrer@gmail.com",
    license='MIT',
    url = "https://github.com/cbirdferrer/collating",
    entry_points={
        'gui_scripts': [
            'collating = collating.__main__:main'
        ]
    },
#    scripts=['morphometrix/morphometrix.py'],
    packages = ['collating']
#    packages= find_packages()
)
