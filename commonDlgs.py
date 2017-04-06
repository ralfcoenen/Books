# commonDlgs.py

import wx

#----------------------------------------------------------------------
def showMessageDlg(message, caption, flag=wx.ICON_ERROR):
    """"""
    msg = wx.MessageDialog(None, message=message,
                           caption=caption, style=flag)
    msg.ShowModal()
    msg.Destroy()