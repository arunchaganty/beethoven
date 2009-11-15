#
#   irify - IR-ifies MIDI files
#

# small = 0, large = 1

def is_small(note1, note2):
    return abs(note1 - note2) <= 3   # a minor third

def same_dir(note1, note2, note3):
    return ((note2 - note1 < 0) and (note3 - note1 < 0)) or ((note2 - note1 > 0) and (note3 - note1 > 0)) 

class Transition:
    def __init__(self, interval, direction):
        interval = (0,0)
        direction = (0,0)

sym = {}

# Type: intervallic change; registral change

# Similar == differential of <= minor third 

# Process: small -> small ; no change 
sym['P'] = lambda(n1, n2, n3):(is_small(n1, n2) and is_small(n2,n3) and same_dir(n1,n2,n3))
# Registral Process: small -> large ; no change 
sym['VP'] = lambda(n1, n2, n3):(is_small(n1, n2) and not is_small(n2,n3) and same_dir(n1,n2,n3))
# Intervallic Process: small -> small; change
sym['IP'] = lambda(n1, n2, n3):(is_small(n1, n2) and is_small(n2,n3) and not same_dir(n1,n2,n3))
# Duplication: X; Same note
sym['D'] = lambda(n1, n2, n3):(n1 == n2 == n3)
# Intervallic Duplication: small -> same small; change
sym['ID'] = lambda(n1, n2, n3):(is_small(n1, n2) and is_small(n2,n3) and abs(n2-n1) == abs(n3-n2) and not same_dir(n1,n2,n3))
# Reversal: large -> small; change
sym['R'] = lambda(n1, n2, n3):(not is_small(n1, n2) and is_small(n2,n3) and not same_dir(n1,n2,n3))
# Registral Reversal : large -> even larger; change
sym['VR'] = lambda(n1,n2,n3):(not is_small(n1, n2) and not is_small(n2,n3) and abs(n2-n1) < abs(n3-n2) and not same_dir(n1,n2,n3))
# Intervallic Reversal: large -> small; same
sym['IR'] = lambda(n1,n2,n3):(not is_small(n1, n2) and is_small(n2,n3) and same_dir(n1,n2,n3))
# Exact registral return: 1st and 3rd tones are same
sym['aba'] = lambda(n1,n2,n3):(n1 == n3 and n1 != n2)
# Near registral return: 1st and 3rd differ by no more than a major 2nd
sym['aba1'] = lambda(n1,n2,n3):(abs(n1 - n3) < 4 and n1 != n2)
# Dyads: two-element groupings - the unrealised implications of processes and reversals
sym['dyn'] = ?
# Monads: one-element groupings - the unrealised implications of processes and reversals
sym['M'] = ?

