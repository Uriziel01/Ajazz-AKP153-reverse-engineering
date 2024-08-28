# Q: Wireshark does not capute the data packets
### A:Wireshark USBpcap does not work properly with USB 3.0 devices, use https://hhdsoftware.com/usb-sniffer instead (it has 14 days trial without registration)
# Q: Images sent to the device are rotated or shifted to one side
### A: The original command from Stream Dock software contains some more controll bytes that make the placement and rotation correct, this is yet to be done here
# Q: I have Mirabox (or another no-name clone from Aliexpress) instead of Ajazz device, it is not getting detected
### A: You have to adjust idVendor and idProduct to match your device you can find it in Windows device manager, or in PowerShell using the command
`Get-PnpDevice -PresentOnly -Class HIDClass | Where-Object { $_.InstanceId -match '^USB' } | Format-Table -AutoSize` (then just plug the device in/out and check out what changed).
# Q: Where is the binary to run
### A: There is no binary, it's just a R&D project that may or may not be converted into a working program
