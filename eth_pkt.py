# Decode an ethernet packet by bytes

MIN_PKT_SIZE = 60

# == Eth ==
OFFSET_DEST_MAC     = 0
OFFSET_SRC_MAC      = 6
OFFSET_ETHERTYPE    = 12

# == ARP ==
OFFSET_ARP_HTYPE    = 14
OFFSET_ARP_PTYPE    = 16
OFFSET_ARP_HLEN     = 18
OFFSET_ARP_PLEN     = 19
OFFSET_ARP_OPER     = 20
OFFSET_ARP_SHA      = 22
OFFSET_ARP_SPA      = 28
OFFSET_ARP_THA      = 32
OFFSET_ARP_TPA      = 38

# == IP ==
OFFSET_IP_VERSION_IHL = 14
OFFSET_IP_DSCP_ECN  = 15
OFFSET_IP_TOTAL_LENGTH = 16
OFFSET_IP_ID        = 18
OFFSET_IP_FLAG_FRAG = 20
OFFSET_IP_TTL       = 22
OFFSET_IP_PROTOCOL  = 23
OFFSET_IP_CHECKSUM  = 24
OFFSET_IP_SRC_IP    = 26
OFFSET_IP_DEST_IP   = 30

# == ICMP ==

# == UDP ==
OFFSET_UDP_SRC_PORT = 34
OFFSET_UDP_DEST_PORT = 36
OFFSET_UDP_LENGTH   = 38
OFFSET_UDP_DATA     = 42

# ===== Ethertypes =====
ETHERTYPE_IPV4      = 0x0800
ETHERTYPE_ARP       = 0x0806
ETHERTYPE_WOL       = 0x0842
ETHERTYPE_VLAN      = 0x8100
ETHERTYPE_IPV6      = 0x86DD
ETHERTYPE_STAG      = 0x88A8
ETHERTYPE_PTP       = 0x88F7

# ===== IPv4 Protocols =====
IPV4_PROTOCOL_IP    = 0
IPV4_PROTOCOL_ICMP  = 1
IPV4_PROTOCOL_IPENCAP = 4
IPV4_PROTOCOL_TCP   = 6
IPV4_PROTOCOL_EGP   = 8
IPV4_PROTOCOL_UDP   = 17
IPV4_PROTOCOL_HMP   = 20
IPV4_PROTOCOL_RDP   = 27
IPV4_PROTOCOL_DDP   = 37
IPV4_PROTOCOL_IPV6  = 41
IPV4_PROTOCOL_IPV6_ROUTE = 43
IPV4_PROTOCOL_IPV6_FRAG = 44
IPV4_PROTOCOL_IDRP  = 45
IPV4_PROTOCOL_IPV6_ICMP = 58
IPV4_PROTOCOL_IPV6_NONXT = 59
IPV4_PROTOCOL_IPV6_OPTS = 60
IPV4_PROTOCOL_PIM   = 103
IPV4_PROTOCOL_L2TP  = 115
IPV4_PROTOCOL_SCTP  = 132
IPV4_PROTOCOL_UDPLITE = 136

def print_mac(pkt, offset):
    print(':'.join(["{:x}".format(x) for x in pkt[offset:offset+6]]))
    return

def print_ip(pkt, offset):
    print('.'.join([str(x) for x in pkt[offset:offset+4]]))
    return

def ethertype(pkt, offset):
    ethtype = (pkt[offset] << 8) + pkt[offset+1]
    types = {
        ETHERTYPE_IPV4: "IPv4",
        ETHERTYPE_ARP: "ARP",
        ETHERTYPE_WOL: "Wake-on-LAN",
        ETHERTYPE_VLAN: "VLAN-tagged frame (IEEE 802.1Q)",
        ETHERTYPE_IPV6: "IPv6",
        ETHERTYPE_STAG: "Service VLAN tag identifier (S-Tag) on Q-in-Q Tunnel",
        ETHERTYPE_PTP: "Precision Time Protocol (PTP) over IEEE 802.3 Ethernet",
    }
    return (ethtype, types.get(ethtype, "Unknown 0x{:x}".format(ethtype)))

def _ipv4_protocol(pkt, offset):
    protocol = pkt[offset]
    protos = {
        IPV4_PROTOCOL_IP: "IP  # internet protocol, pseudo protocol number",
        IPV4_PROTOCOL_ICMP: "ICMP  # internet control message protocol",
        IPV4_PROTOCOL_IPENCAP: "IP-ENCAP # IP encapsulated in IP (officially ``IP'')",
        IPV4_PROTOCOL_TCP: "TCP  # transmission control protocol",
        IPV4_PROTOCOL_EGP: "EGP  # exterior gateway protocol",
        IPV4_PROTOCOL_UDP: "UDP  # user datagram protocol",
        IPV4_PROTOCOL_HMP: "HMP  # host monitoring protocol",
        IPV4_PROTOCOL_RDP: "RDP  # \"reliable datagram\" protocol",
        IPV4_PROTOCOL_DDP: "DDP  # Datagram Delivery Protocol",
        IPV4_PROTOCOL_IPV6: "IPv6  # Internet Protocol, version 6",
        IPV4_PROTOCOL_IPV6_ROUTE: "IPv6-Route # Routing Header for IPv6",
        IPV4_PROTOCOL_IPV6_FRAG: "IPv6-Frag # Fragment Header for IPv6",
        IPV4_PROTOCOL_IDRP: "IDRP  # Inter-Domain Routing Protocol",
        IPV4_PROTOCOL_IPV6_ICMP: "IPv6-ICMP # ICMP for IPv6",
        IPV4_PROTOCOL_IPV6_NONXT: "IPv6-NoNxt # No Next Header for IPv6",
        IPV4_PROTOCOL_IPV6_OPTS: "IPv6-Opts # Destination Options for IPv6",
        IPV4_PROTOCOL_PIM : "PIM  # Protocol Independent Multicast",
        IPV4_PROTOCOL_L2TP: "L2TP  # Layer Two Tunneling Protocol [RFC2661]",
        IPV4_PROTOCOL_SCTP: "SCTP  # Stream Control Transmission Protocol",
        IPV4_PROTOCOL_UDPLITE: "UDPLite  # UDP-Lite [RFC3828]",
    }
    return (protocol, protos.get(protocol, "Unknown 0x{:x}".format(protocol)))

def _ipv4_decoder(pkt):
    version = pkt[OFFSET_IP_VERSION_IHL] >> 4
    if version != 4:
        print("=== ERROR: IPv4 Version is {}. Should be 4".format(version))
    ihl = pkt[OFFSET_IP_VERSION_IHL] & 0xf
    _len = 4*ihl
    if (_len < 20) or (_len > 60):
        print("=== ERROR: Invalid IPv4 header length. IHL = {} (len = {})".format(ihl, _len))
    total_len = (pkt[OFFSET_IP_TOTAL_LENGTH] << 8) + pkt[OFFSET_IP_TOTAL_LENGTH+1]
    print("TOTAL_LEN: {}".format(total_len))
    ttl = pkt[OFFSET_IP_TTL]
    print("TTL: {}".format(ttl))
    protocol, _protostr = _ipv4_protocol(pkt, OFFSET_IP_PROTOCOL)
    print("PROTOCOL: {}".format(_protostr))
    checksum = (pkt[OFFSET_IP_CHECKSUM] << 8) + pkt[OFFSET_IP_CHECKSUM+1]
    print("CHECKSUM: 0x{}".format(checksum))
    print("SOURCE_IP: ", end="")
    print_ip(pkt, OFFSET_IP_SRC_IP)
    print("DEST_IP: ", end="")
    print_ip(pkt, OFFSET_IP_DEST_IP)
    return

def _arp_decoder(pkt):
    # HTYPE (ethernet = 0x0001)
    htype = (pkt[OFFSET_ARP_HTYPE] << 8) + pkt[OFFSET_ARP_HTYPE + 1]
    if htype == 0x0001:
        print("HTYPE: Ethernet")
    else:
        print("HTYPE: Unknown 0x{:x}".format(htype))
    # PTYPE (protocol type)
    ptype = (pkt[OFFSET_ARP_PTYPE] << 8) + pkt[OFFSET_ARP_PTYPE + 1]
    if ptype == 0x0800:
        print("PTYPE: IPv4")
    else:
        print("PTYPE: Unknown 0x{:x}".format(ptype))
    # Hardware address length
    hlen = pkt[OFFSET_ARP_HLEN]
    if hlen != 6:
        print("=== ERROR: HLEN is {}. Should be 6".format(hlen))
    # IP address length
    plen = pkt[OFFSET_ARP_PLEN]
    if plen != 4:
        print("=== ERROR: PLEN is {}. Should be 4".format(plen))
    # Operation
    oper = (pkt[OFFSET_ARP_OPER] << 8) + pkt[OFFSET_ARP_OPER + 1]
    if oper == 1:
        print("OPER: request")
    elif oper == 2:
        print("OPER: reply")
    else:
        print("=== ERROR: Unknown OPER 0x{:x}".format(OPER))
    # SHA/SPA
    print("SHA: ", end="")
    print_mac(pkt, OFFSET_ARP_SHA)
    print("SPA: ", end="")
    print_ip(pkt, OFFSET_ARP_SPA)
    # THA/TPA
    print("THA: ", end="")
    print_mac(pkt, OFFSET_ARP_THA)
    print("TPA: ", end="")
    print_ip(pkt, OFFSET_ARP_TPA)
    return

def get_pkt_docoder(ethtype):
    if ethtype == ETHERTYPE_IPV4:
        return _ipv4_decoder
    elif ethtype == ETHERTYPE_ARP:
        return _arp_decoder
    elif ethtype == ETHERTYPE_WOL:
        print("TODO: WOL decoder")
    elif ethtype == ETHERTYPE_IPV6:
        print("TODO: IPv6 decoder")
    else:
        print("I'm not writing a decoder for this")
    return None

def decode(pkt):
    _len = len(pkt)
    if _len < MIN_PKT_SIZE:
        print("Pkt too small ({} < {})".format(len(pkt), MIN_PKT_SIZE))
    print("DEST_MAC: ", end="")
    print_mac(pkt, OFFSET_DEST_MAC)
    print("SRC_MAC: ", end="")
    print_mac(pkt, OFFSET_SRC_MAC)
    _ethtype, _etstr = ethertype(pkt, OFFSET_ETHERTYPE)
    print("ETHERTYPE: {}".format(_etstr))
    _decoder = get_pkt_docoder(_ethtype)
    if _decoder is not None:
        _decoder(pkt)
    return

def doPktDecode(argv):
    pktHex = argv[1:]
    lhex = []
    for arg in argv[1:]:
        lhex.extend(arg.split())
    pkt = [int(x, 16) for x in lhex]
    decode(pkt)

if __name__ == "__main__":
    import sys
    doPktDecode(sys.argv)
