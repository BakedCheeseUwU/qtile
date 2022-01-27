from typing import List  # noqa: F401

from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy

mod = "mod4"


def open_powermenu():
    qtile.cmd_spawn("rofi -show power-menu -modi power-menu:rofi-power-menu")


def open_wifimenu():
    qtile.cmd_spawn("rofi-wifi-menu.sh")


def open_pavu():
    qtile.cmd_spawn("pavucontrol")


keys = [
    # --------------------------- Switch windows/layouts ----------------------
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    Key([mod], "Tab", lazy.next_layout()),

    # --------------------- Shuffle windows ---------------------------------
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # -------------------------- Resize windows ---------------------------
    Key([mod, "control"], "j", lazy.layout.grow()),
    Key([mod, "control"], "k", lazy.layout.shrink()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.layout.flip()),

    # ------------ Restart,Shutdown & Kill------------------------------
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "shift"], "x", lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu")),

    # -------------------------Spawn apps/programs-----------------------------
    Key([mod], "Return", lazy.spawn("kitty")),
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod], "e", lazy.spawn("rofi -show emoji -modi emoji")),
    Key([mod], "c", lazy.spawn("rofi -show calc -modi calc -no-show-match -no-sort")),
    Key([mod], "w", lazy.spawn("firefox")),

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

groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
    Group("9"),
]


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
                desc="Switch & move focused window to group {}".format(i.name),
            ),
            Key(["mod1"], 'Return', lazy.group['scratchpad'].dropdown_toggle('kitty')),
            Key(["mod1"], 'p', lazy.group['scratchpad'].dropdown_toggle('music')),
            Key(["mod1"], 'm', lazy.group['scratchpad'].dropdown_toggle('mixer')),
            Key(["mod1"], 'n', lazy.group['scratchpad'].dropdown_toggle('nnn')),
        ]
    )

groups.append(
    ScratchPad("scratchpad", [
        DropDown("kitty", 'kitty', y=0.15, height=0.70, width=0.80, opacity=1),
        DropDown("music", 'kitty ncmpcpp', y=0.15, height=0.70, width=0.80, opacity=1),
        DropDown("nnn", 'kitty nnn -d -C', y=0.15, height=0.70, width=0.80, opacity=1),
        DropDown("mixer", 'kitty pulsemixer', y=0.15, height=0.70, width=0.80, opacity=1),

    ]),
)
# --------------------------------- Colors -------------------------------


def init_colors():
    return [
        ["#161320", "#161320"],
        ["#6E6C7E", "#6E6C7E"],
        ["#D9E0EE", "#D9E0EE"],
        ["#E8A2AF", "#E8A2AF"],
        ["#ABE9B3", "#ABE9B3"],
        ["#DDB6F2", "#DDB6F2"],
        ["#F28FAD", "#F28FAD"],
        ["#96CDFB", "#96CDFB"],
        ["#89DCEB", "#89DCEB"],
        ["#F5C2E7", "#F5C2E7"],
    ]


colors = init_colors()

# -------------------------------Layouts------------------------------------
layout_theme = {
    "border_width": 3,
    "margin": 20,
    "font": "JetBrainsMono Nerd Font",
    "font_size": 10,
    "border_focus": colors[7],
    "border_normal": colors[9],
}

# window layouts
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Floating(**layout_theme),
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
    "this_current_screen_border": colors[7],
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
                widget.WindowName(font="JetBrainsMono Nerd Font", fontsize=13),
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
                    foreground=colors[8],
                    mouse_callbacks={"Button1": open_wifimenu},
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                ),
                widget.Battery(
                    charge_char="",
                    discharge_char="",
                    full_char="",
                    font="JetBrainsMono Nerd Font",
                    format="{char} {percent:2.0%}",
                    foreground=colors[4],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.TextBox(
                    text=" ",
                    font="JetBrainsMono Nerd Font",
                    fontsize=16,
                    foreground=colors[5],
                ),
                widget.PulseVolume(
                    limit_max_volume="True",
                    update_interval=0.1,
                    mouse_callbacks={"Button3": open_pavu},
                    fontsize=18,
                    foreground=colors[5],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.TextBox(
                    text=" ", font="Font Awesome", fontsize=16, foreground=colors[6]
                ),
                widget.Clock(format="%A %b %d", fontsize=18, foreground=colors[6]),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.TextBox(
                    text="", font="Font Awesome", fontsize=16, foreground=colors[7]
                ),
                widget.Clock(format="%H:%M", fontsize=18, foreground=colors[7]),
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
            margin=[10, 10, -10, 10],
        ),
        bottom=bar.Gap(-13),
        left=bar.Gap(-13),
        right=bar.Gap(-13),
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
