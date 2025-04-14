# human_high_frequency_algorithm.py
# algorithm designed by Thane Brooker (Ticks-in-Flow on youtube)

"""
- AS = First, Fast, Large sellers
- AB = First, Fast, Large Buyers 
- SS = Sell Stops triggered in the downward direction.
- SB = Buy Stops triggered in the upward direction. 

0: when market is going down
X: when market is going up
ss: fuel pushing the market lower
ab: fuel pushing the market higher
as: volume traded by speculators selling an up move (people who are going short as a "micro" pull back occurs)
ab: volume traded by speculators buying a down move (people who are going long as a "micro" pull back occurs)

  0  |  X
ss ab|as sb
-----|-----




------------
Only look at events that happen within 5ms of new lower offer or new higher bid
"""
