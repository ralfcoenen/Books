# addModRecord.py

import commonDlgs
import controller
import wx


########################################################################
class AddModRecDialog(wx.Dialog):
    """
    Add / Modify Record dialog
    """

    # ----------------------------------------------------------------------
    def __init__(self, row=None, title="Add", addRecord=True):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="%s Record" % title)
        self.addRecord = addRecord
        self.selectedRow = row
        if row:
            bTitle = self.selectedRow.title
            fName = self.selectedRow.first_name
            lName = self.selectedRow.last_name
            isbn = self.selectedRow.isbn
            publisher = self.selectedRow.publisher
        else:
            bTitle = fName = lName = isbn = publisher = ""
        size = (80, -1)
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD) 
        
        # create the sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        authorSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
                
        # create some widgets
        lbl = wx.StaticText(self, label="New Record")
        lbl.SetFont(font)
        mainSizer.Add(lbl, 0, wx.CENTER)
        
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD) 
        titleLbl = wx.StaticText(self, label="Title:", size=size)
        titleLbl.SetFont(font)
        self.titleTxt = wx.TextCtrl(self, value=bTitle)
        mainSizer.Add(self.rowBuilder([titleLbl, self.titleTxt]), 
                      0, wx.EXPAND)
        
        authorLbl = wx.StaticText(self, label="Author:", size=size)
        authorLbl.SetFont(font)
        authorSizer.Add(authorLbl, 0, wx.ALL, 5)
        self.authorFirstTxt = wx.TextCtrl(self, value=fName)
        authorSizer.Add(self.authorFirstTxt, 1, wx.EXPAND|wx.ALL, 5)
        self.authorLastTxt = wx.TextCtrl(self, value=lName)
        authorSizer.Add(self.authorLastTxt, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(authorSizer, 0, wx.EXPAND)
        
        isbnLbl = wx.StaticText(self, label="ISBN:", size=size)
        isbnLbl.SetFont(font)
        self.isbnTxt = wx.TextCtrl(self, value=isbn)
        mainSizer.Add(self.rowBuilder([isbnLbl, self.isbnTxt]),
                      0, wx.EXPAND)
        
        publisherLbl = wx.StaticText(self, label="Publisher:", size=size)
        publisherLbl.SetFont(font)
        self.publisherTxt = wx.TextCtrl(self, value=publisher)
        mainSizer.Add(self.rowBuilder([publisherLbl, self.publisherTxt]),
                      0, wx.EXPAND)
        
        okBtn = wx.Button(self, label="%s Book" % title)
        okBtn.Bind(wx.EVT_BUTTON, self.onRecord)
        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        cancelBtn = wx.Button(self, label="Close")
        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
        
        mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(mainSizer)
        
    # ----------------------------------------------------------------------
    def getData(self):
        """"""
        authorDict = {}
        bookDict = {}
                        
        fName = self.authorFirstTxt.GetValue()
        lName = self.authorLastTxt.GetValue()
        title = self.titleTxt.GetValue()
        isbn = self.isbnTxt.GetValue()
        publisher = self.publisherTxt.GetValue()
        
        if fName == "" or title == "":
            commonDlgs.showMessageDlg("Author and Title are Required!",
                                      "Error")
            return
            
        if "-" in isbn:
            isbn = isbn.replace("-", "")
        authorDict["first_name"] = fName
        authorDict["last_name"] = lName
        bookDict["title"] = title
        bookDict["isbn"] = isbn
        bookDict["publisher"] = publisher
        
        return authorDict, bookDict
            
    # ----------------------------------------------------------------------
    def onAdd(self):
        """
        Add the record to the database
        """
        authorDict, bookDict = self.getData()
        data = ({"author":authorDict, "book":bookDict})
        controller.addRecord(data)
        
        # show dialog upon completion
        commonDlgs.showMessageDlg("Book Added",
                                  "Success!", wx.ICON_INFORMATION)
        
        # clear dialog so we can add another book
        for child in self.GetChildren():
            if isinstance(child, wx.TextCtrl):
                child.SetValue("")
        
    # ----------------------------------------------------------------------
    def onClose(self, event):
        """
        Cancel the dialog
        """
        self.Destroy()
        
    # ----------------------------------------------------------------------
    def onEdit(self):
        """"""
        authorDict, bookDict = self.getData()
        comboDict = dict(authorDict.items() + bookDict.items())
        controller.editRecord(self.selectedRow.id, comboDict)
        commonDlgs.showMessageDlg("Book Edited Successfully!", "Success",
                                  wx.ICON_INFORMATION)
        self.Destroy()
        
    # ----------------------------------------------------------------------
    def onRecord(self, event):
        """"""
        if self.addRecord:
            self.onAdd()
        else:
            self.onEdit()
        self.titleTxt.SetFocus()
        
    # ----------------------------------------------------------------------
    def rowBuilder(self, widgets):
        """"""
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl, txt = widgets
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(txt, 1, wx.EXPAND|wx.ALL, 5)
        return sizer
            
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    dlg = AddRecDialog()
    dlg.ShowModal()
    app.MainLoop()