## Pacman

A modified version of the Pacman educational project from the Berkley AI Lab:
http://ai.berkeley.edu/project_overview.html

### FAQ

**Q:** What version of Python does this project support?  
**A:** Python >= 3.5.
The original version of this project was written for Python 2, but it has since been updated.

**Q:** Why are there no packages? Seems disorganized...  
**A:** You are right, this project is not designed with modern Python package-oriented design principles.
This project is meant for students who may be seeing Python for the first time,
and therefore has been simplified.

**Q:** What's with these `_student` files?  
**A:** The `_student` files are the files that students will edit to complete assignments.
When an assignment is graded, any other pacman files (without the `_student` suffix) that a student submits will
be overwritten.
This makes it clear to the student what files they are allowed to change.
It is not pretty (and not how non-educational projects should be designed), but it is easy for students and graders.

**Q:** How do I get my own copy of repo to develop on?  
**A:** They typical answer would be to [fork](https://help.github.com/en/articles/fork-a-repo).
However GitHub requires that all forks be public, and we don't want this for class assignments.
The following section has instructions on making a private copy of this repo.

### Making a Private Pacman Repo

First, make a [new Github repository](https://github.com/new).
You can name it whatever you want (you can even keep the name `pacman`).
For this example, we will call our repository `cool-pacman`.
Make sure to make the repository private and **do not** initialize the repository with a README.
Private repositories are currently free on GitHub.
After clicking "Create Repository", the next page should have the link to this new repository.
For this example, we will use `https://github.com/eriq-augustine/cool-pacman.git`.

Now, clone **this** pacman repo (the one that you are reading this README on):
```
git clone https://github.com/linqs/pacman.git
cd pacman
```
If you are a cool kid with (ssh keys)[https://help.github.com/en/articles/connecting-to-github-with-ssh], then you can use the ssh endpoint.
If you accidentally already created a pacman fork, then you can just cd into the fork repository you already cloned.
(Just make sure to delete the fork through the GitHub web interface after you finish these steps.)

Next, we will change the cloned repository's remote url to point to our new repository.
You can do this via the `git remote set-url` command:
```
git remote set-url origin https://github.com/eriq-augustine/cool-pacman.git
```
Or, you can just directly edit the `.git/config` file (the url under `[remote "origin"]`).

Finally, you just need to push to your new repository:
```
git push
```

You're all set!
You now have a private copy of this pacman repo.

#### Pulling Changes from This Repo

Rarely, you may need to pull changes/fixes from this repository.
Doing so is super easy.
Just do a `git pull` command and specify this repository as an argument:
```
git pull https://github.com/linqs/pacman.git
```

### Acknowledgements

This project has been built up from the work of many people.
Here are just a few that we know about:
 - The Berkley AI Lab for starting this project. Primarily John Denero and Dan Klein.
 - Barak Michener for providing improved graphics and debugging help.
 - Ed Karuna for providing improved graphics and debugging help.
 - Jeremy Cowles for implementing an initial tournament infrastructure.
 - LiveWires for providing some code from a Pacman implementation (used / modified with permission).
