'''
Author : Palihawadana A. A. N. Perera
IIT ID : 20232667
UoW ID : 20822596

project: SD 1 CW 1 Part C for year 23/24

'''

'''
Module Name: all_functions.py
-----------------------

'''         
'''
References
----------

Stackoverflow.com (2024) 'datetime.datatime.strptime(date, "%Y-%m-%d") adds 00:00:00 for different dates', stackoverflow.com, available at: https://stackoverflow.com/questions/70391399/datetime-datatime-strptimedate-y-m-d-adds-000000-for-different-dates (Accessed on 04/20/2024)

'''



import json
import datetime
def load_transactions_from_json(file_path):
    """
    Load transactions from a JSON file and transform them into the required format.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing transactions in the required format.
    """
    try:
        all_transactions = {}

        with open(file_path, 'r') as file:
            data = json.load(file)

        # this seems complicated but its really not it all comes down checking of the key in the dictionary references a anoth dict ot a list.
        for category, transaction_data in data.items():
            
            if transaction_data.__class__ is dict:
                transaction_type = transaction_data.get('type', 'Not Given') # we get the type of the transaction, and if somehow its not there, it defaults to Not Given
                transactions = transaction_data['transactions']
            
            elif transaction_data.__class__ is list:
                transaction_type = 'Not Given'
                transactions = transaction_data
            
            else:
                return
            
            all_transactions[category.lower()] = {
                'type': transaction_type,
                'transactions': [{'amount': transaction['amount'], 'date': datetime.datetime.strptime(transaction['date'], '%Y-%m-%d').date()} for transaction in transactions]
            } # this line of code is referenced from stackoverflow.com (2024) https://stackoverflow.com/questions/70391399/datetime-datatime-strptimedate-y-m-d-adds-000000-for-different-dates

        return all_transactions
    except FileNotFoundError:
        return 'File not found'
    
