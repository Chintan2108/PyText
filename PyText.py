import wx, os
import wx.lib.dialogs
import wx.stc as stc

faces = {'times': 'Times New Roman',
         'mono': 'Courier New',
         'helv': 'Arial',
         'other': 'Comic Sans MS',
         'size': 14,
         'size2': 8}

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''
        self.filename = ''
        self.leftMarginWidth = 25
        self.lineNumbersEnabled = True
        self.statusBarEnabled = True        

        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control=stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("F:\\Chintan_Data\\CHARUSAT HW\\SEM5\\System Software\\PyText 1.0\\New folder\\pt.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.control.CmdKeyAssign(ord('='),stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.control.CmdKeyAssign(ord('-'),stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.control.SetViewWhiteSpace(False)
        self.control.SetMargins(5,0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)

        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((200,200,200))

        filemenu = wx.Menu()
        menuNew = filemenu.Append(wx.ID_NEW, "&New", "Create a new document")
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open an existing document")
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save", "Save the current document")
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Save &As", "Save a new document")
        filemenu.AppendSeparator()
        menuClose = filemenu.Append(wx.ID_EXIT, "&Close", "Close PyText")

        editmenu = wx.Menu()
        menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", "Undo previous action")
        menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", "Redo previous action")
        menuCut = editmenu.Append(wx.ID_CUT, "Cu&t", "Cut selected text")
        menuCopy = editmenu.Append(wx.ID_COPY, "&Copy", "Copy selected text")
        menuPaste = editmenu.Append(wx.ID_PASTE, "&Paste", "Paste clipboard text")
        editmenu.AppendSeparator()
        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "Select &All", "Select all the text")

        #formatmenu = wx.Menu()
        #menuWordWrap = formatmenu.Append(wx.ID_ANY, "&Word Wrap", "Turn overflow on/off")
        #menuFont = formatmenu.Append(wx.ID_ANY, "&Font", "Change font size/family")

        #viewmenu = wx.Menu()
        #menuStatusBar = viewmenu.Append(wx.ID_ANY, "&Status Bar", "Status Bar")

        preferencesmenu = wx.Menu()
        menuToggle = preferencesmenu.Append(wx.ID_ANY, "&Toggle Line Numbers", "Show/Hide Line Numbers")

        helpmenu = wx.Menu()
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About PyText", "About PyText")
        helpmenu.AppendSeparator()
        menuHowTo = helpmenu.Append(wx.ID_ANY, "&How to", "Getting around in PyText")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        #menuBar.Append(formatmenu, "F&ormat")
        #menuBar.Append(viewmenu, "&View")
        menuBar.Append(preferencesmenu, "&Preferences")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.CheckOnClose, menuClose)
        self.Bind(wx.EVT_CLOSE, self.CheckOnClose)

        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
        
        self.Bind(wx.EVT_MENU, self.OnToggleLineNumbers, menuToggle)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnHowTo, menuHowTo)

        self.control.Bind(wx.EVT_KEY_UP, self.UpdateStatusBar)
        self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)
        
        self.Show()
        self.UpdateStatusBar(self)

        self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(other)s,size:%(size)d" % faces)
        self.control.StyleClearAll()

    def OnNew(self, e):
        print("ONNEW")
        content = self.control.GetValue()
        if (self.filename == ''):
            if(content == ''):
                #self.checked = True
                self.filename = ''
                self.control.SetValue("")
                self.SetTitle("Untitled - PyText")
            else:
                check = wx.MessageDialog(self, "Do you want to save changes to the current file?", "PyText", wx.YES_NO|wx.CANCEL)
                reply = check.ShowModal()
                if (reply == wx.ID_YES):
                    self.OnSaveAs(self)
                    #self.checked = True
                    self.filename = ''
                    self.control.SetValue("")
                    self.SetTitle("Untitled - PyText")
                elif (reply==wx.ID_NO):
                    #self.checked = True
                    self.filename = ''
                    self.control.SetValue("")
                    self.SetTitle("Untitled - PyText")
                elif (reply == wx.ID_CANCEL):
                    pass
                check.Destroy()
        elif (self.filename != ''):
            f = open(os.path.join(self.dirname, self.filename),'r')
            fcontent = f.read()
            f.close()
            if (content == fcontent):
                #self.checked = True
                self.filename = ''
                self.control.SetValue("")
                self.SetTitle("Untitled - PyText")
            else:
                check = wx.MessageDialog(self, "Do you want to save changes to the current file?", "PyText", wx.YES_NO|wx.CANCEL)
                reply = check.ShowModal()
                if (reply == wx.ID_YES):
                    self.OnSave(self)
                    #self.checked = True
                    self.filename = ''
                    self.control.SetValue("")
                    self.SetTitle("Untitled - PyText")
                elif (reply == wx.ID_NO):
                    #self.checked = True
                    self.filename = ''
                    self.control.SetValue("")
                    self.SetTitle("Untitled - PyText")
                elif (reply == wx.ID_CANCEL):
                    pass
                check.Destroy()
        

    def OnOpen(self, e):
        print("ONOPEN")
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.txt", wx.FD_OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename),'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
        self.SetTitle((self.filename[:len(self.filename)-4] + " - PyText"))

    def OnSave(self, e):
        print("ONSAVE")
        try:
            f = open(os.path.join(self.dirname, self.filename),'w')
            f.write(self.control.GetValue())
            f.close()
        except:
            print("SAVEFIRSTEXCEPT")
            try:
                print("testtry inner save")
                dlg = wx.FileDialog(self, "Save File as", self.dirname, "Untitled", "*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if (dlg.ShowModal() == wx.ID_OK):
                    print("dlg create")
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w')
                    f.write(self.control.GetValue())
                    f.close()
                dlg.Destroy()
                self.SetTitle((self.filename[:len(self.filename)-4] + " - PyText"))
            except:
                print("SAVESECONDEXCEPT")
                pass

    def OnSaveAs(self, e):
        print("ONSAVEAS")
        try:
            dlg = wx.FileDialog(self, "Save File as", self.dirname, "Untitled", "*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal() == wx.ID_OK):
                  self.filename = dlg.GetFilename()
                  self.dirname = dlg.GetDirectory()
                  f = open(os.path.join(self.dirname, self.filename), 'w')
                  f.write(self.control.GetValue())
                  f.close()
            dlg.Destroy()
            self.SetTitle((self.filename[:len(self.filename)-4] + " - PyText"))
        except:
            print("SAVEASEXCEPT")
            pass
            
    def OnClose(self, e):
        print("ONCLOSE")
        #self.OnSave(self)
        self.Close(True)

    def OnUndo(self, e):
        self.control.Undo()

    def OnRedo(self, e):
        self.control.Redo()

    def OnCut(self, e):
        self.control.Cut()

    def OnCopy(self, e):
        self.control.Copy()

    def OnPaste(self, e):
        self.control.Paste()

    def OnSelectAll(self, e):
        self.control.SelectAll()

    def OnToggleLineNumbers(self, e):
        if (self.lineNumbersEnabled):
            self.control.SetMarginWidth(1,0)
            self.lineNumbersEnabled = False
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.lineNumbersEnbled = True
            
    def OnAbout(self, e):
        print("ABOUT")
        dlg = wx.MessageDialog(self, "About Content", "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnHowTo(self, e):
        print("HOWTO")
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, "This is how to", "How To",  size=(400,400))
        dlg.ShowModal()
        dlg.Destroy()

    def UpdateStatusBar(self, e):
        line = self.control.GetCurrentLine()+1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        dis = "Line %s, Column %s" % (line,col)
        self.StatusBar.SetStatusText(dis, 0)

    def CheckOnClose(self, e):
        content = self.control.GetValue()
        if (self.filename == ''):
            if(content == ''):
                #self.checked = True
                self.Destroy()
            else:
                check = wx.MessageDialog(self, "Do you want to save changes to the current file?", "PyText", wx.YES_NO|wx.CANCEL)
                reply = check.ShowModal()
                if (reply == wx.ID_YES):
                    self.OnSaveAs(self)
                    #self.checked = True
                    self.Destroy()
                elif (reply==wx.ID_NO):
                    #self.checked = True
                    self.Destroy()
                elif (reply == wx.ID_CANCEL):
                    pass
                check.Destroy()
        elif (self.filename != ''):
            f = open(os.path.join(self.dirname, self.filename),'r')
            fcontent = f.read()
            f.close()
            if (content == fcontent):
                #self.checked = True
                self.Destroy()
            else:
                check = wx.MessageDialog(self, "Do you want to save changes to the current file?", "PyText", wx.YES_NO|wx.CANCEL)
                reply = check.ShowModal()
                if (reply == wx.ID_YES):
                    self.OnSave(self)
                    #self.checked = True
                    self.Destroy()
                elif (reply == wx.ID_NO):
                    #self.checked = True
                    self.Destroy()
                elif (reply == wx.ID_CANCEL):
                    pass
                check.Destroy()
        
                

    def OnCharEvent(self, e):
        keycode = e.GetKeyCode()
        #print(keycode)

        if (keycode == 14): #Ctrl + N
            self.OnNew(self)
        elif (keycode == 15): #Ctrl + O
            self.OnOpen(self)
        elif (keycode == 19): #Ctrl + S
            self.OnSave(self)
        elif (keycode == 351): #F12
            self.OnSaveAs(self)
        elif(keycode == 23): #Ctrl + W
            self.Close(self)
        elif (keycode == 340): #F1
            self.OnHowTo(self)
        elif (keycode == 341): #F2
            self.OnAbout(self)
        else:
            e.Skip()
        

app = wx.App()

frame = MainWindow(None, "PyText")
app.MainLoop()
