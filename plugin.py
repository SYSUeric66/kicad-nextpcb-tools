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
<<<<<<< HEAD
        self.icon_file_name = os.path.join(path, "nextPCB-icon.png")
=======
        self.icon_file_name = os.path.join(path, "jlcpcb-icon.png")
>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937
        self._pcbnew_frame = None

    def Run(self):
        dialog = NextPCBTools(None)
        dialog.Center()
        dialog.Show()


<<<<<<< HEAD


def main():
    plugin =  JLCPCBPlugin()
    plugin.Run()
    plugin.register()

if __name__ == '__main__':
    main()
=======
# def main():
    # JLCPCBPlugin().Run()
    # Plugin().register()

# if __name__ == '__main__':
    # main()
>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937
