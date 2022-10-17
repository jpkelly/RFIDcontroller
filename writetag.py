#! /usr/bin/python3

import mercury

reader = mercury.Reader("llrp://x.x.x.x") # Reader IP address
reader.set_read_plan([1,2,3,4], "GEN2", read_power=1000)

print("Updating RFID tag ID")
print("Connected Ports: " + str(reader.get_connected_ports()))
print("Power Range: " + str(reader.get_power_range()))
print("Antennae: " + str(reader.get_antennas()))
print("Model: " + reader.get_model())
print()

oldTag = input("Enter old tag ID: ")
newTag = input("Enter new tag ID: ")


### WRITE TAG ####
old_epc = oldTag.encode()
new_epc = newTag.encode()


if reader.write(epc_code=new_epc, epc_target=old_epc):
    print('Changed "{}" to "{}"'.format(old_epc, new_epc))
else:
    print('No tag found')

