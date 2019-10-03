"""
The `pacai.ui` package contains the all of the user interfaces for the `pacai` package.

At the core of all our UIs are the concepts of a view (`pacai.ui.view.AbstractView`)
and a frame (`pacai.ui.frame.Frame`).
A view knows how to convert the state of a game (`pacai.core.gamestate.AbstractGameState`)
into an abstract visual representation of the state
and then convert that abstract visual representation into a concrete one.
A frame is the abstract visual representation of the game state.

There are typically three types of graphics:

`pacai.ui.gui.AbstractGUIView`:
This view uses tkinter to open a window and display graphics.
Requires tk to be installed: https://tkdocs.com/tutorial/install.html .

`pacai.ui.text.AbstractTextView`:
This view outputs textual graphics directly to stdout.

`pacai.ui.null.AbstractNullView`:
This view outputs nothing.
This is especially useful when you need to script multiple games.

All children of `pacai.ui.view.AbstractView` support the ability to generate gifs of the game
they are rendering (even if the view does not output graphics).
The `pacman-sprites.png` file in this package contains the default sprites used for this project.
Users can modify this sprite sheet or supply a different on through command-line options.
All sprites are 50x50 pixels.
"""
