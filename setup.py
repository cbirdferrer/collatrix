from setuptools import setup, find_packages
#from distutils import setup, find_packages

setup(
    name = "morphometrix-collating",
    version = "1.0.0",
    description="A GUI for collating MorphoMetriX outputs",
    author = "Clara Bird",
    author_email = "clara.birdferrer@gmail.com",
    license='MIT',
    url = "https://github.com/cbirdferrer/morphometrix-collating",
    entry_points={
        'gui_scripts': [
            'morphometrix-collating = morphometrix-collating.__main__:main'
        ]
    },
#    scripts=['morphometrix/morphometrix.py'],
    packages = ['morphometrix-collating']
#    packages= find_packages()
)
