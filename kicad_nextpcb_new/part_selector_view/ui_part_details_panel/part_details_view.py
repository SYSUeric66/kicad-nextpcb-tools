import wx
import wx.xrc
import wx.dataview
import requests
import webbrowser
import io
import json

from .ui_part_details_panel import UiPartDetailsPanel
import wx.dataview as dv


parameters = {
    "mpn": "MPN",
    "mfg": "Manufacturer",
    "description": "Description",
    "package": "Package / Footprint",
    "category_orgn": "Category",
    "stockNumber": "Stock",
}
attribute_para={
    "contact_plating",
    "packaging",
    "connector_type",
    "contact_material",
    "NextPCB Stair Price ($)",
    "Datasheet"
}

class PartDetailsView(UiPartDetailsPanel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        # ---------------------------------------------------------------------
        # ----------------------- Properties List -----------------------------
        # ---------------------------------------------------------------------
        self.property = self.data_list.AppendTextColumn(
            "Property",width=180, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_LEFT
        )
        self.value = self.data_list.AppendTextColumn(
            "Value",width=-1, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_LEFT
        )

        for k,v in parameters.items():
            self.data_list.AppendItem([v, " "])
        for v in attribute_para:
            self.data_list.AppendItem([v, " "])    
        
            

    def on_open_pdf(self, e):
        """Open the linked datasheet PDF on button click."""
        item = self.data_list.GetSelection()
        row = self.data_list.ItemToRow(item)
        Datasheet = self.data_list.GetTextValue(row, 0)
        if self.pdfurl != "-" and Datasheet == "Datasheet":
            self.logger.info("opening %s", str(self.pdfurl))
            webbrowser.open("https:" + self.pdfurl)    

    def get_scaled_bitmap(self, url):
        """Download a picture from a URL and convert it into a wx Bitmap"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36'
        }
        content = requests.get(url,headers=header).content
        io_bytes = io.BytesIO(content)
        image = wx.Image(io_bytes, type=wx.BITMAP_TYPE_ANY)
        result = wx.Bitmap(image)
        return result

    def get_part_data(self,clicked_part):
        """fetch part data from NextPCB API and parse it into the table, set picture and PDF link"""
        if clicked_part == "":
            self.report_part_data_fetch_error(
                "returned data does not have expected clicked part"
            )

        self.info = clicked_part
        for i in range(self.data_list.GetItemCount()):
            self.data_list.DeleteItem(0)
        for k, v in parameters.items():
            val = self.info.get(k, "-")
            if val != "null" and val:
                self.data_list.AppendItem([v, str(val)])
            else:
                self.data_list.AppendItem([v, "-"])
        self.specs_dict  = json.loads(self.info.get("specs_orgn", []))
        for k, v in self.specs_dict.items():
            self.data_list.AppendItem([k, v])
        
        # -------- prefect the following code,according to the interface ------      
        prices_stair = self.info.get("priceStair", [])
        if prices_stair:
            for price in prices_stair:
                moq = price.get("purchase")
                if moq < self.info.get("minBuynum"):
                    continue
                else:
                    self.data_list.AppendItem(
                        [
                            f"NextPCB Stair Price ($) for >{moq}",
                            str(price.get("hkPrice", "0")),
                        ]
                    )
        else:
            self.data_list.AppendItem(
                [
                    f"NextPCB Stair Price ($)",
                    "0",
                ]
            )

        self.pdfurl = self.info.get("docUrl", "-")
        self.pdfurl = "-" if self.pdfurl == "" else self.pdfurl
        self.data_list.AppendItem(
            [
                "Datasheet",
                self.pdfurl,
            ]
        )
        self.data_list.Bind(wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.on_open_pdf)

        picture = self.info.get("goodsImage", [])
        if picture:
            
            picture = "https:" + picture[0]
            self.part_image.SetBitmap(
                self.get_scaled_bitmap(
                    picture,
                )
            )
        self.Layout()

    def report_part_data_fetch_error(self, reason):
        wx.MessageBox(
            f"Failed to download part detail: ({reason})\r\n"
            f"We looked for a part named:\r\n{self.info.find('mpn')}\r\n[hint: did you fill in the NextPCB field correctly?]",
            "Error",
            style=wx.ICON_ERROR,
        )
        self.Destroy()
        