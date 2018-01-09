
import subprocess
import re

def ping(ip, timeout=1000, num=1, pct_pass=100):

    available = False

    if ip.version == 6:
        pinger = "/bin/ping6"
    else:
        pinger = "/bin/ping"

    ping_str = '%s -c%s -W %d %s' % (pinger, num, timeout, ip)

    ping_response = subprocess.Popen(ping_str, shell=True, stdout=subprocess.PIPE).stdout.read()

    if ping_response.find('100% packet loss') == -1:
        for line in ping_response.split('\n'):
            word_l = line.split()
            if len(word_l) > 3 and word_l[0] == 'rtt' and word_l[2] == '=':
                rtt_times = word_l[3].split('/')
                if len(rtt_times) > 2:
                    sample = rtt_times[1]

                    latency = float(sample)/2 #round trip time divided by two.

        match_obj = re.compile("(\d+)% packet loss").search(ping_response)
        if match_obj == None:
            packet_loss = 100
        else:
            try:
                packet_loss = int(match_obj.group(1))
            except IndexError, TypeError:
                packet_loss = 100   #quick escape from unexpected output from ping

        packet_recieved_pct = 100 - packet_loss   #ping returns percent fail, we need percent pass...

        if packet_recieved_pct >= pct_pass:
            available = True
    else:
        available = False  #ALL pings failed - 100% packet loss

    return available

def ping_bulk(ip_list, timeout=1000):

    ip_return = {}
    ipv4_list = []
    ipv6_list = []
    pinger = "/usr/local/sbin/fping -e"
    v6pinger = "/usr/local/sbin/fping6 -e"

    for ip in ip_list:
        if ip.version == 6:
            ipv6_list.append(ip)
        elif ip.version == 4:
            ipv4_list.append(ip)

        ip_return = {}

    for pinger, list in ( (pinger, ipv4_list), (v6pinger, ipv6_list)):
        if list == []:
            continue

        ip_strings = [str(ip) for ip in list]

        ping_str = 'sudo %s %s 2>/dev/null' % (pinger, ' '.join(ip_strings))

        ping_response = subprocess.Popen(ping_str, shell=True, stdout=subprocess.PIPE).stdout.read()

        for line in ping_response.split('\n'):
            available, latency = False, 0
            words = line.split()
            if len(words) >= 3:
                try:
                    ret_ip = ip(words[0])
                except:
                    #print "%s - bad IP" % (words[0])
                    continue #next line.

                if words[2] == 'alive':
                    available, latency = (True, words[3][1:5])

                ip_return[ret_ip] = (available, latency)

    return ip_return

