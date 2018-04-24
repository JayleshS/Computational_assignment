import numpy as np

a = np.array([ [1,2,3],[1,8,10] ])
b = a>1 

c = a[b]

print '\n a', a
print '\n b', b
print '\n c', c

# print b.shape
#
print np.sum(b)

print a.shape
print c.shape
