
import csv

def query_records(data):

    headers = ['date','intent','location']

    with open('query_insights.csv', 'a') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
    
        writer.writerow(data)