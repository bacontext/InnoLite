import os
import usb.core

usbip_server = "10.0.4.1"


def normalize(value):
    norm_value = value / 4.096
    return int(norm_value)


# The main function
def main():

    print("Testing Phidget InterfaceKit 2-2-2")
    os.environ["USBIP_SERVER"] = usbip_server

    # Find the device you want to work with
    device = usb.core.find(address=int("0022bdcf5b40", 16))  # Find using mac address
    device2 = usb.core.find(address=int("0022bdcf5d40", 16))
    #device = usb.core.find(idVendor=0x06c2, idProduct=0x0036)  # Find using USB Vendor/Product

    if device is None:
        raise ValueError('Device not found')

    # Get the endpoint value of the device
    endpoint = device[0][(0,0)][0]
    # Get the endpoint value of the device2
    endpoint2 = device2[0][(0,0)][0]

    # USB configuration initialization
    device.set_configuration()
    device2.set_configuration()
    print(usb.util.get_string(device, 256, 1))
    print(usb.util.get_string(device, 256, 2))
    print(usb.util.get_string(device, 256, 3))
    device.ctrl_transfer(0x21,0x9,0x200,0x0, [0, 0x77,0x01]) #turn off
    print(usb.util.get_string(device2, 256, 1))
    print(usb.util.get_string(device2, 256, 2))
    print(usb.util.get_string(device2, 256, 3))
    personcount = 0;
    amton = 0
    amtoff = 0

    while True:
        data = device.read(1, endpoint.wMaxPacketSize)
        data0 = (data[0x0b] | ((data[0x0c] & 0xf0) << 4))
        data1 = (data[0x0d] | ((data[0x0c] & 0x0f) << 8))

        data = device2.read(1, endpoint2.wMaxPacketSize)
        data2 = (data[0x0b] | ((data[0x0c] & 0xf0) << 4))
        data3 = (data[0x0d] | ((data[0x0c] & 0x0f) << 8))

        if (normalize(data1) > 100): #sound
            personcount = 20
            device.ctrl_transfer(0x21,0x9,0x200,0x0, [1, 0x77,0x01]) #turn on

        if (normalize(data0) > 200): #pressure
            personcount = 20
            device.ctrl_transfer(0x21,0x9,0x200,0x0, [1, 0x77,0x01]) #turn on

        if (normalize(data3) > 50): #distance
            personcount = 20
            device.ctrl_transfer(0x21,0x9,0x200,0x0, [1, 0x77,0x01]) #turn on

        if (personcount == 0):
            device.ctrl_transfer(0x21,0x9,0x200,0x0, [0, 0x77,0x01]) #turn off
            amtoff = amtoff + 1
        else:
            personcount = personcount - 1
            amton = amton + 1
        # Print out the normalized data
        print (normalize(data0), normalize(data1), normalize(data2), normalize(data3), personcount, round((float(amton)/(amton+amtoff)*100),2) )


if __name__ == "__main__":
    main()