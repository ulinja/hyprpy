#!/usr/bin/env bash

PATH_TO_TEST_LOG='/home/arch/test.log'

hyprctl monitors -j > "$PATH_TO_TEST_LOG"
sleep 5
sudo shutdown now
