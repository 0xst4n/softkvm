from monitorcontrol import get_monitors
import time, os.path, json, win32com.client
import ctypes

monitors = get_monitors()

def run(display_index, usb_connected_source, usb_disconnected_source, usb_device_id):
    while True:
        all_usb = get_usb_devices()
        if usb_device_id in all_usb:
            with monitors[display_index] as m:
                m.set_input_source(usb_connected_source)
        else:
            with monitors[display_index] as m:
                m.set_input_source(usb_disconnected_source)
        time.sleep(0.5)

def get_usb_devices():
    wmi = win32com.client.GetObject ("winmgmts:")
    all_usb = wmi.InstancesOf("Win32_USBHub")
    all_usb = [x.DeviceId for x in all_usb]
    return all_usb

if os.path.exists('config.json'):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    run(config['monitor'], config['usb_connected_source'], config['usb_disconnected_source'], config['usb_device_id'])
else:
    print("Run setup.exe")



            

