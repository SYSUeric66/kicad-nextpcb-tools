import os
from pcbnew import ActionPlugin

from .mainwindow import NextPCBTools


class JLCPCBPlugin(ActionPlugin):
    def defaults(self):
        self.name = "JLCPCB Tools"
        self.category = "Fabrication data generation"
        self.description = (
            "Generate JLCPCB-compatible Gerber, Excellon, BOM and CPL files"
        )
        self.show_toolbar_button = True
        path, filename = os.path.split(os.path.abspath(__file__))
        self.icon_file_name = os.path.join(path, "nextPCB-icon.png")
        self._pcbnew_frame = None

    def Run(self):
        dialog = NextPCBTools(None)
        dialog.Center()
        dialog.Show()




def main():
    plugin =  JLCPCBPlugin()
    plugin.Run()
    plugin.register()

if __name__ == '__main__':
    main()