import os
from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy


mod = "mod4"
terminal = "tilix"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "g", lazy.spawn('google-chrome-stable'),
        desc="Launch Google Chrome"),
    Key([mod], "f", lazy.spawn('firefox'), desc="Launch Firefox"),
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]
groups = [Group(i)
          for i in [" ", " ", " ", " ", " ", " ", " "]]

for i, group in enumerate(groups):
    # Each workspace is identified by a number starting at 1
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N (actual_key)
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N (actual_key)
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

colors = [
    ["#000000", "#000000"],
    ["#ffffff", "#ffffff"],
    ["#d60000", "#d60000"],
    ["#ffc812", "#ffc812"],
    ["#ff9166", '#ff9166'],
    ["#ff3d3d", "#ff3d3d"],
]

layouts = [
    layout.Columns(border_width=1, margin=20, border_focus=colors[1][0]),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(border_width=1, margin=20, border_focus="#ffffff"),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    text=' ',
                    fontsize=25,
                    foreground=colors[2],
                    background=colors[0]
                ),
                widget.GroupBox(
                    fontsize=13,
                    margin_y=3,
                    margin_x=20,
                    padding_x=5,
                    borderwidth=3,
                    active=colors[1],
                    inactive=colors[1],
                    rounded=False,
                    highlight_method="line",
                    this_current_screen_border=colors[2],
                    this_screen_border=colors[0],
                    other_current_screen_border=colors[0],
                    other_screen_border=colors[0],
                    foreground=colors[1],
                    background=colors[0]
                ),

                widget.Spacer(
                    background=colors[0]
                ),

                widget.TextBox(
                    text='',
                    foreground=colors[3],
                    background=colors[0],
                    padding=10,
                    fontsize=25
                ),
                widget.Systray(
                    background=colors[0],
                    foreground=colors[1],
                    padding=5,
                    margin=0
                ),
                widget.TextBox(
                    text='',
                    foreground=colors[3],
                    background=colors[0],
                    padding=10,
                    fontsize=25
                ),
                widget.TextBox(
                    text='',
                    foreground=colors[1],
                    background=colors[0],
                    margin=0,
                    padding=5,
                    fontsize=25
                ),
                widget.Volume(
                    foreground=colors[1],
                    background=colors[0],
                    padding=5
                ),

                widget.TextBox(
                    text='',
                    foreground=colors[3],
                    background=colors[0],
                    padding=10,
                    fontsize=25,
                ),

                widget.Clock(
                    padding=10,
                    foreground=colors[1],
                    background=colors[0],
                    format="%A, %B %d - %H:%M "
                ),

            ],
            30,
            opacity=0.9
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

autostart = ["setxkbmap us",
             "picom --no-fading-openclose --no-vsync &",
             "nitrogen --restore"
             ]

for x in autostart:
    os.system(x)
