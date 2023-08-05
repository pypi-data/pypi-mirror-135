import netaddr

def from_4(ipv4):
    arr = ipv4.split('.')
    return int(arr[0]) << 0x18 | int(arr[1]) << 0x10 | int(arr[2]) << 0x08 | int(arr[3]) << 0x00

def from_6(ipv6):
    ip = netaddr.IPAddress(ipv6)
    arr = ip.format(dialect=netaddr.ipv6_verbose)
    return int(arr[0]) << 0x70 | \
           int(arr[1]) << 0x60 | \
           int(arr[2]) << 0x50 | \
           int(arr[3]) << 0x40 | \
           int(arr[4]) << 0x30 | \
           int(arr[5]) << 0x20 | \
           int(arr[6]) << 0x10 | \
           int(arr[7]) << 0x00 