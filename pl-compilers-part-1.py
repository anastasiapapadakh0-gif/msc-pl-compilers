"""
Ντετερμινιστικό Αυτόματο Στοίβας (ΝΑΣ)
---------------------------------------
Αναγνώριση ορθά δομημένων εκφράσεων παρενθέσεων.
Σύμβολα:
  Αριστερή παρένθεση → 'P'
  Δεξιά   παρένθεση → '0'

Ορισμός ΝΑΣ ως 6-άδα:
  M = (K, Σ, Γ, δ, q0, Z0)   όπου:

  K  = {q0, q_err}             πεπερασμένο σύνολο καταστάσεων
  Σ  = {P, 0}                  αλφάβητο εισόδου
  Γ  = {P, Z0}                 αλφάβητο στοίβας
  δ  = σύνολο κινήσεων (βλ. παρακάτω)
  q0 = q0                      αρχική κατάσταση
  Z0 = Z0                      αρχικό σύμβολο στοίβας

  ** Αποδοχή **
  Η συμβολοσειρά αναγνωρίζεται όταν:
    1. Έχουν διαβαστεί ΟΛΑ τα σύμβολα εισόδου, ΚΑΙ
    2. Το αρχικό σύμβολο Z0 βρίσκεται στην κορυφή της στοίβας.

Κινήσεις δ (move):
  Κάθε κίνηση καθορίζεται από τριάδα:
    (τωρινή κατάσταση, σύμβολο στην κορυφή στοίβας, τωρινό σύμβολο εισόδου)

  δ(q0, Z0, P) = (ΒΑΛΕ(P), ΠΡΟΧΩΡΑ, q0)   → push P
  δ(q0, P,  P) = (ΒΑΛΕ(P), ΠΡΟΧΩΡΑ, q0)   → push P
  δ(q0, P,  0) = (ΒΓΑΛΕ,   ΠΡΟΧΩΡΑ, q0)   → pop P (ταίριασμα)
  δ(q0, Z0, 0) = (ΑΦΗΣΕ,   ΚΡΑΤΑ,  q_err) → '0' χωρίς P → σφάλμα
  -- τέλος εισόδου & Z0 στην κορυφή       → ΑΠΟΔΟΧΗ
  -- τέλος εισόδου & P  στην κορυφή       → ΑΠΟΡΡΙΨΗ (έμεινε P)
"""

OPEN   = 'P'    # αριστερή παρένθεση
CLOSE  = '0'    # δεξιά παρένθεση
BOTTOM = 'Z0'   # αρχικό σύμβολο στοίβας

# Σύνολο καταστάσεων K
Q0   = 'q0'
QERR = 'q_err'


def dpda(expression: str):
    """
    Εκτελεί το ΝΑΣ στην έκφραση και τυπώνει κάθε βήμα.
    Αποδοχή όταν: διαβάστηκε όλη η είσοδος ΚΑΙ Z0 στην κορυφή.
    Επιστρέφει 'YES' ή 'NO'.
    """
    for ch in expression:
        if ch not in (OPEN, CLOSE):
            print(f"  Μη έγκυρος χαρακτήρας '{ch}'. "
                  f"Η έκφραση πρέπει να περιέχει μόνο '{OPEN}' και '{CLOSE}'.")
            return 'NO'

    stack     = [BOTTOM]   # στοίβα — κορυφή = τελευταίο στοιχείο
    state     = Q0
    remaining = list(expression)

    header = f"{'Στοίβα':<20} {'Κατάσταση':<10} {'Υπόλοιπη Είσοδος'}"
    sep    = '-' * len(header)
    print(header)
    print(sep)

    def stack_str():
        return '[' + ', '.join(stack) + ']'

    def print_step(rem_list):
        rem = ''.join(rem_list) if rem_list else 'ε'
        print(f"{stack_str():<20} {state:<10} {rem}")

    idx      = 0
    accepted = False

    while True:
        print_step(remaining[idx:])

        if state == QERR:
            break

        # Τέλος εισόδου — έλεγχος αποδοχής
        if idx == len(remaining):
            # Αποδοχή: Z0 στην κορυφή (όλα τα P ταιριάστηκαν)
            if stack[-1] == BOTTOM:
                accepted = True
            # Απόρριψη: P στην κορυφή (έμειναν ανοιχτές παρενθέσεις)
            else:
                state = QERR
                print_step([])
            break

        symbol = remaining[idx]
        idx += 1
        top = stack[-1]

        if symbol == OPEN:
            # δ(q0, Z0|P, P) = ΒΑΛΕ(P) → push
            stack.append(OPEN)

        elif symbol == CLOSE:
            if top == OPEN:
                # δ(q0, P, 0) = ΒΓΑΛΕ → pop (ταίριασμα)
                stack.pop()
            else:
                # δ(q0, Z0, 0) → σφάλμα, '0' χωρίς αντίστοιχο P
                state = QERR
                print_step(remaining[idx:])
                break

    print(sep)
    if accepted:
        print(f"Τέλος εισόδου & Z0 στην κορυφή → ΑΠΟΔΟΧΗ")
    else:
        print(f"Απόρριψη")
    result = 'YES' if accepted else 'NO'
    print(f"Αποτέλεσμα: {result}\n")
    return result


def main():
    print("=" * 55)
    print("  ΝΑΣ - Αναγνώριση ορθά δομημένων εκφράσεων παρενθέσεων")
    print(f"  Αριστερή παρένθεση: '{OPEN}'  |  Δεξιά παρένθεση: '{CLOSE}'")
    print("=" * 55)
    print("Δώστε έκφραση (ή κενό για έξοδο):\n")

    while True:
        try:
            expr = input("Έκφραση: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not expr:
            print("Έξοδος.")
            break
        dpda(expr)


# --- Demo με παραδείγματα ---
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
    print("  ΝΑΣ - Αναγνώριση Σωστά Φωλιασμένων Παρενθέσεων")
    print(f"  Αριστερή παρένθεση: '{OPEN}'  |  Δεξιά παρένθεση: '{CLOSE}'")
    print("=" * 55)
    print("\n=== Αυτόματη Εκτέλεση Παραδειγμάτων ===\n")

    for expr, cl in examples:
        disp = expr if expr else 'ε'
        print(f"\n>>> Έκφραση: '{disp}'  (κλασ.: '{cl.strip()}')")
        dpda(expr)

    print("\n=== Ολοκλήρωση Παραδειγμάτων ===")
    print("\n--- Διαδραστική λειτουργία ---")
    main()