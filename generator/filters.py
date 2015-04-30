#!/usr/bin/python3

def subnet_filename(cidr):
    return str(cidr).replace(':', '-').replace('.', '-').replace('/', '_')
