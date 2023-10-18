# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class UiPartListPanel
###########################################################################

class UiPartListPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.result_count = wx.StaticText( self, wx.ID_ANY, u"0 Results", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.result_count.Wrap( -1 )

		bSizer2.Add( self.result_count, 0, wx.ALL, 5 )

		self.part_list = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.part_list, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.prev_button = wx.Button( self, wx.ID_ANY, u"Previous", wx.DefaultPosition, wx.Size( 70,26 ), 0 )
		bSizer1.Add( self.prev_button, 0, wx.ALL, 5 )

		self.page_turning = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self.page_turning, wx.ID_ANY, u"0/100", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText2.Wrap( -1 )

		self.m_staticText2.SetFont( wx.Font( 14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "宋体" ) )

		bSizer41.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.SHAPED, 5 )


		self.page_turning.SetSizer( bSizer41 )
		self.page_turning.Layout()
		bSizer41.Fit( self.page_turning )
		bSizer1.Add( self.page_turning, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer4.SetMinSize( wx.Size( 70,26 ) )

		bSizer1.Add( bSizer4, 0, 0, 5 )

		self.next_button = wx.Button( self, wx.ID_ANY, u"Next", wx.DefaultPosition, wx.Size( 70,26 ), 0 )
		bSizer1.Add( self.next_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer2.Add( bSizer1, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()
		bSizer2.Fit( self )

	def __del__( self ):
		pass
