# Taskloop

This utility allows you to create multiple tasks for a
[Taskwarrior](https://taskwarrior.org) project.

# Installation
## via PyPi
` pip install taskloop`
## via git (development)
1. Clone this repo
2. cd taskloop
3. `poetry run taskloop/loop.py`
# Running
> Note: Currently this is in early development and doesn't actually do anything
> except demo an autocomplete of your projects
After pip installing, you may run

`taskloop`

This requires you have a taskrc at ~/.config/task/taskrc.

More flexibility is planned for this though.  If you have an old style
~/.taskrc, you should be able to symlink it with `mkdir -p ~/.config/task/taskrc
&& ln -s ~/.taskrc ~/.config/task/taskrc`
