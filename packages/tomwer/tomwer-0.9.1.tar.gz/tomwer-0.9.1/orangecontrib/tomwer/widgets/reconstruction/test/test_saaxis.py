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
__date__ = "12/04/2021"

import time

from silx.gui.utils.testutils import TestCaseQt
from silx.gui import qt
from tomwer.core.utils.scanutils import MockHDF5
from orangecontrib.tomwer.widgets.reconstruction.SAAxisOW import SAAxisOW as _SAAxisOW
from tomwer.core.process.reconstruction.scores import ComputedScore
from processview.core.manager import ProcessManager, DatasetState
from silx.io.url import DataUrl
import h5py
import tempfile
import shutil
import logging
import numpy
import uuid
import os
from tomwer.core import utils, settings

logger = logging.getLogger(__name__)


class SAAxisOW(_SAAxisOW):
    def __init__(self, parent=None):
        self._scans_finished = []
        super().__init__(parent)

    def processing_finished(self, scan):
        # TODO: add message processing finished
        self._scans_finished.append(scan)

    @property
    def scans_finished(self):
        return self._scans_finished

    def close(self):
        self._scans_finished = {}
        super().close()


class TestProcessing(TestCaseQt):

    DIM = 100

    def setUp(self):
        super().setUp()
        utils.mockLowMemory(False)
        settings.mock_lsbram(False)
        self._source_dir = tempfile.mkdtemp()

        def create_scan(folder_name):
            _dir = os.path.join(self._source_dir, folder_name)
            return MockHDF5(
                scan_path=_dir,
                n_ini_proj=20,
                n_proj=20,
                n_alignement_proj=2,
                create_final_ref=False,
                create_ini_dark=True,
                create_ini_ref=True,
                n_refs=1,
                dim=self.DIM,
            ).scan

        # create scans
        self.scan_1 = create_scan("scan_1")
        self.scan_2 = create_scan("scan_2")
        self.scan_3 = create_scan("scan_3")
        self._process_manager = ProcessManager()

        self.widget = SAAxisOW()
        self.widget.show()

        def patch_score(*args, **kwargs):
            data = numpy.random.random(TestProcessing.DIM * TestProcessing.DIM)
            data = data.reshape(TestProcessing.DIM, TestProcessing.DIM)
            slice_file_path = os.path.join(
                self._source_dir, str(uuid.uuid1()) + ".hdf5"
            )
            data_url = DataUrl(
                file_path=slice_file_path, data_path="data", scheme="silx"
            )
            with h5py.File(slice_file_path, mode="a") as h5f:
                h5f["data"] = data
            return data_url, ComputedScore(
                tv=numpy.random.random(),
                std=numpy.random.random(),
            )

        self.widget._widget._processing_stack.patch_processing(patch_score)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.stop()
        self.widget.close()
        self.widget = None
        self.qapp.processEvents()
        shutil.rmtree(self._source_dir)
        super().tearDown()

    def testAutoFocusUnlock(self):
        self.widget.lockAutofocus(False)

        def manual_processing():
            self.widget.load_sinogram()
            self.widget.compute()
            self.qapp.processEvents()
            self.widget.wait_processing(5000)
            self.qapp.processEvents()

        self.widget.process(self.scan_1)
        manual_processing()
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_1.get_dataset_identifier(),
                process=self.widget,
            ),
            DatasetState.WAIT_USER_VALIDATION,
        )

        self.widget.process(self.scan_2)
        manual_processing()
        self.assertEqual(len(self.widget.scans_finished), 0)
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_1.get_dataset_identifier(),
                process=self.widget,
            ),
            DatasetState.SKIPPED,
        )
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_2.get_dataset_identifier(),
                process=self.widget,
            ),
            DatasetState.WAIT_USER_VALIDATION,
        )
        self.widget.process(self.scan_3)
        manual_processing()
        self.widget.validateCurrentScan()
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_3.get_dataset_identifier(),
                process=self.widget,
            ),
            DatasetState.SUCCEED,
        )
        # insure a cor has been registered
        self.assertNotEqual(self.scan_3.axis_params.relative_cor_value, None)

    def testTestLbsram(self):
        utils.mockLowMemory(True)
        settings.mock_lsbram(True)
        for scan in (self.scan_1, self.scan_2, self.scan_3):
            self.widget.process(scan)
            self.widget.wait_processing(5000)
            self.qapp.processEvents()

        for scan in (self.scan_1, self.scan_2, self.scan_3):
            with self.subTest(scan=str(scan)):
                self.assertEqual(
                    self._process_manager.get_dataset_state(
                        dataset_id=scan.get_dataset_identifier(),
                        process=self.widget,
                    ),
                    DatasetState.SKIPPED,
                )

    def testAutoFocusLock(self):
        self.widget.lockAutofocus(True)
        for scan in (self.scan_1, self.scan_2, self.scan_3):
            self.widget.process(scan)
            self.widget.wait_processing(10000)
            self.qapp.processEvents()
            time.sleep(0.1)
            self.qapp.processEvents()
            self.assertEqual(
                self._process_manager.get_dataset_state(
                    dataset_id=scan.get_dataset_identifier(),
                    process=self.widget,
                ),
                DatasetState.SUCCEED,
            )
