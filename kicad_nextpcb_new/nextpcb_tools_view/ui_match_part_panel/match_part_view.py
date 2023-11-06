import wx
import wx.xrc
import wx.dataview
import os
import csv


from .ui_match_part_panel import UiMatchPartPanel
from kicad_nextpcb_new.button_id import  ID_MANUAL_MATCH, ID_REMOVE_PART, ID_EXPORT
from kicad_nextpcb_new.store import Store
from kicad_nextpcb_new.events import EVT_EXPORT_CSV

class MatchPartView(UiMatchPartPanel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        self.bom = [{
            'reference':'',
            'value' :'',
            'footprint':'',
            'mpn' :'',
            'manufacturer':'',
            'description':'',
            'quantity' :'',
            'bomcheck' :'',
            'poscheck':'',
            'rotation':'',
            'side':''
         }]
        
        self.select_part_button.SetDefault()
        self.select_part_button.SetId(ID_MANUAL_MATCH)
        self.remove_part_button.SetDefault()
        self.remove_part_button.SetId(ID_REMOVE_PART)

        self.export_csv.SetId(ID_EXPORT)
        self.Bind(wx.EVT_BUTTON, self.generate_bom, self.export_csv)
        self.Bind(EVT_EXPORT_CSV, self.generate_bom)

    def generate_bom(self,evt):
        '''Generate the bom file.''' 
        self.BOARD_LOADED = evt.BOARD_LOADED
        self.project_path = evt.project_path 
        self.schematic_name = evt.board_name.split('.')[0]

        self.store = Store(self, self.project_path, self.BOARD_LOADED)
        self.parts = self.store.read_all()
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



