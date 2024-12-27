import tkinter as tk                
from tkinter import font as tkfont 
from tkinter import ttk, PhotoImage, messagebox, Checkbutton
from tkcalendar import DateEntry
from datetime import datetime
import connection
import sqlite3
import random

class Welcome(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Camping')
        self.geometry("")
        container = tk.Frame(self,bg='#D8C4B6')
        container.pack( fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Visitor,Camper,Receptionist,ReceptionistData,Reservation,Rating,DatabaseRecords,ChoseReceptionOptions):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0,column=0,sticky="nsew")


        self.show_frame("Visitor")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StarRating(tk.Frame):
    def __init__(self, parent,controller, num_stars=5, **kwargs):
        tk.Frame.__init__(self, parent,bg='#D8C4B6')

        self.controller = controller
        self.num_stars = num_stars
        self.rating = 0  # Current rating (number of stars selected)
        self.stars = []  # List to hold the star widgets

        # Create the star buttons
        for i in range(1, num_stars + 1):
            star = tk.Label(self, text="★", font=("Times New Roman", 24),background="#D8C4B6", fg="#EFF3EA", cursor="hand2")
            star.grid(row=0, column=i - 1)
            star.bind("<Enter>", lambda e, idx=i: self.highlight(idx))
            star.bind("<Leave>", lambda e: self.highlight(self.rating))
            star.bind("<Button-1>", lambda e, idx=i: self.set_rating(idx))
            self.stars.append(star)

    def highlight(self, num_stars):
        """Highlight stars up to the given number."""
        for idx, star in enumerate(self.stars):
            star.config(fg="#FFC94A" if idx < num_stars else "#EFF3EA")

    def set_rating(self, num_stars):
        """Set the rating and update the star colors."""
        self.rating = num_stars
        self.highlight(num_stars)
        print(f"Rating set to: {self.rating}")

class Visitor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#D8C4B6')
        self.controller = controller
        self.image = PhotoImage(file="tent.png")
        self.image = self.image.subsample(2, 2)
        welcome_label=tk.Label(self, text="Welcome to the Camping",
          background='#997C70', foreground="black",
          font=("Times New Roman", 15)).pack(pady=20)
        label = tk.Label(self, image=self.image,bg='#D8C4B6').pack()
        visitor_label=ttk.Label(self, text="Select the visitor options:",background='#D8C4B6', foreground="black",
          font=("Times New Roman", 15)).pack( padx=10, pady=25)
        n = tk.StringVar()
        visitor_option = ttk.Combobox(self, width=27, textvariable=n)
        visitor_option['values'] = ("receptionist","camper")
        visitor_option.pack()
        button = ttk.Button(self, text="Next ➤", command=lambda: self.button_clicked(visitor_option)).pack(pady=20)

    def button_clicked(self,visitor_option):
        selected = visitor_option.get()
        if selected == "receptionist":
            self.controller.show_frame("Receptionist")
        elif selected == "camper":
            self.controller.show_frame("Camper")
class Rating(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#D8C4B6')
        self.controller = controller
        self.axiologhsh = tk.Label(self, text=" Want to rate our Camping? ", background='#977C70', foreground="black",
                                font=("Times New Roman", 15)).grid(row=0,column=2)
        email_label = tk.Label(self, text="email", font=("Times New Roman", 15), background='#D8C4B6').grid(row=1,
                                                                                                          column=1)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=2)
        self.star_rating = StarRating(self, controller)
        self.star_rating.grid(row=3,column=2)
        comments_label = tk.Label(self, text="Add a Review!", font=("Times New Roman", 15), background='#D8C4B6').grid(row=4,
                                                                                                          column=2)
        self.comments_text = tk.Text(self,height=5,width=20)
        self.comments_text.grid(row=5, column=2)

        button = ttk.Button(self, text="Rating Now➤", command=self.save_rating).grid(row=6,column=3)
        button = ttk.Button(self, text="Camper",
                command=lambda: controller.show_frame("Camper")).grid(row=7, column=3)
        
    def save_rating(self):
        email=self.email_entry.get()
        vathmologia=self.star_rating.rating
        sxolia=self.comments_text.get(1.0, "end-1c")
        conn=sqlite3.connect('camping_v5.db')
        cursor=conn.cursor()
        # fill AXIOLOGHSH
        x=cursor.execute('''Select K.kwd_katask, KR.kwd_krathshs
                From KATASKHNWTHS as K NATURAL JOIN KRATHSH AS KR 
                where email=?''',(email,)).fetchall()
        kwd_katask=x[0][0]
        kwd_krathshs=x[0][1]
        data_insert_query='''INSERT INTO AXIOLOGHSH VALUES(?,?,?,?)'''
        date_insert_tuple=(vathmologia,sxolia,x[0][0],x[0][1])
        cursor.execute(data_insert_query,date_insert_tuple)
        conn.commit()
        conn.close()


class Camper(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#D8C4B6')
        self.controller = controller
        visitor_label=ttk.Label(self, text="Select the camper options:",background='#D8C4B6', foreground="black",
          font=("Times New Roman", 15)).pack( padx=10, pady=25)
        n = tk.StringVar()
        visitor_option = ttk.Combobox(self, width=27, textvariable=n)
        visitor_option['values'] = ("reserve now","rate now")
        visitor_option.pack()
        button = ttk.Button(self, text="Next ➤", command=lambda: self.button_clicked(visitor_option)).pack(pady=20)
        button = ttk.Button(self, text="Back",
                           command=lambda: controller.show_frame("Visitor")).pack()

    def button_clicked(self,visitor_option):
        selected = visitor_option.get()
        if selected == "reserve now":
            self.controller.show_frame("Reservation")
        elif selected == "rate now":
            self.controller.show_frame("Rating")


class Reservation(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#D8C4B6')
        self.controller = controller

        l1 = tk.Label(self, text=" Reservation ", font=("Times New Roman", 15), background='#977C70').grid(row=1,
                                                                                                                column=1)
        
        #select personal data                                                                                               
        name_label = tk.Label(self, text="name", font=("Times New Roman", 15), background='#D8C4B6').grid(row=2,
                                                                                                          column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=2, column=1)

        lname_label = tk.Label(self, text="last name", font=("Times New Roman", 15), background='#D8C4B6').grid(row=3,
                                                                                                                column=0)
        self.lname_entry = tk.Entry(self)
        self.lname_entry.grid(row=3, column=1)
        email_label = tk.Label(self, text="email", font=("Times New Roman", 15), background='#D8C4B6').grid(row=4,
                                                                                                            column=0)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=4, column=1)
        phone_label = tk.Label(self, text="phone number", font=("Times New Roman", 15), background='#D8C4B6').grid(
            row=5, column=0)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=5, column=1)
        id_label = tk.Label(self, text="id number", font=("Times New Roman", 15), background='#D8C4B6').grid(row=6,
                                                                                                             column=0)
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=6, column=1)
        #select checkin checkout dates
        self.checkin_label = tk.Label(self, text="check-in date", font=("Times New Roman", 15), background='#D8C4B6').grid(row=8,
                                                                                                     column=0)
        self.checkin_entry = DateEntry(self)
        self.checkin_entry.grid(row=8, column=1)

        self.checkout_label = tk.Label(self, text="check-out date", font=("Times New Roman", 15), background='#D8C4B6').grid(row=9,
                                                                                                     column=0)
        self.checkout_entry = DateEntry(self)
        self.checkout_entry.grid(row=9, column=1)

        #select service menu button
        self.yphresia_label = ttk.Label(self, text="Select service:",background='#D8C4B6', foreground="black",
          font=("Times New Roman", 15)).grid( row=7,column=0)
        mb= tk.Menubutton ( self, text="Service" )
        mb.grid(row=7, column=1)
        mb.menu  =  tk.Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
        self.P = tk.IntVar()
        self.B= tk.IntVar()
        self.E =tk.IntVar()

        mb.menu.add_checkbutton ( label="Parking", variable=self.P)
        mb.menu.add_checkbutton ( label="Breakfast", variable=self.B)
        mb.menu.add_checkbutton ( label="Electricity supply", variable=self.E)
        # select accomodation 1
        self.stay_label1 = ttk.Label(self, text="Accomondation 1＊:",background='#977C70', foreground="black",
                                     font=("Times New Roman", 15)).grid(row=1, column=2,padx = 10, pady=15)
        self.stay1 = tk.StringVar()
        self.stay_option1 = ttk.Combobox(self, width=7, textvariable=self.stay1)
        self.stay_option1['values'] = ("tent", "room", "rv")
        self.stay_option1.grid(row=1, column=3)

        self.children_label1 = tk.Label(self, text="children number＊", font=("Times New Roman", 15),
                                        background='#D8C4B6').grid(row=2,
                                                                   column=2)
        self.children_entry1 = tk.Entry(self, width=5)
        self.children_entry1.grid(row=2, column=3)

        self.adults_label1 = tk.Label(self, text="adults number", font=("Times New Roman", 15),
                                      background='#D8C4B6').grid(row=3,
                                                                 column=2)
        self.adults_entry1 = tk.Entry(self, width=5)
        self.adults_entry1.grid(row=3, column=3)

        # select acommodation 2
        self.stay_label2 = ttk.Label(self, text="Accomondation 2:", background='#977C70', foreground="black",
                                     font=("Times New Roman", 15)).grid(row=4, column=2,padx = 10, pady=15)
        self.stay2 = tk.StringVar()
        self.stay_option2 = ttk.Combobox(self, width=7, textvariable=self.stay2)
        self.stay_option2['values'] = ("tent", "room", "rv")
        self.stay_option2.grid(row=4, column=3)

        self.children_label2 = tk.Label(self, text="children number", font=("Times New Roman", 15),
                                        background='#D8C4B6').grid(row=5,
                                                                   column=2)
        self.children_entry2 = tk.Entry(self, width=5)
        self.children_entry2.grid(row=5, column=3)

        self.adults_label2 = tk.Label(self, text="adults number", font=("Times New Roman", 15),
                                      background='#D8C4B6').grid(row=6,
                                                                 column=2)
        self.adults_entry2 = tk.Entry(self, width=5)
        self.adults_entry2.grid(row=6, column=3)

        # select acommodation 3
        self.stay_label3 = ttk.Label(self, text="Accomondation 3:", background='#977C70', foreground="black",
                                     font=("Times New Roman", 15)).grid(row=7, column=2,padx = 10, pady=15)
        self.stay3 = tk.StringVar()
        self.stay_option3 = ttk.Combobox(self, width=7, textvariable=self.stay3)
        self.stay_option3['values'] = ("tent", "room", "rv")
        self.stay_option3.grid(row=7, column=3)

        self.children_label3 = tk.Label(self, text="children number", font=("Times New Roman", 15),
                                        background='#D8C4B6').grid(row=8,
                                                                   column=2)
        self.children_entry3 = tk.Entry(self, width=5)
        self.children_entry3.grid(row=8, column=3)

        self.adults_label3 = tk.Label(self, text="adults number", font=("Times New Roman", 15),
                                      background='#D8C4B6').grid(row=9,
                                                                 column=2)
        self.adults_entry3 = tk.Entry(self, width=5)
        self.adults_entry3.grid(row=9, column=3)

        #buttons for reservation and switching frames 
        button2 = ttk.Button(self, text="Reserve Now➤", command=self.enter_data).grid(row=10,column=4)
        button = ttk.Button(self, text="Back",
                           command=lambda: controller.show_frame("Visitor")).grid(row=11,column=4)
        button = ttk.Button(self, text="Camper",
                           command=lambda: controller.show_frame("Camper")).grid(row=12,column=4)
        info_button = ttk.Button(self, text="𝓲＊",
                            command=self.info,width=3).grid(row=13, column=5)

        self.ctime = datetime.now().strftime("%Y-%m-%d")
        current_time = tk.Label(self, text=self.ctime,background='#D8C4B6', foreground="black",
          font=("Times New Roman", 15))
        current_time.place(anchor="sw", relx=0, rely=1)
    def info(self):
        self.info_label = tk.Label(self, text="1) each room can accommodate up to 4 people\n2) children underage deserve a discount\t", font=("Times New Roman", 10),
                                      background='#D8C4B6').grid(row=13, column=5)
    # def accomodation(self, i,j):
    #     self.stay_label1 = ttk.Label(self, text=f"Accomondation {j}:", background='#997C70', foreground="black",
    #                                  font=("Times New Roman", 15)).grid(row=i, column=2,padx = 10, pady=15)
    #     self.stay = tk.StringVar()
    #     self.stay_option = ttk.Combobox(self, width=7, textvariable=self.stay)
    #     self.stay_option['values'] = ("tent", "room", "rv")
    #     self.stay_option.grid(row=i, column= 3)
    #
    #     self.children_label = tk.Label(self, text="children number", font=("Times New Roman", 15),
    #                                    background='#D8C4B6').grid(row=i+1,
    #                                                               column=2)
    #     self.children_entry = tk.Entry(self, width=5)
    #     self.children_entry.grid(row=i+1, column=3)
    #
    #     self.adults_label = tk.Label(self, text="adults number", font=("Times New Roman", 15),
    #                                  background='#D8C4B6').grid(row=i+2,
    #                                                             column=2)
    #     self.adults_entry = tk.Entry(self, width=5)
    #     self.adults_entry.grid(row=i+2, column=3)

    def enter_data(self):

        children1 = self.children_entry1.get()
        print(children1)
        adults1 = self.adults_entry1.get()
        if not children1.strip():
            children1 = 0
        else:
            children1 = int(children1)

        if not adults1.strip():
            adults1 = 0
        else:
            adults1 = int(adults1)
        people1 = children1 + adults1



        children2 = self.children_entry2.get()
        adults2 = self.adults_entry2.get()
        if not children2.strip():
            children2 = 0
        else:
            children2 = int(children2)

        if not adults2.strip():
            adults2 = 0
        else:
            adults2 = int(adults2)
        people2 = children2 + adults2


        children3 = self.children_entry3.get()
        adults3 = self.adults_entry3.get()
        if not children3.strip():
            children3 = 0
        else:
            children3 = int(children3)

        if not adults3.strip():
            adults3 = 0
        else:
            adults3 = int(adults3)
        people3 = children3 + adults3
       
        # convert %m/%d/%y into %Y-%m-%d
        formatCin = datetime.strptime(self.checkin_entry.get(), "%m/%d/%y")
        checkin = formatCin.strftime("%Y-%m-%d")
        formatCout = datetime.strptime(self.checkout_entry.get(), "%m/%d/%y")
        checkout = formatCout.strftime("%Y-%m-%d")

        conn=sqlite3.connect('camping_v5.db')
        cursor=conn.cursor()
        # fill KATASKHNWTHS
        count=cursor.execute("Select count(*) FROM KATASKHNWTHS").fetchone()[0]
        data_insert_query='''INSERT INTO KATASKHNWTHS VALUES(?,?,?,?,?,?)'''
        date_insert_tuple=((count+1),self.name_entry.get(),self.lname_entry.get(),self.email_entry.get(),self.id_entry.get(),self.phone_entry.get())
        cursor.execute(data_insert_query,date_insert_tuple)

        # fill KRATHSH
        count_kratisi = cursor.execute("Select count(*) FROM KRATHSH").fetchone()[0]
        data_insert_query_kratisi = '''INSERT INTO KRATHSH VALUES(?,?,?,?,?,?,?)'''
        date_insert_tuple_kratisi = (f"KR0{count_kratisi+1}", checkin,checkout,self.ctime, (count+1),children1+children2+children3,adults1+adults2+adults3)
        cursor.execute(data_insert_query_kratisi, date_insert_tuple_kratisi)

        # fill KRAT_EPILE_YPHR
        if (self.P.get()):
            choice = "Y001"
            data_insert_query_yphresia = '''INSERT INTO KRAT_EPILE_YPHR VALUES(?,?)'''
            date_insert_tuple_yphresia = (f"KR0{count_kratisi + 1}", f"{choice}",)
            cursor.execute(data_insert_query_yphresia, date_insert_tuple_yphresia)
        if(self.B.get()):
            choice = "Y002"
            data_insert_query_yphresia = '''INSERT INTO KRAT_EPILE_YPHR VALUES(?,?)'''
            date_insert_tuple_yphresia = (f"KR0{count_kratisi + 1}", f"{choice}",)
            cursor.execute(data_insert_query_yphresia, date_insert_tuple_yphresia)
        if(self.E.get()):
            choice = "Y003"
            data_insert_query_yphresia = '''INSERT INTO KRAT_EPILE_YPHR VALUES(?,?)'''
            date_insert_tuple_yphresia = (f"KR0{count_kratisi + 1}", f"{choice}",)
            cursor.execute(data_insert_query_yphresia, date_insert_tuple_yphresia)
        

        dwmatia=cursor.execute('Select kwd_katal,xwrhtikothta FROM DWMATIO ').fetchall()
        rv=cursor.execute('Select kwd_katal,xwrhtikothta FROM RV ').fetchall()
        tents=cursor.execute('Select kwd_katal,xwrhtikothta FROM XWROS_KATASKHNWSHS ').fetchall()

        if (self.stay_option1.get()=='room'):
            for i in dwmatia:
                if(people1==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    dwmatia.remove(i)
                    break;

        elif (self.stay_option1.get()=='rv'):
            for i in rv:
                if(people1==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    rv.remove(i)
                    break;


        elif (self.stay_option1.get()=='tent'):
            for i in tents:
                if(people1==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    tents.remove(i)
                    break;
            

        if (self.stay_option2.get()=='room'):
            for i in dwmatia:
                if(people2==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    dwmatia.remove(i)
                    break;

        elif (self.stay_option2.get()=='rv'):
            for i in rv:
                if(people2==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    rv.remove(i)
                    break;


        elif (self.stay_option2.get()=='tent'):
            for i in tents:
                if(people2==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    tents.remove(i)
                    break;

        if (self.stay_option3.get()=='room'):
            for i in dwmatia:
                if(people3==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    dwmatia.remove(i)
                    break;

        elif (self.stay_option3.get()=='rv'):
            for i in rv:
                if(people3==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    rv.remove(i)
                    break;


        elif (self.stay_option3.get()=='tent'):
            for i in tents:
                if(people3==i[1]):
            # fill KRAT_PERILAMB_KATALYM
                    data_insert_query_krat_peril_katal = '''INSERT INTO KRAT_PERILAMB_KATALYM VALUES(?,?)'''
                    date_insert_tuple_krat_peril_katal =(f"KR0{count_kratisi+1}",i[0])
                    cursor.execute(data_insert_query_krat_peril_katal, date_insert_tuple_krat_peril_katal)
                    tents.remove(i)
                    break;

        conn.commit()
        conn.close()

class DatabaseRecords(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#D8C4B6')
        self.controller = controller
        conn = sqlite3.connect('camping_v5.db')
        cursor = conn.cursor()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # FROM sqlite_master : contains information about all the tables in the database.
        # SELECT name : retrieves the names of the objects (e.g., tables) stored in the sqlite_master table.
        # WHERE type='table' : includes entries where the type is table
        tables = [table[0] for table in cursor.fetchall()]
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)


        for table in tables:
            # Create a frame for each table
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=table)  # Add tab with the table name

            # Fetch table data
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            # Display data in a Treeview
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.pack(fill="both", expand=True)
            #tree.tag_configure("even",background='#D8C4B6', foreground="black",font=("Times New Roman", 15))

            # Set column headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")

            # Insert rows
            for row in rows:
                tree.insert("", "end", values=row)

                # Close the database connection
        conn.commit()
        conn.close()

class ReceptionistData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#D8C4B6')
        self.controller = controller

        # Create a Treeview (table) with columns
        self.tree = ttk.Treeview(self, columns=(
        "Year", "Reservations", "Profit from TENTS", "Profit from ROOMS", "Profit from RV", "Total Rating"),
                                 show="headings")
        # Define column headers
        self.tree.heading("Year", text="Year")
        self.tree.heading("Reservations", text="Reservations")
        self.tree.heading("Profit from TENTS", text="Profit from TENTS")
        self.tree.heading("Profit from ROOMS", text="Profit from ROOMS")
        self.tree.heading("Profit from RV", text="Profit from RV")
        self.tree.heading("Total Rating", text="Total Rating")

        # Style Configuration for Header and Rows
        style = ttk.Style()
        style.theme_use('clam')

        # Style for the Treeview heading (header)
        style.configure("Treeview.Heading", background='#997C70', font=("Times New Roman", 10))

        # Set column widths (optional)
        self.tree.column("Year", width=100, anchor="center")
        self.tree.column("Reservations", width=100, anchor="center")
        self.tree.column("Profit from TENTS", width=150, anchor="center")
        self.tree.column("Profit from ROOMS", width=150, anchor="center")
        self.tree.column("Profit from RV", width=150, anchor="center")
        self.tree.column("Total Rating", width=150, anchor="center")


        # Style for Treeview rows (records)
        style.configure("Treeview", background='#D8C4B6', foreground="black",  font=("Times New Roman", 10))

        # Insert data into the Treeview
        for index, r in enumerate(connection.records):
            count_t = self.calculate_profit(connection.records1, r[0])
            count_r = self.calculate_profit(connection.records2, r[0])
            count_rv = self.calculate_profit(connection.records3, r[0])
            AVGrating = self.calculate_avg_rating(connection.records4, r[0])

            # Insert each row into the treeview
            self.tree.insert("", "end", values=(r[0], r[1], count_t, count_r, count_rv, AVGrating))

        # Place the treeview in the grid
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Add a back button
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("Visitor"))
        back_button.grid(row=1, column=0, pady=10)

    def calculate_profit(self, records, year):
        total = 0
        for record in records:
            if record[0] == year:
                # Handle None values and sum profits
                profit = record[2] if record[2] is not None else 0
                total += profit
        return total

    def calculate_avg_rating(self, records, year):
        total_rating = 0
        count = 0
        for record in records:
            if record[0] == year:
                total_rating += record[1]
                count += 1
        return total_rating // count if count > 0 else 0


class ChoseReceptionOptions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#D8C4B6')
        self.controller = controller
        button2 = ttk.Button(self, text="Receptionist Data➤", command=self.Button2)
        button3 = ttk.Button(self, text="Enter the Database➤", command=self.Button3)
        button2.pack(pady=10)
        button3.pack(pady=10)
        button = ttk.Button(self, text="Back",command=lambda: controller.show_frame("Visitor")).pack()

    def Button2(self):self.controller.show_frame("ReceptionistData")
    def Button3(self):self.controller.show_frame("DatabaseRecords")

class Receptionist(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#D8C4B6')
        self.controller = controller
        code = tk.Label(self, text="enter code number",
            font=("Times New Roman", 15),background='#D8C4B6').pack(pady=10)
        self.e1= tk.Entry(self, show="*", width=10)
        self.e1.pack()
        button1 = ttk.Button(self, text="continue➤", command=self.check_password).pack(pady=10)
        button = ttk.Button(self, text="Back",
                           command=lambda: controller.show_frame("Visitor")).pack(pady=10)
        
    def check_password(self):
        if self.e1.get()=="01234":
            self.controller.show_frame("ChoseReceptionOptions")

        else: message = tk.messagebox.showerror(title="WRONG PASSWORD", message="try again")

if __name__ == "__main__":
    app = Welcome()
    app.mainloop()
