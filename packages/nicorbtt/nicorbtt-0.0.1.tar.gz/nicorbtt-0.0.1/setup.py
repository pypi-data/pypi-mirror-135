import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='nicorbtt',  
     version='0.0.1',
     author="Nico Rubattu",
     author_email="iamnicown@gmail.com",
     description="just for fun...",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/nicorbtt/nicorbtt",
     packages=['nicorbtt'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
