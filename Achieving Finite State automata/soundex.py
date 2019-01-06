from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """
    removing=['a','e','h','i','o','u','w','y']
    group_1=['b','f','p','v']
    group_2=['c','g','j','k','q','s','x','z']
    group_3=['d','t']
    group_4=['l']
    group_5=['m','n']
    group_6=['r']
    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('next')
    f1.initial_state = 'start'
    
    # Set all the final states
#    f1.set_final('next')

    # Add the rest of the arcs
    for letter in string.ascii_lowercase:
        f1.add_arc('start', 'next', (letter), (letter))
    
    f1.add_state('next_r')
    f1.add_state('next_1')
    f1.add_state('next_2')
    f1.add_state('next_3')
    f1.add_state('next_4')
    f1.add_state('next_5')
    f1.add_state('next_6')
    
    f1.set_final('next_r')
    f1.set_final('next_1')
    f1.set_final('next_2')
    f1.set_final('next_3')
    f1.set_final('next_4')
    f1.set_final('next_5')
    f1.set_final('next_6')
    
    #Removing letters: a,e,h,i,o,u,w,y 
    for letter in removing:
        f1.add_arc('next','next_r', letter,'')
        f1.add_arc('next_r','next_r', letter, '')
        f1.add_arc('next_1','next_r',(letter),'')
        f1.add_arc('next_2','next_r',(letter),'')
        f1.add_arc('next_3','next_r',(letter),'')
        f1.add_arc('next_4','next_r',(letter),'')
        f1.add_arc('next_5','next_r',(letter),'')
        f1.add_arc('next_6','next_r',(letter),'')    

    #Removing letters: b','f','p','v' 
    for letter in group_1:
        f1.add_arc('next','next_1',(letter),(str(1)))
        f1.add_arc('next_1','next_1',(letter),'')
        f1.add_arc('next_r','next_1',(letter),(str(1)))
        f1.add_arc('next_2','next_1',(letter),(str(1)))
        f1.add_arc('next_3','next_1',(letter),(str(1)))
        f1.add_arc('next_4','next_1',(letter),(str(1)))
        f1.add_arc('next_5','next_1',(letter),(str(1)))
        f1.add_arc('next_6','next_1',(letter),(str(1)))
    
    #Removing letters:'c','g','j','k','q','s','x','z'                           
    for letter in group_2:
        f1.add_arc('next','next_2',(letter),(str(2)))
        f1.add_arc('next_2','next_2',(letter),'')
        f1.add_arc('next_r','next_r',(letter),(str(2)))
        f1.add_arc('next_1','next_2',(letter),(str(2)))
        f1.add_arc('next_3','next_2',(letter),(str(2)))
        f1.add_arc('next_4','next_2',(letter),(str(2)))
        f1.add_arc('next_5','next_2',(letter),(str(2)))
        f1.add_arc('next_6','next_2',(letter),(str(2))) 
     
    #Removing letters: 'd','t'
    for letter in group_3:
        f1.add_arc('next','next_3',(letter),(str(3)))
        f1.add_arc('next_3','next_3',(letter),'')
        f1.add_arc('next_r','next_3',(letter),(str(3)))
        f1.add_arc('next_1','next_3',(letter),(str(3)))
        f1.add_arc('next_2','next_3',(letter),(str(3)))
        f1.add_arc('next_4','next_3',(letter),(str(3)))
        f1.add_arc('next_5','next_3',(letter),(str(3)))
        f1.add_arc('next_6','next_3',(letter),(str(3)))
    
    #Removing letters: 'l'
    for letter in group_4:
        f1.add_arc('next','next_4',(letter),(str(4)))
        f1.add_arc('next_4','next_4',(letter),'')
        f1.add_arc('next_r','next_4',(letter),(str(4)))
        f1.add_arc('next_1','next_4',(letter),(str(4)))
        f1.add_arc('next_3','next_4',(letter),(str(4)))
        f1.add_arc('next_2','next_4',(letter),(str(4)))
        f1.add_arc('next_5','next_4',(letter),(str(4)))
        f1.add_arc('next_6','next_4',(letter),(str(4)))
    
    #Removing letters: 'm','n'  
    for letter in group_5:
        f1.add_arc('next','next_5',(letter),(str(5)))
        f1.add_arc('next_5','next_5',(letter),'')
        f1.add_arc('next_r','next_5',(letter),(str(5)))
        f1.add_arc('next_1','next_5',(letter),(str(5)))
        f1.add_arc('next_3','next_5',(letter),(str(5)))
        f1.add_arc('next_4','next_5',(letter),(str(5)))
        f1.add_arc('next_2','next_5',(letter),(str(5)))
        f1.add_arc('next_6','next_5',(letter),(str(5)))
     
    #Removing letter: 'r' 
    for letter in group_6:
        f1.add_arc('next','next_6',(letter),(str(6)))
        f1.add_arc('next_6','next_6',(letter),'')
        f1.add_arc('next_r','next_6',(letter),(str(6)))
        f1.add_arc('next_1','next_6',(letter),(str(6)))
        f1.add_arc('next_3','next_6',(letter),(str(6)))
        f1.add_arc('next_4','next_6',(letter),(str(6)))
        f1.add_arc('next_5','next_6',(letter),(str(6)))
        f1.add_arc('next_2','next_6',(letter),(str(6)))
    
    return f1
    
    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?


def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.add_state('1_1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')
    f2.add_state('5')
    f2.add_state('6')
    f2.add_state('7')
    f2.add_state('8')
    
    f2.initial_state = '1'
    f2.set_final('5')
    f2.set_final('8')
    
    # Add the arcs
    
    #Classifying the first letter
    for letter in string.letters:
        f2.add_arc('1', '2', (letter), (letter))
        
    #Classifying the first digit
    for n in range(10):
        f2.add_arc('2', '3', (str(n)), (str(n)))
        f2.add_arc('1', '1_1', (str(n)), (str(n)))
        f2.add_arc('1_1', '4', (str(n)), (str(n)))
        
    #Classifying the second digit
    for n in range(10):
        f2.add_arc('3', '4', (str(n)), (str(n)))
    
    #Classfying the third digit
    for n in range(10):
        f2.add_arc('4', '5', (str(n)), (str(n)))
    
    #Rest of it would become ''
    for n in range(10):
        f2.add_arc('5', '5', (str(n)), '')
    
    f2.add_arc('2', '6', '', '')
    f2.add_arc('6', '7', '', '')
    f2.add_arc('3', '7', '', '')
    f2.add_arc('7', '8', '', '')
    f2.add_arc('4', '8', '', '')
    f2.add_arc('1_1', '7', '', '')
        
    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?


def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')
    
    f3.add_state('start')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('2a')
    f3.add_state('2b')
    f3.add_state('3a')
    f3.add_state('3b')
    
    f3.initial_state = 'start'
    
    f3.set_final('3a')
    f3.set_final('3b')

    for letter in string.letters:
        f3.add_arc('start', '1a', (letter), (letter))
        
    for number in xrange(10):
        f3.add_arc('start', '1b', (str(number)), (str(number)))
        f3.add_arc('1a', '1b', (str(number)), (str(number)))
        f3.add_arc('1b', '2a', (str(number)), (str(number)))
        f3.add_arc('2a', '3a', (str(number)), (str(number)))
        
    f3.add_arc('1b', '2b', '', '0')
    f3.add_arc('2b', '3b', '', '0')
    f3.add_arc('2a', '3b', '', '0')
    
    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!


if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input),f1,f2,f3)))
