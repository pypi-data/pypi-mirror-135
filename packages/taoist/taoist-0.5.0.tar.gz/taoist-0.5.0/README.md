# taoist: Python-based command line interface for Todoist

[![Upload Python Package](https://github.com/popgendad/taoist/actions/workflows/python-publish.yml/badge.svg)](https://github.com/popgendad/taoist/actions/workflows/python-publish.yml)

This project is still under development and is not yet ready for release. It is a simple utility that relies on the [official Todoist Python API](https://github.com/Doist/todoist-api-python). This software is not created by, affiliated with, or supported by Doist. The `taoist` utility has functionality for performing basic transactions involving Todoist projects, sections, labels and tasks. The goal of the project is to enable most major components of 
a ["getting-things-done"](https://todoist.com/productivity-methods/getting-things-done) workflow from a terminal environment and is not intended to replicate the functionality of the Todoist app.

Quick Start
-----------

The taoist package can be install via PyPi
```
$ pip3 install taoist
```

Next, connect `taoist` to your Todoist account. First you must retrieve the API token from the Todoist app.
Once you have the API token, you run
```
taoist init --token <TOKEN>
```
if run without the `--token` switch, you will be interactively prompted to provide the API token.

To see your list of projects, run
```
taoist project list
```
Similarly, to see your list of tasks, run
```
taoist task list
```

Working with Projects
---------------------

The `taoist` utility currently has the functionality to perform the following project-related requests:

1. `list`: list user's projects
2. `create`: create a new user project
3. `delete`: delete an existing user project

Working with Tasks
------------------

The `taoist` utility can perform the following task-related requests:

1. `list`: list user's tasks
2. `create`: create a new user task
3. `delete`: delete an existing user task
4. `label`: add a label to an existing user task
5. `done`: mark an existing user task as completed or done

Working with Labels
-------------------

The `taoist` utility currently has the functionality to perform the following label-related requests:

1. `list`: list user's labels
2. `create`: create a new user label
3. `delete`: delete an existing user label

Working with Sections
---------------------

The `taoist` utility currently has the functionality to perform the following section-related requests:

1. `list`: list sections within a given project
2. `create`: create a new section within a given project
3. `delete`: delete an existing section
