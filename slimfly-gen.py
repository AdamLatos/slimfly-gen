#!/usr/bin/env python3

# from ibsim net-examples:
# Net configuration file example
#
# The file defines node records as follows:
# < node header line: >
# < first connected port >
# < second connected port >
# < ... >
# < last connected port >
# < newlines (at least one) >
# < next record ...>
#
# The header line format is as follows:
# type(Switch|Hca)	ports(1-255)	"nodeid"(unique string)
#
# The connected port line format is:
# [localport] "remoteid" [remoteport]
#
# Optionally, link width can be supplied by adding 'w=(1|4|12)':
# [localport] "remoteid" [remoteport]	w=12
#
# The first port in the file is used as the SM port.



# 1. Connecting routers

import argparse
import sys

description = "Generate SlimFly topology for use with ibsim."
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-q", type=int, help="Parameter q of the network. Has to be a prime power and satisfy q = 4n + {-1, 0, 1}. Number of routers in network is 2q^2. By default q = 5.", default=5)
q = parser.parse_args().q

if q != 5:
    sys.exit("q != 5 not yet implemented!")

print(f"q = {q}")

Fq = range(q)
print(f"Galois field: {list(Fq)}")


for elem in Fq:
    hist = []
    for power in range(1,q+1):
        res = pow(elem,power) % q
        if res in hist:
            break
        hist.append(res)
    if len(hist) == q-1:
        primitive_element = elem
        break
        
print(f"Primitive element: {primitive_element}")