# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class UiMatchPartPanel
###########################################################################

class UiMatchPartPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 569,65 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.down_toolbar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TB_HORIZONTAL )
		self.down_toolbar.SetToolSeparation( 1 )
		self.select_part_button = wx.Button( self.down_toolbar, wx.ID_ANY, u" Manual Match ", wx.Point( 0,0 ), wx.DefaultSize, 0 )
		self.down_toolbar.AddControl( self.select_part_button )
		self.remove_part_button = wx.Button( self.down_toolbar, wx.ID_ANY, u" Remove Assigned MPN ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.down_toolbar.AddControl( self.remove_part_button )
		self.down_toolbar.Realize()

		bSizer1.Add( self.down_toolbar, 0, 0, 0 )


		bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.export_csv = wx.Button( self, wx.ID_ANY, u" Epxort... ", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.export_csv, 0, 0, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

	def __del__( self ):
		pass













