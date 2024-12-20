import wx
import wx.lib.dialogs
import wx.stc as stc
import os


fasec = {
    'times': 'Times new Roman',
    'mono': 'Couriei New',
    'helv': 'Arial',
    'other': 'Comic Sans MS',
    'size': 10,
    'size2': 8,
}



class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        self.dirname = ''    # hold the currnt directory
        self.filename = ''      #hold the file name
        self.leftMarginWidth = 25

        # toggle line numbers in preferences menu
        self.lineNumbersEnable = True

        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        if os.path.exists('./logo.ico'):
            icone = wx.Icon('./logo.ico', wx.BITMAP_TYPE_ANY)
            self.SetIcon(icone)
            self.Show()
        else:
            pass
        # control + = to zoom in
        self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)

        # control - = to zoom out
        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        # not show white space
        self.control.SetViewWhiteSpace(False)

        # line numbers
        self.control.SetMargins(5, 0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)

        # status  bar
        self.CreateStatusBar()
        # Menubar
        filemenu = wx.Menu()
        menunew = filemenu.Append(wx.ID_NEW, "&New", "Create a new Document")
        menuOpen = filemenu.Append(wx.ID_OPEN, "&open", "Open a existing document")
        menuSave = filemenu.Append(wx.ID_SAVE, "&save", "save the current Document")
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Save &As", "Save a new Document")
        filemenu.AppendSeparator()
        menuClose = filemenu.Append(wx.ID_EXIT, "&close", "Close the Application")

        editmenu = wx.Menu()
        menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", "Undo last action")
        menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", "Redo last action")
        editmenu.AppendSeparator()

        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "&Select All", "Select the entire Document")
        menuCopy = editmenu.Append(wx.ID_COPY, "&Copy", "Copy Selected text")
        menuCut = editmenu.Append(wx.ID_CUT, "&Cut", "Cut the selected text")
        menuPast = editmenu.Append(wx.ID_PASTE, "&Paste", "Paste text from the clipboard")

        prefmenu = wx.Menu()
        menulineNumber = prefmenu.Append(wx.ID_ANY, "Toggle &Line Numbers", "Show/Hide line numbers colum")

        helumenu = wx.Menu()
        menushortcuts = helumenu.Append(wx.ID_VIEW_LIST, "&shortcuts", "all shortcuts")
        menuAbout = helumenu.Append(wx.ID_ABOUT, "&about", "Read about the editor and its making")

        #meunu bar creating
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(prefmenu, "&Preferences")
        menuBar.Append(helumenu, "&help")
        self.SetMenuBar(menuBar)

        # calling the functions
        self.Bind(wx.EVT_MENU, self.OnNew, menunew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAS, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.onClose, menuClose)

        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPast)

        self.Bind(wx.EVT_MENU, self.OnToggleLineNUmber, menulineNumber)

        self.Bind(wx.EVT_MENU, self.OnHowTo, menushortcuts)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)

        #key bind
        self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)

        self.Show()
        self.UpdateLineCol(self)


        #functions on menu bars
    def OnNew(self, e):
        self.filename = ''
        self.control.SetValue("")

    def OnOpen(self, e):
        try:
            dlg = wx.FileDialog(self, "Choose a file", self.dirname,"", "*.*",wx.FD_OPEN)
                                     # title ,direcoty,type,id
            if(dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'r')
                self.control.SetValue(f.read())
                f.close()
            dlg.Destroy()
        except:
            dlg = wx.MessageDialog(self, "Coudn't open the file", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def OnSave(self, e):
        try:
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.control.GetValue())
        except:
            try:
                dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if(dlg.ShowModal() == wx.ID_OK):
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w')
                    f.write(self.control.GetValue())
                    f.close()
                dlg.Destroy()
            except:
                pass

    def OnSaveAS(self, e):
        try:
            dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*",
                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w')
                f.write(self.control.GetValue())
                f.close()
            dlg.Destroy()
        except:
            pass

    def onClose(self, e):
        self.Close(True)
    def OnUndo(self, e):
        self.control.Undo()
    def OnRedo(self, e):
        self.control.Redo()
    def OnSelectAll(self, e):
        self.control.SelectAll()
    def OnCopy(self ,e):
        self.control.Copy()
    def OnCut(self, e):
        self.control.Cut()
    def OnPaste(self, e):
        self.control.Paste()
    def OnToggleLineNUmber(self, e):
        if(self.lineNumbersEnable == True):
            self.control.SetMarginWidth(1, 0)
            self.lineNumbersEnable = False
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.lineNumbersEnable = True
    def OnHowTo(self, e):
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, """these are shortcuts used by Xcceleratext
to start new document # Ctrl + N
to open a file# Ctrl + o
to save a file # Ctrl + s
to save a file as ...  # Alt + s
to close the editor # Ctrl + q
to zoom in # Ctrl + (+)
to zoom out # Ctrl + (-)
to look up all shortcuts here  # F1
to open the about window  # F2""", "shortcut", size=(400, 400))
        dlg.ShowModal()
        dlg.Destroy()
    def OnAbout(self, e):
        dlg =wx.MessageDialog(self, "Xcceleratext 1.0 made by wedu ", " About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


    def UpdateLineCol(self, e):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        stat = "Line %s, Column %s" % (line,col)

    def OnCharEvent(self, e):
        keyCode = e.GetKeyCode()
        altDown = e.AltDown()
        #print(keyCode)
        if(keyCode == 14): # Ctrl + N
            self.OnNew(self)
        elif(keyCode == 15): # Ctrl + o
            self.OnOpen(self)
        elif (keyCode == 19):  # Ctrl + s
            self.OnSave(self)
        elif (altDown and (keyCode == 115) ):  # Alt + s
            self.OnSaveAS(self)
        elif (keyCode == 23):  # Ctrl + w
            self.onClose(self)
        elif (keyCode == 340):  # F1
            self.OnHowTo(self)
        elif (keyCode == 341):  # F2
            self.OnAbout(self)
        else:
            e.Skip()
            #pass
            #pass wont work cause then it will check all the keyword so you cant code

app = wx.App()
frame = MainWindow(None, "Xcceleratext")
app.MainLoop()