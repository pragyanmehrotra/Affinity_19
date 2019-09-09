n = 825321266319602503456977005474981604870402407335194099572979028339224439122246767155608828548258547874076592811333439775645799852274012447643240804287007452861599291275940862131595970247906775549656137041013432613989092491697319873901497907382123859210758943466373193369020798176192106305153278525778145033
ct = 801050608421922967220624523903721496853411844056321773877598932155971380872263121340024512973182420871402804237809506243995703890886804092449855251892886296340338442367792297266755554172082930224889412735287102163161928535579728998850091020972410977027707699268899998522781790134147981974412918582618345868


def getKeys(f):
	#p and q are made by this logic for any given f-> factorBigInt
	p = 7351 + (3*f + 4*pow(f,2))
	q = 1379 + (18*f + 19*pow(f,2))
	if(p*q == n):
		return p,q
	assert 1 == 0
	return

def poly(x):
	#We know that n = p*q which evalutes to a polynomial P(x)
	#P(x) - n is the following polynomial
	return 76*pow(x,4) + 129*pow(x,3) + 145239*pow(x,2) + 136455*x + 10137029 - n

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b / a) * y, y)


#binary searching the solutions
low = 0
high = n

while True:
	mid = (low + high)/2
	if poly(mid) == 0:
		#print mid
		break
	if poly(mid) > 0:
		high = mid -1
		continue
	else:
		low = mid + 1

f = mid

p,q = getKeys(mid)

mp = pow(ct,(p+1)/4,p)
mq = pow(ct,(q+1)/4,q)

a,yp,yq = egcd(p,q)
r1 = (yp*p*mq + yq*q*mp)%n
r2 = n-r1
r3 = (yp*p*mq - yq*q*mp)%n
r4 = n - r3

try:
	print "AFFCTF{" + hex(r1)[2:-1].decode('hex') + "}"
except:
	pass
try:
	print "AFFCTF{" + hex(r2)[2:-1].decode('hex') + "}"
except:
	pass
try:
	print "AFFCTF{" + hex(r3)[2:-1].decode('hex') + "}"
except:
	pass
try:
	print "AFFCTF{" + hex(r4)[2:-1].decode('hex') + "}"
except:
	pass