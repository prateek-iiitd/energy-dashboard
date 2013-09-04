__author__ = 'prateek'

from Tkinter import *
import ttk
import tkMessageBox

from Main import *

class Flat():
    def __init__(self, flatnum, frame):
        self.flatnum = flatnum
        self.frame = frame

class main_window(Tk):
    def __init__(self, parent):
        Tk.__init__(self,parent)
        self.parent = parent
        #self.i = 1
        self.initialise()

    def check(self):
        flatnum = self.apt_combobox.get()
        meter_type = self.type_combobox.get()
        meter_id = get_meter_id(flatnum,meter_type)
        rate = get_polling_rate_from_meter_id(meter_id)

        # rate = '5'
        # top = Toplevel()
        # top.title('Test')
        # rate_label = Label(top,text = "Polling rate is %s seconds."%rate)
        # rate_label.pack()

        tkMessageBox.showinfo("Rate Information", "Current polling rate for this meter is %s seconds"%str(rate))


    def change(self):
        # print self.type_combobox.get()

        # flatnum = self.apt_combobox.get()
        # meter_type = self.type_combobox.get()
        # meter_id = get_meter_id(flatnum,meter_type)

        top = Toplevel()
        top.title('Select')

        select_group = LabelFrame(top,text="Select new polling rate: ",padx=5,pady=5)
        select_group.grid(column=0, row=0)

        self.select_combobox = ttk.Combobox(select_group,state='readonly')
        self.select_combobox.grid(column=0,row=0,sticky=(W,E))
        self.select_combobox['values'] = self.rate_options
        self.select_combobox.current(0)

        setButton = Button(top,text="Set Rate",padx=5,pady=5,command = self.set)
        setButton.grid(row=1, column=0)

    def set(self):
        flatnum = self.apt_combobox.get()
        meter_type = self.type_combobox.get()
        meter_id = get_meter_id(flatnum,meter_type)
        rate = self.select_combobox.get()
        result = change_rate_for_meter_id(meter_id,rate)

        if result:
            tkMessageBox.showinfo("Success", "Meter rate successfully changed to %s seconds"%str(rate))
        else:
            tkMessageBox.showerror("Failed", "Could not change meter rate.")


    def refresh(self):
        self.initialise()

    def selected(self,event=None):
        self.type_combobox['values'] = self.check[self.apt_combobox.get()]
        self.type_combobox.current(0)

    def initialise(self):
        self.grid()

        self.mainframe = Frame(self, padx="3",pady= "3")
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.grid(column=0, row=0, sticky=W+E)


        # self.menubar = Menu(self)
        # self.menubar.add_command(label="Refresh",command = self.refresh)
        # self.config(menu=self.menubar)

        self.rate_options = [str(x) for x in xrange(1,31)]
        self.flats = ['101','102','103']
        self.check = {'101':('1','2'),'102':('2','3'),'103':('3','4')}

        self.apt_group = LabelFrame(self.mainframe,text="Select Apartment: ",padx=5,pady=5)
        self.apt_group.grid(column=0, row=0,columnspan=2)

        #self.apt_combobox = ttk.Combobox(self.apt_group,values=self.flats,state='readonly')
        self.apt_combobox = ttk.Combobox(self.apt_group,values=self.flats,state='readonly')
        self.apt_combobox.current(0)
        self.apt_combobox.grid(column=0, row=0, sticky=(W, E))
        self.apt_combobox.bind("<<ComboboxSelected>>", self.selected)


        self.type_group = LabelFrame(self.mainframe,text="Select MeterType: ",padx=5,pady=5)
        self.type_group.grid(column=0, row=1,columnspan=2)

        self.type_combobox = ttk.Combobox(self.type_group,state='readonly')
        self.type_combobox.grid(column=0,row=0,sticky=(W,E))
        self.type_combobox['values'] = self.check[self.apt_combobox.get()]
        self.type_combobox.current(0)


        self.checkButton=Button(self.mainframe, text="Check Rate",padx=5,pady=5,command = self.check)
        self.checkButton.grid(column=0,row=2)

        self.changeButton=Button(self.mainframe, text="Change Rate ",padx=5,pady=5,command = self.change)
        self.changeButton.grid(column=1,row=2)




if __name__ == "__main__":
    root = main_window(None)
    root.title("Rate Change Utility")
    #print "Here"
    root.mainloop()