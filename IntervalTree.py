
class FakeIntervalTree:
    def __init__(self, nodes = []):
        self.nodes = nodes

    def add(self,node):
        self.nodes.append(node)

    def query(self, interval):
        return list(filter(lambda node: node.interval.intersection(interval) > 0, self.nodes))


class Interval:
    def __init__(self, lo, hi):
        self.lo = lo
        self. hi = hi
    
    def intersection(self, other):
        '''
            returns intersection between one interval and another
        '''
        return max(0, min(self.hi, other.hi) - max(self.lo, other.lo))
    
    def __repr__(self):
        return '{}<->{}'.format(self.lo, self.hi)

class Node:
    def __init__(self, lo, hi, data):
        self.interval = Interval(lo,hi)
        self.data = data
    
    def __repr__(self):
        return '({} : {})'.format(self.interval, self.data)

    

if __name__ == "__main__":

    #Example 
    tree = FakeIntervalTree([
        Node(0,1,'0-1'),
        Node(2,5,'2-5'),
        Node(2,3,'2-3'),
        Node(5,9,'5-9'),
    ])

    print(tree.query(Interval(6,7)))
