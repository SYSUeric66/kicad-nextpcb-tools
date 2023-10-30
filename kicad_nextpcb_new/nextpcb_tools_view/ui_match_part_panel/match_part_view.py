import wx
import wx.xrc
import wx.dataview
import os
import csv


from .ui_match_part_panel import UiMatchPartPanel
from kicad_nextpcb_new.button_id import  ID_MANUAL_MATCH, ID_REMOVE_PART, ID_TOGGLE_POS, ID_SAVE_MAPPINGS, ID_EXPORT
from kicad_nextpcb_new.board_manager import load_board_manager
from kicad_nextpcb_new.store import Store


class MatchPartView(UiMatchPartPanel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)
        
        self.BOARD_LOADED = load_board_manager()
        self.project_path = os.path.split(self.BOARD_LOADED.GetFileName())[0]
        self.board_name = os.path.split(self.BOARD_LOADED.GetFileName())[1]
        self.schematic_name = self.board_name.split('.')[0]
        self.store = Store(self, self.project_path, self.BOARD_LOADED)
        self.parts = self.store.read_all()


        self.bom = [{
            'reference':'',
            'value' :'',
            'footprint':'',
            'mpn' :'',
            'manufacturer':'',
            'description':'',
            'bomcheck' :'',
            'poscheck':'',
            'rotation':'',
            'side':''
         }]
        
        self.select_part_button.SetDefault()
        self.select_part_button.SetId(ID_MANUAL_MATCH)
        self.down_toolbar.SetToolLongHelp(
            ID_MANUAL_MATCH,
            "Assign MPN number to a part by manual"
        )

        self.down_toolbar.AddControl(self.select_part_button)
        self.down_toolbar.AddSeparator()
        
        self.remove_part_button.SetDefault()
        self.remove_part_button.SetId(ID_REMOVE_PART)

        self.down_toolbar.AddControl(self.remove_part_button)
        self.down_toolbar.SetFocus()
        self.down_toolbar.AddStretchableSpace()
        self.down_toolbar.Realize()
        self.export_csv.SetId(ID_EXPORT)

        self.Bind(wx.EVT_BUTTON, self.generate_bom, self.export_csv)


    def generate_bom(self,temp_dir):
        '''Generate the bom file.''' 
        temp_dir = self.project_path
        bomFileName = self.schematic_name+'.csv'
        if len(self.bom) > 0:
            with open((os.path.join(temp_dir, bomFileName)), 'w', newline='', encoding='utf-8-sig') as outfile:
                csv_writer = csv.writer(outfile)
                # writing headers of CSV file
                csv_writer.writerow(self.bom[0].keys())

                # Output all of the component information
                for component in self.parts:
                    # writing data of CSV file
                    csv_writer.writerow(component)
                wx.MessageBox(f"outfile:{outfile}", "Help", style=wx.ICON_INFORMATION)



