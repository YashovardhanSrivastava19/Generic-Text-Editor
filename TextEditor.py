""" [A Simple Generic Text Editor] """
import os
from nltk import text #Testing(V2)
from ttkthemes import ThemedTk
from tkinter import filedialog
import threading
from tkinter import *
from tkinter import Label, Menu, StringVar, messagebox
from tkinter.ttk import Treeview, Notebook
import subprocess
import ctypes
from pygments.lexers.c_cpp import CLexer,CppLexer
from pygments.lexers.python import PythonLexer #For testing
from pygments import lex
import Pmw
class Editor(Frame):
    def __init__(self, master=None) -> None:
        """ [Initialize the root window and configure its properties] """
        super().__init__(master)
        self.master = master
        self.master.title(MasterProperties.Title)
        self.master.geometry(MasterProperties.Geometry)
        self.master.config(bg = Color)
        self.CurrentTheme = MasterProperties.Themes["ThemeCLAM"]
        self.ChangeTheme(self.CurrentTheme)
        self.ConfigureAllInitial()



    def ConfigureAllInitial(self):
        """ [Setup all the necessary function calls] """
        self.TitleBar()
        self.StatusBar()
        self.Menu()
        self.TextSpace()
        self.SideTreeViewSpace()



    def Menu(self): 
        """ [Add a menubar to the windows and configure its parts] """ 
        self.menubar = MenuOptions(self.master)
        self.menubar.configure(background=Color)
        self.master.config(menu=self.menubar)
        self.ConfigureAllMenus()



    def ConfigureFileMenu(self):
        """ [Setup the file menu cascade of the Menubar] """
        self.filemenu = FileMenuOptions(self.menubar)
        
        self.filemenu.AddCommand("New", "Ctrl+N", self.newfile)
        self.filemenu.AddCommand("Open", "Ctrl+O", self.openfile)
        self.filemenu.AddCommand("Save", "Ctrl+S", self.savefile)
        self.filemenu.AddCommand("SaveAs", "Ctrl+D", self.saveasfile)
        
        self.filemenu.Separator()
        
        self.filemenu.AddCommand("Exit", "Ctrl+E", self.exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

    

    def ConfigureEditMenu(self):
        """ [Setup the edit menu cascade of the Menubar] """
        self.editmenu = EditMenuOptions(self.menubar)
        
        self.editmenu.AddCommand("Cut", "Ctrl+X", self.cut)
        self.editmenu.AddCommand("Copy", "Ctrl+C", self.copy)
        self.editmenu.AddCommand("Paste", "Ctrl+V", self.paste)    
        self.editmenu.AddCommand("Undo", "Ctrl+Z", self.undo)
        self.editmenu.AddCommand("Redo","Ctrl-Shift-Z",self.redo)

        self.editmenu.Separator()
        
        self.editmenu.AddCommand("Comment","Ctrl-M",self.CommentBlock)
        self.editmenu.AddCommand("Comment Block","Shift-Alt-A",self.InsertMultiSingleLine)
        self.editmenu.AddCommand("Shift Line Up","Alt-Up",self.ShiftLineUp)
        self.editmenu.AddCommand("Shift Line Down","Alt-Down",self.ShiftLineDown)
        self.editmenu.AddCommand("Copy Line Up","Shift-Alt-Up",self.CopyLineUp)
        self.editmenu.AddCommand("Shift Line Up","Alt-Up",self.CopyLineDown)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)



    def ConfigureViewMenu(self):
        """ [Setup the view menu cascade of the Menubar] """
        self.viewmenu= ViewMenuOptions(self.menubar)

        self.viewmenu.AddCommand("Show Line Numbers",Accelerator="Ctrl-Shift-L",Command=self.ToggleLineNumbers)
        self.viewmenu.AddCommand("Show Directory",Accelerator="Ctrl-B",Command=self.ToggleDirectory)
        self.viewmenu.AddCommand("Show Logs",Accelerator="Shift+F2",Command=self.DisplayLogs)
        
        self.viewmenu.Separator()
        
        self.viewmenu.AddCommand("Full Screen",Accelerator="F11",Command=self.FullScreen)
        self.viewmenu.AddCommand("Zen Mode",Accelerator="Ctrl-Alt-F",Command=self.ZenMode)

        self.menubar.add_cascade(label="View", menu=self.viewmenu)



    def ConfigureCompileMenu(self):
        """ [Setup the compile menu cascade of the Menubar] """
        self.compilemenu = ComplieMenuOptions(self.menubar)
        self.compilemenu.AddCommand("Compile",self.Compile,"Ctrl-F5")
        self.compilemenu.AddCommand("Create New Console",self.CreateNewConsole,"Ctrl-Shift-C")
        self.menubar.add_cascade(label="Compile",menu = self.compilemenu)



    def ConfigureHelpMenu(self):
        """ [Setup the help menu cascade of the Menubar] """
        self.helpmenu = HelpMenuOptions(self.menubar)
        self.helpmenu.AddCommand("About","",self.infoabout)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)



    def ConfigureSettingsMenu(self):
        self.settingsmenu = SettingsMenuOptions(self.menubar)
        self.settingsmenu.AddCommand("Settings","Ctrl+,",self.Settings)
        self.menubar.add_cascade(label="Settings",menu=self.settingsmenu)



    def Settings(self,*args):
        
        # This needs a class on its own,will see it later!
        self.settingswindow = Toplevel(self.master)

        #Lines below this are to be made into a class(inherited from frame --> main things and layout will be decided later!!) 
        self.settingswindow.geometry("800x900+20+20")
        self.settingswindow.title("Settings")
        self.settingswindow.resizable(True,True)

        lb = Label(self.settingswindow,text="General Settings",foreground="blue",font=16)


        #ThemeSetting !
        self.O1 = StringVar()
        optionslist = self.master.themes
        self.O1.set(self.CurrentTheme)
        option1 = OptionMenu(self.settingswindow,self.O1,*optionslist,command=self.ChangeTheme)
        
        #General Setting !
        option2 = Button(self.settingswindow,text="Show Line Numbers",command=self.ToggleLineNumbers)
        option3 = Button(self.settingswindow,text="Show Treeview",command=self.ToggleDirectory)
        option4 = Button(self.settingswindow,text="Full Screen",command=self.FullScreen)
        option5 = Button(self.settingswindow,text="Zen Mode",command=self.ZenMode)
        

        lb.pack(pady=20)

        option1.pack()
        option2.pack()
        option3.pack()
        option4.pack()
        option5.pack()

        lb2 = Label(self.settingswindow,text="Shortcuts",foreground="blue",font=16)
        lb2.pack()
        for i in Shortcuts.ShortcutDict:
            l = Button(self.settingswindow,text = i)
            l.pack()



    def ChangeTheme(self,theme):
        self.master.set_theme(theme)



    def ConfigureAllMenus(self):
        """ [Configure all the menu cascades of the main menubar (Warning: Should be called before Menu)] """
        self.ConfigureFileMenu()
        self.ConfigureEditMenu()
        self.ConfigureViewMenu()
        self.ConfigureCompileMenu()
        self.ConfigureHelpMenu()
        self.ConfigureSettingsMenu()



    def TextSpace(self):
        """ [Setup the main textspace of the Editor] """
        self.frame = Frame(self.master,background=Color)
        self.ConfigureNoteBook()
        self.frame.pack(padx=5)
        self.shortcuts()



    def ConfigureNoteBook(self):
        """ [Setup the Notebook in the Editor-(The order of calling is very important)] """
        self.nbook = Notebook(self.frame,width=NBSpecs.Width,height=NBSpecs.Height,style=NBSpecs.Style,padding=NBSpecs.Padding)         
        
        self.ConfigureScrollBarandTextArea()
        self.nbook.add(self.txtarea, text=self.TabName())
        self.nbook.pack(side=NBSpecs.Side,expand=NBSpecs.Expand,padx=NBSpecs.PadX)
        # print(self.nbook.children.items())
        self.ConfigureLineNumbers()
        self.ConfigureLogsSetup()



    def ConfigureScrollBarandTextArea(self):
        """ [Setup necessay requirements for textarea(Setting up TextArea and Scrollbars)] """
        self.txtarea = TextArea(self.nbook)
        self.scrol_y = Scrollbar(self.frame,orient=VERTICAL,width=ScrollbarSpecs.WidthY,command=self.ScrollBoth,borderwidth=ScrollbarSpecs.BorderWY)
        self.scrol_x = Scrollbar(self.frame,orient=HORIZONTAL,width=ScrollbarSpecs.WidthX,command=self.txtarea.xview,borderwidth=ScrollbarSpecs.BorderWX)
        self.scrol_x.pack(side=BOTTOM,fill=ScrollbarSpecs.FillX,in_=self.txtarea)
        self.scrol_y.pack(side=RIGHT, fill=ScrollbarSpecs.FillY)
        self.txtarea.pack(fill=NONE, side=RIGHT)
        self.TagBindsForTextArea()



    def TagBindsForTextArea(self,*args):
        TagTokenKeyWords(self.txtarea)
        TagTokenNames(self.txtarea)
        TagTokenOperators(self.txtarea)
        TagTokenPunctuation(self.txtarea)
        TagTokenComments(self.txtarea)
        TagTokenLiterals(self.txtarea)
        TagTokenErrors(self.txtarea)



    def UpdateOnChangeinTextArea(self,*args):
        # print("It is called now!!")
        t = ThreadSafe(target=self.DrawLineNumberCanvas(),name="Thread5")
        t.start()
        t2 = ThreadSafe(target=self.SyntaxHighlighting()) 
        t2.start()
        # self.DrawLineNumberCanvas()
        # self.SyntaxHighlighting()



    def ConfigureLineNumbers(self):
        """ [Setup necessay requirements for textarea(Setting up Linenumbers)] """
        self.linenumbers = Canvas(self.frame,width=50,background=Color)
        self.linenumbers.pack(side=RIGHT,fill=Y,expand=TRUE,pady=(33,0))
        


    def ConfigureLogsSetup(self):
        """ [Setup necessay requirements for textarea(Setting up Logs widget's TextArea and Scrollbar)] """
        self.logstext = Text(self.frame,width=900,height=10,foreground="red",font="bold")        
        self.logstext.pack(side = BOTTOM,in_=self.txtarea)
        #Just have to place it in logstext window side
        self.logstext.insert("1.0","Logs:")
        self.logstext.config(state=DISABLED,background=Color)



    def SideTreeViewSpace(self):
        """ [Setup the treeview(directory manager) in the Editor] """
        self.treeview = Treeview(self.frame,style= TreeviewSpecs.Style, selectmode=TreeviewSpecs.Selectmode)
        self.Name = "Folder"
        
        self.btn = Button(self.treeview,text="Open File",command=self.OpenFolder)
        self.btn.place(relx=0.5,rely=0.5,anchor="center") 
        
        self.treeview.heading(TreeviewSpecs.RootHead, text=self.Name, anchor=W)

        self.CallTreeRoot()
        self.PackTreeview()
        self.treeview.bind("<<TreeviewSelect>>",self.Selected)
        self.treeview.bind("<<TreeviewOpen>>",self.Open)
        self.treeview.bind("<<TreeviewClose>>",self.Closed)
        #After this adding tabs etc would be easy ! 



    def PackTreeview(self):
        """ [Pack the treeview in the editor] """
        self.treeview.pack(side= TreeviewSpecs.Side,expand=TreeviewSpecs.Expand, fill=TreeviewSpecs.Fill,padx=TreeviewSpecs.PadX)



    def DrawLineNumberCanvas(self,*args):
        """ [Setup the line numbers to the side of the Editor.(WARNING: Before editing line numbers make sure to make the state normal)] """
        self.linenumbers.config(state=NORMAL)
        self.linenumbers.delete(ALL)
        i = self.txtarea.index("@0,0")
        while True:
            dline = self.txtarea.dlineinfo(i)
            if dline is None : break
            y = dline[1]
            linenum,column = i.split(".")
            self.linenumbers.create_text(10,y,anchor=NW,text=linenum,font=TextFontEditor.Font(),justify=RIGHT)
            i = self.txtarea.index("{}+1line".format(i))
        self.linenumbers.config(state=DISABLED)



    def UpdateScrollY(self,first,last,type=None):
        """ [Update the scrollbar to move along the Y direction in text area(Both text and line numbers)] """
        self.txtarea.yview_moveto(first)
        self.scrol_y.set(first,last)



    def ScrollBoth(self,action,position,type=None):
        """ [Scroll both line linenumbers and text area] """
        self.txtarea.yview_moveto(position)
    


    def TitleBar(self):
        """ [Setup the title bar of the Editor] """
        self.filename = None
        self.title = StringVar()
        self.title_bar = TitleBar(self.master,self.title,self.filename,Font=TextFontUI.Font())
        self.title_bar.pack(side=TOP, fill=BOTH)
        self.settitle()



    def StatusBar(self):
        """ [Setup the status bar of the Editor] """
        self.status = StringVar()
        self.statusbar = StatusBar(self.master,self.status,Font=TextFontUI.Font())
        self.ConfigureLabelsinStatusBar()
        self.statusbar.pack(side=BOTTOM, fill=BOTH)
        self.status.set("All Notifications are Here")



    def settitle(self):
        """ [Set the title of the Editor] """
        if self.filename:
            self.title.set(self.filename)
        else:
            self.title.set("Untitled")
    


    def ConfigureLabelsinStatusBar(self):
        """ [Setup necessary text that is to be displayed on StatusBar] """

        self.labeltext = LineColumnLabel(self.master,Text="Line:{} Col:{}".format(1,1),Font=TextFontUI.Font())
        self.langtext = LanguageLabel(self.master,"Plaintext",Font=TextFontUI.Font())    
        self.complietext = CompilerLabel(self.master,"",Font=TextFontUI.Font())

        self.complietext.pack(side=RIGHT,padx=20,in_=self.statusbar)
        self.langtext.pack(side=RIGHT,padx=20,in_=self.statusbar)
        self.labeltext.pack(side=RIGHT,padx=20,in_=self.statusbar)
            


    def newfile(self, *args):
        """ [Erase the contents of the textarea] """
        self.ClearLineNumbers()
        if not self.IsTextAreaEmpty():  
            op = messagebox.askyesno(Errors.ErrorsDictErrorHeadings["UnsavedData"],Errors.ErrorsDictMessage["UnsavedData"])
            if op:
                self.ClearTextArea()
                self.DrawLineNumberCanvas()



    def ClearTextArea(self):
        """ [Clear the text are of the editor] """
        self.txtarea.delete("1.0", END)
        self.filename = None
        self.settitle()
        self.status.set("New File Created")



    def openfile(self, *args):
        """ [Open a file from the computer into the editor] """
        try:
            OpenedFile = filedialog.askopenfile(title=OpenFileDialog.title, filetypes=OpenFileDialog.filetypes)
            if OpenedFile:
                self.ClearTextArea()
                with open(OpenedFile.name, OpenedFile.mode) as infile:
                    for line in infile:
                        self.DrawLineNumberCanvas()
                        self.txtarea.insert(END, line)    

                self.filename = OpenedFile.name
                self.SetLanguageinStatus()
                self.settitle()
                self.CallTreeRoot() 
                self.SyntaxHighlighting()
                print("Is it Highlighted!! ?? ")
                # self.nbook.tab()
                
                if not self.IsTreeViewEmpty():
                    self.RemoveButtoninTreeview()

                self.status.set("Opened Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e)
            self.DeleteTreeContents()



    def savefile(self, *args):
        """ [Save the file] """
        try:
            if self.filename:
                data = self.txtarea.get("1.0", END)
                with open(self.filename,"w") as outfile:
                    outfile.write(data)
                self.settitle()
                self.status.set("Saved Successfully")
            else:
                self.saveasfile()
        except Exception as e:
            messagebox.showerror("Exception", e)



    def saveasfile(self, *args):
        """ [Save file that is not previously saved.] """
        try:
            untitledFile = filedialog.asksaveasfilename(title=SaveasFileDialog.title, defaultextension=SaveasFileDialog.defaultExt, 
            initialfile=SaveasFileDialog.defaultFile, filetypes=SaveasFileDialog.filetypes)
            
            data = self.txtarea.get("1.0", END)
            with open(untitledFile, "w") as outfile:
                outfile.write(data)
            self.filename = untitledFile

            self.settitle()
            self.SetLanguageinStatus()
            self.status.set("Saved Successfully")
        
        except Exception as e:
            messagebox.showerror("Exception", e)



    def DisplayLogs(self,*args):
        """ [Toggle(Show/Hide) the Logs widget] """
        if self.IsLogsMapped():
            self.logstext.pack_forget()
        else:
            self.logstext.pack(side=BOTTOM,in_=self.txtarea)        



    def IsLogsMapped(self):
        """ [Check wheather the Logs widget is mapped in the Editor or not] """
        return self.logstext.winfo_ismapped()



    def exit(self, *args):
        """ [Exit from the editor] """
        op = messagebox.askyesno(Errors.ErrorsDictErrorHeadings["UnsavedData"], Errors.ErrorsDictMessage["UnsavedData"])
        if op > 0:
            self.master.destroy()
        return



    def cut(self, *args):
        """ [Cut text from the Editor(Control-X)] """
        Cut(self.txtarea).GenerateEvent()



    def copy(self, *args):
        """ [Copy text from the Editor(Control-C)] """
        Copy(self.txtarea).GenerateEvent()



    def paste(self, *args):
        """ [Paste text to the Editor(Control-V)] """
        Paste(self.txtarea).GenerateEvent()



    def undo(self, *args):
        """ [Undo the last action(Control-Z)] """
        try:
            Undo(self.txtarea).GenerateEvent()
        except Exception:
            pass   



    def redo(self,*args):
        """ [Undo the last action(Control-Y/Control-Shift-Z)] """
        try:
            Redo(self.txtarea).GenerateEvent()
        except Exception:
            pass



    def infoabout(self):
        """ [Show information about the Editor in a infobox.] """
        messagebox.showinfo(Information.MessageHeadings["AboutInfo"],Information.MessageContents["AboutInfo"])



    def FullScreen(self,*args):
        """ [Full screen the editor.(F11)] """
        if self.IsNotFullScreen():
            self.master.attributes("-fullscreen",True)
        else:
            self.EscapeFullScreen()    



    def IsNotFullScreen(self,*args):
        return not self.master.attributes("-fullscreen")



    def EscapeFullScreen(self,*args):
        """ [Exit from full screen.(Escape)] """
        self.master.attributes("-fullscreen",False)



    def ZenMode(self,*args):
        """ [View editor in ZenMode-no extra widgets mapped,only textspace.(Control-Alt-F)] """
        #Try reversing the things already done using the same button,makes it more user freindly!
        if self.IsDirectoryMapped():
            self.ToggleDirectory()    
        if self.IsLineWindowMapped():
            self.ToggleLineNumbers()
        if self.IsLogsMapped():
            self.DisplayLogs()        
        if self.IsNotFullScreen():
            self.FullScreen()



    def ClearLineNumbers(self):
        """ [Clear the line numbers on the linenumbers widget.] """
        self.linenumbers.delete("2.0",END)



    def Eventloop(self,*args):
        """ [Function called on any keypress(Not Complete)] """
        index = self.GetIndexLineColumnTextArea()
        # print((self.txtarea.get(index,"{} lineend".format(index))))
        if (self.txtarea.get(index,"{} lineend".format(index))):
            pass

        
        pass



    def ToggleDirectory(self,*args):
        """ [Show/Hide the treeview-directory manager.(Control-B)] """
        if self.IsDirectoryMapped():
            self.treeview.pack_forget()
        else:
            if self.IsLineWindowMapped():
                self.treeview.pack(side=LEFT,expand=True, fill=BOTH,after=self.linenumbers)
            else:
                self.treeview.pack(side=LEFT,expand=True, fill=BOTH)



    def IsDirectoryMapped(self):
        """ [Check if treeview is mapped in the window or not] """
        return self.treeview.winfo_ismapped()



    def IsLineWindowMapped(self):
        """ [Check if linenumbers are mapped in the window or not] """
        return self.linenumbers.winfo_ismapped()



    def shortcuts(self):
        """ [Calls the BindAll method of the Editor] """
        self.BindAllShortcuts()



    def BindAllShortcuts(self):
        """ [Bind all the shorcuts of the Editor] """

        BindShortcuts(self.master, "Exit", self.exit)
        BindShortcuts(self.txtarea, "Undo", self.undo)
        BindShortcuts(self.txtarea,"Redo",self.redo)
        BindShortcuts(self.txtarea,"Comment Line",self.CommentBlock)
        BindShortcuts(self.txtarea,"Compile",self.Compile)
        BindShortcuts(self.txtarea,"LineCol",self.UpdateLineandColumn)
        BindShortcuts(self.txtarea,"ShiftLineUp",self.ShiftLineUp)
        BindShortcuts(self.txtarea,"ShiftLineDown",self.ShiftLineDown)
        BindShortcuts(self.txtarea,"CopyLineUp",self.CopyLineUp)
        BindShortcuts(self.txtarea,"CopyLineDown",self.CopyLineDown)
        BindShortcuts(self.txtarea,"InsertMultiComment",self.InsertMultiSingleLine)
        # BindShortcuts(self.txtarea,"Keywords",self.SyntaxHighlighting) Checking for performance
        BindShortcuts(self.txtarea,"Brackets",self.OpenCloseComplete)
        BindShortcuts(self.txtarea,"QuotesD",self.SymmetericComplete)
        BindShortcuts(self.txtarea,"QuotesS",self.SymmetericComplete)
        BindShortcuts(self.txtarea,"SquareB",self.OpenCloseComplete)
        BindShortcuts(self.txtarea,"CurlyB",self.OpenCloseComplete)
        # BindShortcuts(self.txtarea,"PointyB",self.OpenCloseComplete) These are used in comparision,(can be enabled)
        BindShortcuts(self.txtarea,"Change",self.UpdateOnChangeinTextArea)
        # BindShortcuts(self.txtarea,"AngleBracketClose",self.CheckCloseCharacter) Not necessary for C/C++
        BindShortcuts(self.txtarea,"RoundBracketClose",self.CheckCloseCharacter)
        BindShortcuts(self.txtarea,"SquareBracketClose",self.CheckCloseCharacter)
        BindShortcuts(self.txtarea,"CurlyBracketClose",self.CheckCloseCharacter)
        BindShortcuts(self.txtarea,"EnterConfig",self.ConfigEnter)
        BindShortcuts(self.txtarea,"IndentColon",self.AutoIndent)
        BindShortcuts(self.txtarea,"Tabs",self.Tab)


        #Master/Functions of the editor
        
        BindShortcuts(self.master, "New", self.newfile)
        BindShortcuts(self.master, "Open", self.openfile)
        BindShortcuts(self.master, "Save", self.savefile)
        BindShortcuts(self.master, "SaveAs", self.saveasfile)
        BindShortcuts(self.master,"CreateConsole",self.CreateNewConsole)
        BindShortcuts(self.master,"Show Line Numbers",self.ToggleLineNumbers)
        BindShortcuts(self.master,"Full Screen",self.FullScreen)
        BindShortcuts(self.master,"Normal Screen",self.EscapeFullScreen)
        BindShortcuts(self.master,"Hide Directory",self.ToggleDirectory)
        BindShortcuts(self.master,"Zen Mode",self.ZenMode)
        BindShortcuts(self.master,"Logs",self.DisplayLogs)
        BindShortcuts(self.master,"Settings",self.Settings)
        BindShortcuts(self.master,"Close",self.exit)



    def Tab(self,event):
        self.txtarea.insert(INSERT,' '*4)
        return "break"



    def ConfigEnter(self,args):
        """ [Remove the tag from single line comments!!] [Some problem in space to tabs]"""
        index = self.GetIndexLineColumnTextArea()
        line,col = self.GetLineandColumnofTextArea()
        # print(self.txtarea.tag_ranges("Token.Comment.Single"))
        self.txtarea.tag_remove("Token.Comment.Single","{}.0".format(line),END)
        data = self.txtarea.get("{} linestart".format(index),"{} lineend".format(index))
        currentIndent = len(data) - len(data.lstrip())
        # print(currentIndent)
        self.txtarea.insert(INSERT,"\n{}".format(" "*currentIndent))
        return "break"



    def CheckCloseCharacter(self,args):
        """ By mistake, sometimes we press the closing bracket even when autocomplete is on- this is a small patch on it """
        if self.OpenCloseGood:
            return "break"    



    def OpenCloseComplete(self,args):
        # print(args)
        """ [Complete the opening and closing of the symbols that are mirror image(brackets and other)] """
        offsetDict={"(":1,"{":2,"[":2,"<":2}
        self.OpenCloseGood = 0
        index = self.GetIndexLineColumnTextArea()
        if not self.txtarea.tag_ranges(SEL):
            self.txtarea.edit_separator()
            self.txtarea.insert(index,chr(ord(args.char)+offsetDict[args.char])) #Most of open close characters are off by one
            self.OpenCloseGood = 1
            self.txtarea.mark_set(INSERT,index)
        else:
            txt = self.txtarea.selection_get()
            self.txtarea.edit_separator()
            self.txtarea.insert(INSERT,"{}{}{}".format(args.char,txt,chr(ord(args.char)+offsetDict[args.char])))
            self.txtarea.edit_separator()
            self.txtarea.delete(SEL_FIRST,SEL_LAST)
            index = self.GetIndexLineColumnTextArea()
            self.txtarea.mark_set(INSERT,"{}-1c".format(index))
            return "break" 
        self.OpenCloseGood = 0    



    def GetIndexLineColumnTextArea(self):
        line,col = self.GetLineandColumnofTextArea()
        return "{}.{}".format(line,col)



    def SymmetericComplete(self,args):
        """ [Complete the opening and closing of the symbols that are similar] """
        if not self.txtarea.tag_ranges(SEL):
            index = self.GetIndexLineColumnTextArea()
            self.txtarea.edit_separator()
            self.txtarea.insert(index,args.char)
            self.txtarea.mark_set(INSERT,index)
        else:
            txt = self.txtarea.selection_get()
            self.txtarea.edit_separator()
            self.txtarea.insert(INSERT,"{}{}{}".format(args.char,txt,args.char))
            self.txtarea.edit_separator()
            self.txtarea.delete(SEL_FIRST,SEL_LAST)
            index = self.GetIndexLineColumnTextArea()
            self.txtarea.mark_set(INSERT,"{}-1c".format(index))
            return "break"



    def CreateNewConsole(self,*args):
        if self.filename:
            cnl = Console(self.filename)
            cnl.NewConsoleLaunch()
        else:
            messagebox.showerror("No folder opened","Open a folder first")



    def ToggleLineNumbers(self,*args):
        """ [Show/Hide the line numbers widget] """
        if self.IsLineWindowMapped():
            self.linenumbers.pack_forget()
        else:
            if self.IsDirectoryMapped():
                self.linenumbers.pack(side = RIGHT,fill = Y,before=self.treeview,pady=(40,0),padx=3)
            else:    
                self.linenumbers.pack(side = RIGHT,fill = Y,after=self.nbook,pady=(40,0),padx=3)



    def CommentBlock(self,*args):
        """ [Comment a line in the text space.(Control-C)] """
        line,col = self.GetLineandColumnofTextArea()
        if self.CheckifSelectedText(): 
            self.InsertMultilineComment(SEL_FIRST,SEL_LAST)
        else:
            self.InsertSingleLineComment(line,col)
   


    def CheckifSelectedText(self):
        """ [Check if any text in text area is selected or not] """
        #Use tag_ranges(sel.first,sel.last)
        try:
            self.txtarea.selection_get()
            return True
        except Exception:
            return False    



    def GetLineandColumnofTextArea(self):
        """ [Retuns the index of the current line in the textspace.] """
        return  self.txtarea.index('insert').split(".")



    def InsertSingleLineComment(self,line,col):
        """ [Add the language specific(currently C,C++)identifier of the start of a single line comment in a line of textarea.] """
        self.txtarea.edit_separator()
        string = self.txtarea.get("{}.0".format(line),"{}.{}".format(line,LanguageC.LenSLC))
        if self.IsaCommentLine(string.strip()):
            self.UncommentLine(line)
        else:
            self.txtarea.insert("{}.0".format(line),LanguageC.SingleLineCommentsStart)
            # ,"{}.0".format(line)



    def InsertMultilineComment(self,startIndex:str,endIndex:str):
        """ [Add the language specific(currently C,C++)identifier of the start and end of a multi line comment in textarea.] """
        self.txtarea.edit_separator()
        if self.IsaMultilineComment(self.txtarea.get("{} linestart".format(startIndex),"{} lineend".format(endIndex))):
            self.UncommentBlock(startIndex,endIndex)
            self.txtarea.tag_delete("Token.Comment.Multiline")

        else:
            self.txtarea.insert("{} linestart".format(startIndex),LanguageC.MultilineCommentStart)
            self.txtarea.insert("{} lineend".format(endIndex),LanguageC.MultilineCommentEnd)
            self.TagBindsForTextArea()



    def UncommentLine(self,line):
        """ [Uncomment the line commented by CommentBlock ] """
        self.txtarea.edit_separator()
        self.txtarea.delete("{}.0".format(line),"{}.{}".format(line,LanguageC.LenSLC))
        self.txtarea.tag_remove("Token.Comment.Single","{}.0".format(line),"{}.0 lineend".format(line))



    def IsaMultilineComment(self,string:str):
        """ [Check if a block of text is a mutliline comment or not.] """
        return string.startswith(LanguageC.MultilineCommentStart) and string.endswith(LanguageC.MultilineCommentEnd)



    def UncommentBlock(self,first,last):
        """ [Uncomment the previously commented block of program.Edit:Improved version] """
        self.txtarea.edit_separator()
        self.txtarea.delete("{} linestart".format(first),"{} linestart +{}c".format(first,LanguageC.LenMLCStart))
        self.txtarea.delete("{} lineend -{}c".format(last,LanguageC.LenMLCEnd),"{} lineend".format(last))



    def InsertMultiSingleLine(self,*args):
        index = self.GetIndexLineColumnTextArea()
        self.txtarea.edit_separator()
        self.txtarea.insert("{} linestart".format(index),LanguageC.MultilineCommentStart)
        self.txtarea.insert("{} lineend".format(index),LanguageC.MultilineCommentEnd)



    def IsaCommentLine(self,string:str):
        """ [Check wheather the string is a comment line or not(used by-Comment/Uncomment).Currently supports C,C++] """
        return string.startswith(LanguageC.SingleLineCommentsStart)    



    def Compile(self,*args):  
        """ [Comile the code written in the text area(Currently supports C,C++)] """ 
        if self.filename:
            self.savefile()
            cmplObject = CompilerInterface(self.filename)
            Msg = cmplObject.CallCompiler()
            self.HighlightErrorLine(Msg)
            if not Msg:
                self.DisplayErrorMessageinLogs(Msg)
                self.UpdateTreeview()
                self.TagRemove()
                # self.ClearMessagesinLogs()

        elif self.IsTextAreaEmpty():
            messagebox.showerror(Errors.ErrorsDictErrorHeadings["EmptyTextCompile"],Errors.ErrorsDictMessage["EmptyTextCompile"])
        else: 
            self.savefile()

        def CheckMessage(self,Message):
            pass



    def UpdateTreeview(self):
        """ [Update the treeview] """
        self.DeleteTreeContents()
        self.CallTreeRoot()



    def IsTextAreaEmpty(self):
        """ [Check if the textarea is empty or not] """
        return len(self.txtarea.get("1.0",END))<=1



    def DisplayErrorMessageinLogs(self,msg:str):
        """ [Display error message in Logs widget in case of compilation error.] """
        self.logstext.config(state=NORMAL)    
        self.logstext.insert(END,"\n{}".format(msg))
        self.bell() 
        self.logstext.config(state=DISABLED,font="bold")    



    def ClearMessagesinLogs(self):
        """ [Clear the error messages in the Logs widget] """
        self.logstext.config(state=NORMAL)
        self.logstext.delete("2.0",END)
        self.logstext.config(state=DISABLED)



    def ShiftLineUp(self,*args):
        """ [Shift Lines Up(Alt + Uparrow)] """
        line,_ = self.GetLineandColumnofTextArea()
        curLine = self.txtarea.get("{}.0".format(line),"{}.0 lineend".format(line))
        aboveline = self.txtarea.get("{}.0".format(int(line)-1),"{}.0 lineend".format(int(line)-1))
        self.txtarea.edit_separator()
        self.txtarea.delete("{}.0".format(int(line)-1),"{}.0 lineend".format(int(line)-1))
        self.txtarea.insert("{}.0".format(int(line)-1),curLine)
        self.txtarea.edit_separator()
        self.txtarea.delete("{}.0".format(line),"{}.0 lineend".format(line))
        self.txtarea.insert("{}.0".format(line),aboveline)



    def ShiftLineDown(self,*args):
        """ [Shift Lines Down(Alt + Downarrow)] """
        line,_ = self.GetLineandColumnofTextArea()
        curLine = self.txtarea.get("{}.0".format(line),"{}.0 lineend".format(line))
        belowline = self.txtarea.get("{}.0".format(int(line)+1),"{}.0 lineend".format(int(line)+1))
        self.txtarea.delete("{}.0".format(int(line)+1),"{}.0 lineend".format(int(line)+1))
        self.txtarea.edit_separator()
        self.txtarea.insert("{}.0".format(int(line)+1),curLine)
        self.txtarea.delete("{}.0".format(line),"{}.0 lineend".format(line))
        self.txtarea.edit_separator()
        self.txtarea.insert("{}.0".format(line),belowline)



    def CopyLineUp(self,event):
        """ [Copy the contents of current line to the line above] """
        index = self.GetIndexLineColumnTextArea()
        self.CopyLineDown()
        self.txtarea.mark_set(INSERT,"{} lineend".format(index))
        return "break"



    def CopyLineDown(self,*args):
        """ [Copy the contents of the current line to the line below] """
        line,_ = self.GetLineandColumnofTextArea()
        totalLinesbelow = len(self.txtarea.get(self.GetIndexLineColumnTextArea(),END).split("\n"))+1
        # print(totalLinesbelow) Debug
        self.txtarea.insert(END,"\n")
        for i in range(totalLinesbelow,int(line)-1,-1):
            currline = self.txtarea.get("{}.0".format(i),"{}.0 lineend".format(i))
            self.txtarea.edit_separator()
            self.txtarea.delete("{}.0".format(i+1),"{}.0 lineend".format(i+1))
            self.txtarea.edit_separator()
            self.txtarea.insert("{}.0".format(i+1),currline) #Because the line is deleted
        return "break"



    def OpenFolder(self):
        """ [Binded function of the Button initially placed in treeview.Call the openfile method and destroys itself] """
        self.openfile()
        self.RemoveButtoninTreeview()



    def TraverseDir(self,parent,path):
        """ [Populate the treeview after opening a file(Currently nothing happens on selecting them.)] """
        for d in os.listdir(path):
            fullPath = os.path.join(path,d)
            isDir = os.path.isdir(fullPath)
            id = self.treeview.insert(parent,"end",text = d,open = False)
            if isDir:
                self.TraverseDir(id,fullPath)



    def DeleteTreeContents(self):
        """ [Delete the contents of the treeview.] """
        self.treeview.delete(list(self.treeview.get_children()))



    def CallTreeRoot(self):
        """ [Call the root folder of the treeview and call TraverseDir to populate it] """
        if len(self.treeview.get_children())>1:
            self.btn.destroy()    
        if self.filename:
            path =os.path.dirname(self.filename)
            node = self.treeview.insert("","end",text="Opened Folder", open=True)
            self.TraverseDir(node,path)



    def IsTreeViewEmpty(self):
        """ [Checks if the treeview is empty or not] """
        return len(self.treeview.get_children())<1



    def RemoveButtoninTreeview(self):
        self.btn.destroy()



    def TabName(self):
        """ [Returns the tab name that is to be displayed on the notebook tab.] """
        return os.path.basename(self.filename) if self.filename else "Untitled"



    def Refresh(self):
        """ [Refresh some functions that might need it(Updating values of some instances).] """
        self.TabName()
        self.settitle()
        self.status.set("Refresh")



    def AutoIndent(self,event):
        """ [Bounded function for colon(:) for indentation] """
        line = self.txtarea.get("insert linestart", "insert lineend")
        current_indent = len(line) - len(line.lstrip()) 
        new_indent = current_indent+MasterProperties.TabSize
        self.txtarea.insert(INSERT,"{}\n{}".format(event.char," "*new_indent))
        return "break"



    def SyntaxHighlighting(self,*args):
        """ [Syntax highlighting for textarea - called on <<Change>> and runs on different thread(safe)] """
        index = self.GetIndexLineColumnTextArea()
        self.txtarea.mark_set("range_start", "{} linestart".format(index))
        data = self.txtarea.get("{} linestart".format(index), "{} lineend".format(index))
        for token, content in lex(data, CLexer()):
            self.txtarea.mark_set("range_end", "range_start + {}c".format(len(content)))
            if str(token) == "Token.Comment.Single":
                self.txtarea.tag_add(str(token), "range_start", "range_start lineend")
            self.txtarea.tag_add(str(token), "range_start", "range_end")
            self.txtarea.mark_set("range_start", "range_end")
            # print(content)



    def HighLightOpenedFile(self,*args):
        self.txtarea.mark_set("range_start", "1.0")
        data = self.txtarea.get("1.0", END)
        for token, content in lex(data, CLexer()):
            self.txtarea.mark_set("range_end", "range_start + {}c".format(len(content)))
            self.txtarea.tag_add(str(token), "range_start", "range_end")
            self.txtarea.mark_set("range_start", "range_end")



    def HighlightErrorLine(self,Message:str):
        try:
            emess = self.ExtractErrorMessage(Message)
            idxStart = self.txtarea.search(emess,index="1.0",stopindex=END)
            if idxStart:
                self.txtarea.tag_add("Error",idxStart,idxStart+" lineend")
                self.txtarea.tag_configure("Error",foreground="red")
                l,_ = idxStart.split(".")
                self.linenumbers.tag_add("Glow","{}.0".format(l),"{}.0 lineend".format(l))
                self.linenumbers.tag_configure("Glow",foreground="red")
        except Exception as e:
            print(e)



    def ExtractErrorMessage(self,Message):
        """ [Find the error message in logs text.] """
        lineseq = Message.split("\n")
        emess = lineseq[2].strip()
        return emess



    def TagRemove(self):
        """ [Remove the highlight text tag from the textarea] """
        self.txtarea.tag_delete("Error")
        # self.linenumbers.tag_delete("Glow")



    def UpdateLineandColumn(self,*args):
        """ [Update the line number and column in StatusBar text.] """
        line,column = self.GetLineandColumnofTextArea()
        self.labeltext.config(text="Line:{} Col:{}".format(line,column))



    def SetLanguageinStatus(self,*args):
        """ [Set the language currently working on in the textarea(Currently only supports C/C++)] """
        self.extension = (self.filename.split(".")[1]).lower()
        if self.extension =="c" or self.extension =="cpp":
            self.langtext.config(text="C/C++")
            self.complietext.config(text="GNU/GCC",font=5)



    def Selected(self,event):
        """ [Treeview Select bound function.] """
        item = self.treeview.selection()[0]
        tabName = self.treeview.item(item,"text")



    def Open(self,event):
        """ [Treeview Open bounded function] """
        item = self.treeview.selection()[0]
        # print("Opened",self.treeview.item(item,"open"))
        #Add tab adding stuff here !!
        tabName = self.treeview.item(item,"text")
        newTab = TextArea(self.nbook)
        # print(self.nbook.children)
        self.nbook.add(newTab,text=tabName)
        raise NotImplementedError    



    def Closed(self,event):
        """ [Treeview Closed bound function] """
        print("Closed",event)
        raise NotImplementedError

    
    
    def TagBindText(self,*args):
        """ [Testing function for selection tag] """
        self.txtarea.tag_configure(SEL,foreground="red",underline=True)



class FileDialog:
    """ Base class for Dialogs """
    title = ""
    filetypes = (("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"),("C Files","*.c"),("CPP Files","*.cpp"))



class OpenFileDialog(FileDialog):
    """ [Derived class for opening a file dialog] """
    title = "Select File"



class SaveasFileDialog(FileDialog):
    """ [Derived class for closing a file dialog] """
    title = "Save File as"
    defaultExt = ".txt"
    defaultFile = "Untitled.txt"



class TreeviewSpecs:
    """ [Abstract Class containing specifications of Treeview widget(may derive from abc)] """
    Style = "Treeview"
    Selectmode="extended"
    RootHead = "#0"
    Anchor = W
    Side=RIGHT
    Expand=True
    Fill=BOTH
    PadX=2



class NBSpecs:
    """ [Abstract Class containing specifications of Notebook widget(may derive from abc)] """
    Width=1450
    Height=1300
    Style = "TNotebook"
    Side = RIGHT
    Expand = True
    PadX = 4
    Padding = (0,0,0,0)



class ScrollbarSpecs:
    """ [Abstract Class containing specifications of Scrollbar widget(both X and Y)[may derive from abc]] """
    WidthX = 30
    WidthY = 30
    BorderWY = 5
    BorderWX = 5
    SideX = BOTTOM
    SideY = RIGHT
    FillX = X
    FillY = Y



class Shortcuts:
    """ [Abstract Class containing shorcuts and event as a dictionary for textarea(may derive from abc)] """
    ShortcutDict = {"Cut": "<Control-x>", "Copy": "<Control-c>", "Paste": "<Control-v>", "Undo": "<Control-z>","Redo":"<Control-Z>" ,"Exit": "<Control-e>",
                    "SaveAs": "<Control-S>", "Save": "<Control-s>", "Open": "<Control-o>", "New": "<Control-n>","DrawLine":"<Key>,<Return>","RemoveLine":"<Key>"
                    ,"Comment Line":"<Control-m>","Show Line Numbers":"<Control-L>","Compile":"<Control-F5>","Full Screen":"<F11>","Normal Screen":"<Escape>",
                    "Hide Directory":"<Control-b>","Zen Mode":"<Control-Alt-f>","Logs":"<Shift-F2>","LineCol":"<Any-KeyPress>",
                    "Settings":"<Control-,>","Close":"<Alt-F4>","ShiftLineUp":"<Alt-Up>","ShiftLineDown":"<Alt-Down>","CopyLineUp":"<Shift-Alt-Up>",
                    "CopyLineDown":"<Shift-Alt-Down>","InsertMultiComment":"<Shift-Alt-A>","Keywords":"<KeyRelease>","CreateConsole":"<Control-C>",
                    "Brackets":"<KeyPress-parenleft>","QuotesD":"<KeyPress-quoteright>","QuotesS":"<KeyPress-quotedbl>","SquareB":"<[>","CurlyB":"<{>",                    
                    "PointyB":"<KeyPress- < >","Change":"<<Change>>","AngleBracketClose":"<KeyPress- > >","RoundBracketClose":"<KeyPress- ) >","SquareBracketClose":"<KeyPress- ] >",
                    "CurlyBracketClose":"<KeyPress- } >","EnterConfig":"<Return>","IndentColon":"<:>","Tabs":"<Tab>",
                    }



class BindShortcuts(Shortcuts):
    """ [Class for binding shorcuts for the editor(both text and general purpose).] """
    def __init__(self, TextWidget: Text, Option: str, Callable,Add=True) -> None:
        TextWidget.bind(self.ShortcutDict[Option], Callable,add=Add)



class Console:
    def __init__(self,directory:str) -> None:
        """ [Calls] """
        self.dir =  os.path.dirname(directory)



    def CreateConsole(self):
        """ [Creates a new console,(Runs on differnet thread)] """
        process = subprocess.Popen(["cmd"],creationflags=subprocess.CREATE_NEW_CONSOLE,cwd = self.dir,close_fds=True)
        out,err = process.communicate()
        process.kill()
        process.terminate()



    def NewConsoleLaunch(self,*args):    
        t = ThreadSafe(target=self.CreateConsole,name="Thread2")
        t.start()



class Option:
    """ [Abstract class for options] """
    pass



class EditOption(Option):
    """ [Class for edit options] """
    def __init__(self,textArea,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.TextArea = textArea

    def GenerateEvent(self): #Override this in derived classes
        pass



class Undo(EditOption):
    """ [Class for generating Undo Event.] """
    def __init__(self, textArea, *args, **kwargs) -> None:
        super().__init__(textArea, *args, **kwargs)
    
    #DRY: The Undo Redo Mechanism is built into Textby default,don't reinvent the wheel(DRW)
    def GenerateEvent(self): 
        self.TextArea.get("1.0",END)

        self.TextArea.edit_undo()



class Cut(EditOption):
    """ [Class for generating Cut Event.] """
    def __init__(self, textArea, *args, **kwargs) -> None:
        super().__init__(textArea, *args, **kwargs)

    def GenerateEvent(self,*args):
        self.TextArea.event_generate(Events.EventDict["Cut"])    



class Copy(EditOption):
    """ [Class for generating Copy Event.] """
    def __init__(self, textArea, *args, **kwargs) -> None:
        super().__init__(textArea, *args, **kwargs)

    def GenerateEvent(self,*args):
        self.TextArea.event_generate(Events.EventDict["Copy"])    



class Paste(EditOption):
    """ [Class for generating Paste Event.] """
    def __init__(self, textArea, *args, **kwargs) -> None:
        super().__init__(textArea, *args, **kwargs)

    def GenerateEvent(self,*args):
        self.TextArea.event_generate(Events.EventDict["Paste"])    



class Redo(EditOption):
    """ [Class for generating Redo Event.] """
    def __init__(self, textArea, *args, **kwargs) -> None:
        super().__init__(textArea, *args, **kwargs)

    def GenerateEvent(self):
        self.TextArea.edit_redo()   



class Events:
    """ [Class containing events in the form of dictionary.] """
    EventDict={"Cut":"<<Cut>>","Copy":"<<Copy>>","Paste":"<<Paste>>"}



class MasterProperties:
    """ [Class containing root properties.] """
    Title = "Generic Text Editor"
    Geometry = "1800x900"
    Themes = {'ThemeBREEZE': 'breeze', 'ThemeALT': 'alt', 'ThemeBLACK': 'black', 'ThemeSCIDMINT': 'scidmint', 'ThemePLASTIK': 'plastik', 'ThemeXPNATIVE': 'xpnative', 'ThemeCLASSIC': 'classic', 'ThemeKERAMIK': 'keramik', 'ThemeKROC': 'kroc', 'ThemeDEFAULT': 'default', 'ThemeITFT1': 'itft1', 'ThemeCLEARLOOKS': 'clearlooks', 'ThemeSCIDGREEN': 'scidgreen', 'ThemeYARU': 'yaru', 'ThemeELEGANCE': 'elegance', 'ThemeSMOG': 'smog', 'ThemeEQUILUX': 'equilux', 'ThemeSCIDSAND': 'scidsand', 'ThemeSCIDGREY': 'scidgrey', 'ThemeRADIANCE': 'radiance', 'ThemeARC': 'arc', 'ThemeAQUATIVO': 'aquativo', 'ThemeUBUNTU': 'ubuntu', 'ThemeBLUE': 'blue', 'ThemeSCIDBLUE': 'scidblue', 'ThemeWINNATIVE': 'winnative',
              'ThemeADAPTA': 'adapta', 'ThemeWINXPBLUE': 'winxpblue', 'ThemeCLAM': 'clam', 'ThemeSCIDPINK': 'scidpink', 'ThemeVISTA': 'vista', 'ThemeSCIDPURPLE': 'scidpurple'}
    TabSize = 2



class TextFontUI:
    """ [Class containing font specification of UI (as static variables,could be overrided if values are passed as instance).] """
    FontSpec = {"Font": "Times New Roman", "Size": 14, "Weight": "normal",
                "Slant": "roman", "Underline": 0, "Overstrike": 0}

    def __init__(self, FontName: str, FontSize: int, FontWeight: str, FontSlant: str, Underline: bool, Overstrike: bool) -> None:
        TextFontUI.FontSpec["Font"] = FontName
        TextFontUI.FontSpec["Size"] = FontSize
        TextFontUI.FontSpec["Weight"] = FontWeight
        TextFontUI.FontSpec["Slant"] = FontSlant
        TextFontUI.FontSpec["Underline"] = Underline
        TextFontUI.FontSpec["Overstrike"] = Overstrike


    @classmethod
    def Font(cls):
        return (cls.FontSpec["Font"],cls.FontSpec["Size"],cls.FontSpec["Weight"],)

    @classmethod
    def FontTag(cls):
        return (cls.FontSpec["Font"],cls.FontSpec["Size"],cls.FontSpec["Weight"],cls.FontSpec["Slant"],cls.FontSpec["Underline"],cls.FontSpec["Overstrike"])

        

class TextFontEditor:
    """ [Class containing font specification of the editor (as static variables,could be overrided if values are passed as instance).] """
    FontSpec = {"Font": "Consolas", "Size": 15, "Weight": "normal",
                "Slant": "roman", "Underline": False, "Overstrike": False}

    def __init__(self, FontName: str, FontSize: int, FontWeight: str, FontSlant: str, Underline: bool, Overstrike: bool) -> None:
        TextFontEditor.FontSpec["Font"] = FontName
        TextFontEditor.FontSpec["Size"] = FontSize
        TextFontEditor.FontSpec["Weight"] = FontWeight
        TextFontEditor.FontSpec["Slant"] = FontSlant
        TextFontEditor.FontSpec["Underline"] = Underline
        TextFontEditor.FontSpec["Overstrike"] = Overstrike
    
    @classmethod
    def Font(cls):
        return (cls.FontSpec["Font"],cls.FontSpec["Size"],cls.FontSpec["Weight"],)


    @classmethod
    def FontTag(cls):
        return (cls.FontSpec["Font"],cls.FontSpec["Size"],cls.FontSpec["Weight"],cls.FontSpec["Slant"],cls.FontSpec["Underline"],cls.FontSpec["Overstrike"])
        


class TitleBar(Label):
    """ [Class for creating Titlebar.(Dervided from Label)] """
    def __init__(self, Master,Textvariable,Filename,Font=3) -> None:
        super().__init__(master=Master,textvariable=Textvariable,font=Font,background=Color)

    def AdditionFeatures(self):
        raise NotImplementedError



class StatusBar(Label):
    """ [Class for creating Statusbar.(Dervided from Label)] """
    def __init__(self, Master,Textvariable,Font=3) -> None:
        super().__init__(master=Master,textvariable=Textvariable,font = Font,background=Color)

    def AdditionalFeatures(self):
        raise NotImplementedError



class LineColumnLabel(Label):
    """ [Class for creating Line and Column display in StatusBar.(Dervided from Label)] """
    def __init__(self,Master,Text,Font=5):
        super().__init__(master=Master,text=Text,font=Font)
        


class LanguageLabel(Label):
    """ [Class for creating language display in StatusBar.(Dervided from Label)] """
    def __init__(self,Master,Text,Font=5):
        super().__init__(master=Master,text=Text,font=Font)
        


class CompilerLabel(Label):
    """ [Class for creating compiler display in StatusBar.(Dervided from Label)] """
    def __init__(self,Master,Text,Font=5):
        super().__init__(master=Master,text=Text,font=Font)
                


class MenuOptions(Menu): 
    """ [Base Class for all menu options.] """
    def __init__(self, Menubar) -> None:
        super().__init__(master=Menubar,tearoff=False,background=Color)

    def AddCommand(self, Label, Accelarator, Command):
        self.add_command(label=Label, accelerator=Accelarator, command=Command)

    def Separator(self):
        self.add_separator()



class FileMenuOptions(Menu):
    """ [Class for file menu options.] """
    def __init__(self, Menubar) -> None:
        # Here in MenuBar, add the one created using MenuOptions.
        super().__init__(master=Menubar,font=TextFontUI.Font(),tearoff=False)

    def AddCommand(self, Label, Accelarator, Command):
        self.add_command(label=Label, accelerator=Accelarator, command=Command)

    def Separator(self):
        self.add_separator()



class EditMenuOptions(Menu):
    """ [Class for edit menu options.] """
    def __init__(self, Menubar) -> None:
        # Here in MenuBar, add the one created using MenuOptions.
        super().__init__(master=Menubar,font=TextFontUI.Font(),tearoff=False)

    def AddCommand(self, Label, Accelarator, Command):
        self.add_command(label=Label, accelerator=Accelarator, command=Command)

    def Separator(self):
        self.add_separator()



class HelpMenuOptions(Menu):
    """ [Class for help menu options.] """
    def __init__(self, Menubar) -> None:
        super().__init__(master=Menubar,font=TextFontUI.Font(),tearoff=False)

    def AddCommand(self, Label, Accelarator, Command):
        self.add_command(label=Label, accelerator=Accelarator, command=Command)

    def Separator(self):
        self.add_separator()



class AboutMenuOptions(Menu):
    """ [Class for about menu options.(Not Completed)] """
    def __init__(self,Menubar):
        super().__init__(master=Menubar,font=TextFontUI.Font(),tearoff=False)

    def AddCommand(self, Label,Command,Accelerator=str(None)):
        self.add_command(label=Label,accelerator=Accelerator,command=Command)

    def Separator(self):
        self.add_separator()    



class ComplieMenuOptions(Menu):
    """ [Class for compile menu options.] """
    def __init__(self, Menubar) -> None:
        super().__init__(master=Menubar,font=TextFontUI.Font(),tearoff=False)

    def AddCommand(self, Label,Command,Accelerator=str(None)):
        self.add_command(label=Label,accelerator=Accelerator,command=Command)

    def Separator(self):
        self.add_separator()



class ViewMenuOptions(Menu):
    """ [Class for view menu options.] """
    def __init__(self, Menubar) -> None:
        super().__init__(master=Menubar,font=TextFontUI.Font(),tearoff=False)

    def AddCommand(self, Label,Command,Accelerator=str(None)):
        self.add_command(label=Label, accelerator=Accelerator,command=Command)
    
    def Separator(self):
        self.add_separator()



class SettingsMenuOptions(Menu):
    """ [Class for settings menu options.] """
    def __init__(self, Menubar) -> None:
        super().__init__(master=Menubar,font=TextFontUI.Font(),tearoff=False)
    

    def AddCommand(self, Label, Accelarator, Command):
        self.add_command(label=Label,accelerator=Accelarator,command=Command)

    def Separator(self):
        self.add_separator()



class TextArea(Text):
    """ [Class derived from text for textarea.] """
    def __init__(self, Master,Relief=GROOVE, ColorBG="#FFFFFF", BorderWidth=5,Tabs="1c",BackGround = 'gray') -> None:        
        super().__init__(master=Master,font=TextFontEditor.Font(),relief=Relief,background=ColorBG,borderwidth=BorderWidth,undo=True,
        tabs=Tabs,inactiveselectbackground=BackGround,wrap=NONE,insertbackground="blue")
        self._orig = self._w + "_orig"
        self.tk.call('rename',self._w,self._orig)
        self.tk.createcommand(self._w,self._proxy)
    
    def _proxy(self,*args):
        cmd = (self._orig,)+args
        result = self.tk.call(cmd)
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):self.event_generate("<<Change>>", when="tail")
        return result

    

class CompileCode:
    """ [We will get the file as a path] For now only,extension is needed for C and C++,others are dynamically typed"""
    ComplileDict = {"c":"gcc","cpp":"g++"}
    
    def __init__(self,File:str) -> None:
        self.File = File
        self.extention = self.File.split(".")[1]
        self.FolderPath = os.path.dirname(self.File) 
        self.Name = os.path.basename(self.File)
        self.LogFile =  os.path.join(self.FolderPath,"Logs.txt")
        self.exefile = "{}".format(self.Name.split(".")[0])



    def Compile(self):
        """ If the compilation is Successful,does nothing if not then returns the Error Message
        UPDATE: Now Execute runs on different thread for parallel processing."""
        with open(self.LogFile,"w+") as file:
            try:
                subprocess.check_output([self.ComplileDict[self.extention],"-Wall",self.File,"-o",self.exefile],stderr=file) #For C and C++ only
                subprocess.call([self.ComplileDict[self.extention],"-Wall",self.File,"-o",self.exefile],cwd=self.FolderPath)
                self.ProcessExecute()
                file.seek(0)
                return "".join(file.readlines())
                #We will override Execute method for Python File.
            except subprocess.CalledProcessError as e:
                file.seek(0)  #This step is the key
                self.ErrMess = "".join(file.readlines())      
                return self.ErrMess
            except Exception as e:
                file.seek(0)  #This step is the key
                print(e,file=file)
                return e
    
    

    def ProcessExecute(self,*args):
        t = ThreadSafe(target=self.Execute,name="Thread3")
        t.start()



    def Execute(self):
        """ [Call the executable] """
        import time
        import trace

        t1 = time.time()
        # print(self.exefile,self.FolderPath)
        process = subprocess.Popen([self.exefile],creationflags=subprocess.CREATE_NEW_CONSOLE,cwd=self.FolderPath)
        out,err = process.communicate()
        t2 = time.time()
        finmess = "Process returned:{} Execution Time:{}s".format(out,(t2-t1))
        print(finmess)
        process.kill()
        process.terminate()



    def ExecutionMessage(self):
        return self.ErrMess



class Errors:
    """ [Class containing error messages in the form of dictionary.] """
    ErrorsDictErrorHeadings={"EmptyTextCompile":"Empty Text Error",
                             "EmptyTextComment":"Unselected Text Comment Error",
                             "UnsavedData":"Warning - Unsaved Data",}
    
    ErrorsDictMessage={"EmptyTextCompile" :"Only non-empty code could not be compiled",
                        "EmptyTextComment":"Cannot comment unselected text. Select the text to comment.",
                        "UnsavedData":"Warning: Unsaved Data will be lost"}



class Information:
    """ [Class containing information about the Editor.] """
    MessageHeadings={"AboutInfo":"About"}
    MessageContents={"AboutInfo":"Write something that changes your Text"}



class RunCCode(CompileCode):
    """ [Class for running C code] """
    def __init__(self, File) -> None:
        super().__init__(File)



class RunCPPCode(CompileCode):
    """ [Class for running C++ code] """
    def __init__(self, File: str) -> None:
        super().__init__(File)



class RunPythonCode(CompileCode):
    """ [Class for running Python code(Not Complete)] """
    pass



class CompilerInterface:
    """ [Call required compiler of the code in text area(currently only C and C++)] """
    RedirectDict = {"c":RunCCode,"cpp":RunCPPCode,"py":RunPythonCode}
    def __init__(self,File) -> None:
        self.File= File
        self.Extention = self.File.split(".")[1]

    def CallCompiler(self):
        cmplobj = CompilerInterface.RedirectDict[self.Extention](self.File)
        return cmplobj.Compile()



class Language:
    """ [Abstract class for defining any language.] """
    Keywords=[]  #This should be a list!
    Identifiers =[] #It might not be a list,we'll see later
    Strings=[]
    Operators=[]    
    Constants =[]
    SpecialCharacters=[]
    SingleLineCommentsStart = ""
    MultilineCommentStart = ""
    MultilineCommentEnd = ""



class LanguageC(Language):
    """ [Class with Specifications of C language] """
    SingleLineCommentsStart = "//"
    MultilineCommentStart = "/*"
    MultilineCommentEnd = "*/"
    LenSLC=len(SingleLineCommentsStart)
    LenMLCStart=len(MultilineCommentStart)
    LenMLCEnd=len(MultilineCommentEnd)



class LanguageCPP(Language):
    """ [Class with Specifications of C++ language] """

    SingleLineCommentsStart = "//"
    MultilineCommentStart = "/*"
    MultilineCommentEnd = "*/"
    LenSLC=len(SingleLineCommentsStart)
    LenMLCStart=len(MultilineCommentStart)
    LenMLCEnd=len(MultilineCommentEnd)



class SettingsWindow(Frame):
    """ [Class for settings window that is in Toplevel of editor(Not Complete).] """
    def __init__(self,master):
        super().__init__(master)
    
    def AddOption(self):
        pass



class TagTokens:
    """ [Base class for all tags that will be used for syntax highlighting-->(Containership is preferred over inheritance)] """
    def __init__(self,TextWidget:TextArea) -> None:
        self.text = TextWidget



class TagTokenKeyWords(TagTokens):
    """ [Class containing tag configurations for keywords token] """
    def __init__(self,TextWidget:TextArea) -> None:
        super().__init__(TextWidget=TextWidget)
        self.tw = TextWidget
        self.tw.tag_configure("Token.Keyword.Constant", foreground="blue",font=KeywordsFontDescription.FontTag())
        self.tw.tag_configure("Token.Keyword.Declaration", foreground="blue",font=KeywordsFontDescription.FontTag())
        self.tw.tag_configure("Token.Keyword.Namespace", foreground="blue",font=KeywordsFontDescription.FontTag())
        self.tw.tag_configure("Token.Keyword.Pseudo", foreground="blue",font=KeywordsFontDescription.FontTag())
        self.tw.tag_configure("Token.Keyword.Reserved", foreground="blue",font=KeywordsFontDescription.FontTag())
        self.tw.tag_configure("Token.Keyword.Type", foreground="blue",font=KeywordsFontDescription.FontTag())
        self.tw.tag_configure("Token.Keyword", foreground="blue",font=KeywordsFontDescription.FontTag())
        self.tips = Pmw.Balloon()
        self.tips.tagbind(self.tw,"Token.Keyword","This is a keyword")
        # print("See if it is working !!") Not implemented completely,need documentation of all keywords 



class TagTokenNames(TagTokens):
    """ [Class containing tag configurations for named tokens] """
    def __init__(self,TextWidget:TextArea) -> None:
        super().__init__(TextWidget=TextWidget)
        self.tw = TextWidget
        self.tw.tag_configure("Token.Name", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Attribute", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Builtin.Pseudo", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Class", foreground="blue")
        self.tw.tag_configure("Token.Name.Constant", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Decorator", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Entity", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Exception", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Function", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Function.Magic", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Label", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Namespace", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Other", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Tag", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Variable", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Variable.Class", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Variable.Global", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Variable.Instance", foreground="#003D99")
        self.tw.tag_configure("Token.Name.Variable.Magic", foreground="#003D99")



class TagTokenOperators(TagTokens):
    """ [Class containing tag configurations for operator tokens] """
    def __init__(self,TextWidget:TextArea) -> None:
        super().__init__(TextWidget=TextWidget)
        self.tw = TextWidget        
        self.tw.tag_configure("Token.Operator", foreground="#CC7A00")
        self.tw.tag_configure("Token.Operator.Word", foreground="#CC7A00")
        self.tips = Pmw.Balloon()
        self.tips.tagbind(self.tw,"Token.Operator","This is an Operator")



class TagTokenPunctuation(TagTokens):
    """ [Class containing tag configurations for punctuation tokens] """
    def __init__(self,TextWidget:TextArea) -> None:
        super().__init__(TextWidget=TextWidget)
        self.tw = TextWidget
        self.tw.tag_configure("Token.Punctuation", foreground="blue")
        self.tw.tag_configure("Token.Punctuation.Marker", foreground="blue")
        self.tips = Pmw.Balloon()
        self.tips.tagbind(self.tw,"Token.Punctuation","This is a Punctuation")



class TagTokenComments(TagTokens):
    """ [Class containing tag configurations for comment tokens] """
    def __init__(self,TextWidget:TextArea) -> None:
        super().__init__(TextWidget=TextWidget)
        self.tw = TextWidget
        self.tw.tag_configure("Token.Comment", foreground="gray",)
        self.tw.tag_configure("Token.Comment.Hashbang", foreground="gray",)
        self.tw.tag_configure("Token.Comment.Multiline", foreground="gray",)
        self.tw.tag_configure("Token.Comment.Preproc", foreground="gray",)
        self.tw.tag_configure("Token.Comment.Single", foreground="gray",)
        self.tw.tag_configure("Token.Comment.Special", foreground="gray",)        
        self.tips = Pmw.Balloon()
        self.tips.tagbind(self.tw,"Token.Comment","This is a Comment")



class TagTokenLiterals(TagTokens):
    def __init__(self, TextWidget: TextArea) -> None:
        super().__init__(TextWidget)
        self.tw = TextWidget
        self.tw.tag_configure("Token.Literal",foreground="red")
        self.tw.tag_configure("Token.Literal.Date",foreground="red")
        self.tw.tag_configure("Token.Literal.String",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Affix",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Backtick",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Char",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Delimiter",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Doc",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Double",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Escape",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Heredoc",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Interpol",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Other",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Regex",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Single",foreground="red")
        self.tw.tag_configure("Token.Literal.String.Symbol",foreground="red")
        self.tw.tag_configure("Token.Literal.Number",foreground="red")
        self.tw.tag_configure("Token.Literal.Number.Bin",foreground="red")
        self.tw.tag_configure("Token.Literal.Number.Float",foreground="red")
        self.tw.tag_configure("Token.Literal.Number.Hex",foreground="red")
        self.tw.tag_configure("Token.Literal.Number.Integer",foreground="red")
        self.tw.tag_configure("Token.Literal.Number.Integer.Long",foreground="red")
        self.tw.tag_configure("Token.Literal.Number.Oct",foreground="red")



class TagTokenErrors(TagTokens):
    """ [Class containing tag configurations for error tokens.] """
    def __init__(self, TextWidget: TextArea) -> None:
        super().__init__(TextWidget)
        self.tw = TextWidget
        self.tw.tag_configure("Token.Error",foreground="red",underline=True)



class KeywordsFontDescription:
    """ [Class containing font description for keyword tokens] """
    FontDesc = {"Font":TextFontEditor.FontSpec["Font"],"Size":TextFontEditor.FontSpec["Size"],"Weight":"bold"
    ,"Slant":TextFontEditor.FontSpec["Slant"],"Underline": False, "Overstrike": False}
    
    @classmethod
    def FontTag(cls):
        return (KeywordsFontDescription.FontDesc["Font"],KeywordsFontDescription.FontDesc["Size"],KeywordsFontDescription.FontDesc["Weight"])



class CommentsFontDescription:
    """ [Class containing font description for comment tokens] """
    FontDesc = {"Font":TextFontEditor.FontSpec["Font"],"Size":TextFontEditor.FontSpec["Size"],"Weight":TextFontEditor.FontSpec["Weight"]
    ,"Slant":"italic",}
    
    @classmethod
    def FontTag(cls):
        return (CommentsFontDescription.FontDesc["Font"],CommentsFontDescription.FontDesc["Size"],CommentsFontDescription.FontDesc["Weight"],CommentsFontDescription.FontDesc["Slant"])



class ThreadSafe(threading.Thread):
    """ [Class containing implementation of Thread-Safe(using Lock(other could be semaphores))] """
    def __init__(self, group=None, target=None, name= None, args=(), kwargs={}) -> None:
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)
        self._Lock = threading.Lock()
    
    def start(self) -> None:
        self._Lock.acquire()
        super().start()
        self._Lock.release()



#For testing purpose
Color = "#FFFFFF"
CompleColor="#FFFFFF"
ctypes.windll.shcore.SetProcessDpiAwareness(1)


root = ThemedTk()
app = Editor(root)
app.mainloop()
