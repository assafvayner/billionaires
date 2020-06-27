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
    if not os.path.exists('prev_update_time.txt'):
        refresh = True
        with open('prev_update_time.txt', 'w') as time_file:
            time_file.write(str(0.0))
    else:
        with open('prev_update_time.txt') as time_file:
            time_cond = time.time() - float(time_file.read() + "0") > 3600 # 1 hour
    data_not_present = not os.path.exists('net_worth_json.txt')
    if refresh or time_cond or data_not_present:
        print('invoking forbes400 api')
        response = requests.get('https://forbes400.herokuapp.com/api/forbes400/?limit=12')
        with open('net_worth_json.txt', 'w') as out:
            out.write(response.text)
        with open('prev_update_time.txt', 'w') as time_file:
            time_file.write(str(time.time()))

def get_net_worths(refresh=False):
    _refresh_func(refresh)
    data = pd.read_json('net_worth_json.txt')
    # fin = 'financialAssets'
    data = data[data['countryOfCitizenship'] == 'United States']
    columns_select = ['uri', 'rank', 'finalWorth', 'personName', 'state', 
                      'city', 'source', 'countryOfCitizenship', 'squareImage']
    data = data[columns_select] # filter only wanted columns
    data['squareImage'] = 'https:' + data['squareImage'] # formats for api call
    data['finalWorth'] = data['finalWorth'].apply(round, 6) / 1000 # puts values in billions
    return data

def get_encoded_img(file_name):
    encoded_image = base64.b64encode(open(file_name, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

def get_square_image(name, df, curr_img):
    if  not os.path.exists('square_image.png') or curr_img != name:
        uri = df.loc[df['personName'] == name, 'squareImage'].values[0]
        print('invoking image api')
        response = requests.get(uri)
        with open('square_image.png', 'wb') as f:
            f.write(response.content)
    return get_encoded_img('square_image.png')

def billionaire_dropdown_options(net_worths):
    df = pd.DataFrame()
    df['label'] = net_worths['personName']
    df['value'] = net_worths['personName']
    return df.to_dict('records')

def _add_strings(*args):
    return " ".join(args)

def make_person_intro(name, net_worths):
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
    person_row = net_worths[net_worths['personName'] == name].to_dict('records')[0]
    sen1 = f'The total cost of the items selected is ${cost}.'
    diff = person_row['finalWorth'] * billion - cost
    sen2 = f'If {name} bought all of the items selected at those quantities he would have ${diff} left.'
    quot = round(diff / POP_US, 2)
    sen3 = f'That is enough left over to pay everyone in the United States ${quot}.'
    return _add_strings(sen1, sen2, sen3)


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