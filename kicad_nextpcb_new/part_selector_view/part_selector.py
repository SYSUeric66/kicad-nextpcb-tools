import logging

import wx
import requests
import threading
import json
import wx.dataview
from kicad_nextpcb_new.events import AssignPartsEvent, UpdateSetting
from kicad_nextpcb_new.helpers import HighResWxSize, loadBitmapScaled
from requests.exceptions import Timeout
from .ui_part_details_panel.part_details_view import PartDetailsView
from .ui_search_panel.search_view import SearchView
from .ui_part_list_panel.part_list_view import PartListView
from kicad_nextpcb_new.library import Library

ID_SELECT_PART = wx.NewIdRef()

def ceil(x, y):
    return -(-x // y)

class PartSelectorDialog(wx.Dialog):
    def __init__(self, parent, parts):
        wx.SizerFlags.DisableConsistencyChecks()
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="NextPCB Search Online",
            pos=wx.DefaultPosition,
            size=HighResWxSize(parent.window, wx.Size(1200, 800)),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )
        self.library = Library(self)

        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.parts = parts
        self.MPN_stockID_dict = {}

        self.current_page = 0
        self.total_pages = 0

        part_selection = self.get_existing_selection(parts)
        self.part_info = part_selection.split(",")

        self.part_details_view = PartDetailsView(self)
        self.search_view = SearchView(self)
        self.part_list_view = PartListView(self)
        # ---------------------------------------------------------------------
        # ---------------------------- Hotkeys --------------------------------
        # ---------------------------------------------------------------------
        quitid = wx.NewId()
        self.Bind(wx.EVT_MENU, self.quit_dialog, id=quitid)

        entries = [wx.AcceleratorEntry(), wx.AcceleratorEntry(), wx.AcceleratorEntry()]
        entries[0].Set(wx.ACCEL_CTRL, ord("W"), quitid)
        entries[1].Set(wx.ACCEL_CTRL, ord("Q"), quitid)
        entries[2].Set(wx.ACCEL_SHIFT, wx.WXK_ESCAPE, quitid)
        accel = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(accel)

        # ---------------------------------------------------------------------
        # ---------------------------- bind events ----------------------------
        # ---------------------------------------------------------------------
        self.search_view.description.SetValue(self.part_info[2])
        self.search_view.description.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.search)
        self.search_view.mpn_textctrl.Bind(wx.EVT_TEXT_ENTER, self.search)
        self.search_view.manufacturer.Bind(wx.EVT_TEXT_ENTER, self.search)
        self.search_view.search_button.Bind(wx.EVT_BUTTON, self.search)

        self.part_list_view.part_list.Bind(wx.dataview.EVT_DATAVIEW_COLUMN_HEADER_CLICK, self.OnSortPartList)
        self.part_list_view.part_list.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_part_selected)
        self.part_list_view.part_list.Bind(wx.dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.on_right_down)


        self.part_list_view.prev_button.Bind(wx.EVT_BUTTON, self.on_prev_page)
        self.part_list_view.next_button.Bind(wx.EVT_BUTTON, self.on_next_page)
        self.update_page_label()

        self.part_list_view.select_part_button.Bind(wx.EVT_BUTTON, self.select_part)
        self.part_list_view.select_part_button.SetBitmap(
            loadBitmapScaled(
                "nextpcb-select-part.png",
                # self.parent.scale_factor,
            )
        )

        self.enable_toolbar_buttons(False)
        # ---------------------------------------------------------------------
        # ------------------------------ layout  ------------------------------
        # ---------------------------------------------------------------------
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        bSizer2.Add(self.search_view, 0,  wx.EXPAND, 5)
        bSizer2.Add(self.part_list_view, 1, wx.LEFT | wx.EXPAND, 5)

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer1.Add( bSizer2, 15, wx.EXPAND |wx.ALL, 5 )
        bSizer1.Add( self.part_details_view, 7, wx.EXPAND |wx.ALL, 0 )
        
        layout = wx.BoxSizer(wx.VERTICAL)
          
        layout.Add( bSizer1, 1, wx.EXPAND, 5 )
        
        self.SetSizer(layout)
        self.Layout()
        self.Centre(wx.BOTH)
        


    def upadate_settings(self, event):
        """Update the settings on change"""
        wx.PostEvent(
            self.parent,
            UpdateSetting(
                section="partselector",
                setting=event.GetEventObject().GetName(),
                value=event.GetEventObject().GetValue(),
            ),
        )

    @staticmethod
    def get_existing_selection(parts):
        """Check if exactly one LCSC part number is amongst the selected parts."""
        s = set(val for val in parts.values())
        return list(s)[0]

    def quit_dialog(self, e):
        self.Destroy()
        self.EndModal(0)

    def OnSortPartList(self, e):
        """Set order_by to the clicked column and trigger list refresh."""
        self.library.set_order_by(e.GetColumn())
        self.search(None)

    def enable_toolbar_buttons(self, state):
        """Control the state of all the buttons in toolbar on the right side"""
        for b in [
            self.part_list_view.select_part_button,
        ]:
            b.Enable(bool(state))

    def search(self, e):
        """Search the library for parts that meet the search criteria."""
        if self.current_page == 0:
            self.current_page = 1 
        if self.search_view.mpn_textctrl.GetValue()=="":
            mpn = None
        else:
            mpn = self.search_view.mpn_textctrl.GetValue()    
        if self.search_view.manufacturer.GetValue()=="":
            mfg = None
        else:
            mfg = self.search_view.manufacturer.GetValue()
        if self.search_view.description.GetValue()=="":
            comment = None
        else:
            comment = self.search_view.description.GetValue()
        body = {'material': [ 
                     mpn,                       # (1)mpn,
                     mfg,                       # (2)mfg,
                     None,                      # (3)package/footprint,
                     None,                      # (4)ref,
                     None,                      # (5)quantity,
                     comment                    # (6)comment
                     ]}
        
        url = "http://192.168.50.100:5010/material_analyze"
        self.search_view.search_button.Disable()
        try:
            threading.Thread(target=self.search_api_request(url, body)).start()
        finally:
            self.search_view.search_button.Enable()

    def search_api_request(self, url, data):
        wx.CallAfter(wx.BeginBusyCursor)

        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=5
            )
            print("json")
            print(json)
        except Timeout:
            
            self.report_part_search_error("HTTP response timeout")

        if response.status_code != 200:
            self.report_part_search_error(f"non-OK HTTP response status：{response.status_code}")
            return
        self.search_part_list = []
        data = response.json()
        self.total_num = len(data)
        if self.total_num == 0:
            self.current_page = 0 
        for item in data:
            if not item.get("_source", {}):
                self.report_part_search_error(
                    "returned JSON data does not have expected '_source' attribute"
                )
            search_part = item.get("_source", {})
            self.search_part_list.append(search_part)
        
        wx.CallAfter(self.populate_part_list)
        wx.CallAfter(wx.EndBusyCursor)
        

    def populate_part_list(self):
        """Populate the list with the result of the search."""
        self.part_list_view.part_list.DeleteAllItems()
        if self.search_part_list is None:
            return
        self.total_pages = ceil(self.total_num, 100)
        self.update_page_label()
        self.part_list_view.result_count.SetLabel(f"{self.total_num} Results")
        if self.total_num >= 1000:
            self.part_list_view.result_count.SetLabel("1000 Results (limited)")
        else:
            self.part_list_view.result_count.SetLabel(f"{self.total_num} Results")

        parameters = [
            "mpn",
            "mfg",
            "description",
            "package",
            "stockNumber"
        ] 
        self.item_list = []
        for idx, part_info in enumerate(self.search_part_list, start=1):
            part = []
            for k in parameters:
                val = part_info.get(k, "")
                val = "-" if val == "" else val
                part.append(val)
            
        
            pricelist = part_info.get("priceStair", [])
            if pricelist:
                stair_num = len(pricelist)
                min_price = (pricelist[stair_num - 1]).get("hkPrice", 0)
            else:
                min_price = 0            

            pricelist = part_info.get("priceStair", [])
            if pricelist:
                stair_num = len(pricelist)
                min_price = (pricelist[stair_num - 1]).get("hkPrice", 0)
            else:
                min_price = 0
            part.insert(4, str(min_price))
            suppliername = part_info.get("supplierName", "")
            suppliername = "-" if suppliername == "" else suppliername
            part.insert(6, suppliername)
            part.insert(0, f'{idx}')
            self.part_list_view.part_list.AppendItem(part)



    def select_part(self, e):
        """Save the selected part number and close the modal."""
        item = self.part_list_view.part_list.GetSelection()
        row = self.part_list_view.part_list.ItemToRow(item)
        if row == -1:
            return
        selection = self.part_list_view.part_list.GetValue(row, 1)
        manu = self.part_list_view.part_list.GetValue(row, 2)
        des = self.part_list_view.part_list.GetValue(row, 3)
        self.selected_part = self.search_part_list[row]
        evt = AssignPartsEvent(
            mpn=selection,
            manufacturer=manu,
            description=des,
            references=list(self.parts.keys()),
            selected_part_detail = self.selected_part
        )
        wx.PostEvent(
            self.parent,
            evt
        )
        self.EndModal(wx.ID_OK)



    def on_part_selected(self, e):
        """Enable the toolbar buttons when a selection was made."""
        if self.part_list_view.part_list.GetSelectedItemsCount() > 0:
            self.enable_toolbar_buttons(True)
        else:
            self.enable_toolbar_buttons(False)
        
        item = self.part_list_view.part_list.GetSelection()
        row = self.part_list_view.part_list.ItemToRow(item)
        if row == -1:
            return
        self.clicked_part = self.search_part_list[row]
        if self.clicked_part != "":
            try:
                wx.BeginBusyCursor()
                self.part_details_view.get_part_data(self.clicked_part)
            finally:
                 wx.EndBusyCursor()
        else:
            wx.MessageBox(
                "Failed to get clicked part from NextPCB\r\n",
                "Error",
                style=wx.ICON_ERROR,
            )

    def on_prev_page(self,event):
        self.FindWindowByLabel('0').Destroy()

        if self.current_page > 1:
            self.current_page -= 1
            self.search(None)
            self.update_page_label()

    def on_next_page(self, event):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.search(None)
            self.update_page_label()        


    def update_page_label(self):
        self.part_list_view.page_label.SetLabel(f"{self.current_page}/{self.total_pages}")


    def help(self, e):
        """Show message box with help instructions"""
        title = "Help"
        text = """
        Use % as wildcard selector. \n
        For example DS24% will match DS2411\n
        %QFP% wil match LQFP-64 as well as TQFP-32\n
        The keyword search box is automatically post- and prefixed with wildcard operators.
        The others are not by default.\n
        The keyword search field is applied to "LCSC Part", "Description", "MFR.Part",
        "Package" and "Manufacturer".\n
        Enter triggers the search the same way the search button does.\n
        The results are limited to 1000.
        """
        wx.MessageBox(text, title, style=wx.ICON_INFORMATION)

    def report_part_search_error(self, reason):
        wx.MessageBox(
            f"Failed to download part detail from the NextPCB API ({reason})\r\n",
            "Error",
            style=wx.ICON_ERROR,
        )
        wx.CallAfter(wx.EndBusyCursor)
        wx.CallAfter(self.search_view.search_button.Enable())
        return
    
    
    def on_right_down(self, e):
        conMenu = wx.Menu()
        selcet_part = wx.MenuItem(conMenu,  ID_SELECT_PART , "Select Part")
        conMenu.Append(selcet_part)
        conMenu.Bind(wx.EVT_MENU, self.select_part, selcet_part)
        item = self.part_list_view.part_list.GetSelection()
        row = self.part_list_view.part_list.ItemToRow(item)
        if row == -1:
            return
        conMenu.Enable(ID_SELECT_PART, True)
        self.part_list_view.part_list.PopupMenu(conMenu)
        conMenu.Destroy()
    