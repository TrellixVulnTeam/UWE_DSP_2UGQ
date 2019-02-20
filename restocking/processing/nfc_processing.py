import nfc, time
from ndef import TextRecord
import restocking.processing.usb_processing as usb_processing

def nfc_basic_info(device_identifier):
    clf = nfc.ContactlessFrontend()
    device_path = 'usb:003:' + device_identifier
    assert clf.open(str(device_path)) is True

    to_return = clf.__str__()

    clf.close()

    return to_return

def nfc_encode_tag(device_identifier, product_id):
    clf = nfc.ContactlessFrontend()
    device_path = 'usb:003:' + device_identifier
    assert clf.open(str(device_path)) is True

    after1s = lambda: time.time() - current_time > 1
    current_time = time.time(); tag = clf.connect(rdwr={'on-connect': lambda tag: False}, terminate=after1s)

    if tag is not None:
        tag.format()
        tag.ndef.records = [TextRecord(product_id)]
        clf.close()
        return True
    else:
        clf.close()
        return False

def nfc_identify_tag(device_identifier):
    clf = nfc.ContactlessFrontend()
    device_path = 'usb:003:' + device_identifier
    print str(device_path)

    assert clf.open(str(device_path)) is True

    after1s = lambda: time.time() - current_time > 1
    current_time = time.time(); tag = clf.connect(rdwr={'on-connect': lambda tag: False}, terminate=after1s)

    if tag is not None:
        product_id = tag.ndef.records[0].text
        clf.close()
        return product_id
    else:
        clf.close()
        return None

def nfc_find_devices():
    from restocking.models import NfcUnit
    #delete all NFC units first.
    NfcUnit.objects.all().delete()
    readers = usb_processing.get_readers()
    if len(readers) == 0:
        return False
    else:
        for reader in readers:
            nfc_unit = NfcUnit(device_identifier=reader)
            nfc_unit.save()
        return True
