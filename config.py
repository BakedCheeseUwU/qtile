from typing import List  # noqa: F401

from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()
# --- Keybindings ---


def open_pavu():
    qtile.cmd_spawn("pavucontrol")


def open_powermenu():
    qtile.cmd_spawn("powermenu.sh")


keys = [
    # --------------------------- Switch windows/layouts ----------------------
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    Key([mod], "space", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # --------------------- Shuffle windows ---------------------------------
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left",
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # -------------------------- Resize windows ---------------------------
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        desc="Grow window to the left",
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right",
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # ------------ Restart,Shutdown & Kill------------------------------
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "x", lazy.spawn("powermenu.sh"), desc="Kill focused window"),
    # -------------------------Spawn apps/programs-----------------------------
    Key([mod], "Return", lazy.spawn(terminal), desc="Spawn a terminal"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Spawn rofi"),
    Key([mod], "e", lazy.spawn("rofi -show emoji"), desc="Spawn emoji menu"),
    Key(
        [mod],
        "c",
        lazy.spawn("rofi -show calc -modi calc -no-show-match -no-sort"),
        desc="Spawn rofi",
    ),
    Key([mod], "w", lazy.spawn("firefox"), desc="Spawn firefox"),
    # -----------------------Sound and brightness----------------------------
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    Key(["mod1"], "j", lazy.spawn("playerctl --player mpd volume 0.1-")),
    Key(["mod1"], "k", lazy.spawn("playerctl --player mpd volume 0.1+")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),
]
# ---------------------------------- Groups --------------------------------

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # -- Switch groups --
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # -- Move window to group --
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )
# --------------------------------- Colors -------------------------------

def init_colors():
    return [
        ["#15161E", "#282a36"],  # color 0 | bg
        ["#545c7e", "#545c7e"],  # color 1 | bg
        ["#f8f8f2", "#f8f8f2"],  # color 2 | fg
        ["#f7768e", "#ff5555"],  # color 3 | red
        ["#9ece6a", "#50fa7b"],  # color 4 | green
        ["#e0af68", "#f1fa8c"],  # color 5 | yellow
        ["#bb9af7", "#bd93f9"],  # color 6 | blue
        ["#7aa2f7", "#ff79c6"],  # color 7 | magenta
        ["#7dcfff", "#8be9fd"],  # color 8 | cyan
        ["#a9b1d6", "#bbbbbb"],
    ]  # color 9 | white


colors = init_colors()
# -------------------------------Layouts------------------------------------
layout_theme = {
    "border_width": 3,
    "margin": 15,
    "font": "JetBrainsMono Nerd Font",
    "font_size": 10,
    "border_focus": colors[6],
    "border_normal": colors[9],
}

# window layouts
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Stack(num_stacks=2, **layout_theme),
    layout.Bsp(**layout_theme),
    layout.Tile(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="pavucontrol"),  # pavucontrol
    ],
    **layout_theme
)
# --------------------------- Bar and screens -----------------------------

widget_defaults = dict(
    font="JetBrainsMono Nerd Fonts",
    fontsize=18,
    padding=3,
)
extension_defaults = widget_defaults.copy()

group_box_options = {
    "active": colors[2],
    "inactive": colors[1],
    "spacing": 5,
    "rounded": True,
    "this_current_screen_border": colors[6],
    "font": "JetBrainsMono Nerd Font",
}

text_options = {}


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.GroupBox(**group_box_options),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.CurrentLayout(
                    font="JetBrainsMono Nerd Font",
                    foreground=colors[7],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.WindowName(
                    font="JetBrainsMono Nerd Font",
                ),
                widget.Systray(
                    padding=10,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.Wlan(
                    interface="wlp3s0",
                    font="JetBrainsMono Nerd Font",
                    format=" {essid}",
                    fontsize="18",
                    padding=5,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.Battery(
                    charge_char="",
                    discharge_char="",
                    full_char="",
                    font="JetBrainsMono Nerd Font",
                    format="{char} {percent:2.0%}",
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.TextBox(
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=16,
                ),
                widget.PulseVolume(
                    limit_max_volume="True",
                    update_interval=0.1,
                    mouse_callbacks={"Button3": open_pavu},
                    fontsize=18,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.TextBox(
                    text=" ",
                    font="Font Awesome",
                    fontsize=16,
                ),
                widget.Clock(
                    format="%A %b %d",
                    fontsize=18,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.TextBox(
                    text="",
                    font="Font Awesome",
                    fontsize=16,
                ),
                widget.Clock(
                    format="%H:%M",
                    fontsize=18,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.TextBox(
                    text=" ",
                    mouse_callbacks={"Button1": open_powermenu},
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                ),
            ],
            30,
            margin=[10, 10, 10, 10],
        ),
        bottom=bar.Gap(10),
        left=bar.Gap(10),
        right=bar.Gap(10),
    ),
]
# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
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
