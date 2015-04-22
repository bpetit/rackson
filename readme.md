# rackson #

Rackson's purpose is to permit a simple and clean documentation of an IT infrastructure.
It can be used to document either physical and/or ip layer.
For now, it is just a piece of software that looks at json files (containing data for racks, datacenters, ip addresses, devices, ...) and generates static html files.

State: **experimental**

## How to use ##

Edit json data in `data/` and run `python3 generate.py`.
The html files are in `output`.
