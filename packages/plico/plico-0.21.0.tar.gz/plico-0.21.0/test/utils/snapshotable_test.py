#!/usr/bin/env python
import unittest
import os
import numpy as np
import astropy.io.fits as pyfits
from test.test_helper import TestHelper
from plico.utils.snapshotable import Snapshotable


class SnapshotableTest(unittest.TestCase):
    TEMP_FITS = "./tmp.fits"

    def setUp(self):
        if os.path.exists(self.TEMP_FITS):
            os.remove(self.TEMP_FITS)

    def test_prefix_prepending(self):
        snapshot = {"AB": 1, "CD": 2}
        Snapshotable.prepend("FOO", snapshot)
        self.assertEqual(2, len(list(snapshot.keys())))
        self.assertEqual(1, snapshot["FOO.AB"])
        self.assertEqual(2, snapshot["FOO.CD"])

    def test_prepending_supports_chaining(self):
        snapshot = {"A": 42}
        result = Snapshotable.prepend("FOO", snapshot)
        self.assertEqual(snapshot, result)

    def test_FITSHeader_conversion(self):
        snapshot = {"A": 3, "B": 3.5, "C": False, "D": "urga"}
        hdr = Snapshotable.asFITSHeader(snapshot)
        restoredSnapshot = Snapshotable.fromFITSHeader(hdr)
        self.assertEqual(snapshot, restoredSnapshot)

    def test_skips_FITS_header_value_for_NoneType(self):
        hdr = Snapshotable.asFITSHeader({"A": None})
        self.assertEqual({}, Snapshotable.fromFITSHeader(hdr))

    def _checkSnapshotKeyRestore(self, KEY, VALUE, snapshot):
        hdr = Snapshotable.asFITSHeader(snapshot)
        pyfits.writeto(self.TEMP_FITS, np.array([1]), hdr)
        restoredHdr = pyfits.getheader(self.TEMP_FITS)
        restoredSnapshot = Snapshotable.fromFITSHeader(restoredHdr)
        self.assertEqual(VALUE, restoredSnapshot[KEY])

    def test_longest_uncutted_FITS_card_image(self):
        key = "K" * 59
        value = "V" * 8
        self._checkSnapshotKeyRestore(key, value, {key: value})

    def test_FITS_card_with_max_key_length_and_overlong_value_is_cutted(self):
        key = "K" * 59
        value = "1234567890"
        self._checkSnapshotKeyRestore(key, "12345678", {key: value})

    def test_FITS_card_image_with_overlong_value_is_cutted(self):
        key = "K" * 9
        value = "V" * 200
        self._checkSnapshotKeyRestore(key, value[0:58], {key: value})

    @unittest.skip("Do we understand FITS standard?")
    def test_FITS_card_image_with_max_key_length_and_overlong_stringified_float_value(self):
        key = "K" * 59
        value = 1 / 3.
        self._checkSnapshotKeyRestore(key, value, {key: value})

    def test_remove_items_with_value_None(self):
        d = {'a': 3, 'b': None, 'c': "Ceh"}
        Snapshotable.removeEntriesWithValueNone(d)
        TestHelper.areDictEqual({'a': 3, 'c': "Ceh"}, d)


if __name__ == "__main__":
    unittest.main()
