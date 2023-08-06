# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "27/03/2020"


import logging
import os
import shutil
import tempfile
from silx.gui import qt
from orangecontrib.tomwer.widgets.reconstruction.FtseriesOW import FtseriesOW
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.synctools.ftseries import QReconsParams
from tomwer.test.utils import UtilsTest
from silx.gui.utils.testutils import TestCaseQt
from tomoscan.scanbase import _FOV
import h5py
import gc

logging.disable(logging.INFO)


class TestPyHstWidget(TestCaseQt):
    """class testing the DarkRefWidget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._recons_params = QReconsParams()
        self.widget = FtseriesOW(parent=None, _connect_handler=False)
        self.scan_dir = tempfile.mkdtemp()
        # create dataset
        self.master_file = os.path.join(self.scan_dir, "frm_edftomomill_twoentries.nx")
        shutil.copyfile(
            UtilsTest.getH5Dataset(folderID="frm_edftomomill_twoentries.nx"),
            self.master_file,
        )
        self.scan = HDF5TomoScan(scan=self.master_file, entry="entry0000")

    def tearDown(self):
        self._recons_params = None
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        self.qapp.processEvents()
        gc.collect()
        TestCaseQt.tearDown(self)

    def patch_fov(self, value: str):
        with h5py.File(self.scan.master_file, mode="a") as h5s:
            for entry in ("entry0000", "entry0001"):
                entry_node = h5s[entry]
                if "instrument/detector/field_of_view" in entry_node:
                    del entry_node["instrument/detector/field_of_view"]
                entry_node["instrument/detector/field_of_view"] = value

    def testSetConfiguration(self):
        """Make sure the configuration evolve from scan information"""
        axis_widget = self.widget._ftserie._recParamSetEditor._axisWidget
        self.assertFalse(axis_widget._qcbHalfAcq.isChecked())
        self.patch_fov(value=_FOV.HALF.value)
        self.widget._ftserie.setScan(self.scan)
        self.qapp.processEvents()
        self.assertTrue(axis_widget._qcbHalfAcq.isChecked())

        self.patch_fov(value=_FOV.FULL.value)
        self.scan.clear_caches()
        self.qapp.processEvents()
        self.widget._ftserie.setScan(self.scan)
        self.qapp.processEvents()
        self.assertFalse(axis_widget._qcbHalfAcq.isChecked())
