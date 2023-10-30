import wx
import sys
from wx.lib.mixins.inspection import InspectionMixin
from kicad_nextpcb_new.mainwindow import NextPCBTools


def _main():    
    app = BaseApp()
    app.MainLoop()


def _displayHook(obj):
    if obj is not None:
        print(repr(obj))

class BaseApp(wx.App, InspectionMixin):
    def __init__(
        self, 
    ):
         super().__init__()

    def OnInit(self):
        self.Init()  # InspectionMixin
        # work around for Python stealing "_"
        sys.displayhook = _displayHook
        self.locale = None
        self.startup_dialog()
        return True

    def startup_dialog(self):
        self.w = NextPCBTools(None)
        self.w.Show()
