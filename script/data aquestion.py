import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def collect_flight_data(day, flight_direction):
    '''
    this fun scrape data from Bahrain airport and return it as a table

    args: 
        day (str): it will be today (TD) or tomorrow (TM)
        flight_direction(str) : it will be arrival or departures

    returns:
        panas DataFram that have 8 columns

    '''
    url= f"https://www.bahrainairport.bh/flight-{flight_direction}?date={day}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    time_lst= []
    destination_lst = []
    airways_lst = []
    gate_lst = []
    status_lst = []
    flight_lst = []
    flights = soup.find_all("div", {"class": f"flight-table-list row dv{flight_direction[:-1].title()}List"})
    #flights = soup.find_all("div", {"class": f"flight-table-list row dv{flight_direction[:-1].title()}List"}) #ArrivalList
    for flight in flights:
        try:
                airways_lst.append(flight.find('img')['alt'])
        except:
                airways_lst.append(pd.NA)
        flight_lst.append(flight.find('div',class_="col col-flight-no").text.strip())
        status_lst.append(flight.find('div',class_="col col-flight-status").text.strip())
        destination_lst.append(flight.find('div',class_="col col-flight-origin").text.strip())
        gate_lst.append(flight.find('div',class_="col col-gate").text.strip())
        time_lst.append(flight.find('div',class_="col col-flight-time").text.strip())


    flights_data = {'destination':destination_lst,
                'flight_number':flight_lst,
                'airways':airways_lst,
                'gate':gate_lst,
                'status':status_lst,
                'time':time_lst}
    df = pd.DataFrame(flights_data)
    today_date = datetime.date.today()
    if day =='TD':
        date= today_date
    elif day== 'TM':
        date = today_date + datetime.timedelta(days=1)
    df['date'] = date 
    df['direction'] = flight_direction 

    return df

def collect_arrival_departure():
    tables = []
    directions = ['arrivals','departures']
    days = ['TD','TM'] 
    
    for direction in directions:
        for day in days:
            tables.append(collect_flight_data(day, direction))
            time.sleep(5)
    df = pd.concat(tables)
    return df

def save_dat(df):
    today = datatime.date.today()
    path = f'all_flight_data_{today}.cvs'.replace('-','-')
    df.to.cvs(path)

df = collect_arrival_departure()
save_data