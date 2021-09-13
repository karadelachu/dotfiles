#!/bin/sh

xrandr --setprovideroutputsource modesetting NVIDIA-0
xrandr --auto
xrandr --output eDP-1-1 --off --output HDMI-1-2 --primary --gamma 1.25:1.25:1.25 --dpi 96 --mode 1600x900

exec qtile start
