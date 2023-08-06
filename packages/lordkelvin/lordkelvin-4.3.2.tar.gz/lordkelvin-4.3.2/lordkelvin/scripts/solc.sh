#!/bin/sh
exec solc-0.7.6 --no-color -oout --abi --bin --overwrite --allow-paths=. --optimize "$@"
