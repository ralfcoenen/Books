# ------------------------------------------------------------
# mediaLocker.py
#
# Author: Mike Driscoll
# Contact: mike@pythonlibrary.org
#
# This program demonstrates how to work with a SQLite database
# using wxPython and SqlAlchemy. It is also an example of MVC
# concepts and how to put together a fully working wxPython
# application.
# ------------------------------------------------------------

import os
import addModRecord
import commonDlgs
import controller
import wx
from ObjectListView import ObjectListView, ColumnDefn
import xlsxwriter


########################################################################
class BookPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        try:
            self.bookResults = controller.getAllRecords()
        except:
            self.bookResults = []
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        searchSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD) 
        
        # create the search related widgets
        cat = ["Author", "Title", "ISBN", "Publisher"]
        searchByLbl = wx.StaticText(self, label="Search By:")
        searchByLbl.SetFont(font)
        searchSizer.Add(searchByLbl, 0, wx.ALL, 5)
        
        self.categories = wx.ComboBox(self, value="Author", choices=cat)
        searchSizer.Add(self.categories, 0, wx.ALL, 5)
        
        self.search = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search.Bind(wx.EVT_TEXT_ENTER, self.onSearch)
        searchSizer.Add(self.search, 0, wx.ALL, 5)
        
        self.bookResultsOlv = ObjectListView(self, style=wx.LC_REPORT
                                                        |wx.SUNKEN_BORDER)
        self.bookResultsOlv.SetEmptyListMsg("No Records Found")
        self.setBooks()
        
        # create the button row
        addRecordBtn = wx.Button(self, label="Add")
        addRecordBtn.Bind(wx.EVT_BUTTON, self.onAddRecord)
        btnSizer.Add(addRecordBtn, 0, wx.ALL, 5)
        
        editRecordBtn = wx.Button(self, label="Edit")
        editRecordBtn.Bind(wx.EVT_BUTTON, self.onEditRecord)
        btnSizer.Add(editRecordBtn, 0, wx.ALL, 5)
        
        deleteRecordBtn = wx.Button(self, label="Delete")
        deleteRecordBtn.Bind(wx.EVT_BUTTON, self.onDelete)
        btnSizer.Add(deleteRecordBtn, 0, wx.ALL, 5)
        
        showAllBtn = wx.Button(self, label="Show All")
        showAllBtn.Bind(wx.EVT_BUTTON, self.onShowAllRecord)
        btnSizer.Add(showAllBtn, 0, wx.ALL, 5)

        showExportBtn = wx.Button(self, label="Export")
        showExportBtn.Bind(wx.EVT_BUTTON, self.onExport)
        btnSizer.Add(showExportBtn, 0, wx.ALL, 5)

        mainSizer.Add(searchSizer)
        mainSizer.Add(self.bookResultsOlv, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(mainSizer)
        
    # ----------------------------------------------------------------------
    def onAddRecord(self, event):
        """
        Add a record to the database
        """
        dlg = addModRecord.AddModRecDialog()
        dlg.ShowModal()
        dlg.Destroy()
        self.showAllRecords()
        
    # ----------------------------------------------------------------------
    def onEditRecord(self, event):
        """
        Edit a record
        """
        selectedRow = self.bookResultsOlv.GetSelectedObject()
        if selectedRow == None:
            commonDlgs.showMessageDlg("No row selected!", "Error")
            return
        dlg = addModRecord.AddModRecDialog(selectedRow, title="Modify",
                                           addRecord=False)
        dlg.ShowModal()
        dlg.Destroy()
        self.showAllRecords()
        
    # ----------------------------------------------------------------------
    def onDelete(self, event):
        """
        Delete a record
        """
        selectedRow = self.bookResultsOlv.GetSelectedObject()
        if selectedRow == None:
            commonDlgs.showMessageDlg("No row selected!", "Error")
            return
        controller.deleteRecord(selectedRow.id)
        self.showAllRecords()
        
    # ----------------------------------------------------------------------
    def onSearch(self, event):
        """
        Searches database based on the user's filter choice and keyword
        """
        filterChoice = self.categories.GetValue()
        keyword = self.search.GetValue()
        print "%s %s" % (filterChoice, keyword)
        self.bookResults = controller.searchRecords(filterChoice, keyword)
        self.setBooks()
        
    # ----------------------------------------------------------------------
    def onShowAllRecord(self, event):
        """
        Updates the record list to show all of them
        """
        self.showAllRecords()
        
    # ----------------------------------------------------------------------
    def setBooks(self):
        self.bookResultsOlv.SetColumns([
            ColumnDefn("Title", "left", 350, "title"),
            ColumnDefn("Author", "left", 150, "author"),
            ColumnDefn("ISBN", "right", 150, "isbn"),
            ColumnDefn("Publisher", "left", 150, "publisher")
        ])
        self.bookResultsOlv.SetObjects(self.bookResults)
        
    # ----------------------------------------------------------------------
    def showAllRecords(self):
        """
        Show all records in the object list view control
        """
        self.bookResults = controller.getAllRecords()
        self.setBooks()

    def onExport(self, event):
        selectedRow = self.bookResultsOlv.GetSelectedObjects()
        if not selectedRow:
            commonDlgs.showMessageDlg("No row selected!", "Error")
        else:
            result=self.export2excel(selectedRow)

    def export2excel(l,event):
        workbook = xlsxwriter.Workbook('Export.xlsx')
        worksheet = workbook.add_worksheet()
        # Header
        row = 1
        col = 0
        worksheet.write('A1', 'Author')
        worksheet.write('B1', 'Firstname')
        worksheet.write('C1', 'ID')
        worksheet.write('D1', 'ISBN')
        worksheet.write('E1', 'Lastname')
        worksheet.write('F1', 'Publisher')
        worksheet.write('H1', 'Title')
        # Data
        for r in l:
            worksheet.write_string(row, col, r.author)
            worksheet.write_string(row, col + 1, r.first_name)
            worksheet.write_number(row, col + 2, r.id)
            worksheet.write_string(row, col + 3, r.isbn)
            worksheet.write_string(row, col + 4, r.last_name)
            worksheet.write_string(row, col + 5, r.publisher)
            worksheet.write_string(row, col + 6, r.title)
            row += 1
        res = workbook.close()
        os.system('Export.xlsx')
        return


# #######################################################################
class BookFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="MvP Media Organizer",
                          size=(800, 600))
        panel = BookPanel(self)
        
        self.Show()
        
# ----------------------------------------------------------------------



if __name__ == "__main__":
    app = wx.App(False)
    frame = BookFrame()
    app.MainLoop()