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
__date__ = "24/01/2017"

import logging
import shutil
import tempfile
import unittest

from silx.gui import qt

from orangecontrib.tomwer.widgets.visualization.ImageStackViewerOW import (
    ImageStackViewerOW,
)
from tomwer.core.utils.scanutils import MockEDF
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.core.scan.edfscan import EDFTomoScan

logging.disable(logging.INFO)

# TODO: use a QtCase instead
# Makes sure a QApplication exists
_qapp = QApplicationManager()


class TestFilePatterns(unittest.TestCase):
    """Make sure the viewer recognize each possible file pattern"""

    N_ACQUI = 20
    """number of acquisition runned"""

    N_RECONS = 4
    """Number of non Paganin reconstruction"""

    N_PAG_RECONS = 2
    """Number of Paganin reconstructions"""

    @classmethod
    def setUpClass(cls):
        cls.stackViewer = ImageStackViewerOW()
        cls.stackViewer.setAttribute(qt.Qt.WA_DeleteOnClose)

    @classmethod
    def tearDownClass(cls):
        cls.stackViewer.close()
        del cls.stackViewer

    def setUp(self):
        self._folder = tempfile.mkdtemp()
        MockEDF.fastMockAcquisition(self._folder, n_radio=self.N_ACQUI)

    def tearDown(self):
        shutil.rmtree(self._folder)

    def testAcquisition(self):
        """
        Make sure the viewer is able to found and load the acquisition files
        """
        self.stackViewer.addScan(EDFTomoScan(self._folder))

        radioDict = self.stackViewer.viewer._stackImageViewerRadio.images
        self.assertTrue(radioDict.size() == self.N_ACQUI)

    def testReconsNotPag(self):
        """
        Make sure the viewer is able to found and load the reconstruction files
        """
        MockEDF.mockReconstruction(self._folder, nRecons=self.N_RECONS)
        self.stackViewer.addScan(EDFTomoScan(self._folder))

        scanDict = self.stackViewer.viewer._stackImageViewerScan.images
        self.assertTrue(scanDict.size() == self.N_RECONS)

    def testReconsPaganin(self):
        """
        Make sure the viewer is able to found and load the paganin recons files
        """
        MockEDF.mockReconstruction(
            self._folder, nRecons=0, nPagRecons=self.N_PAG_RECONS
        )
        self.stackViewer.addScan(EDFTomoScan(self._folder))

        scanDict = self.stackViewer.viewer._stackImageViewerScan.images
        self.assertTrue(scanDict.size() == self.N_PAG_RECONS)

    def testAllRecons(self):
        """
        Make sure the viewer is able to found and load the paganin and the
        not paganin reconstruction and display both
        """
        MockEDF.mockReconstruction(
            self._folder, nRecons=self.N_RECONS, nPagRecons=self.N_PAG_RECONS
        )
        self.stackViewer.addScan(EDFTomoScan(self._folder))

        scanDict = self.stackViewer.viewer._stackImageViewerScan.images
        self.assertTrue(scanDict.size() == self.N_RECONS + self.N_PAG_RECONS)

    def testReconsVolFile(self):
        """Make sure the viewer is able to detect .vol file"""
        MockEDF.mockReconstruction(
            self._folder, nRecons=self.N_RECONS, nPagRecons=0, volFile=True
        )
        self.stackViewer.addScan(EDFTomoScan(self._folder))
        scanDict = self.stackViewer.viewer._stackImageViewerScan.images
        # we create only one .vol file
        self.assertEqual(scanDict.size(), self.N_RECONS + 1)
