import pandas as pd
import os
import requests
import base64
import time
import csv

million = 1000000
billion = million * 1000
POP_US = 328.2 * million

def _refresh_func(refresh):
    """
    Function to determine if the data needs to be refreshed and
    refresh data from forbes400 API, can explicitly request to refresh
    """
    # check if previous update time file exists
    if not os.path.exists('prev_update_time.txt'):
        refresh = True
    else:
        # open time file and check if enough time has passed to refresh
        with open('prev_update_time.txt') as time_file:
            # time_cond True if more than an hour passed since last refresh
            time_cond = time.time() - float(time_file.read() + "0") > 3600
    # check if data doesn't exist at all
    data_not_present = not os.path.exists('net_worth_json.txt')
    if refresh or time_cond or data_not_present:
        print('invoking forbes400 api')
        # API call
        response = requests.get('https://forbes400.herokuapp.com/api/forbes400/?limit=12')
        # write data to file
        with open('net_worth_json.txt', 'w') as out:
            out.write(response.text)
        # write time new time file
        with open('prev_update_time.txt', 'w') as time_file:
            time_file.write(str(time.time()))

def get_net_worths(refresh=False):
    """
    refresh and parse net worth data about American billionaires 
    """
    _refresh_func(refresh)
    data = pd.read_json('net_worth_json.txt')
    # fin = 'financialAssets'
    # filter American Billionaires
    data = data[data['countryOfCitizenship'] == 'United States']
    # choose only relevant columns
    columns_select = ['uri', 'rank', 'finalWorth', 'personName', 'state', 
                      'city', 'source', 'countryOfCitizenship', 'squareImage']
    data = data[columns_select] # filter only wanted columns
    # formats for api call
    data['squareImage'] = 'https:' + data['squareImage']
    # puts values in billions
    data['finalWorth'] = data['finalWorth'].apply(round, 6) / 1000
    return data

def get_encoded_img(file_name):
    """
    encodes image so that dash can present it
    """
    encoded_image = base64.b64encode(open(file_name, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

def get_square_image(name, df):
    """
    retrieves image 
    """
    if  not os.path.exists('square_img/' + name + '.png'):
        uri = df.loc[df['personName'] == name, 'squareImage'].values[0]
        print('invoking image api')
        response = requests.get(uri)
        with open('square_img/' + name + '.png', 'wb') as f:
            f.write(response.content)
    return get_encoded_img('square_img/' + name + '.png')

def billionaire_dropdown_options(net_worths):
    """
    create's dict required for billionaire dropdown UI element
    """
    df = pd.DataFrame()
    df['label'] = net_worths['personName']
    df['value'] = net_worths['personName']
    return df.to_dict('records')

def _add_strings(*args):
    """
    helper method to combine strings
    """
    return " ".join(args)

def make_person_intro(name, net_worths):
    """
    returns string containing selected billionaire information
    """
    person_row = net_worths[net_worths['personName'] == name].to_dict('records')[0]
    sen1 = name + " has a net worth of " + str(person_row['finalWorth']) + \
            " billion dollars and is ranked " + str(person_row['rank']) + \
            " in the world by net worth."
    sen2 = name + "'s fortune was made through " + \
            str(person_row['source']) + "."
    sen3 = name + " is from " + str(person_row['city']) + ", " + \
            person_row['state'] + ", " + \
            str(person_row['countryOfCitizenship']) + "."
    return _add_strings(sen1, sen2, sen3)

def post_purchase(cost, name, net_worths):
    """
    returns string containing information about billionaire's net worth if
    they were to buy all the selected items
    """
    person_row = net_worths[net_worths['personName'] == name].to_dict('records')[0]
    sen1 = f'The total cost of the items selected is ${cost}.'
    diff = person_row['finalWorth'] * billion - cost
    sen2 = f'If {name} bought all of the items selected at those quantities he would have ${diff} left.'
    quot = round(diff / POP_US, 2)
    sen3 = f'That is enough left over to pay everyone in the United States ${quot}.'
    return _add_strings(sen1, sen2, sen3)

def make_receipt(items, quants, name, net_worths):
    receipt_cards = [dbc.Row([items[i + j].make_item_receipt_card(quants[i + j]) for j in range(3)]) for i in range(0, len(items), 3)]
    print(type(receipt_cards))
    return receipt_cards




# def main():
#     items = make_items_list()
#     for item in items:
#         print(item)
#     # link_to_billionaires = 'http://onforb.es/1iK2bS7'
#     # net_worths = get_net_worths()
#     # print(net_worths)
#     # print(net_worths)
#     # get_square_image('Bill Gates', net_worths, '')
#     # print(make_person_intro('Bill Gates', net_worths))

# if __name__ == '__main__':
#     main()