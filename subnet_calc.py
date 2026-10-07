#!/usr/bin/env python3
"""
Subnet Calculator
=================
A simple command-line subnet calculator for network technicians.

Usage:
    python3 subnet_calc.py 192.168.1.0/24
    python3 subnet_calc.py 10.0.0.0/8 --split 4
    python3 subnet_calc.py 172.16.0.0/16 --new-prefix 24

Only the Python standard library is required.
"""

import argparse
import ipaddress
import sys


def describe(network: ipaddress.IPv4Network) -> str:
    """Return a human-readable description of an IPv4 network."""
    hosts = list(network.hosts())
    lines = [
        f"Network address : {network.network_address}",
        f"Broadcast addr  : {network.broadcast_address}",
        f"Subnet mask     : {network.netmask}",
        f"Wildcard mask   : {network.hostmask}",
        f"Prefix length   : /{network.prefixlen}",
        f"Total addresses : {network.num_addresses}",
    ]
    if network.prefixlen < 31:
        lines.append(f"Usable hosts    : {network.num_addresses - 2}")
        lines.append(f"First usable    : {hosts[0]}")
        lines.append(f"Last usable     : {hosts[-1]}")
    elif network.prefixlen == 31:
        lines.append("Usable hosts    : 2 (point-to-point /31)")
    else:
        lines.append("Usable hosts    : 1 (host route /32)")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Subnet calculator: describe a network or split it into subnets."
    )
    parser.add_argument(
        "network",
        help="Network in CIDR notation, e.g. 192.168.1.0/24",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--split",
        type=int,
        metavar="N",
        help="Split the network into N equal subnets",
    )
    group.add_argument(
        "--new-prefix",
        type=int,
        metavar="LEN",
        help="Split the network into subnets of the given prefix length",
    )
    args = parser.parse_args()

    try:
        network = ipaddress.IPv4Network(args.network, strict=False)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(describe(network))

    if args.split:
        if args.split < 1:
            print("Error: --split must be >= 1", file=sys.stderr)
            return 1
        # Find the smallest prefix length that yields at least N subnets.
        new_prefix = network.prefixlen
        while 2 ** (new_prefix - network.prefixlen) < args.split:
            new_prefix += 1
            if new_prefix > 30:
                print("Error: cannot split into that many subnets", file=sys.stderr)
                return 1
        subnets = list(network.subnets(new_prefix=new_prefix))
        print(f"\n--- Split into {len(subnets)} subnets (/{new_prefix}) ---")
        for i, sub in enumerate(subnets, 1):
            print(f"\n[{i}] {sub}")
            print(describe(sub))
    elif args.new_prefix:
        if not network.prefixlen < args.new_prefix <= 30:
            print("Error: --new-prefix must be larger than the network prefix (max /30)",
                  file=sys.stderr)
            return 1
        subnets = list(network.subnets(new_prefix=args.new_prefix))
        print(f"\n--- Split into {len(subnets)} subnets (/{args.new_prefix}) ---")
        for i, sub in enumerate(subnets, 1):
            print(f"[{i}] {sub}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
