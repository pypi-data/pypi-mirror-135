# Taskloop

This utility allows you to create multiple tasks for a
[Taskwarrior](https://taskwarrior.org) project.

# Installation

## via PyPi
` pip install taskloop`

## via git (development)
1. Clone this repo
2. cd taskloop
3. Add deps using poetry `poetry install`
4. `poetry run taskloop/loop.py`

# Running
After pip installing, you may run

`taskloop`

This requires you have a taskrc at ~/.config/task/taskrc.

More flexibility is planned for this though.  If you have an old style
~/.taskrc, you should be able to symlink it with `mkdir -p ~/.config/task/taskrc
&& ln -s ~/.taskrc ~/.config/task/taskrc`

## Entering tasks
You will be prompted for a project.  This will autocomplete from your list of
projects (currently only pending, planned to optionally pull from "completed"
also)

After entering a project, you will loop through adding tasks to the project.  if
you want to make your task dependent on the last task, start your task with a
period.

Entry will continue to loop until you end by entering an empty line

Now sync will be attempted.   There are currently no checks in place, so if you
don't have a taskserver configured,this will fail.

# Screencast Demo
[![asciicast](https://asciinema.org/a/B5IzyeUWdGRjK1bUtCjy52gpp.svg)](https://asciinema.org/a/B5IzyeUWdGRjK1bUtCjy52gpp)
