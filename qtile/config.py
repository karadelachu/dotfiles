#  _  __     _      ____       _      ____    _____   _          _    
# | |/ /    / \    |  _ \     / \    |  _ \  | ____| | |        / \   
# | ' /    / _ \   | |_) |   / _ \   | | | | |  _|   | |       / _ \  
# | . \   / ___ \  |  _ <   / ___ \  | |_| | | |___  | |___   / ___ \ 
# |_|\_\ /_/   \_\ |_| \_\ /_/   \_\ |____/  |_____| |_____| /_/   \_\
#
#   ___    _____   ___   _       _____ 
#  / _ \  |_   _| |_ _| | |     | ____|
# | | | |   | |    | |  | |     |  _|  
# | |_| |   | |    | |  | |___  | |___ 
#  \__\_\   |_|   |___| |_____| |_____|


from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess

mod = "mod4"
terminal = "kitty"


keys = [
    
    Key([mod], "h",
        lazy.layout.left(),
        desc="Move focus to left"
        ),
    Key([mod], "l",
        lazy.layout.right(),
        desc="Move focus to right"
        ),
    Key([mod], "j",
        lazy.layout.down(),
        desc="Move focus down"
        ),
    Key([mod], "k",
        lazy.layout.up(),
        desc="Move focus up"),
    Key([mod], "space",
        lazy.layout.next(),
        desc="Move window focus to other window"
        ),
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"
        ),
    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        desc="Grow window to the left"
        ),
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right"
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        desc="Grow window down"
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        desc="Grow window up"
        ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes"
        ),
    Key([mod, "shift"], "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"
        ),
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"
        ),
    Key([mod], "Home",
        lazy.spawn("flameshot gui"),
        desc="Take a screenshot"
        ),
    Key([mod, "shift"], "e",
        lazy.spawn("bash .config/rofi/bin/powermenu"),
        desc="Launch powermenu"
        ),
    Key([mod], "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating"
        ),
    Key([mod], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"
        ),
    Key([mod], "q",
        lazy.window.kill(),
        desc="Kill focused window"
        ),
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen"
        ),
    Key([mod, "control"], "r",
        lazy.restart(),
        desc="Restart Qtile"
        ),
    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"
        ),
    Key([mod], "p",
        lazy.spawn("dmenu_run -nf '#F8F8F2' -nb '#282A36' -sb '#6272A4' -sf '#F8F8F2' -fn 'monospace-10'"),
        desc="Spawn a command using dmenu"
        ),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(margin=6, border_normal='#282A36', border_focus='#6272A4', border_width=2),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(margin=6, border_normal='#282A36', border_focus='#6272A4', border_width=2),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Ubuntu',
    fontsize=11,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(borderwidth=3, inactive='ffffff',
                                margin_x=0,
                                hide_unused=True, rounded=False,
                                disable_drag=True, highlight_method='block', 
                                this_current_screen_border='44475a',background='282a36'),
                widget.Sep(padding=10,background='282a36'),
                widget.CurrentLayoutIcon(background='282a36'),
                widget.Spacer(background='282a36'),
                widget.Net(background='282a36', format='{down} ↓', foreground='a2ffa2'),
                widget.TextBox(background='282a36', text='|'),
                widget.Net(background='282a36', format='↑ {up}', foreground='a2a2ff'),
                widget.Sep(background='282a36', padding=10, linewidth=1),
                widget.Systray(background='282a36', ),
                widget.Sep(background='282a36', padding=10, linewidth=1),
                widget.Clock(background='282a36', format='%Y-%m-%d %a %I:%M %p'),
                #widget.QuickExit(),
            ],
            20,
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
    Match(wm_class='Steam'),  # Steam
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], border_normal='#282A36', border_focus='#6272A4', border_width=2)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
