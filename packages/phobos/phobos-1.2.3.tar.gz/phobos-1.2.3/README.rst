===================
Phobos
===================

A Utility Library that assists in Geospatial Machine Learning by: 

* supporting creation of a project with boilerplate code for model training
* exporting annotations from `Europa <https://europa.granular.ai>`_
* populating template project with configurable components for model
* fetching samples from dataset shards available at ``AIStore``
* orchestrating model training and validation
* deploying project to `Arche <https://arche.granular.ai>`_ for efficient training in a node cluster   

Flow
----
.. image:: docs/phobos.png
    :width: 1200

Features
--------

* Polyaxon auto-param capture
* Configuration enforcement and management for translation into Dione environment
* Precomposed loss functions and metrics
* Get annotations from Europa 


TODO
----

* ETL datasets via CLI on AIStore
* Multi Input and Multi Output models
* Static analysis code 
* Dataset abstraction 
* Standard dataset loaders 
* Pretrained models 


Build Details
-------------

* packages are managed using poetry
* packages poetry maintains pyproject.toml
* PRs and commits to `develop` branch trigger github actions


Tests
-----

>>> make install
>>> make test-light


A GPU machine is requried for test-heavy

>>> make install
>>> make test-heavy


Installation
------------

```pip install phobos```


Usage
-----

Get all the annotation tasks available in Europa 

```phobos get --all --email <email> --passwd <password>```

Download one particular annotation task from Europa 

```phobos get --task <task ID> --path <directory to save anntoations> --email <email> --passwd <password>```

Create a project boilerplate code 

```phobos init --project_name <project name> --project_description <project description>```

Run an experiment 

```phobos run```

Run associated tensorboard 

```phobos tensorboard --uuid <project id>```

License
-------
GPLv3

Documentation
-------------

View documentation `here <https://phobos.granular.ai/>`_

Image
-----
Use gcr.io/granular-ai/phobos:latest
