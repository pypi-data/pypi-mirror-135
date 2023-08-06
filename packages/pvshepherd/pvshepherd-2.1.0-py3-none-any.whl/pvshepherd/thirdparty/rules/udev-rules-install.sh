#!/bin/bash

[ "$UID" -eq 0 ] || exec sudo "$0" "$@"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cp "$DIR"/../st/linux/rules/*.rules /etc/udev/rules.d/
cp "$DIR"/../nxp/linux/rules/*.rules /etc/udev/rules.d/
