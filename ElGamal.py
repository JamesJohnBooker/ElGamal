import random #This is necessary to make use of Python's `random' function, as random numbers are used for generating and testing potential primes.
import math #This is necessary to make use of the `ceil' function in generating bounds for the RSA modulus and primes.



def modularExponentiation(base, exponent, modulus): #This function performs modular exponentiation using a square-and-multiply algorithm, reducing intermediate steps modulo `modulus'. The algorithm can also perform exponentiation without reducing intermediate steps, if desired, by passing 0 as the `modulus' parameter (since performing calculations modulo 0 isn't defined anyway).
    value = 1 #The variable `value' is initialised to 1, and is returned as `value' = `base'^(`exponent') mod (`modulus').
    while exponent > 0: #The square-and-multiply algorithm based on the one described in the RSA section of this project runs by incrementally increasing `value' based on the current value of `exponent`, until `exponent' = 0.
        if exponent % 2 == 1: #If `exponent' is odd, then `value' is multiplied by `base' and `exponent' is decremented by 1.
            value = value * base
            if modulus != 0: #If the value of `modulus' is non-zero, then `value' is reduced modulo `modulus' between calculations.
                value = value % modulus
            exponent = exponent - 1
        else: #If `exponent' is even, then `base' is squared and `exponent' is halved.
            base = base * base
            if modulus != 0: #If the value of `modulus' is non-zero, then `base' is reduced modulo `modulus' between calculations.
                base = base % modulus
            exponent //= 2
    return value #The variable `value' (which now equals `base'^(`exponent') mod (`modulus')) is passed back to wherever modularExponentiation() was called from.



def generateLargeOddNumber(lowerBound, upperBound): #This function takes an upper and lower bound for a potential prime, and generates numbers in that range until an odd one is found. This eliminates trivially non-prime numbers and theoretically halves the number of numbers that would need to be tested before a prime is found (as mentioned previously in the RSA section of this project).
    pIsOdd = False #The boolean variable `pIsOdd' (determining whether or not `p' is an odd number) is initialised to be false.
    while pIsOdd == False: #This while loop runs until a generated `p' is odd.
        p = random.randint(lowerBound, upperBound) #`p' is defined to be a random integer between the variables `lowerBound' and `upperBound' (inclusive).
        if p % 2 == 1: #If `p' is odd then the loop ends, otherwise another value of `p' is generated.
            pIsOdd = True
    return p #The generated odd number `p' is returned to generateSophieGermainPrimeCongruentToOneModuloFour() to be tested for primality.



def primalityTestMillerRabin(p, repetitionsOfMillerRabin): #This function performs `repetitionsOfMillerRabin' repetitions of the Miller-Rabin primality test on the number `p'. 
    pMinusOneFactor = p - 1 #`pMinusOneFactor' is initialised to be `p' - 1. Since `p' is odd, `p' - 1 is even, and so `p' - 1 = (2^(k))*t for some natural numbers k and t, where t is odd.
    powerOfTwo = 0 #`powerOfTwo' is initialised to be 0, and is incremented to be equal to k (as defined above).
    while pMinusOneFactor % 2 == 0: #This while loop divides `pMinusOneFactor' by 2 until the resulting value is odd, incrementing `powerOfTwo' by 1 with each division. That is, it divides `pMinusOneFactor' by 2 and increments `powerOfTwo' k times until `pMinusOneFactor' = t and `powerOfTwo' = k, as k and t are defined above.
        pMinusOneFactor //= 2
        powerOfTwo += 1
    t = pMinusOneFactor #Since `pMinusOneFactor' = t (as t is defined above), the variable `t' is initialised for convenience.
    k = powerOfTwo #Since `powerOfTwo' = k (as k is defined above), the variable `k' is initialised for convenience.
    parametersTested = [] #This list keeps track of all the parameters used to test `p' for primality.
    for i in range(0, repetitionsOfMillerRabin): #This for loop repeats the Miller-Rabin primality test on `p' a number of times equal to `repetitionsOfMillerRabin'. Note that `for i in range(0, repetitionsOfMillerRabin)' here means for all i in {0, 1, 2, ..., `repetitionsOfMillerRabin' - 1} and so the loop runs `repetitionsOfMillerRabin' times.
        parameterTestedAlready = True
        while parameterTestedAlready == True: #This while loop generates parameters until a new one that hasn't been tested before is generated, at which point the loop breaks and the test begins.
            a = random.randint(2, p - 2) #Generates a random parameter to test the prime `p'.
            if a not in parametersTested:
                parametersTested.append(a)
                break
        at = modularExponentiation(a, t, p) #Initialises the variable `at' as `at' = `a'^(`t') mod (`p').
        if at != 1: #These nested if statements track the conditions of the Miller-Rabin primality test. If `a'^(`t') is not congruent to 1 or -1 mod (`p') and if `a'^(`t'*2^(`j')) is not congruent to -1 mod (`p') for all 1 <= `j' <= `k' - 1, then `p' is composite, in which case the function returns false. Otherwise, the code skips to the next loop where a new parameter `a' is generated and tested.
            if at != p - 1:
                for j in range(0, k):
                    at = modularExponentiation(at, 2, p)
                    if at != p - 1:
                        if j == k - 1: #If `p' has met the conditions of each if statement up to `j' = `k' - 1, then it has met all the requirements of the test to prove that `p' is composite.
                            return False #The fact that `p' is not prime is returned.
                        else:
                            continue
                    else:
                        break
                continue
            else:
                continue
        else:
            continue
    return True #If `p' has failed to be proven composite for each iteration of the for loop, then the probability that `p' is not prime is at most (1/4)^(-`repetitionsOfMillerRabin'), and so the fact that `p' is (almost certainly) prime is returned to generateSophieGermainPrimeCongruentToOneModuloFour().



def generateSophieGermainPrimeCongruentToOneModuloFour(minBitLength, repetitionsOfMillerRabin): #This function generates a Sophie Germain prime `p' congruent to 1 modulo 4, of bit length at least `minBitLength', and returns 2`p' + 1, which is a prime with the desired property that 2 is a primitive root modulo 2`p' + 1.
    primeDecimalLengthLowerBound = math.ceil((minBitLength * math.log(2, 10)) + 1) #The lower bound for the bit length of `p' is converted to decimal so that less exponentiation operations are required.
    lowerBound = modularExponentiation(10, primeDecimalLengthLowerBound - 1, 0) #The lower bound for `p' is set to be the smallest `primeDecimalLengthLowerBound'-digit number.
    upperBound = modularExponentiation(10, primeDecimalLengthLowerBound, 0) - 1 #The upper bound for `p' is set to be the largest `primeDecimalLengthLowerBound'-digit number.
    pIsProbablyPrime = False
    pIsProbablySophieGermainPrime = False
    while pIsProbablySophieGermainPrime == False: #This while loop continually generates odd numbers `p' and tests them for until a Sophie Germain prime congruent to 1 modulo 4 is found that passes `repetitionsOfMillerRabin' iterations of the Miller-Rabin test.
        p = generateLargeOddNumber(lowerBound, upperBound) #An odd number in the appropriate range is generated.
        if p % 4 == 1: #`p' is only tested for primality if it is congruent to 1 modulo 4.
            pIsProbablyPrime = primalityTestMillerRabin(p, repetitionsOfMillerRabin) #`p' is tested for primality.
            if pIsProbablyPrime == True:
                pIsProbablySophieGermainPrime = primalityTestMillerRabin((2 * p) + 1, repetitionsOfMillerRabin) #2`p' + 1 is tested for primality (i.e. `p' is tested for Sophie Germain primality).
    return (2 * p) + 1 #Returns the (probable) prime 2`p' + 1 to DiffieHellmanKeyExchange(). Note that 2`p' + 1 is at most two bits longer than `p'.



def ElGamalEncryption(p, alpha, beta, m): #This function performs the ElGamal encryption operation (following the algorithm in the ElGamal section of this project).    
    k = random.randint(1, p - 1) # k is generated randomly each time encryption is performed for security purposes. The value of k does not affect the decryption procedure.
    gamma = modularExponentiation(alpha, k, p)
    delta = (modularExponentiation(beta, k, p) * m) % p
    return gamma, delta #This pair of values is the ciphertext for the message m, which is returned. 



def ElGamalDecryption(p, d, gamma, delta): #This function peforms the ElGamal encryption operation (following the algorithm in the ElGamal section of this project).
    n = (modularExponentiation(gamma, p - 1 - d, p) * delta) % p
    return n #The returned value n will be equal to the message m.
    


def ElGamalKeyGeneration(minBitLength, repetitionsOfMillerRabin):
    p = generateSophieGermainPrimeCongruentToOneModuloFour(minBitLength, repetitionsOfMillerRabin) #A prime q is generated to be a Sophie Germain prime of the desired size such that `q' is congruent to 1 modulo 4 (for reasons discussed in the Diffie-Hellman section of this project). Then, the prime `p' = 2q + 1 is returned.
    alpha = 2 #For the generated `p' with the desired properties, 2 is certainly a primitive root modulo `p' so `alpha' is chosen to be equal to 2.
    d = random.randint(1, p - 1)
    beta = modularExponentiation(alpha, d, p)
    return p, alpha, beta, d #Here, (`p', `alpha', `beta') is the user's public key and `d' is the user's private key.



def main(): #This function just initialises the lower bound for the bit length of the prime used and the number of repetitions of the Miller-Rabin test desired, then calls function to begin generating a Diffie-Hellman shared secret.
    minBitLength = 100
    repetitionsOfMillerRabin = 100
    p, alpha, beta, d = ElGamalKeyGeneration(minBitLength, repetitionsOfMillerRabin) #A public key (`p', `alpha', `beta') and private key `d' is generated for some user.
    m = random.randint(0, p - 1) #Here `m' is just a randomly generated value, while in practice there would be some method of converting a message into an integer in the appropriate range.
    gamma, delta = ElGamalEncryption(p, alpha, beta, m) #The ciphertext for m is generated.
    n = ElGamalDecryption(p, d, gamma, delta) #The decryption procedure recovers the value `n' from the ciphertext (which will be equal to `m').



main() #This just calls the main() function which runs through initialising certain variables and calling the relevant functions for ElGamal key generation, encryption and decryption.