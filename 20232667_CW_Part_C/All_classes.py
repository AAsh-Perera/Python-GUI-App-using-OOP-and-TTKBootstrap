'''
Author : Palihawadana A. A. N. Perera
IIT ID : 20232667
UoW ID : 20822596

project: SD 1 CW 1 Part C for year 23/24

'''

'''
Module Name: all_classes.py
-----------------------

'''         
'''
References
----------
Tkinter.com (2021 - 2024) 'Making Moderr GUI's Using Tkinter and ttkbootstrap', youtube.com, video playlist, available at https://www.youtube.com/@TkinterPython (accessed: 04/20/2024)

W3 Recorces (2023) 'Python Tkinter Treeview widget: Sorting and columns made easy', w3recorces.com, available at https://www.w3resource.com/python-exercises/tkinter/python-tkinter-widgets-exercise-18.php#:~:text=Import%20tkinter%20as%20 (accessed on 04/27/2024)

stackoverflow.com (2019) 'Get data from treeview in tkinter', stackoverflow.com, available at: https://stackoverflow.com/questions/23829409/get-data-from-treeview-in-tkinter (Accessed on 04/20/2024)

Gaddis, T. (2008), 'Starting out with Python', 5th edn. London: Pearson. (accessed: March 2024)
Many of the input validation loops used in this program were adapted from code from this reference, as well as fundamental coding principals.

'''


import os 
import datetime
import tkinter as tk
from tkinter import ttk # we will use tkinter's logic only
import ttkbootstrap as ttkb # the program will use the more modern style of ttkbootstrap with the logic of tkinter.
from PIL import Image, ImageTk # these two functions will be used to convert png icons into Tkinter PhotoImages.

class CustomFrameWithBorder(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master, highlightbackground='black', highlightthickness=2, background='#fec5bb') # create a special frame with a border

class CustomMainWindow(ttkb.Window):
    """
    Main application window class.
    """

    def __init__(self, title: str, theme_name: str = 'minty'):
        """
        Initialize the main application window.

        Args:
            title (str): The title of the window.
            theme_name (str, optional): The name of the theme. Defaults to 'minty'.
        """
        super().__init__(themename=theme_name)
        self.set_window_dimensions()
        self.configure_window(title=title)
        
    def configure_window(self, title: str):
        """
        Configure the window settings.

        Args:
            title (str): The title of the window.
        """
        self.geometry('1000x563')  # Set initial window size to 16:9 aspect ratio
        self.title(title)
        
        # Set window icon
        # direct reference from ttkbootstrap.com (2024)
        icon_path = os.path.abspath('Assets\\Icons\\MainIcon.png')
        icon_image = ImageTk.PhotoImage(Image.open(icon_path)) # here we call a function with in a function to make our code simpler.
        self.iconphoto(False, icon_image)
        
    def set_window_dimensions(self):
        """Set the minimum window size."""
        self.minsize(1000, 563)

class CustomFrame(ttkb.Frame):
    """
    Custom frame widget class.
    """

    def __init__(self, master, style: str = 'custom.TFrame', color: str = None, relief: str = None):
        """
        Initialize the custom frame widget.

        Args:
            master: The parent widget.
            style (str, optional): The style of the frame. Defaults to 'custom.TFrame'.
            color (str, optional): The background color of the frame. Defaults to None.
            relief (str, optional): The relief type of the frame. Defaults to None.
        """
        self.configure_style(color=color, relief=relief)
        super().__init__(master=master, style=style) 
    
    def configure_style(self, color: str = None, relief: str = None):
        """
        Configure the style of the frame.

        Args:
            color (str, optional): The background color of the frame. Defaults to None.
            relief (str, optional): The relief type of the frame. Defaults to None.
        """
        my_style = ttkb.Style()
        my_style.configure(
            'custom.TFrame',
            # the user can parse a specific color or refief if they want to or not.
            background='#fec5bb' if color is None else color, # pech
            relief='flat' if relief is None else relief
        )

class PopUpWindow(ttkb.Window):
    """
    Pop-up window widget class.
    """
    def __init__(self, title:str, label_text:ttkb.Label =''):
        super().__init__(title= title)
        w = 525
        h = 200
        self.geometry(f'{w}x{h}')
        self.title(title)
        self.add_widgets(label_text=label_text, title= title)

    def close_window(self):

        self.destroy() # my favorite line of code in the whole assignment 
    
    def add_widgets(self, label_text:ttkb.Label, title:str):
        """
        Add widgets to the pop-up window.

        Args:
            label_text (ttkb.Label): The text to display in the window.
            title (str): The title of the window.
        """    
        frame1 = CustomFrame(master=self)
        frame1.pack(padx= 0, pady=0, fill='both', expand=True)
        
        # style the labels
        my_style = ttkb.Style()
        my_style.configure(
            'custom.TLabel',
            background = '#e8e8e4'
        )

        # add the text
        label1 = ttkb.Label(master= frame1, text=f'{title}:', font= ('Berlin Sans FB Demi', 30 , 'bold'), justify= 'center', style='custom.TLabel')
        label1.pack(padx=10, pady=10)
        label2 = ttkb.Label(master=frame1, text=label_text, font= ('Berlin Sans FB Demi', 10), wraplength= 460, justify= 'center', style='custom.TLabel')
        label2.pack(padx=10, pady=10)

        # add the button
        ok_button = ttkb.Button(master= frame1, text='Okay', style='primary.TButton',padding=(10),command= lambda: self.close_window(), width=20)
        ok_button.pack(pady=20)

class CustomTreeview(ttk.Treeview):
    """
    Customized Treeview widget for displaying financial transactions.
    """

    def __init__(self, master, column_names, data):
        """
        Initialize the CustomTreeview widget.

        Args:
            master (tk.Widget): The parent widget.
            column_names (list): Names of the columns.
            data (dict): Data to be displayed in the treeview.
        """
        super().__init__(master=master, show='headings')

        self.sort_order = {}  # Dictionary to keep track of sort order for each column!

        # Set up columns and headings
        self['columns'] = column_names
        self.set_columns(column_names)

        # Bind headings to sort functions
        for column in column_names:
            self.heading(column, text=column, anchor=tk.CENTER,command=lambda c =column: self.sort_column(c)) # here using lambda we can pass an argument to the function

            # Default sort order is ascending
            self.sort_order[column] = True

        # set the style
        self.configure_style()

        # Add data
        self.add_data(data)

        # Add vertical scrollbar
        self.add_scrollbar(master)

    def set_columns(self, column_names):
        """
        Set up columns for the treeview.
        """
        for column in column_names:
            self.column(column, width=100, anchor=tk.CENTER, minwidth=50)

    def configure_style(self):
        style = ttk.Style()
        style.configure("Treeview", rowheight=50)
        style.configure("Treeview.Heading", rowheight=40, font= ('Berlin Sans FB Demi',15), background='#C28D84', foreground='white') # very dark melon
        # sent labels for odd and even columns
        self.tag_configure('evenrow', background='white', font=('Berlin Sans FB Demi', 13)) # light platinum
        self.tag_configure('oddrow', background= '#A9E4D3', font=('Berlin Sans FB Demi', 13)) # cambridge blue        

    def add_data(self, data):
        """
        Add data to the treeview.
        """
        try:
            count = 0
            for description, transaction_data in data.items():
                transaction_type = transaction_data['type']
                transactions = transaction_data['transactions']
                for transaction in transactions:
                    # Even rows will be platinum and odd rows will be lighter platinum.
                    count += 1
                    if count % 2 == 0:
                        self.insert('', tk.END, values=(description, transaction_type, f'{transaction["amount"]:,.2f}', transaction['date']), tags='evenrow')
                    else:
                        self.insert('', tk.END, values=(description, transaction_type, f'{transaction["amount"]:,.2f}', transaction['date']), tags='oddrow')
        except Exception as e:
            
            print(f'An error occurred while loading data into the main treeview: {e}')

    def sort_column(self, column):
        data = [(self.set(child, column), child) for child in self.get_children('')] # this looks complicated but its really simple, its just list comprehension,
        # we get the children of the treeview from the method .get_children() and then we set it in a touple contailing the position of the child (which is take from the .set() method) and the child itself.
        reverse_order = self.sort_order[column] # this is reference the atribue called sort_order
        data.sort(reverse=not reverse_order) # this sorts the data

        # the bellow loop is a direct reference from w3recorces.com https://www.w3resource.com/python-exercises/tkinter/python-tkinter-widgets-exercise-18.php#:~:text=Import%20tkinter%20as%20'tk'%20and,()%20and%20set%20its%20title.
        for index, (_, child) in enumerate(data):
            self.move(child, '', index)

        self.sort_order[column] = not reverse_order

    def add_scrollbar(self, master):
        """
        Add a vertical scrollbar to the treeview.
        """
        vsb = ttk.Scrollbar(master, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

class CustomMenuButton(ttkb.Menubutton):

    '''
    to add a command to the menu, you must first make a method for the command in the class, then pass the name of the option(str), the value and the command(pass None if no command) as a tuple of strings in the list of options.
    example options list:
    options = [
        ('Ascending', 'Ascending', 'ascending_comand'),
        ('Descending', 'Descending', 'descending_comand')
    ]
    '''

    def __init__(self, master, text:str, options:list, option_var:ttkb.StringVar, style:str = 'custom.TMenubutton'):
        self.configure_button_style()
        super().__init__(master= master, text= text, style= style) # initialixe menu button.
        
        # add menue options
        menu = tk.Menu() # menu will use the menu from tkinter, styling is different.
        # direct reference from ttkbootstrap.com(2024)
        for option, value ,command in options:
            menu.add_radiobutton(
                label       = option, 
                value       = value, 
                variable    = option_var, 
                command      = command
                )
        self.configure_menu_style(menu=menu)
        self['menu'] = menu

    def configure_button_style(self):
        """
        Configure the style for the menu button.
        """
        # style the menu button.
        my_style = ttkb.Style()
        my_style.configure(
            'custom.TMenubutton',
            arrowsize           = 5,
            arrowcolor          = 'black',
            arrowpadding        = 5,
            background          = '#ffd7ba', # pastel light peach
            compound            = 'top',
            bordercolor         = 'black', 
            borderwidth         = 0,
            darkcolor           = '#fec89a', # pastel peach
            focusthickness      = 6, # basically the y hight of the button
            focuscolor          = '#ffe5d9', # pastel melon
            foreground          = 'black',
            font                = ('Berlin Sans FB Demi', 12),
            lightcolor          = '#ffe5d9', # light pastel melon
            padding             = (40,5),
            relief              = 'solid',
            activebackground    = '#d8e2dc', # pestel platinum
        )

    def configure_menu_style(self, menu):
        """
        Configure the style for the menu.

        Args:
            menu: The menu widget.
        """        
        # style the menu
        menu.configure(
            bg                  = '#ffd7ba',
            fg                  = 'black',
            font                = ('Berlin Sans FB Demi', 11),
            bd                  = 0, # border around the choice (tick)
            activebackground    = '#d8e2dc', # pestel platinum
            activeborderwidth   = 5,
            activeforeground    = '#85817E', # earthy gray
            selectcolor         = '#6d765b', # dark platinum
        )
    
class CustomEntry(ttkb.Entry):
    """
    Customized Entry widget class.

    Args:
        master (tk.Widget)                      : The parent widget.
        default_text (str, optional)            : The default text to display in the entry. Defaults to 'Search for a transaction...'.
        default_font (tuple, optional)          : The default font for the entry. Defaults to ('Berlin Sans FB Demi', 12).
        default_width (int, optional)           : The default width of the entry. Defaults to 50.
        style (str, optional)                   : The style to be applied. Defaults to 'custom.TEntry'.
        textvariable (ttkb.StringVar, optional) : The StringVar variable to associate with the entry. Defaults to None.
    """
    def __init__(
            self, 
            master, 
            default_text:str                    = 'Search for a transaction...', 
            default_font:tuple[str, int, str]   = ('Berlin Sans FB Demi', 12), 
            default_width:int                   = 50,
            style                               = 'custom.TEntry',
            textvariable:ttkb.StringVar         = None
            ) -> None:
        
        self.configure_style(default_font=default_font)
        if textvariable == None:
            textvariable = ttkb.StringVar()
        super().__init__(master= master, style= style, width= default_width, textvariable=textvariable)
        self.insert('end', default_text)
    
    def configure_style(self, default_font:tuple[str, int, str] = ('Berlin Sans FB Demi', 12)):
        """
        Configure the style for the CustomEntry widget.
        """
        my_style = ttkb.Style()
        my_style.configure(
            'custom.TEntry',
            background          = '#fcd5ce', # pale dogwood
            darkcolor           = '#dba159', # pastel clay
            fieldbackground     = '#ffe5d9', # lighter pastel peach
            foreground          = 'black',
            font                = default_font,
            lightcolor          = '#ffd7ba', # light pastel peach
            padding             = 10,
            relief              = 'solid', # flat, groove, raised, ridge, solid, sunken
            selectbackground    = '#84dcc6', # platinum
            selectborderwidth   = 0,
            selectforeground    = 'white', # earthy gray
            )
        my_style.map(
            'custom.TEntry', 
            foreground=[
                ('disabled', 'gray'),
                ('focus !disabled', '#85817E'),
                ('hover !disabled', '#222222')
                ]
            )

class CustomBackButton(ttkb.Button):
    """
    Customized Back Button widget class.

    Args:
        master (tk.Widget)                  : The parent widget.
        data                                : The data to be used for the button functionality.
        text (str, optional)                : The text to display on the button. Defaults to 'Back to All Transactions'.
        style (str, optional)               : The style to be applied to the button. Defaults to 'custom2.TButton'.
        treeview (CustomTreeview, optional) : The main treeview widget. Defaults to None.
        entry (CustomEntry, optional)       : The entry widget associated with the treeview. Defaults to None.
    """
    def __init__(
            self,
            master,
            data:dict[str:dict], # we need this to display the original data.
            text: str = 'Back to All Transactions',
            style:str = 'custom2.TButton',
            treeview: CustomTreeview = None, # this is the main treeview
            entry: CustomEntry      = None 
            ):
        self.configure_style()
        super().__init__(master=master, text=text, style=style, state='disabled', command= lambda: self.back_func(data=data, treeview=treeview, entry=entry)) 
              
    def configure_style(self):
        """
        Configure the style for the CustomBackButton widget.
        """        
        my_style = ttkb.Style()
        my_style.configure(
            'custom2.TButton',
            anchor              = tk.CENTER,
            highlightcolor      = '#fec5bb', # pastel pink peach.
            font                = ('Berlin Sans FB Demi', 12),
            foreground          = 'black',
            justify             = tk.CENTER,
            padding             = 9,
            relief              = 'flat',#flat, groove, raised, ridge, solid, sunken
        )        
        
    def back_func(self, data, treeview:CustomTreeview, entry:CustomEntry):
        """
        Functionality for the back button.
        """
        # even though its a back function, it doesmt really take us back to an older instance of data, it takes the original data and overrides th current data, creating an illusion of going back.
        treeview.delete(*treeview.get_children()) # deletets all the children of the tree view 
        # the above line of code is referenced from stackoverflow.com (2019) https://stackoverflow.com/questions/23829409/get-data-from-treeview-in-tkinter
        treeview.add_data(data)
        entry.delete('0', 'end') # remove the stuff in the entry set by user
        entry.insert('0', 'Search for a transaction...') # set my own text.
        self.configure(state= 'disabled')

class CustomSearchButton(ttkb.Button):
    """
    Customized Search Button widget class.

    Args:
        master                                      : The parent widget.
        data                                        : The data to be used for the button functionality.
        icon_path (str, optional)                   : The path to the icon image file. Defaults to 'Assets\\Icons\\Search.png'.
        icon_size (tuple, optional)                 : The size of the icon. Defaults to (25, 25).
        text (str, optional)                        : The text to display on the button. Defaults to an empty string.
        style (str, optional)                       : The style to be applied to the button. Defaults to 'custom.TButton'.
        entry_text (ttkb.StringVar, optional)  : The variable to hold the search term. Defaults to None.
        menu_button_text (ttkb.StringVar, optional)  : The variable to hold the search type. Defaults to None.
        tree_view (CustomTreeview, optional)        : The treeview widget. Defaults to None.
        back_butt (CustomBackButton, optional)      : The back button widget. Defaults to None.
    """
    def __init__(
            self, 
            master,
            data:dict[str:dict], 
            icon_path:str                   = os.path.abspath('Assets\\Icons\\Search.png'),
            icon_size:tuple                 = (25, 25),  # Default icon size     
            text:str                        = '',
            style:str                       = 'custom.TButton',
            entry_text:ttkb.StringVar  = None,
            menu_button_text:ttkb.StringVar  = None,
            tree_view:CustomTreeview        = None, # must make sure it is a CustomTreeview obj and not a tk or ttkb.Treeview obj
            back_butt: CustomBackButton     = None, # this needs to passed to diable the button when all transactions are already displayed.
            ) -> None:
        
        # configure icon
        icon_dir_path = icon_path
        original_icon = Image.open(icon_dir_path)
        resized_icon = original_icon.resize(icon_size, Image.ADAPTIVE)  # Resize the icon
        self.icon_img = ImageTk.PhotoImage(resized_icon)  # Store as instance variable

        self.configure_style()
        super().__init__(
            master, 
            text=text, 
            image=self.icon_img,
            style=style, 
            command=lambda: self.search(
                entry_text=entry_text, 
                menu_button_text=menu_button_text, 
                tree_view=tree_view,
                data=data,
                back_button=back_butt
                ) # using lambda as a function allows us to call a function with args.
            )
    
    def configure_style(self):
        """
        Configure the style for the CustomSearchButton widget.
        """
        my_style = ttkb.Style()
        my_style.configure(
            'custom.TButton',
            anchor=tk.CENTER,
            focuscolor='#ffd7ba',  # light pastel peach.
            focusthickness=2,
            highlightcolor='#d8e2dc',  # pastel platinum.
            highlightthickness=2,
            justify=tk.CENTER,
            padding=3,
            relief='flat',  # flat, groove, raised, ridge, solid, sunken
            width=25
        )

    def search(self, data, back_button: CustomBackButton, entry_text: ttkb.StringVar = None, menu_button_text: ttkb.StringVar = None, tree_view: CustomTreeview = None) -> None:
        """
        Functionality for the search button.
        """
        if entry_text is None or menu_button_text is None or tree_view is None or not data: # Check if all necessary variables are provided
            print('Error: Missing required variables')
            return
        search_type_tuple = ('description', 'type', 'amount', 'date')
        search_type = menu_button_text.get().lower()
        search_term = entry_text.get().lower()

        if not search_term or search_term == 'search for a transaction...' or search_type not in search_type_tuple: # checks if the criteria are met.
            popupwindow = PopUpWindow(title= 'Error', label_text='Please enter a search term and/or set a search by value.')
            popupwindow.mainloop()
            return
        else:
            back_button.configure(state='normal')

            new_data = {}

            if search_type == 'description':
                for entry in data:
                    if entry.lower() == search_term: # Case-insensitive comparison
                        new_data[entry] = data[entry]

            elif search_type == 'amount':
                try:
                    for entry, entry_data in data.items():
                        new_data[entry] = {'type': entry_data['type'], 'transactions': []}
                        for transaction in entry_data['transactions']:
                            if transaction['amount'] == float(search_term):
                                new_data[entry]['transactions'].append(transaction)
                except ValueError:
                    popupwindow2 = PopUpWindow(title= 'Error', label_text='When searching for a transaction by amount please enter an integer or decimal number as the search term.')
                    popupwindow2.mainloop
                    return

            elif search_type == 'type':
                for entry, entry_data in data.items():
                    if entry_data['type'].lower() == search_term: # Case-insensitive comparison
                        new_data[entry] = data[entry]

            elif search_type == 'date':
                # Convert search term string to datetime.date object
                try:
                    search_date = datetime.datetime.strptime(search_term, '%Y-%m-%d').date() # this does input validation as well, cus you can not enter an invalid date like 2056-89-32
                except ValueError:
                    back_button.configure(state='disabled')
                    popupwindow2 = PopUpWindow(title= 'Error', label_text='When searching for a transaction by date please enter a VALID date in the following format: yyyy-MM-dd. Example: 2024-02-05')
                    popupwindow2.mainloop
                    return

                for entry, entry_data in data.items():
                    new_data[entry] = {'type': entry_data['type'], 'transactions': []}
                    for transaction in entry_data['transactions']:
                        if transaction['date'] == search_date:
                            new_data[entry]['transactions'].append(transaction)

            # Add the filtered data to the treeview
            if new_data == {}:
                popupwindow = PopUpWindow(title= 'Error', label_text='Either the search term you entered is wrong or there were no transactions found with the specified search term, please try again with another search term or type.')
                popupwindow.mainloop()
                return
            else:
                tree_view.delete(*tree_view.get_children())
                tree_view.add_data(new_data)

