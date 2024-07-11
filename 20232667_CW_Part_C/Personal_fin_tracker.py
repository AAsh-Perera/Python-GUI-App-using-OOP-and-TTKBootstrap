'''
Author : Palihawadana A. A. N. Perera
IIT ID : 20232667
UoW ID : 20822596

project: SD 1 CW 1 Part C for year 23/24

'''

'''
Module Name: Personal_fin_tracker.py
-----------------------

'''   

from All_classes import *
from ALL_functions import *



def main(all_transactions:dict[str:dict]):
        
    # main window
    root = CustomMainWindow(title= 'Enhanced Personal Finance Tracker')   

    # frame for the search widgets
    frame_1 = CustomFrame(master= root)
    frame_1.pack(fill='both')

    # frame with border for entry
    entry_frame = CustomFrameWithBorder(master=frame_1)
    entry_frame.grid(column=0, row=0, padx=(20,5), pady=(20,10))
    # search entry widget
    entry_1_var = tk.StringVar() # create a tkinter variable.
    entry_1 = CustomEntry(master= entry_frame, textvariable= entry_1_var)
    entry_1.configure(font=('Bauhaus 93', 12))
    entry_1.pack()

    # border with frame
    search_type_mb_frame = CustomFrameWithBorder(master= frame_1)
    search_type_mb_frame.grid(column=1, row=0, padx=(5), pady=(20, 10))
    # search options menu button
    search_type_options = [
        ('Description', 'Description', None),
        ('Amount', 'Amount', None),
        ('Type', 'Type', None),
        ('Date', 'Date', None)
    ]
    search_type_var = tk.StringVar()
    search_type_mb = CustomMenuButton(master= search_type_mb_frame, text= 'Search by', option_var= search_type_var, options= search_type_options)
    search_type_mb.pack()
    

    # frames for the main treeview
    frame_2= CustomFrame(master= root)
    frame_2.pack(fill='both', expand= True)

    frame_3 = CustomFrameWithBorder(master= frame_2)# create a special frame with a border for the treeview
    frame_3.pack(fill= 'both', expand= True, padx=20, pady=20)

    # create the main treeview
    main_treeview_col = [
        'Description',
        'Type',
        'Amount',
        'Date'
    ] # order of this list is important dont change unless you specifically want to.
    main_treeview = CustomTreeview(master= frame_3, column_names= main_treeview_col, data= all_transactions)
    main_treeview.pack(fill= 'both', expand= True)

    back_butt_frame = CustomFrameWithBorder(master=frame_1)
    back_butt_frame.grid(column=2, row=0, padx=(5), pady=(20, 10))
    # back button
    back_butt = CustomBackButton(master= back_butt_frame, data= all_transactions, treeview= main_treeview, entry= entry_1)
    back_butt.pack()

    search_button_frame = CustomFrameWithBorder(master=frame_1)
    search_button_frame.grid(column=3, row=0, padx=(5), pady=(20,10))
    # search button
    search_button = CustomSearchButton(master= search_button_frame, data= all_transactions, entry_text= entry_1, menu_button_text= search_type_var, tree_view= main_treeview, back_butt= back_butt)
    search_button.pack()

    root.mainloop()

if __name__ == '__main__':
        all_transactions = load_transactions_from_json('transactions.json')
        # check if it loads correctly. (error handling in a different way i guess)
        if all_transactions == 'File not found' or None:
            root = PopUpWindow(title='Error', label_text='The "transactions.json" file can not be found, please ensure that the file is in the correct directory and is rightly named and try again.')
            root.mainloop() 
        else: 
            try:  
                main(all_transactions)  # Call the main function with the loaded transactions
            except Exception as e:
                error_str = f'An error ocurred while trying to initiate the program: {e}'
                root = PopUpWindow(title='Error', label_text=error_str)
                root.mainloop() 
                 