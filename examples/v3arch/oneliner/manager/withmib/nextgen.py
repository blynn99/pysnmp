# GETNEXT Commnd Generator with MIB resolution
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.entity.rfc3413 import mibvar

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, \
                 varBindTable = cmdGen.nextCmd(
    # SNMP v1
#    cmdgen.CommunityData('public', mpModel=0),
    # SNMP v2
#    cmdgen.CommunityData('public'),
    # SNMP v3
    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    # Transport
    cmdgen.UdpTransportTarget(('localhost', 161)),
    # Request variable(s)
#    (('TCP-MIB', ''),),
    (('SNMPv2-MIB', ''),),
#    (('IF-MIB', ''),),
#    (('', 'interfaces'),),
#    (1,3,6,1,2,1)
#    (('','system'),)
    )

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            varBindTable[-1][int(errorIndex)-1]
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for oid, val in varBindTableRow:
                (symName, modName), indices = mibvar.oidToMibName(
                    cmdGen.mibViewController, oid
                    )
                val = mibvar.cloneFromMibValue(
                    cmdGen.mibViewController, modName, symName, val
                    )
                print('%s::%s.%s = %s' % (
                    modName, symName,
                    '.'.join([ v.prettyPrint() for v in indices]),
                    val.prettyPrint()
                    )
                )
