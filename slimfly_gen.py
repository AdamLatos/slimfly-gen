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

import argparse
import sys
from collections import deque

# Find primitive element

def find_primitive(q, Fq):
    primitive_element = 0
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
    if primitive_element == 0:
        sys.exit("primitive_element == 0")
        
    return primitive_element


# Find generator sets

def find_generator_sets(q, primitive_elem):
    X1 = [1]
    X2 = []
    for i in range(1,q-1):
        elem = pow(primitive_elem, i) % q
        if i % 2 == 0:
            X1.append(elem)
        else:
            X2.append(elem)
    return (X1, X2)

# Create routes - each route as list in dict with ({0,1}, x, y) as key

def create_routes(q, Fq, X1, X2):
    keys = [(i,x,y) for i in range(2) for x in Fq for y in Fq]
    routes = {k: [] for k in keys}

    for x in Fq:
        for y in Fq:
            for yp in Fq:
                if (y - yp) in X1:
                    routes[(0,x,y)].append((0,x,yp))
                    routes[(0,x,yp)].append((0,x,y))
                if (y - yp) in X2:
                    routes[(1,x,y)].append((1,x,yp))
                    routes[(1,x,yp)].append((1,x,y))
                for xp in Fq:
                    if (xp * x + yp) % q == y:
                        routes[(0,x,y)].append((1,xp,yp))
                        routes[(1,xp,yp)].append((0,x,y))
    return routes


def main():

    description = "Generate SlimFly topology for use with ibsim."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-q", type=int, help="Parameter q of the network. Has to be a prime power and satisfy q = 4n + {-1, 0, 1}. Number of routers in network is 2q^2. By default q = 5.", default=5)
    q = parser.parse_args().q

    # Check q

    if q != 5:
        sys.exit("q != 5 not yet implemented!")
    print(f"q = {q}")

    # Find Galois field

    Fq = range(q)
    

    primitive_elem = find_primitive(q, Fq)
    (X1, X2) = find_generator_sets(q, primitive_elem)
    routes = create_routes(q, Fq, X1, X2)

    print(f"Galois field: {list(Fq)}")
    print(f"Primitive element: {primitive_elem}")
    print(f"X1: {X1}")
    print(f"X2: {X2}")


 
if __name__ == "__main__":
	main()