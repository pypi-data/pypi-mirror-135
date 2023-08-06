Simple streamlit component module

*Introduction*
-----------------------

The purpose of this document is to illustrate how one can package a streamlit & python module. This specific module is a simple proof of concept 
that shows to incorporate python & streamlit to produce a streamlit compnenet that allows a developer the add a title to the streamlt slider function. 
Following the streamlit & python module has been packaged, this document will detail how to upload this package from pypi. 
In additon to the above, this document will deomstrate how to install the pyhton module onto yuour local machine and use it within 
a project. For the official document on creating python packes see https://packaging.python.org/en/latest/tutorials/packaging-projects/ .
This document is the end result of following the link above.



*Requirements/Installations*

**Ensure python is installed. Click on the following link: https://www.python.org/downloads/ **


Install Streamlit in your environment

**pip install streamlit** (or 3 based upon your python version)

Copy

Or if you want to create an easily-reproducible environment, replace pip with pipenv every time you install something:

**pipenv install streamlit"**(credit to streamlit documentation)

Install ipython

**pip install ipython**

The setup.cfg file reads the pyproject.toml. The pyproject.toml file tells a tool such as pip what the build configuration is for this project.
Click on the following link below for a more detailed explanation on the pyproject.toml file:

** (https://snarky.ca/what-the-heck-is-pyproject-toml/ **

Once 