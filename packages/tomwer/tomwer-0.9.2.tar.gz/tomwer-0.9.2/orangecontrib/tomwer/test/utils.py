# # coding: utf-8
# # /*##########################################################################
# #
# # Copyright (c) 2016-2017 European Synchrotron Radiation Facility
# #
# # Permission is hereby granted, free of charge, to any person obtaining a copy
# # of this software and associated documentation files (the "Software"), to deal
# # in the Software without restriction, including without limitation the rights
# # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# # copies of the Software, and to permit persons to whom the Software is
# # furnished to do so, subject to the following conditions:
# #
# # The above copyright notice and this permission notice shall be included in
# # all copies or substantial portions of the Software.
# #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# # THE SOFTWARE.
# #
# # ###########################################################################*/
#
# __authors__ = ["H. Payno", "Orange"]
# __license__ = "MIT"
# __date__ = "03/03/2017"
#
# """
# Unit test from the Orange canvas main instance
#
# """
# import os
# import sys
# import gc
# import re
# import logging
# import pickle
# import pkg_resources
# from AnyQt.QtGui import QFont
# from AnyQt.QtCore import Qt, QDir
# import AnyQt.importhooks
#
# if AnyQt.USED_API == "pyqt5":
#     # Use a backport shim to fake leftover PyQt4 imports
#     AnyQt.importhooks.install_backport_hook("pyqt4")
#
# from silx.gui.utils.testutils import TestCaseQt
#
# from Orange import canvas
# from tomwer.gui.qtapplicationmanager import QApplicationManager
# from orangecanvas.application.canvasmain import CanvasMainWindow
# from Orange.canvas.config import cache_dir
# from Orange.canvas import config
# from orangecanvas.registry.base import WidgetRegistry
# from orangecanvas.registry import qt
# from orangecanvas.registry import set_global_registry
# from orangecanvas.scheme import SchemeNode, SchemeLink
# from orangecanvas.registry import cache
# from orangecanvas import config as canvasconfig
# from unittest import TestCase
#
# try:
#     import graypy
# except:
#     graypy = None
# else:
#     from tomwer.web import config as configweb
# log = logging.getLogger(__name__)
#
#
# class OrangeWorkflowMixIn:
#     """MixIn class for the orange workflows"""
#
#     def processOrangeEvents(self):
#         self.canvas_window.current_document().scheme().signal_manager.process_queued()
#
#     def processOrangeEventsStack(self):
#         node_update_front = (
#             self.canvas_window.current_document()
#             .scheme()
#             .signal_manager.node_update_front()
#         )
#         if node_update_front:
#             self.processOrangeEvents()
#             self.processOrangeEventsStack()
#             self.app.processEvents()
#
#     def init(self):
#         # set default application configuration
#         config_ = config.Config()
#         canvasconfig.set_default(config_)
#         self.app = QApplicationManager()
#         config_.init()
#
#         # File handler should always be at least INFO level so we need
#         # the application root level to be at least at INFO.
#
#         rootlogger = logging.getLogger(canvas.__name__)
#
#         if graypy is not None and configweb.grayport_host is not None:
#             # graypy > 1.1
#             if hasattr(graypy, "GELFUDPHandler"):
#                 cls = graypy.GELFUDPHandler
#             else:
#                 cls = graypy.GELFHandler
#             self.graylogHandler = cls(configweb.grayport_host, configweb.grayport_port)
#             rootlogger.addHandler(self.graylogHandler)
#
#         # Standard output stream handler at the requested level
#         stream_hander = logging.StreamHandler()
#         rootlogger.addHandler(stream_hander)
#
#         log.info("Starting 'Orange Canvas' application.")
#         log.debug("Starting CanvasApplicaiton ")
#         # NOTE: config.init() must be called after the QApplication constructor
#
#         file_handler = logging.FileHandler(
#             filename=os.path.join(config.log_dir(), "canvas.log"), mode="w"
#         )
#
#         rootlogger.addHandler(file_handler)
#
#         # intercept any QFileOpenEvent requests until the main window is
#         # fully initialized.
#         # NOTE: The QApplication must have the executable ($0) and filename
#         # arguments passed in argv otherwise the FileOpen events are
#         # triggered for them (this is done by Cocoa, but QApplicaiton filters
#         # them out if passed in argv)
#
#         open_requests = []
#
#         def onrequest(url):
#             log.info("Received an file open request %s", url)
#             open_requests.append(url)
#
#         self.app.fileOpenRequest.connect(onrequest)
#
#         stylesheet = "orange"
#         stylesheet_string = None
#
#         if stylesheet != "none":
#             if os.path.isfile(stylesheet):
#                 with open(stylesheet, "r") as f:
#                     stylesheet_string = f.read()
#             else:
#                 if not os.path.splitext(stylesheet)[1]:
#                     # no extension
#                     stylesheet = os.path.extsep.join([stylesheet, "qss"])
#
#                 pkg_name = canvas.__name__
#                 resource = "styles/" + stylesheet
#
#                 if pkg_resources.resource_exists(pkg_name, resource):
#                     stylesheet_string = pkg_resources.resource_string(
#                         pkg_name, resource
#                     ).decode()
#
#                     base = pkg_resources.resource_filename(pkg_name, "styles")
#
#                     pattern = re.compile(
#                         r"^\s@([a-zA-Z0-9_]+?)\s*:\s*([a-zA-Z0-9_/]+?);\s*$",
#                         flags=re.MULTILINE,
#                     )
#
#                     matches = pattern.findall(stylesheet_string)
#
#                     for prefix, search_path in matches:
#                         QDir.addSearchPath(prefix, os.path.join(base, search_path))
#                         log.info(
#                             "Adding search path %r for prefix, %r", search_path, prefix
#                         )
#
#                     stylesheet_string = pattern.sub("", stylesheet_string)
#
#                 else:
#                     log.info("%r style sheet not found.", stylesheet)
#
#         # Add the default canvas_icons search path
#         dirpath = os.path.abspath(os.path.dirname(canvas.__file__))
#         QDir.addSearchPath("canvas_icons", os.path.join(dirpath, "icons"))
#         self.canvas_window = CanvasMainWindow()
#         self.canvas_window.setWindowIcon(config.application_icon())
#
#         if stylesheet_string is not None:
#             self.canvas_window.setStyleSheet(stylesheet_string)
#
#         reg_cache = None
#         widget_discovery = qt.QtWidgetDiscovery(cached_descriptions=reg_cache)
#
#         widget_registry = qt.QtWidgetRegistry()
#         widget_discovery = config_.widget_discovery(
#             widget_registry, cached_descriptions=reg_cache)
#
#         try:
#             widget_discovery.run(config.widgets_entry_points(False))
#         except:
#             widget_discovery.run(config.widgets_entry_points())
#
#         set_global_registry(widget_registry)
#         self.canvas_window.set_widget_registry(widget_registry)
#         self.canvas_window.show()
#         self.widget_registry = widget_registry
#
#         # Process events to make sure the self.canvas_window layout has
#         # a chance to activate (the welcome dialog is modal and will
#         # block the event queue, plus we need a chance to receive open file
#         # signals when running without a splash screen)
#         self.app.processEvents()
#         log.info("discovery ended")
#         # Tee stdout and stderr into Output dock
#         log.info("End initialization")
#
#     def addWidget(self, widgetID):
#         """Create an instanciation of the widgetID
#
#         :return SchemeNode: the node created
#         """
#         assert type(widgetID) is str
#         assert self.widget_registry.has_widget(widgetID)
#         widget_desc = self.widget_registry.widget(widgetID)
#         myItem = SchemeNode(widget_desc)
#         self.canvas_window.current_document().scheme().add_node(myItem)
#         return myItem
#
#     def removeNode(self, widget):
#         self.canvas_window.current_document().scheme().remove_node(widget)
#
#     def link(self, schemeNode1, outNode1, schemeNode2, inputNode2):
#         """Create a link between the node on the given input and output
#
#         :param SchemeNode schemeNode1: the node emitting the output signal
#         :param outNode1: the output chanel to be linked
#         :param SchemeNode schemeNode2: the node receiving the input signal
#         :param inputNode2: the input chanel to be linked
#         :return: the link created between the two nodes
#         """
#         assert type(schemeNode1) is SchemeNode
#         assert type(schemeNode2) is SchemeNode
#         assert type(outNode1) is str
#         assert type(inputNode2) is str
#         link = SchemeLink(schemeNode1, outNode1, schemeNode2, inputNode2)
#         self.canvas_window.current_document().scheme().add_link(link)
#         return link
#
#     def getWidgetForNode(self, node):
#         """
#
#         :param SchemeNode node: the node for which we want the corresponding
#             widget
#         :return: the widget instanciated for the given node
#         """
#         assert type(node) is SchemeNode
#         return self.canvas_window.current_document().scheme().widget_for_node(node)
#
#     def tearDown(self):
#         signal_manager = self.canvas_window.current_document().scheme().signal_manager
#         self.canvas_window.setAttribute(qt.Qt.WA_DeleteOnClose)
#         self.canvas_window.closeEvent = self.closeEventMonkeyPatch
#         self.canvas_window.close()
#         self.canvas_window = None
#         self.widget_registry = None
#
#         self.app.removePostedEvents(signal_manager)
#         try:
#             del self.canvas_window
#         except AttributeError:
#             pass
#         gc.collect()
#         self.app.flush()
#         self.app.quit()
#
#         self.app = None
#
#     @classmethod
#     def closeEventMonkeyPatch(cls, event):
#         """monkey patch clsoe event to skip modification saving request..."""
#         event.ignore()
#
#
# class OrangeWorflowTest(OrangeWorkflowMixIn, TestCaseQt):
#     """Define a specific TestCase reltive to OrangeWorkflow"""
#
#     @classmethod
#     def setUpClass(cls):
#         TestCaseQt.setUpClass()
#         super(OrangeWorflowTest, cls).setUpClass()
#         super(OrangeWorflowTest, cls).init(cls)
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.app.processEvents()
#         # make sure no events are resting
#         super(OrangeWorflowTest, cls).tearDown(cls)
#         TestCaseQt.tearDownClass()
#
#     def tearDown(self):
#         import time
#
#         while self.app.hasPendingEvents():
#             time.sleep(0.1)
#             self.app.processEvents()
#             self.processOrangeEventsStack()
#             time.sleep(0.1)
#             self.app.processEvents()
#
#         TestCase.tearDown(self)
