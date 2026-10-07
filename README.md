# Subnet Calculator

A lightweight command-line subnet calculator for network technicians and students.
Built with only the Python standard library — no dependencies to install.

## Features

- Describe any IPv4 network: network/broadcast address, subnet & wildcard masks,
  usable host range, and host count
- Split a network into N equal subnets (`--split`)
- Split a network into subnets of a given prefix length (`--new-prefix`)
- Handles edge cases (`/31` point-to-point links, `/32` host routes)

## Usage

```bash
# Describe a network
python3 subnet_calc.py 192.168.1.0/24

# Split 10.0.0.0/8 into 4 equal subnets
python3 subnet_calc.py 10.0.0.0/8 --split 4

# Split 172.16.0.0/16 into /24 subnets
python3 subnet_calc.py 172.16.0.0/16 --new-prefix 24
```

## Example output

```
$ python3 subnet_calc.py 192.168.1.0/24
Network address : 192.168.1.0
Broadcast addr  : 192.168.1.255
Subnet mask     : 255.255.255.0
Wildcard mask   : 0.0.0.255
Prefix length   : /24
Total addresses : 256
Usable hosts    : 254
First usable    : 192.168.1.1
Last usable     : 192.168.1.254
```

## Requirements

- Python 3.8+

## License

MIT
