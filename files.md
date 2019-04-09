Here we describe all the source files used in this codebase.

## Core Files
All the "core" Pac-Man files are ones with complete implementations.
Students should not make changes to these files.
These files will be provided by the autograder during grading.

### baselineTeam.py
A baseline team for the capture competition.
All submissions should consistently beat the baseline.

### captureAgents.py
The base class for agents participating in a capture game.

### captureGraphicsDisplay.py
Graphics for the capture game.

### capture.py
The core logic of the capture game.
This file can be invoked directly to play capture.

### crawler.py
The core logic of the crawler simulation.
this file can be involed to start the simulation.

### distanceCalculator.py
Useful classes for computing distances in mazes.

### eightpuzzle.py
A non-pacman search problem that your Pac-Man search agent should work will on.

### environment.py
The base class for an environment.

### featureExtractors.py
Extracts features from game states.

### game.py
The logic behind how the Pac-Man world works.
This file describes several supporting types like AgentState, Agent, Direction, and Grid.

### ghostAgents.py
Agents to control ghosts.

### graphicsCrawlerDisplay.py
The graphics for the crawler simulation.

### graphicsDisplay.py
Graphics for Pac-Man.

### graphicsGridworldDisplay.py
The graphics for the gridworld simulations.

### graphicsUtils.py
Support for Pac-Man graphics.

### gridworld.py
The core logic of the gridworld simulation.
this file can be invoked to start the simulation.

### keyboardAgents.py
Keyboard interfaces to control Pac-Man.

### layout.py
Code for reading layout files and storing their contents.
Many layouts are provided in the `layouts` directory.

### learningAgents.py
Base classes for value estimation and reinforcement agents.

### mazeGenerator.py
Generates random Pac-Man mazes.

### mdp.py
The base class for Markov Decision Processes.

### pacmanAgents.py
Some stock (and not smart) pacman agents.

### pacman.py
The main file that runs Pac-Man games.
This file describes a Pac-Man GameState type, which you use in this project.

### search.py
The base class for search problems.

### searchAgents.py
The base class for search-based agents.
Also includes some already implemented agents.

### textDisplay.py
ASCII graphics for Pac-Man environments.

### textGridworldDisplay.py
The text interface for the gridworld simulation.

### util.py
Useful data structures for implementing search algorithms.

## Student Files
These are files that the student is expected to implement during the course of various assignments.
The exact files that are to be implemented will be discussed in the project instructions.

### analysis_student.py
Answers to various analysis questions in the form of functions.
Submitted in **P3**.

### multiAgents_student.py
Where all of the student's multi-agent search agents will reside.
Submitted in **P2**.

### myTeam_student.py
A group's submission for the capture tournament.
Initially filled with DummyAgents.
Submitted in **P4**.

### qlearningAgents_student.py
Approximate agents that use Q-Learning.
Submitted in **P3**.

### search_student.py
Generic search algorithms to be implemented by the student.
Submitted in **P1**.

### searchAgents_student.py
Pac-Man search agents to be implemented by the student.
Submitted in **P1**.

### valueIterationAgents_student.py
Agents that learn using some heuristic over iterations.
Submitted in **P3**.
