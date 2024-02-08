import ezdxf
import os

filelist = [['Half-Moon, Bot.dxf','Half-Moon, Bot (R2000).dxf'], ['Half-Moon, Top.dxf','Half-Moon, Top (R2000).dxf'],]  # input and output file pairs
entitylist = []  # will get filled with unique entities

for file in filelist:
    unique  = 0
    duplicate = 0
    nonzero = 0
    print('\n\nReading: ' + file[0])
    doc = ezdxf.readfile(file[0])
    msp = doc.modelspace()
    before = len(msp)
    for e in msp:
        if e.dxftype() == "LINE":
            s = str(e.dxf.start) + ' ' + str(e.dxf.end) + ' ' + e.dxftype()
            z0 = e.dxf.start[2]
            z1 = e.dxf.end[2]
            if z0 < -0.0000001 or z0 > 0.0000001 or z1 < -0.0000001 or z1 > 0.0000001:
                print('   Z ' + s)
                nonzero = nonzero + 1
                e.destroy() # msp.delete_entity(e)
            elif s in entitylist:
                print('   D ' + s)
                duplicate = duplicate + 1
                e.destroy() # msp.delete_entity(e)
            else:
                print(s)
                entitylist.append(s)
                unique = unique + 1
        elif e.dxftype() == "ARC":
            s = str(e.dxf.center) + ' ' + str(e.dxf.radius) + ' ' + e.dxftype()
            z0 = e.dxf.center[2]
            if z0 < -0.0000001 or z0 > 0.0000001:
                print('   Z ' + s)
                nonzero = nonzero + 1
                e.destroy() # msp.delete_entity(e)
            elif s in entitylist:
                print('   D ' + s)
                duplicate = duplicate + 1
                e.destroy() # msp.delete_entity(e)
            else:
                print(s)
                entitylist.append(s)
                unique = unique + 1
    # r12export.saveas(doc, file[1])
    # odafc.saveas(file[1])
    doc.saveas(file[1])  # could not get the other options to work
    del msp
    del doc

    print('Reading: ' + file[1])
    doc = ezdxf.readfile(file[1])
    msp = doc.modelspace()
    after = len(msp)

    print('   Non-zero Z value: ' + str(nonzero))
    print('   Unique entities: ' + str(unique))
    print('   Duplicate entities: ' + str(duplicate))
    print('   Before and After: ' + str(before) + ' -> ' + str(after))

    del msp
    del doc

print()
print()
os.system('PAUSE')
#EOF
