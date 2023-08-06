Orange3 ESRF Add-on
======================

Tomwer is offering tools to automate acquisition and reconstruction processes for Tomography.
It contains:

- a library to access each acquisition process individually
- gui and applications to control main processes (reconstruction, data transfert...) and execute them as a stand alone application.
- an orange add-on to help users defining their own workflow (http://orange.biolab.si)



.. image:: http://www.edna-site.org/pub/doc/tomwer/extra/tomwer_start_short.gif


.. |Gitlab Status| image:: https://gitlab.esrf.fr/tomotools/tomwer/badges/master/pipeline.svg
    :target: https://gitlab.esrf.fr/tomotools/tomwer/pipelines


Documentation
-------------

Documentation of latest release is available at http://www.edna-site.org/pub/doc/tomwer/latest

Installation
------------

Step 0 - Create a virtual env
'''''''''''''''''''''''''''''

It is recommended to create a python virtual environment to run the workflow tool.
Virtual environment might avoid some conflict between python packages. But you can also install it on your 'current' python environment and move to step 1.

.. code-block:: bash

   virtualenv --python=python3 --system-site-packages myvirtualenv


Then activate the virtual environment

.. code-block:: bash

   source myvirtualenv/bin/activate
   

First update pip and setuptools to avoid some potential errors

.. code-block:: bash

   pip install --upgrade pip
   pip install setuptools --upgrade


.. note:: To quit the virtual environment

   .. code-block:: bash

      deactivate

Step 1 - Orange3 installation
'''''''''''''''''''''''''''''

You will need a fork of the original Orange project in order to run the tomwer project.
This is needed because small modification have been made in order to get the behavio we wanted (has looping workflows).

The fork is accessible here : https://github.com/payno/orange3.git

So install this fork :

.. code-block:: bash

   pip install git+https://github.com/payno/orange3.git

.. note:: Orange will try to access '/var/log/orange' to store logs of the last ten execusion.
          So if you want to keep those log make sure the directory exists.


Step 2 - tomwer
'''''''''''''''

From wheel
----------

To install it with the 'minimal' features:

.. code-block:: bash

    pip install tomwer


To install it with all the potential 'feature':

.. code-block:: bash

    pip install tomwer[full]


From source
-----------
clone the tomwer project

.. code-block:: bash

   git clone git@gitlab.esrf.fr:payno/tomwer.git


then install it

.. code-block:: bash

   cd tomwer
   pip install .

or for the 'full' version

.. code-block:: bash

   pip install .[full]

Step 3 - web log
''''''''''''''''

the workflow tool can send some log into graylog in order to get view of the status of the workflow execution.
If this is active (by default) then you will be able to see important log from a web interface.

To get more information see https://www.graylog.org/


Launching applications
::::::::::::::::::::::

After the installation tomwer is embedding several applications.

Those applications can be launched by calling:

.. code-block:: bash

   tomwer appName {options}

.. note:: if you only call `tomwer` then the man page will be displayed.

.. note:: You can access each application help using ``

    .. code-block:: bash

       tomwer appName --help


tomwer canvas - orange canvas
'''''''''''''''''''''''''''''

You can launch the canvas to create workflows from the different 'bricks'

.. code-block:: bash

   tomwer canvas

.. note:: you can also use `orange-canvas`

.. note:: if your installed a virtual environment do not forget to active it :

    .. code-block:: bash

       source myvirtualenv/bin/activate


Documentation
:::::::::::::

.. code-block:: bash

   cd doc
   make html

The documentation is build in doc/build/html and the entry point is index.html

.. code-block:: bash

   firefox build/html/index.html

.. note:: the build of the documentation need sphinx to be installed. This is not an hard dependacy. So you might need to install it.


You also should generate documentation to be accessible from Orange GUI (pressing the F1 key).

.. code-block:: bash

   cd doc
   make htmlhelp