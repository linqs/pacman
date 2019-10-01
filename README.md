## Pacman

A modified version of the Pacman educational project from the [Berkeley AI Lab](http://ai.berkeley.edu/project_overview.html).

Some improvements from the original project:
 - Upgraded to Python 3.
 - Organized into packages.
 - Brought up to a common style with a style checker.
 - Added logging.
 - Added tests.
 - Fixed several bugs.
 - Generalized and reorganized several project elements.
 - Replaced the graphics systems.
 - Added the ability to generate gifs from any pacman or capture game.

### FAQ

**Q:** What version of Python does this project support?  
**A:** Python >= 3.5.
The original version of this project was written for Python 2, but it has since been updated.

**Q:** What dependencies do I need for this project?  
**A:** This project has very limited dependencies.
The pure Python dependencies can be installed via pip and are all listed in the requirements file.
These can be installed via: `pip3 install -r requirements.txt`.
To use a GUI, you also need `Tk` installed.
The process for installing Tk differs depending on your OS, instructions can be found [here](https://tkdocs.com/tutorial/install.html).

**Q:** How do I run this project?  
**A:** All the binary/executables for this project are located in the `pacai.bin` package.
You can invoke them from this repository's root directory (where this file is located) using a command like:
```
python3 -m pacai.bin.pacman
```

**Q:** How can I run the style checker?  
**A:** The easiest way to run the style checker is to execute the `run_style.sh` script in the root of this repository.
If a `0` comes up, then you are good!

**Q:** What's with the `student` package?  
**A:** The `student` package is for the files that students will edit to complete assignments.
When an assignment is graded, all files will be placed in the `student` package.
The rest will be supplied by the autograder.
This makes it clear to the student what files they are allowed to change.

**Q:** How do I get my own copy of repo to develop on?  
**A:** They typical answer would be to [fork it](https://help.github.com/en/articles/fork-a-repo).
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
If you are a cool kid with [ssh keys](https://help.github.com/en/articles/connecting-to-github-with-ssh), then you can use the ssh endpoint instead of the http endpoint listed above.

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

#### Pulling Changes from This Repo Into Your Fork

Occasionally, you may need to pull changes/fixes from this repository.
Doing so is super easy.
Just do a `git pull` command and specify this repository as an argument:
```
git pull https://github.com/linqs/pacman.git
```

### Acknowledgements

This project has been built up from the work of many people.
Here are just a few that we know about:
 - The Berkley AI Lab for starting this project. Primarily John Denero and Dan Klein.
 - Barak Michener for providing the original graphics and debugging help.
 - Ed Karuna for providing the original graphics and debugging help.
 - Jeremy Cowles for implementing an initial tournament infrastructure.
 - LiveWires for providing some code from a Pacman implementation (used / modified with permission).
 - The LINQS lab from UCSC.
 - Graduates of the CMPS 140 class who have helped pave the way for future classes (their identities are immortalized in the git history).
