import io
import logging
import webbrowser
import json
import requests
import wx
<<<<<<< HEAD
from requests.exceptions import Timeout

from .helpers import HighResWxSize, loadBitmapScaled
from .debug import Print

# class URLRenderer(wx.dataview.DataViewCustomRenderer):
    # def __init__(self):
        # super().__init__()
# 
    # def Render(self, rect, dc, state):
        # self.SetBackgroundColour(wx.WHITE)
        # dc.SetBrush(wx.WHITE_BRUSH)
        # dc.SetTextForeground(wx.BLUE)
# 
        # item = self.GetDataObject()
        # url = item.GetValue()
# 
        # dc.DrawText(url, rect.GetLeft(), rect.GetTop())
# 
    # def ActivateCell(self, cell, model, item):
        # url = item.GetValue()  
        # webbrowser.open(url)  
=======

from .helpers import HighResWxSize, loadBitmapScaled

>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937

class PartDetailsDialog(wx.Dialog):
    def __init__(self, parent, stockID):
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="NextPCB Part Details",
            pos=wx.DefaultPosition,
            size=HighResWxSize(parent.window, wx.Size(1000, 800)),
            style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP,
        )

        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.stockID = stockID
        self.pdfurl = None
        #self.picture = None

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
        # ----------------------- Properties List -----------------------------
        # ---------------------------------------------------------------------
        self.data_list = wx.dataview.DataViewListCtrl(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            style=wx.dataview.DV_SINGLE,
        )
        self.property = self.data_list.AppendTextColumn(
            "Property",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(self.parent.scale_factor * 200),
            align=wx.ALIGN_LEFT,
        )
        self.value = self.data_list.AppendTextColumn(
            "Value",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(self.parent.scale_factor * 300),
            align=wx.ALIGN_LEFT,
        )

        # ---------------------------------------------------------------------
        # ------------------------- Right side ------------------------------
        # ---------------------------------------------------------------------
        self.image = wx.StaticBitmap(
            self,
            wx.ID_ANY,
            loadBitmapScaled("placeholder.png", self.parent.scale_factor, static=True),
            wx.DefaultPosition,
            HighResWxSize(parent.window, wx.Size(200, 200)),
            0,
        )
        # self.openpdf_button = wx.Button(
            # self,
            # wx.ID_ANY,
            # "Open Datasheet",
            # wx.DefaultPosition,
            # wx.DefaultSize,
            # 0,
        # )

        # self.openpdf_button.Bind(wx.EVT_BUTTON, self.openpdf)

        # self.openpdf_button.SetBitmap(
            # loadBitmapScaled(
                # "mdi-file-document-outline.png",
                # self.parent.scale_factor,
            # )
        # )
        # self.openpdf_button.SetBitmapMargins((2, 0))

        # ---------------------------------------------------------------------
        # ------------------------ Layout and Sizers --------------------------
        # ---------------------------------------------------------------------

        right_side_layout = wx.BoxSizer(wx.VERTICAL)
        right_side_layout.Add(self.image, 10, wx.ALL | wx.EXPAND, 5)
        right_side_layout.AddStretchSpacer()
        #right_side_layout.Add(self.openpdf_button, 5, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.data_list, 30, wx.ALL | wx.EXPAND, 5)
        layout.Add(right_side_layout, 10, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)
        self.Layout()
        self.Centre(wx.BOTH)

        self.get_part_data()

    def quit_dialog(self, e):
        self.Destroy()
<<<<<<< HEAD
        self.EndModal(wx.ID_OK)

    def on_open_pdf(self, e):
        """Open the linked datasheet PDF on button click."""
        item = self.data_list.GetSelection()
        row = self.data_list.ItemToRow(item)
        Datasheet = self.data_list.GetTextValue(row, 0)
        if self.pdfurl != "-" and Datasheet == "Datasheet":
            self.logger.info("opening %s", str(self.pdfurl))
            webbrowser.open("https:" + self.pdfurl)

    def get_scaled_bitmap(self, url, width, height):
        """Download a picture from a URL and convert it into a wx Bitmap"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36'
        }

        content = requests.get(url,headers=header).content
        #content = requests.get(url).content
        io_bytes = io.BytesIO(content)
        image = wx.Image(io_bytes, type=wx.BITMAP_TYPE_ANY)
=======
        self.EndModal(0)

    def openpdf(self, e):
        """Open the linked datasheet PDF on button click."""
        self.logger.info("opening %s", str(self.pdfurl))
        webbrowser.open(self.pdfurl)

    def get_scaled_bitmap(self, url, width, height):
        """Download a picture from a URL and convert it into a wx Bitmap"""
        content = requests.get(url).content
        io_bytes = io.BytesIO(content)
        image = wx.Image(io_bytes)
>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return result

    def get_part_data(self):
        """fetch part data from NextPCB API and parse it into the table, set picture and PDF link"""
        headers = {
            "Content-Type": "application/json",
        }
        body = {
            "stockId": self.stockID
        }
        body_json = json.dumps(body, indent=None, ensure_ascii=False)
<<<<<<< HEAD
        try:
            response = requests.post(
                "https://edaapi.nextpcb.com/edapluginsapi/v1/stock/detail",
                headers=headers,
                data=body_json,
                timeout=5
            )
        except Timeout:
            self.Destroy()
            self.EndModal(wx.ID_OK)
        except Exception as e:
            self.Destroy()
            self.EndModal(wx.ID_OK)

=======
        response = requests.post(
            "https://uat-edaapi.nextpcb.com/edapluginsapi/v1/stock/detail",
            headers=headers,
            data=body_json
        )
>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937
        if response.status_code != 200:
            self.report_part_data_fetch_error("non-OK HTTP response status")

        data = response.json()
        #wx.MessageBox(f"return data detail:{data}", "Help", style=wx.ICON_INFORMATION)
        if not data.get("result"):
            self.report_part_data_fetch_error(
                "returned JSON data does not have expected 'result' attribute"
            )
        if not data.get("result").get("stock"):
            self.report_part_data_fetch_error(
                "returned JSON data does not have expected 'stock' attribute"
            )
        
        self.info = data.get("result").get("stock", {})
        parameters = {
            "goodsName": "MPN",
            "providerName": "Manufacturer",
            "goodsDesc": "Description",
            "encap": "Package / Footprint",
            "categoryName": "Category",
            "stockNumber": "Stock",
            "minBuynum": "Minimum Order Quantity(MOQ)",
        }
        for k, v in parameters.items():
            val = self.info.get(k, "-")
            if val != "null" and val:
                self.data_list.AppendItem([v, str(val)])
            else:
                self.data_list.AppendItem([v, "-"])
        prices_stair = self.info.get("priceStair", [])
        #wx.MessageBox(f"priceStair:{prices_stair}", "Help", style=wx.ICON_INFORMATION)
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
<<<<<<< HEAD
        self.data_list.Bind(wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.on_open_pdf)
        
        #renderer = URLRenderer()
        #self.data_list.SetItemCustomRenderer(datasheet_item, 1, renderer)
        picture = self.info.get("goodsImage", [])
        #wx.MessageBox(f"self.pdfurl{self.pdfurl}", "Help", style=wx.ICON_INFORMATION)
        #wx.MessageBox(f"picture:{picture}", "Help", style=wx.ICON_INFORMATION)
        if picture:
            
            picture = "https:" + picture[0]
            #webbrowser.open(picture)
            #Print(self, str(picture)).ShowModal()
            
=======
        picture = self.info.get("goodsImage", [])[0]
        #wx.MessageBox(f"self.pdfurl{self.pdfurl}", "Help", style=wx.ICON_INFORMATION)
        #wx.MessageBox(f"picture{picture}", "Help", style=wx.ICON_INFORMATION)
        if picture:
            # get the full resolution image instead of the thumbnail
            picture = "https:" + picture
>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937
            self.image.SetBitmap(
                self.get_scaled_bitmap(
                    picture,
                    int(200 * self.parent.scale_factor),
                    int(200 * self.parent.scale_factor),
                )
            )

<<<<<<< HEAD
    # def on_datasheet_pdf(self):
        # item = self.data_list.GetSelection()
        # row = self.data_list.ItemToRow(item)
        # pdf_url = self.data_list.GetTextValue(row, 1)

=======
>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937
    def report_part_data_fetch_error(self, reason):
        wx.MessageBox(
            f"Failed to download part detail from the NextPCB API ({reason})\r\n"
            f"We looked for a part named:\r\n{self.stockID}\r\n[hint: did you fill in the NextPCB field correctly?]",
            "Error",
            style=wx.ICON_ERROR,
        )
<<<<<<< HEAD
        self.Destroy()
        self.EndModal(wx.ID_OK)
        #self.EndModal(-1)
=======
        self.EndModal(-1)
>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937
