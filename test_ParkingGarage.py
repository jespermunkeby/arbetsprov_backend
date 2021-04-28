import unittest
from ParkingGarage import ParkingGarage
from datetime import datetime

#Some very minimal testing

class TestParkingGarage(unittest.TestCase):

    def test_tick(self):
        p = ParkingGarage(datetime(1999,1,9,12,0,0,0))
        time_before = p.datetime
        p.tick()
        time_after = p.datetime
        self.assertTrue(time_before<time_after)
    
    def test_enter(self):
        p = ParkingGarage(datetime(1999,1,9,12,0,0,0))
        p.enter('abc123')
        self.assertTrue('abc123' in p.in_garage)

    def test_exit(self):
        p = ParkingGarage(datetime(1999,1,9,12,0,0,0))
        p.enter('abc123')
        p.exit('abc123')
        self.assertEqual(p.backlog.nodes[0].data, 'abc123') 

    def test_get_summary(self):
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
        p = ParkingGarage(datetime(1999,1,1,0,0,0,0)) #00:00
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

        all_time_report = p.get_summary(p.start_datetime,p.datetime)
        self.assertEqual(len(all_time_report['cars_parked']), 5)
        self.assertEqual(all_time_report['income'], (1+1+3+0+1)*12)

        #Partial query
        report = p.get_summary(datetime(1999,1,1,1,0,0,0), datetime(1999,1,1,2,0,0,0)) #01:00 - 02:00
        self.assertEqual(len(report['cars_parked']), 3)


        #Empty queries

        p = ParkingGarage(datetime(1999,1,1,0,0,0,0))
        report = p.get_summary(p.start_datetime,p.datetime)
        self.assertEqual(len(report['cars_parked']), 0)


if __name__ == '__main__':
    unittest.main()