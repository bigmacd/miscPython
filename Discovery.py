#!/usr/bin/env python
#
import sys
import argparse
import pdb

from DiscoverTools import ping
from NetworkThings import ip


class DiscoveryController(object):

    def __init__(self, args):
        self.startip = ip(args.startip)
        self.endip = ip(args.endip)
        self.currentip = ip(args.startip)
        self.devices = []


    def next(self):
        if self.currentip < self.endip:
            self.currentip = self.currentip.next()
            return True
        return False


    def run(self):
        while True:
            print "checking ip: %s" % (self.currentip)
            d = Device(self.currentip)
            d.discover()
            if d.pingable:
                self.devices.append(d)
            if not self.next():
                print "done"
                break
            else:
                print "getting another ip from range"
        pdb.set_trace()


class Device(object):
    """

    """
    def __init__(self, ip_address, timeout=1, dns_discovery=False, dhcp_discovery=False):
        self.ip = ip_address
        self.timeout = timeout
        self.dns_discovery = dns_discovery
        self.dhcp_discovery = dhcp_discovery
        self.pingable = False

        # future
        self.nmap_xml_out = ""


    def discover(self):
        self.tryPing()


    def tryPing(self):
        """Does it ping?"""
        self.pingable = ping(self.ip, self.timeout)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--startip", help="the beginning IP address")
    parser.add_argument("--endip", help="the ending IP address")
    args = parser.parse_args()
    dc = DiscoveryController(args)
    dc.run()
