from IntervalTree import FakeIntervalTree, Node, Interval
from datetime import datetime, timedelta
from math import floor
import functools

#some helper functions
def datetime_to_seconds(datetime):
    return floor(datetime.timestamp())

def seconds_to_datetime(seconds):
    return datetime.fromtimestamp(seconds)

class ParkingGarage:
    def __init__(self, start_datetime, hour_price_sek = 12):
        self.hour_price_sek = hour_price_sek
        self.start_datetime = start_datetime
        self.datetime = start_datetime

        self.in_garage = {}
        self.backlog = FakeIntervalTree()
    
    def tick(self, seconds = 1):
        '''
            ticks internal clock
        '''
        self.datetime += timedelta(seconds = seconds)

    def enter(self, lic_plate):
        '''
            lic_plate: string 

            adds lic_plate and datetime of entering to internal log self.in_garage
        '''
        self.in_garage[lic_plate] = self.datetime

    def exit(self, lic_plate):
        '''
            lic_plate: string

            removes log of lic_plate from self.in_garage and adds it to self.backlog as 
            node containing lic_plate, timestamp for entering and timestamp for exiting
        '''
        if lic_plate in self.in_garage.keys():
            #remove from in_garage and add to backlog

            timestamp_in  = datetime_to_seconds(self.in_garage.pop(lic_plate))
            timestamp_out = datetime_to_seconds(self.datetime)
            

            self.backlog.add(
                Node(
                    timestamp_in,
                    timestamp_out,
                    lic_plate
                    ))

        else:
            #raise error
            raise KeyError('no car with lic_plate = {} in garage'.format(lic_plate))
    
    def get_summary(self,datetime_from, datetime_to):
        '''
            datetime_from: datetime object
            datetime_to: datetime object

            Returns dictionary containing income and log of veicles
            that was in the garage between datetime_from and datetime_to
        '''
        interval = Interval(
            datetime_to_seconds(datetime_from),
            datetime_to_seconds(datetime_to))

        nodes = self.backlog.query(interval)

        previously_parked = list(map(lambda node: {
            'lic_plate':node.data, 
            'time_entered': seconds_to_datetime(node.interval.lo), 
            'time_exited': seconds_to_datetime(node.interval.hi)
            }, nodes))

        currently_parked_inside_inteval = [(key,val) for key,val in self.in_garage.items() if datetime_from < val < datetime_to]
        
        currently_parked = [
            {
            'lic_plate':key, 
            'time_entered': val, 
            'time_exited': None,
            } for key, val in currently_parked_inside_inteval
        ]
        
        def calculate_income(node):
            hours = (node.interval.hi - node.interval.lo) // 3600
            return hours*self.hour_price_sek if seconds_to_datetime(node.interval.hi) < datetime_to else 0

        income = sum(map(calculate_income, nodes))

        return {'income':income, 'cars_parked': currently_parked+previously_parked}


if __name__ == "__main__":

    #Example 
    p = ParkingGarage(datetime(1999,1,9,12,0,0,0))
    p.enter('abc123')
    p.tick(10000)
    p.exit('abc123')
    print(p.get_summary(datetime(1999,1,9,12,0,0,0),datetime(1999,2,9,12,0,0,0)))