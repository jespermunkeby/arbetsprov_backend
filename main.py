from ParkingGarage import ParkingGarage 
from datetime import datetime

parse = "%d/%m/%Y %H:%M:%S"
def datetime_to_string(dt):
    return dt.strftime(parse)

def string_to_datetime(s):
    return datetime.strptime(s, parse)

'''
        00:00   01:00   02:00   03:00   04:00
          |   |   |   |   |   |   |   |   |
          *--A1-------*
          |   |   |   |   |   |   |   |   |
              *--B2---*
          |   |   |   |   |   |   |   |   |
              *-----------C3----------*
          |   |   |   |   |   |   |   |   |
                          *-----D4--------*
          |   |   |   |   |   |   |   |   |
                              *---E5--*
'''
        
#Simulate
p = ParkingGarage(datetime(1999,1,1,0,0,0,0)) #00:0
p.enter('A1')

p.tick(60*30) #00:30
p.enter('B2')
p.enter('C3')

p.tick(60*60) #01:30
p.exit('B2')
p.exit('A1')

p.tick(60*30) #02:00
p.enter('D4')

p.tick(60*30) #02:30
p.enter('E5')

p.tick(60*60) #03:30
p.exit('E5')
p.exit('C3')

p.tick(60*30) #04:00
p.exit('D4')

time_from = string_to_datetime("01/01/1999 00:00:00") #EDIT THIS AND TEST
time_to = string_to_datetime("01/01/1999 01:30:00") #EDIT THIS AND TEST

all_time_report = p.get_summary(time_from,time_to)

print()
print('Querying pagrking garage from {} to {}'.format(datetime_to_string(time_from), datetime_to_string(time_to)), '\n')

print('Cars in garage:')
[print('{} ({} - {})'.format(carlog['lic_plate'], datetime_to_string(carlog['time_entered']), datetime_to_string(carlog['time_exited']))) for carlog in all_time_report['cars_parked']]
print()

print('Income:')
print('{} sek'.format(all_time_report['income']))