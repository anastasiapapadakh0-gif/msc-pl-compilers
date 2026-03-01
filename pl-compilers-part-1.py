"""
Ντετερμινιστικό Αυτόματο Στοίβας (ΝΑΣ)
---------------------------------------
Αναγνώριση ορθά δομημένων εκφράσεων παρενθέσεων.
Σύμβολα:
  Αριστερή παρένθεση → 'P' (αρχικό γράμμα επωνύμου: PAPADAKI)
  Δεξιά   παρένθεση → '0'  (τελευταίο ψηφίο ΑΜ: 2530)

Ορισμός ΝΑΣ ως 6-άδα:
  M = (K, Σ, Γ, δ, q0, Z0)   όπου:

  K  = {q0, q_err}             πεπερασμένο σύνολο καταστάσεων
  Σ  = {P, 0}                  αλφάβητο εισόδου
  Γ  = {P, Z0}                 αλφάβητο στοίβας
  δ  = σύνολο κινήσεων
  q0 = q0                      αρχική κατάσταση
  Z0 = Z0                      αρχικό σύμβολο στοίβας

  ** Αποδοχή **
  Η συμβολοσειρά αναγνωρίζεται όταν:
    1. Έχουν διαβαστεί όλα τα σύμβολα εισόδου, και
    2. Το αρχικό σύμβολο Z0 βρίσκεται στην κορυφή της στοίβας.

Κινήσεις δ (move):
  Κάθε κίνηση καθορίζεται από τριάδα:
    (τωρινή κατάσταση, σύμβολο στην κορυφή στοίβας, τωρινό σύμβολο εισόδου)

  δ(q0, Z0|P, P) → push(P),  q0      -- αριστερή παρένθεση: ώθηση στη στοίβα
  δ(q0, P,   0)  → pop,      q0      -- ταίριασμα: αναίρεση από στοίβα
  δ(q0, Z0,  0)  → skip,     q_err   -- '0' χωρίς P: σφάλμα
  δ(q0, Z0,  ε)  → skip,     ACCEPT  -- τέλος εισόδου & Z0: αποδοχή
  δ(q0, P,   ε)  → skip,     REJECT  -- τέλος εισόδου & P: απόρριψη

"""

OPEN   = 'P'
CLOSE  = '0'
BOTTOM = 'Z0'

Q0   = 'q0'   
QERR = 'q_err'


def dpda(expression: str):

    for ch in expression:
        if ch not in (OPEN, CLOSE):
            print(f"  Μη έγκυρος χαρακτήρας '{ch}'. "
                  f"Η έκφραση πρέπει να περιέχει μόνο '{OPEN}' και '{CLOSE}'.")
            return

    stack     = [BOTTOM]
    state     = Q0
    symbols   = list(expression)

    header = f"{'Στοίβα':<25} {'Κατάσταση':<12} {'Υπόλοιπη Είσοδος'}"
    sep    = '-' * len(header)
    print(header)
    print(sep)

    def stack_str():
        return '[' + ', '.join(stack) + ']'

    def print_step(sym_list):
        if sym_list:
            rem = ''.join(sym_list)
        else:
            rem = 'ε'
        print(f"{stack_str():<25} {state:<12} {rem}")

    idx      = 0
    accepted = False

    while True:
        print_step(symbols[idx:])

        if state == QERR:
            break

        if idx == len(symbols):
            if stack[-1] == BOTTOM:
                accepted = True
            else:
                state = QERR
                print_step([])
            break

        symbol = symbols[idx]
        idx += 1
        top = stack[-1]

        if symbol == OPEN:
            stack.append(OPEN)

        elif symbol == CLOSE:
            if top == OPEN:
                stack.pop()
            else:
                state = QERR
                print_step(symbols[idx:])
                break

    print(sep)
    if accepted:
        result = 'YES'
    else:
        result = 'NO'
    print(f"Αποτέλεσμα: {result}\n")

def main():
    print("=" * 55)
    print(" ΝΑΣ - ΜΑΙΝ - Αναγνώριση ορθά δομημένων παρενθέσεων")
    print(f"  Αριστερή παρένθεση: '{OPEN}'  |  Δεξιά παρένθεση: '{CLOSE}'")
    print("=" * 55)
    print("Δώστε έκφραση (ή κενό για έξοδο):\n")

    while True:
        expr = input("Έκφραση: ").strip()
        if not expr:
            print("Έξοδος.")
            break
        dpda(expr)

# Demo - Αυτόματη εκτέλεση παραδειγμάτων
if __name__ == '__main__':
    examples = [
        ('PP00P0', '(())()'),
        ('P0P0',   '()()  '),
        ('PPP000', '((()))'),
        ('0P0P',   ')()(  '),
        ('PP0',    '(()   '),
        ('',       'ε     '),
        ('P0P00',  '()()) '),
    ]

    print("=" * 55)
    print(" ΝΑΣ - DEMO - Αναγνώριση ορθά δομημένων παρενθέσεων")
    print(f"  Αριστερή παρένθεση: '{OPEN}'  |  Δεξιά παρένθεση: '{CLOSE}'")
    print("=" * 55)

    for expr, cl in examples:
        if expr:
            disp = expr
        else:
            disp = 'ε'
        print(f"Έκφραση: '{disp}'  [αντίστοιχο: '{cl.strip()}']")
        dpda(expr)
    main()