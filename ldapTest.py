from ldap3 import Server, Connection, AUTO_BIND_TLS_AFTER_BIND, SUBTREE, ALL_ATTRIBUTES, ALL, BASE
import sys
import argparse

server = "ldapad.nih.gov"
port = 389
user = 'nih\\BTRIS_Admin'
password = 'Push@Acurah0me$'
group = "CC-BTRIS Cognos Users"
member = "cooleyma"
searchBase = 'DC=NIH,DC=GOV'


def login(host, port, adminUser, adminPassword):
    """ log into AD as an admin to do things"""

    # define the server using its full active domain name
    server = Server(host, port=port, get_info=ALL) 
    # define the connection & bind using userID being checked
    connection = Connection(server, user=adminUser, password=adminPassword)
    # perform the Bind operation
    if not connection.bind():
        print('error in bind', connection.result)
        connection = None
    return connection


def getLdapInfo(u):
    with Connection(Server(server, port=port, use_ssl=True),
                    auto_bind=AUTO_BIND_TLS_AFTER_BIND,
                    read_only=True,
                    check_names=True,
                    user=user, password=password) as c:
 
        c.search(search_base='CN=Users,DC=NIH,DC=GOV',
                 search_filter='(&(samAccountName=' + u + '))',
                 search_scope=BASE,
                 attributes=ALL_ATTRIBUTES,
                 get_operational_attributes=True)
    print ("In getLdapInfo:")
    print(c.response_to_json())
    print(c.result)
    print ("leaving getLdapInfo")
 

def searchForThing(connection, thing):
    # get the field names for the attributes using the LDAP Admin Tool
    connection.search(search_base = searchBase,
                search_filter =  '(cn={0})'.format(thing),
                search_scope = SUBTREE,
                attributes = ALL_ATTRIBUTES)
    printC(connection)


def showMembers(conn):
    c.search(search_base = searchBase,
             search_filter =  '(cn={0})'.format(group),
             search_scope = SUBTREE,
             attributes = ['member'])
    print ("In showMembers:")
    printC(conn)
    print ("leaving showMembers")


def removeMemberFromGroup(connection, memberName, groupName):
    connection.extend.microsoft.remove_members_from_groups([memberName], [groupName])


def addMemberToGroup(connection, memberName, groupName):
    connection.extend.microsoft.add_members_to_groups([memberName], [groupName])


def printC(c):
    print(c.entries)
    if c.response is not None and len(c.response) > 0:
        if 'attributes' in c.response:
            for k, v in c.response['attributes'].items():
                print ("key: {0}, value: {1}".format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",   help="AD Admin User Name")
    parser.add_argument("-p", "--password",   help="AD Admin Password")
    parser.add_argument("-H", "--host",       help="the hostname/IP of the AD server")
    parser.add_argument("-P", "--port",       help="the port on which AD is listening, defaults to 389")
    parser.add_argument("-m", "--membername", help="member of interest")
    parser.add_argument("-g", "--group",      help="group of interest")
    parser.add_argument("-r", "--remove",     action="store_true", help="remove user from group")
    parser.add_argument("-a", "--add",        action="store_true", help="add user to group")
    parser.add_argument("-s", "--show",       action="store_true", help="displays the user and/or group, overrides add and remove")
    parser.add_argument("-b", "--searchBase", help="Base DC specification")
    args = parser.parse_args()


    if args.username is None or args.password is None or args.host is None or args.searchBase is None:
        print(parser.print_help())
        sys.exit()

    port = args.port
    if port is None:
        port = 389
    else:
        port = int(args.port)

    connection = login(args.host, port, args.username, args.password)
    if connection is None:
        sys.exit()

    if args.show:
        if args.membername is not None:
            searchForThing(connection, args.membername)
            userDn = connection.response[0]['attributes']['distinguishedName']
        if args.group is not None:
            searchForThing(connection, args.group)
            groupDn = connection.response[0]['attributes']['distinguishedName']
    elif args.remove:
        if args.membername is None:
            print("-r, --remove needs a user to remove, express via -m or --membername")
        if args.group is None:
            print("-r, --remove needs a group from which to remove the member, express via -g or --group")
        if args.membername is not None and args.group is not None:
            searchForThing(connection, args.membername)
            userDn = connection.response[0]['attributes']['distinguishedName']
            searchForThing(connection, args.group)
            groupDn = connection.response[0]['attributes']['distinguishedName']
            removeMemberFromGroup(connection, userDn, groupDn)
    elif args.add:
        if args.membername is None:
            print("-a, --add needs a user to add, express via -m or --membername")
        if args.group is None:
            print("-a, --add needs a group to which the member will be added, express via -g or --group")
        if args.membername is not None and args.group is not None:
            searchForThing(connection, args.membername)
            userDn = connection.response[0]['attributes']['distinguishedName']
            searchForThing(connection, args.group)
            groupDn = connection.response[0]['attributes']['distinguishedName']
            addMemberToGroup(connection, userDn, groupDn)


