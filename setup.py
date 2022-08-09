from monitorcontrol import get_monitors
import time, os.path, json, win32com.client, os, ctypes, shutil

def get_usb_devices():
    wmi = win32com.client.GetObject ("winmgmts:")
    all_usb = wmi.InstancesOf("Win32_USBHub")
    all_usb = [x.DeviceId for x in all_usb]
    return all_usb

usb_connected_source = input('What should the source be if the USB switch is connected? (DP1, DP2, HDMI1, HDMI2, DVI1, DVI2) ')
usb_disconnected_source = input('What should the source be if the USB switch is disconnected? (DP1, DP2, HDMI1, HDMI2, DVI1, DVI2) ')
input("Enable your USB switch for this device and press enter ")
all_usb_plugged = get_usb_devices()
input("Press enter and disconnect only the USB switch (The script will sleep for 5 seconds so you can disconnect the USB switch) ")
time.sleep(5)
all_usb_unplugged = get_usb_devices()
print("The following devices are related to the USB switch:")

usb_hub_related = []

for x in all_usb_plugged:
    if x not in all_usb_unplugged:
        usb_hub_related.append(x)

print(usb_hub_related)

print(f'Will use the first one: {usb_hub_related[0]}')
usb_device_id = usb_hub_related[0]

time.sleep(3)

print("Now we will test which monitor should be switched")

monitors = get_monitors()
for i in range(0, len(monitors)):
    with monitors[i] as m:
        print(f'Swapping source of monitor {i} and then sleeping for 5 seconds')
        time.sleep(2)
        m.set_input_source(usb_disconnected_source)
        time.sleep(10)
monitor = input("Which monitor do you want to switch? Enter a number: ")

config_dict = {"monitor": int(monitor), "usb_connected_source": usb_connected_source, "usb_disconnected_source": usb_disconnected_source, "usb_device_id": usb_device_id}
with open(f'config.json', 'w', encoding="utf-8") as f:
    json.dump(config_dict, f)

print("Now you can run softkvm.exe or softkvm.py")
print("To start this after logging in, refer to https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10")