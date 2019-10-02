"""
Various graphics utilities for gridworld.
"""

import sys
import time
import tkinter

_root_window = None  # The root window for graphics output
_canvas = None  # The canvas which holds graphics
_canvas_xs = None  # Size of canvas object
_canvas_ys = None
_canvas_x = None  # Current position on canvas
_canvas_y = None
_canvas_col = None  # Current colour (set to black below)
_canvas_tsize = 12
_canvas_tserifs = 0

def formatColor(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

def sleep(secs):
    global _root_window

    if (_root_window is None):
        time.sleep(secs)
    else:
        _root_window.update_idletasks()
        _root_window.after(int(1000 * secs), _root_window.quit)
        _root_window.mainloop()

def begin_graphics(width = 640, height = 480, color = formatColor(0, 0, 0), title = None):
    global _root_window, _canvas, _canvas_x, _canvas_y, _canvas_xs, _canvas_ys, _bg_color

    # Check for duplicate call
    if _root_window is not None:
        # Lose the window.
        _root_window.destroy()

    # Save the canvas size parameters
    _canvas_xs, _canvas_ys = width - 1, height - 1
    _canvas_x, _canvas_y = 0, _canvas_ys
    _bg_color = color

    # Create the root window
    _root_window = tkinter.Tk(baseName = 'pacman')
    _root_window.protocol('WM_DELETE_WINDOW', _destroy_window)
    _root_window.title(title or 'Graphics Window')
    _root_window.resizable(0, 0)

    # Create the canvas object
    try:
        _canvas = tkinter.Canvas(_root_window, width=width, height=height)
        _canvas.pack()
        draw_background()
        _canvas.update()
    except Exception as ex:
        _root_window = None
        raise RuntimeError("Unable to create tkinter canvas.") from ex

    # Bind to key-down and key-up events
    _root_window.bind("<KeyPress>", _keypress)
    _root_window.bind("<KeyRelease>", _keyrelease)
    _root_window.bind("<FocusIn>", _clear_keys)
    _root_window.bind("<FocusOut>", _clear_keys)
    _clear_keys()

def draw_background():
    corners = [(0, 0), (0, _canvas_ys), (_canvas_xs, _canvas_ys), (_canvas_xs, 0)]
    polygon(corners, _bg_color, fillColor=_bg_color, filled=True, smoothed=False)

def _destroy_window(event=None):
    sys.exit(0)

def clear_screen(background=None):
    global _canvas_x, _canvas_y
    _canvas.delete('all')
    draw_background()
    _canvas_x, _canvas_y = 0, _canvas_ys

def polygon(coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
    c = []
    for coord in coords:
        c.append(coord[0])
        c.append(coord[1])

    if (fillColor is None):
        fillColor = outlineColor

    if filled == 0:
        fillColor = ""

    poly = _canvas.create_polygon(c, outline=outlineColor, fill=fillColor,
            smooth=smoothed, width=width)
    if behind > 0:
        _canvas.tag_lower(poly, behind)  # Higher should be more visible
    return poly

def circle(pos, r, outlineColor, fillColor, endpoints=None, style='pieslice', width=2):
    x, y = pos
    x0, x1 = x - r - 1, x + r
    y0, y1 = y - r - 1, y + r
    if (endpoints is None):
        e = [0, 359]
    else:
        e = list(endpoints)

    while e[0] > e[1]:
        e[1] = e[1] + 360

    return _canvas.create_arc(x0, y0, x1, y1, outline=outlineColor, fill=fillColor,
                              extent=e[1] - e[0], start=e[0], style=style, width=width)

def text(pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw"):
    global _canvas_x, _canvas_y

    x, y = pos
    font = (font, str(size), style)
    return _canvas.create_text(x, y, fill=color, text=contents, font=font, anchor=anchor)

def line(here, there, color=formatColor(0, 0, 0), width=2):
    x0, y0 = here[0], here[1]
    x1, y1 = there[0], there[1]
    return _canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

###########################
#   Keypress handling     #
###########################

# We bind to key-down and key-up events.

_keysdown = {}
# This holds an unprocessed key release.  We delay key releases by up to
# one call to keys_pressed() to get round a problem with auto repeat.
_got_release = None

def _keypress(event):
    global _got_release
    _keysdown[event.keysym] = 1
    # print(event.char, event.keycode)
    _got_release = None

def _keyrelease(event):
    global _got_release

    try:
        del _keysdown[event.keysym]
    except Exception:
        pass

    _got_release = 1

def _clear_keys(event=None):
    global _keysdown, _got_release

    _keysdown = {}
    _got_release = None

def keys_pressed(d_o_e=None, d_w=tkinter._tkinter.DONT_WAIT):
    global _root_window

    if (d_o_e is None):
        d_o_e = _root_window.tk.dooneevent

    d_o_e(d_w)
    if _got_release:
        d_o_e(d_w)

    return list(_keysdown.keys())

# Block for a list of keys...

def wait_for_keys():
    keys = []
    while keys == []:
        keys = keys_pressed()
        sleep(0.05)
    return keys
