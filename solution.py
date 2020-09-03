from partner import Partner
from country import Country
from dateutil.parser import parse
import datetime
import requests
import json



def get_data():
    data = requests.get('https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=a5d99c16e745ba5bb064fef31c8c')
    return data.json()

def send_data(data):
    r = requests.post('https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=a5d99c16e745ba5bb064fef31c8c', data=json.dumps(data))
    print(data)
    print(r)


def parse_json(json_in):
    country_list = []
    cdp = dict()

    
    for p in json_in['partners']:
        person = Partner(p)
        if person.country not in cdp:
            cdp[person.country] = dict()

       
        for date in person.availableDates:
            if date not in cdp[person.country]:
                cdp[person.country][date] = set()
            cdp[person.country][date].add(person)


    for c_name, dates in cdp.items():

        sorted_dates = sorted(dates.keys())
        min_attendees = float('-inf')
        min_days = None
        max_attendees = set()

        for i in range(len(sorted_dates[:-1])):

            curr = sorted_dates[i]
            tomorrow = sorted_dates[i+1]
            curr_formatted = parse(curr)
            tomorrow_formatted = parse(tomorrow)

            date_attendees = dates[curr]
            tomorrow_attendees = dates[tomorrow]

            if tomorrow_formatted - curr_formatted != datetime.timedelta(1):
                continue
            

            attendees = date_attendees & tomorrow_attendees
            attend_total = len(attendees)
            
            if attend_total > min_attendees:
                min_attendees = attend_total
                min_days = curr
                max_attendees = attendees
            
        country = Country()
        country.name = c_name
        if min_attendees > 0:
            country.start_date = min_days
        for attendee in max_attendees:
            country.add(attendee)
        country_list.append(country)

    #print(country_list)
    return country_list

def final_touch(countries):
    ans = dict()
    ans['countries'] = list(map(lambda result: result.get_payload(), countries))
    return ans



def main():
    data = get_data()
    countries = parse_json(data)
    data = final_touch(countries)
    send_data(data)


if __name__ == '__main__':
    main()