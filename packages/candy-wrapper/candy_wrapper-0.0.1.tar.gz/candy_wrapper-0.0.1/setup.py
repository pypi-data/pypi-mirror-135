from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'A sweet wrapper that lets object act js objects'
LONG_DESCRIPTION = '''
                    Wraps python object in a wrapper which allows attributes 
                    to be added like keys to a dict. 
                   '''

# Setting up
setup(
    name="candy_wrapper",
    version=VERSION,
    author="magedavee (Daniel Davee)",
    author_email="<daniel.v.davee@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['yes_or_no'],
    keywords=['python', 'debug'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)