from scapy.all import IP, ICMP, TCP, sr1
import sys

def icmp_probe(ip):
	icmp_packet = IP(dst=ip)/ICMP()
	resp_packet = sr1(icmp_packet, timeout=10)
	return resp_packet != None
	
def syn_scan(ip, port):
	syn_packet = IP(dst=ip)/TCP(dport=int(port), flags='S')
	resp_packet = sr1(syn_packet, timeout=10)
	return resp_packet != None and resp_packet.getlayer('TCP').flags==0x12, resp_packet
	
	
if __name__ == "__main__":
	ip = sys.argv[1]
	port = sys.argv[2]
	if icmp_probe(ip):
		print ("ICMP probe OK");
		ok, syn_ack_packet = syn_scan(ip, port)
		if ok:
			syn_ack_packet.show()
	else:
		print("ICMP probe failed")
		
					
