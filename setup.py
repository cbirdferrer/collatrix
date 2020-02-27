from setuptools import setup, find_packages
#from distutils import setup, find_packages

setup(
    name = "morphometrix_collating",
    version = "1.0.0",
    description="A GUI for collating MorphoMetriX outputs",
    author = "Clara Bird",
    author_email = "clara.birdferrer@gmail.com",
    license='MIT',
    url = "https://github.com/cbirdferrer/MorphometrixCollating",
    entry_points={
        'gui_scripts': [
            'MorphometrixCollating = morphometrix_collating.__main__:main'
        ]
    },
#    scripts=['morphometrix/morphometrix.py'],
    packages = ['morphometrix_collating']
#    packages= find_packages()
)
