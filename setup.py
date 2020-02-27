from setuptools import setup, find_packages
#from distutils import setup, find_packages

setup(
    name = "collating_tool",
    version = "1.0.0",
    description="A GUI for collating MorphoMetriX outputs",
    author = "Clara Bird",
    author_email = "clara.birdferrer@gmail.com",
    license='MIT',
    url = "https://github.com/cbirdferrer/morphometrix-collating",
    entry_points={
        'gui_scripts': [
            'collating_tool = collating_tool.__main__:main'
        ]
    },
#    scripts=['morphometrix/morphometrix.py'],
    packages = ['collating_tool']
#    packages= find_packages()
)
