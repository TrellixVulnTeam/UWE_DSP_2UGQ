import nfc, time

clf = nfc.ContactlessFrontend()
device_path = 'usb:003:' + '009'
print device_path

assert clf.open(device_path) is True

after1s = lambda: time.time() - current_time > 1
current_time = time.time(); tag = clf.connect(rdwr={'on-connect': lambda tag: False}, terminate=after1s)

if tag is not None:
    product_id = tag.ndef.records[0].text
    clf.close()
else:
    clf.close()
