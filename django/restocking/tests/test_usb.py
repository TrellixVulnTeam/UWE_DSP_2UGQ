import re
import subprocess

from django.test import TestCase
class TestUsb(TestCase):
    def test_list_devices_all(self):
        print 'test_list_devices_all'
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        devices = []
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        for device in devices:
            print device

        self.assertIsNotNone(devices, 'No devices detected.')

    def test_list_devices_readers(self):
        print 'test_list_devices_readers'
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        devices = []
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        readers = []
        for device in devices:
            if device['id'] == '072f:2200':
                readers.append(device)
                print device

        self.assertIsNotNone(readers, 'No readers detected')

    def test_zget_device_identifiers(self):
        print 'test_get_device_identifiers'
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        devices = []
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        readers = []
        for device in devices:
            if device['id'] == '072f:2200':
                readers.append(device['device'])
                print device['device'][-3:]

        self.assertIsNotNone(readers, 'No readers detected')
