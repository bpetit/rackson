#!/usr/bin/python3

def subnet_filename(cidr):
    return str(cidr).replace(':', '-').replace('.', '-').replace('/', '_')

def percentage(value, max_value):
    return (value * 100.0 / max_value)
