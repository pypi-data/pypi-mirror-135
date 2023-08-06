.. _getting_started:


***************
Getting started
***************

Installing Topoly
=======================

Topoly is distributed as a python 3 package. The easiest method of installation is using the **pip** package manager.
Make sure you have a recent version of **pip**. You can upgrade it by running::

    pip3 install --upgrade pip

Now you are ready to install topoly::

    pip3 install topoly

Topoly can be installed without administrative privileges in the home folder of a particular user.
In that case all files (binaries, documentation, libraries and python modules) will be installed in::

    $HOME/.local/

If you choose to install Topoly with administrative privileges than everything will be installed in::

    /usr/local/


Verifying the installation
=============================

The easiest way to check if Topoly is working correctly is to grab our test project from github: https://github.com/ilbsm/topoly_tutorial.git ::

    git clone https://github.com/ilbsm/topoly_tutorial.git

Next create a python3 virtual environment, activate it and install topoly::

    cd topoly_tutorial
    python3 -m virtualenv venv
    venv/bin/activate
    pip install -r requirements.txt

Now you should be ready to run one of the examples::

    python knot_polynomials.py
