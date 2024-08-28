import sys
import usb.core
import usb.util
from usb.core import find
import usb.backend.libusb1
import time
import libusb
import libusb_package

# find USB devices for Ajazz AKP153
idVendor=0x300
idProduct=0x1010
dev = libusb_package.find(idVendor=idVendor, idProduct=idProduct)

dev.set_configuration()

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]
ep_out = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

ep_in = usb.util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert ep_out is not None
assert ep_in is not None

print(ep_out)
print(ep_in)

sys.stdout.write('Decimal VendorID=' + str(dev.idVendor) + ' & ProductID=' + str(dev.idProduct) + '\n')
sys.stdout.write('Hexadecimal VendorID=' + hex(dev.idVendor) + ' & ProductID=' + hex(dev.idProduct) + '\n\n')

#Some test code to check if the concept works
action = 'set_screen_brightness'
match action:
    case 'read_key_event':
      payload = bytearray(512)
      states = ep_in.read(size_or_buffer=512, timeout=5000)
      print(states)
      print("PRESSED KEY: {:02x}".format(states[9])) #it is indexed starting from bottom right corner (code 1) to left bottom corner (code 15)
    case 'set_screen_brightness':
        payload = bytearray(512)
        brightness  = 0x64
        payload[0:13] = [0x43, 0x52, 0x54, 0x00, 0x00, 0x4C, 0x49, 0x47,  0x00, 0x00, brightness, 0x00, 0x00]
        ep_out.write(payload)
    case 'set_key_image':
        payload = bytearray(512)
        payload[0:13] = [0x43, 0x52, 0x54, 0x00, 0x00, 0x42, 0x41, 0x54, 0x00, 0x00, 0x19, 0x3f, 0x0d]
        ep_out.write(payload)
        with open("img2.jpg", "rb") as image: #85x85 pixels JPEG
            while 1:
                byte_s = image.read(512)
                if not byte_s:
                    break
                ep_out.write(byte_s)
        
        payload = bytearray(512)
        payload[0:13] = [0x43, 0x52, 0x54, 0x00, 0x00, 0x53, 0x54, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00]
        ep_out.write(payload)
    case  'copied_image_upload':
        payload = bytearray(512)
        payload[0:13] = [0x43, 0x52, 0x54, 0x00, 0x00, 0x42, 0x41, 0x54, 0x00, 0x00, 0x19, 0x3f, 0x0d]
        ep_out.write(payload)
        payload = bytearray.fromhex('ffd8ffe000104a46494600010101006000600000ffdb00430001010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101ffdb00430101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101ffc00011080055005503012200021101031101ffc4001f0000010501010101010100000000000000000102030405060708090a0bffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffc4001f0100030101010101010101010000000000000102030405060708090a0bffc400b51100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a43444546474849')
        ep_out.write(payload)
        payload = bytearray.fromhex('4a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9faffda000c03010002110311003f00f91e8a28affaa03fed6028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a0028a28a00ffd9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        ep_out.write(payload)
        print(payload)
        payload = bytearray(512)
        payload[0:13] = [0x43, 0x52, 0x54, 0x00, 0x00, 0x53, 0x54, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00]
        ep_out.write(payload)


# Some usb packets dumps
#43 52 54 00 00 42 41 54 00 00 08 7C 0D 00 00 00    CRT..BAT...|....  <- sent before image is sent downpipe
#43 52 54 00 00 53 54 50 00 00 00 00 00 00 00 00    CRT..STP........  <- sent after image is sent downpipe
