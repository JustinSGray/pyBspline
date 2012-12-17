import pstats

s = pstats.Stats('cb_prof3')

print s.sort_stats('cumulative').print_stats(15)