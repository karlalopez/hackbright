import random

print "Welcome to the guessing game"
player = raw_input("What's your name? ")
high_score = 0

while True:

    number = random.choice(range(1,100))
    print number

    guesses = 0

    while True:
        guesses +=1
        guess = raw_input("Guess a number between 1 and 100: ")
        if int(guess) == number:
            print "Wonderful, {}. The number is {} and you guessed in only {}!".format(player, number, guesses)
            break
        else:
            if number < int(guess) and int(guess) <= 100:
                print "Too high!"
            if number > int(guess) and int(guess) >=1:
                print "Too low!"
            else:
                print "I said between 1 and 100."


    if guesses < high_score:
        high_score = guesses
    cont = raw_input("Do you want to play again? (y/n)")

    if cont == "n" or cont == "no":
        print "Your highest score on this session was {}".format(high_score)
        break
