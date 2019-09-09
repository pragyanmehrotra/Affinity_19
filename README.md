# GolanG Heights - 350pts

### Description 

Note: put flag into AFFCTF{} format and 2 attatchments were given (can be found in the challenge folder)

### The Approach

We were given a .go file which means it was coded in the Go programming language and obviously it followed the Go's syntax. Now, Analyzing the code.

We have our main function - 

```Go
func main() {
	messageInt, err := strconv.ParseInt(os.Args[1], 10, 64)
	if err != nil {
		return
	}
	messageBigInt := big.NewInt(messageInt)
	_, publicKey, err := getKeys()
	if err != nil {
		return
	}
	encryptedMessage := encrypt(messageBigInt, publicKey)
	fmt.Println("Encrypted message: ", encryptedMessage)
}
```
Well we can cleary see that an integer argument must be passed to the program, then we call `getKeys()` to get the `publicKey` and then the message is simply encrypted by the `publickey`, which is what we were given (LOL obviously).

Before moving on to the `getKeys()` function let's have a look at the `encrypt()` function,

```Go
func encrypt(message *big.Int, publicKey *big.Int) *big.Int {
	encryptedMessage := new(big.Int).Rem(new(big.Int).Exp(message, big.NewInt(2), nil) , publicKey)
	return encryptedMessage
}
```

Nice!! So it's the (Rabin cryptosystem)[https://en.wikipedia.org/wiki/Rabin_cryptosystem] we are up against. Now moving on to the `getKeys()` function let's see what it does.

```Go
func getKeys() (privateKeys, *big.Int, error) {
	for true {
		factorHex := make([]byte, 32)
		_, err := rand.Read(factorHex)
		if err != nil {
			return privateKeys{}, big.NewInt(0), err
		}
		factorBigInt := new(big.Int)
		factorBigInt.SetBytes(factorHex)

		p := new(big.Int).Add(new(big.Int).Add(new(big.Int).Mul(new(big.Int).Exp(factorBigInt, big.NewInt(2), nil), big.NewInt(4)), new(big.Int).Mul(factorBigInt, big.NewInt(3))), big.NewInt(7351))
		q := new(big.Int).Add(new(big.Int).Add(new(big.Int).Mul(new(big.Int).Exp(factorBigInt, big.NewInt(2), nil), big.NewInt(19)), new(big.Int).Mul(factorBigInt, big.NewInt(18))), big.NewInt(1379))

		if isPrime(p) && isPrime(q) {
			n := new(big.Int).Mul(p, q)
			return privateKeys{p, q}, n, nil
		}	}

	return privateKeys{}, big.NewInt(0), nil
}
```

Hmmmmmmm, have a look at the definition of p and q, too many function calls, probably to throw us off of something. Exactly! that's what it was just to scare us. Looking closely and obviously reading upon the syntax of Go, It evaluated to a simple formula for p and q for some number `factorBigInt`.

Basically, We got -  (f->factorBigInt)

p = 4f<sup>2</sup> + 3f + 7351
q = 19f<sup>2</sup> + 18f + 1379

Now from the `getKeys()` function we are sure that p, q are primes and our `publicKey` = pq. Now the problem got even easier, although for a good while I completely ignored the fact that p and q were generated like this and wasted time on finding security flaws in `SetBytes()` and `rand.Read()` since they seemed to be generating the same numbers on every run, but moving on from this. Now, we know that 


n = (4f<sup>2</sup> + 3f + 7351)(19f<sup>2</sup> + 18f + 1379)

which evaluates to 

n = 76f<sup>4</sup> + 129f<sup>3</sup> + 145239f<sup>2</sup> + 136455f + 10137029

so we simply needed to find the solution to the above polynomial since we can see all the coefficients are positive thus the above polynomial is monotonically increasing in the positive domain. So we can easily use binary search to find it's solution. Once we have the solutions we have p and q which pretty much solves the problem.

### Final Exploit

```python
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

#rabin decrypt 
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
```
