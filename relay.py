#!/usr/bin/python3
#
# SYNOPSIS
#   sr-201-relay.py relay-hostname [command...]
#
#
# DESCRIPTION
#
#   Configures and controls a SR-201 Ethernet relay.  If no commands are given
#   'config' is assumed.  If you don't supply relay-hostname a short help
#   message will be issued listing the available commands.
#
# BUGS
#
#   Although this program can be used to issue control commands to the relay
#   I recommend doing it directly instead.  It will be be faster, more
#   reliable, and the task is so simple the code will be shorter.  The
#   primary purpose of this code is to document how to do it, with a working
#   example.
#
#
# THE DEVICE: Factory Defaults
#
#    Default IP Address:        192.168.1.100
#    Port 6722:                 TCP control
#    Port 6723:                 UDP control
#    Port 5111:                 TCP Configuration
#
#    The device can be reset to these defaults by shorting the CLR pins
#    on the header next to the RJ45 connector.  CLR is adjacent to the +5V
#    and P30 pins.
#
# THE DEVICE: Commands that can be sent over the TCP and UDP control ports
#
#    Commands are ASCII strings that must be sent in one packet
#    (even for TCP):
#
#        0R     No operation (but return status).
#
#        1R*    Close relay if it's open, wait approx 1/2 a second, open
#               relay.
#
#        1R     Close relay if it's open.
#
#        1R:0   Close relay if it's open.
#
#        1R:n   Close relay if it's open, then in n seconds (1 <= n <= 65535)
#               open it.
#
#        2R     Open relay if it's closed.
#
#    Where:
#
#        R      is the relay number, '1' .. '8'.  The main board has relay's
#               '1' and '2', the extension board (if present) has the rest.
#               If R is 'X' all relays are effected.
#
#    If the command is sent over TCP (not UDP, TCP only), the relay will
#    reply with a string of 8 0's and 1's, representing the "before" command
#    was executed" state of relay's 1..8 in that order.  A '0' is sent if the
#    relay is open, '1' if closed.
#
#
# THE DEVICE: TCP Configuration
#
#    Commands are ASCII strings that must be sent in one TCP packet.  'i'
#    is a random number in the range '1000' .. '9999':
#
#    #1i;       Query State.  Response is a comma separated list of fields
#               terminated by a semicolon (';').  Example response:
#
#                 >192.168.1.100,255.255.255.0,192.168.1.1,,0,435,F44900F6087457000000,192.168.1.1,connect.tutuuu.com,0;
#
#               Fields in order of appearance are:
#
#               ID  Value in example     Description
#               --  -------------------- ---------------------------------
#                2  192.168.1.100        Devices IP Address.
#                3  255.255.255.0        Devices subnet mask.
#                4  192.168.1.1          Gateway.
#                5                       Unknown.
#                6  0                    '1'=Save relay state across poweroff.
#                7  435                  Software version is 1.0.435 / reset.
#               na  F44900F6087457000000 Device serial number.
#                8  192.168.1.1          DNS Server to look up cloud service.
#                9  connect.tutuuu.com   Cloud service.
#                A  0                    Cloud service enabled if = '1'.
#
#
#    #Di,F;    Set the state whose ID is 'D' to value 'F'.  For example:
#
#                #61234,1;      Persist relay state across power cycle.
#                #71234;        Reset the device so changes take effect.
#
#              ID 'B' sets the cloud service password.
#
#
# THE DEVICE: Cloud operation
#
#   If cloud operation is enabled (by setting ID "A" to "1"), the device sends
#   a HTTP "POST" request every second or so to server stipulated in setting
#   ID "9".  The request is:
#
#      POST /SyncServiceImpl.svc/ReportStatus HTTP/1.1
#      User-Agent: SR-201W/M96Y
#      Content-Type: application/json
#      Host: 192.168.1.1
#      Content-Length: 30
#
#      "F0123456789ABCXXXXXX00000000"
#
#   The post body contains the following fields:
#
#       F0123456789ABCXXXXXX00000000
#       \------------/\----/\------/
#             |         |      |
#             |         |      +---- State of relays 1..8, 0=open, 1=closed.
#             |         +----------- Password.
#             +--------------------- Serial number.
#
#   The response must have the Content-Length header set, and the body must
#   be a singe application/json string starting with "A" optionally followed
#   by a single relay control command, eg:
#
#      HTTP/1.1 200 OK
#      Content-Type: application/json
#      Content-Length: 7
#
#      "A11:2"
#
#
# Home page: https://sr-201-relay.sourceforge.net/
#
# Author: Russell Stuart, russell-debian@stuart.id.au
#
