
import os
import socket
import struct
import time
import abc


class ip(object):
    """
    An IP Address
    """

    def __cmp__(self, other):
        """
        Compare an IP Address to myself
        """
        if not isinstance(other, ip):
            raise TypeError("Comparing ip to " +other.__class__.__name__+" is unsupported")
        if self.valid != True:
            raise TypeError("IP on left is an invalid ip" + self.address)
        if other.valid != True:
            raise TypeError("IP on right is an invalid ip" + self.address)
        if other.version != self.version:
            raise TypeError("Can't compare IPv4 to IPv6")

        if self.to_decimal() < other.to_decimal():
            return -1
        if self.to_decimal() == other.to_decimal():
            return 0
        if self.to_decimal() > other.to_decimal():
            return 1

    def __init__(self, ip_address):
        self.address = False
        if isinstance(ip_address, str):
            self.address = ip_address

    def __str__(self):
        return self.address

    @staticmethod
    def is_valid(ip_str):
        try:
            ip(ip_str)
        except:
            return False
        else:
            return True

    def get_valid(self):
        """ property valid """
        if self.address == False:
            return False

        if self.__valid_ipv4() == True:
            return True
        elif self.__valid_ipv6() == True:
            return True
        else:
            return False

    def get_version(self):
        """ property version """
        if self.address == False:
            return 0

        if self.__valid_ipv4() == True:
            return 4
        elif self.__valid_ipv6() == True:
            return 6
        else:
            return 0


    def prev(self, decrement=1):
        return self.next(increment=-decrement)

    def next(self, increment=1):
        dec = self.decimal + increment
        try:
            ret = decimal_to_ip(dec, self.version)
        except:
            raise StopIteration

        return ret

    def __valid_ipv4(self):
        """
        Checks an IPV4 address for validity.
        Returns False for error or True for valid
        """
        # First pass convert address for comparison
        try:
            num = socket.inet_aton(self.address)
        except socket.error:
            return False
        except:
            # The specific socket.error exception does not catch all cases
            return False

        # Second pass convert address int back to an address
        add = socket.inet_ntoa(num)

        # If the second pass address is not equal to the original
        # address this is not valid
        if (add != self.address):
            return False
        else:
            return True

    def __valid_ipv6(self):
        """
        Checks an IPV6 address for validity.
        Returns -1 for error or 0 for valid
        """

        # First pass convert address to a packed string
        try:
            num = socket.inet_pton(socket.AF_INET6, self.address)
        except socket.error:
            return False

        # Second pass convert packed string address to an address
        # We use this as the comparison going forward
        add = socket.inet_ntop(socket.AF_INET6, num)

        # Third pass convert second pass address to packed string
        add_p = socket.inet_pton(socket.AF_INET6, add)

        # Compare first pass to third pass
        if (add_p != num):
            return False
        else:
            return True

    def to_decimal(self):
        """ property decimal """

        if self.version == 4:
            return struct.unpack('!L', socket.inet_aton(self.address))[0]
        elif self.version == 6:
            items = []
            index = 0
            fill_pos = None

            # Split string into a list, example:
            #   '1080:200C::417A' => ['1080', '200C', '417A'] and fill_pos=2
            # and fill_pos is the position of '::' in the list
            while index < len(self.address):
                text = self.address[index:]
                if text.startswith("::"):
                    fill_pos = len(items)
                    index += 2
                    continue
                pos = text.find(':')
                if pos != -1:
                    items.append(text[:pos])
                    if text[pos:pos+2] == "::":
                        index += pos
                    else:
                        index += pos+1
                else:
                    items.append(text)
                    break

            # Expand fill_pos to fill with '0'
            # ['1','2'] with fill_pos=1 => ['1', '0', '0', '0', '0', '0', '0', '2']
            if fill_pos is not None:
                diff = 8 - len(items)
                items = items[:fill_pos] + ['0']*diff + items[fill_pos:]

            # Here we have a list of 8 strings so convert strings to long integer and return
            value = 0L
            index = 0
            for item in items:
                item = int(item, 16)
                value = (value << 16) + item
                index += 1
            return value

    @staticmethod
    def from_hexip(hexip, logger, printable=False):
        """
        Find the IP address of the neighbor, which is binary encoded hex data.
        This method can throw an IPAddressError if the IP to be converted is
        not a valid IP address.
        """

        # Step 1. Convert to hex octets
        if printable:
            printable_hexip = hexip
        #else:
        #    printable_hexip = HexString(hexip).makeprintable()

        hexlist = printable_hexip.split()

        # Step 2. Convert to IP string
        # can raise ValueError
        ip_addr = ".".join([str(int('0x%s' % (octet,), 16)) for octet in hexlist])

        # Step 3. Convert to IP object
        ip_obj = ip(ip_addr)

        return ip_obj

    version = property(get_version)
    valid = property(get_valid)
    decimal = property(to_decimal)


def decimal_ip(ip_int, version=4):
    """ Wrap decimal_to_ip assuming version 4 """
    return decimal_to_ip(ip_int, version)

def decimal_to_ip(ip_int, version):
    """ Transform an integer into an IP address. """
    ip_string = ''
    try:
        ip_int = long(ip_int)
    except (ValueError, TypeError):
        raise TypeError, "decimal argument must be a number: %s" % (ip_int)

    if ip_int < 0:
        raise TypeError, "IPs can't be negative: %d" % (ip_int)

    if version == 4:
        if ip_int > 0xffffffffL:
            raise TypeError, "IPv4 Addresses can't be larger than 0xffffffff %s" % (hex(ip_int))
        for l in range(4):
            ip_string = str(ip_int & 0xffL) + '.' + ip_string
            ip_int = ip_int >> 8

        ip_string = ip_string[:-1]

    elif version == 6:
        if ip_int > 0xffffffffffffffffffffffffffffffffL:
            raise TypeError, "IPv6 Addresses can't be larger than 0xffffffffffffffffffffffffffffffff: %s" % (hex(ip_int))
        l = '0' * 32 + hex(ip_int)[2:-1]
        for x in range(1, 33):
            ip_string = l[-x] + ip_string
            if x % 4 == 0:
                ip_string = ':' + ip_string
        ip_string = ip_string[1:]
    else:
        raise TypeError, "only IPv4 and IPv6 supported"

    return ip(ip_string)


def get_net_addr(ipaddr, subnet):
    """ Retrun the network address given an ip and subnet mask. Returns False on error."""

    if not isinstance(ipaddr, ip) and isinstance(ipaddr, str):
        try:
            ipaddr = ip(ipaddr)
        except:
            return False

    if not isinstance(subnet, ip) and isinstance(subnet, str):
        try:
            subnet = ip(subnet)
        except:
            return False

    try:
        return decimal_ip(ipaddr.to_decimal() & subnet.to_decimal())
    except:
        return False


def resolve_hostname(hostname):

    try:
        return socket.gethostbyname(hostname)
    except:
        return None
