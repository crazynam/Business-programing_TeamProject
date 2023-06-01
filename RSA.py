import math
import random
import time


def isPrime(ilnteger):
 if ilnteger <= 1:
   return False
 else:
   for d in range(2, int(math.sqrt(ilnteger))+1):
     if ilnteger % d == 0:
       return False

   return True

# i프라임넘버가 1씩 증가시켜 소수면 리스트에 추가시키는함수
def createListPrimeNumber(iNPrimeNumbers,iMinimumPrimeNumber=2):
  liPrime = []
  i = iMinimumPrimeNumber
  while True:
    if isPrime(i):
      liPrime.append(i)
      if len(liPrime) >= iNPrimeNumbers:
        break

    i += 1
  return liPrime

# 소수리스트 liPrime 으로부터 pq선택후 n,phi계산
liPrime = createListPrimeNumber(100,100)
p = liPrime[random.randint(0,len(liPrime))]
q = liPrime[random.randint(0,len(liPrime))]
n = p * q
phi = (p - 1) * (q - 1)

# d선택 pq보다 크고 phi보다 작은 수중 phi와 서로소인 정수 리스트 함수
def createListCoprimeNumber(p,q,phi):
  liCoprime = []
  for i in range(max(p,q),phi):
    if math.gcd(i,phi) == 1:
      liCoprime.append(i)
  return liCoprime

# phi와 개인키 생성 함수
def createPrivateKey(iNPrimeNumbers,iMinimumPrimeNumber=2):
  liPrime = createListPrimeNumber(iNPrimeNumbers,iMinimumPrimeNumber)
  p = liPrime[random.randint(0,len(liPrime))]
  q = liPrime[random.randint(0,len(liPrime))]
  n = p * q
  phi = (p - 1) * (q - 1)
  liCoprime = createListCoprimeNumber(p,q,phi)
  d = liCoprime[random.randint(0,len(liCoprime))]
  return d, n, phi

#개인키 d 공개키 n phi값으로 공개키 계산
def calculateE(d,n,phi):
  IX = [phi,d]
  IA = [1,0]
  IB = [0,1]
  IQ = [0]
  i = 2

  while True:
    qi_1 = IX[i-2] // IX[i-1]
    xi = IX[i-2] % IX[i-1]
    if xi == 0:
      break
    ai = IA[i-2] - qi_1 * IA[i-1]
    bi = IB[i-2] - qi_1 * IB[i-1]
    IQ.append(qi_1)
    IX.append(xi)
    IA.append(ai)
    IB.append(bi)
    i += 1
  if IB[-1] >= 0:
    return IB[-1] % phi
  else:
    return IB[-1] + phi * ((-IB[-1]) // phi + 1)

def createPublicKey(d,n,phi):
  e = calculateE(d, n, phi)
  return e, n


def power(a, b, m): #b를 2로 나누면서 제곱을 해주는 것
  result = 1
  while b > 0:
    if b % 2 != 0: #지수(b)가 홀수면 result에 a를 곱함
      result = (result * a) % m
    b //= 2 #지수를 반으로 나눈 몫으로 지정 , 지수가 짝수이면 result 연산안해줌)
    a = (a * a) % m # a는 계속 커지는 중

  return result


#암호화 함수
def encrypt(liCardNumber, e, n):
  liCipher = []
  for i in liCardNumber:
    liCipher.append(power(i,e,n))
  return liCipher

#복호화 함수
def decrypt(liCipher, d, n):
  return encrypt(liCipher, d, n)

random.seed(int(time.time() * 1000000))

d,n,phi = createPrivateKey(100,100)
e, n = createPublicKey(d,n,phi)

strattime = time.time()

#카드번호넣기
#sCardNumber = input("16자리 숫자를 입력하세요 : ")  입력
sCardNumber = "1111222233334444"   # 속도 비교를 위한 값 미리 정해놓기
liCardNumber = [int(sCardNumber[0:4]),int(sCardNumber[4:8]),int(sCardNumber[8:12]),int(sCardNumber[12:16])]
print("Original Card Number:", liCardNumber)

liCipher = encrypt(liCardNumber,e,n)
print("Encrypted Card Number:", liCipher)

liDecryptedCardNumber = decrypt(liCipher,d,n)
print("Decrypted Card Number: ",liDecryptedCardNumber)

endtime = time.time()
a = endtime - strattime

print(a)

