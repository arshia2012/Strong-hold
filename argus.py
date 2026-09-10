import BetterRich
from time import sleep
from collections import defaultdict
from scapy.all import sniff, IP, TCP, UDP
import argparse
from datetime import datetime
from event_logger import logInfo
from stats_logger import log_traffic_stats

#flag
parser = argparse.ArgumentParser(description="Tool to Protect you from getting hacked")
parser.add_argument("-d", "--delay", type=float, default=0.0, help="delay between every packet sniff", required=False)
parser.add_argument("-c", "--count", type=int, default=0, help="Number of packets to capture (leave empty for infinit)")
parser.add_argument("-t", "--timeout", type=float, default=0, help="Time to sniff", required=False)
parser.add_argument("-w", "--window", type=float, default=5, help="Time Window for data to check", required=False)
parser.add_argument("-f", "--filter", help="Filter result", required=False)
parser.add_argument("-ft", "--flood-threshold", type=int, default=500, help="Max data send from an IP, to alert", required=False)
parser.add_argument("-pt", "--port-threshold", type=int, default=50, help="Max data send from an IP to diffrent ports, to alert", required=False)
parser.add_argument("-i", "--iface", help="Interface internet to work on", required=False)
arg_parse = parser.parse_args()

#Banner
def print_banner():
    banner = r"""
                                                              
███████╗████████╗██████╗  ██████╗ ███╗   ██╗ ██████╗               ██╗  ██╗ ██████╗ ██╗     ██████╗ 
██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝               ██║  ██║██╔═══██╗██║     ██╔══██╗
███████╗   ██║   ██████╔╝██║   ██║██╔██╗ ██║██║  ███╗    █████╗    ███████║██║   ██║██║     ██║  ██║
╚════██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║██║   ██║    ╚════╝    ██╔══██║██║   ██║██║     ██║  ██║
███████║   ██║   ██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝              ██║  ██║╚██████╔╝███████╗██████╔╝
╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝               ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═════╝ 
                                                                                                    
                        DoS, Port-scan protector
                        made by aCoDeR(Arshia Rahbari)
"""
    print(banner)
print_banner()


#dicts
ipAct = defaultdict(list)
ipPort = defaultdict(set)
floodip = set()
portScanip = set()

#port list refresh
last_reset = datetime.now()
RESET_INTERVAL = 60

#stats logging refresh
last_stats_log = datetime.now()
STATS_LOG_INTERVAL = arg_parse.window

#collector, Engine
def packetProcess(delay, window, packet, floodFilter, portFilter):
    if not packet.haslayer(IP):
        return

    srcIp = packet[IP].src
    dstIp = packet[IP].dst

    now = datetime.now()
    ipAct[srcIp] = [t for t in ipAct[srcIp] if (now - t).total_seconds() <= window]
    ipAct[srcIp].append(now)
    
    #alert flood
    if len(ipAct[srcIp]) >= floodFilter:
        if srcIp not in floodip:
            BetterRich.warn(f"ALERT, Flood ATTACK DETECTED!! from IP: {srcIp}")
            floodip.add(srcIp)
            #log info area
            logInfo(
                source="sniffer",
                event_type="flood",
                src_ip=srcIp,
                severity="high",
                details=f"{len(ipAct[srcIp])} packets in {window}s window"
            )
    else:
        floodip.discard(srcIp)

    if packet.haslayer(TCP):
        srcPort = packet[TCP].sport
        dstPort = packet[TCP].dport
        proto = "TCP"
        ipPort[srcIp].add(dstPort)
    
    elif packet.haslayer(UDP):
        srcPort = packet[UDP].sport
        dstPort = packet[UDP].dport
        proto = "UDP"
        ipPort[srcIp].add(dstPort)
    
    #port refresh
    global last_reset
    if (datetime.now() - last_reset).total_seconds() >= RESET_INTERVAL:
        ipPort.clear()
        portScanip.clear()
        last_reset = datetime.now()

    #send even normal data
    global last_stats_log
    if (datetime.now() - last_stats_log).total_seconds() >= STATS_LOG_INTERVAL:
        for ip in set(list(ipAct.keys()) + list(ipPort.keys())):
            log_traffic_stats(
                src_ip=ip,
                packet_count=len(ipAct[ip]),
                distinct_ports=len(ipPort[ip]),
                window_seconds=window
            )
        last_stats_log = datetime.now()

    #alert port scan
    if len(ipPort[srcIp]) >= portFilter:
        if srcIp not in portScanip:
            BetterRich.warn(f"ALERT, PORTSCAN DETECTED!! from IP: {srcIp}")
            portScanip.add(srcIp)
            logInfo(
                source="sniffer",
                event_type="port_scan",
                src_ip=srcIp,
                severity="high",
                details=f"{len(ipPort[srcIp])} distinct ports scanned"
            )


    if delay > 0:
        sleep(delay)

#sniffer
timeout_value = None if arg_parse.timeout == 0 else arg_parse.timeout
try:
    if arg_parse.filter is None:
        sniff(
            prn=lambda pkt: packetProcess(delay=arg_parse.delay,window=arg_parse.window,packet=pkt,floodFilter=arg_parse.flood_threshold,portFilter=arg_parse.port_threshold),
            count=arg_parse.count,
            timeout=timeout_value,
            iface=arg_parse.iface
        )
    elif arg_parse.filter is not None:
        sniff(
            prn=lambda pkt: packetProcess(delay=arg_parse.delay,window=arg_parse.window,packet=pkt,floodFilter=arg_parse.flood_threshold,portFilter=arg_parse.port_threshold),
            count=arg_parse.count,
            timeout=timeout_value,
            filter=arg_parse.filter,
            iface=arg_parse.iface
        )

except KeyboardInterrupt:
    BetterRich.red("Action stopped by user")