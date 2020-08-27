# Import libraries
import aima.utils
import aima.logic


# The main entry point for this module
def main():
    # Init
    sen = ["(ADJ(x, y) & ADJ(x, z) & B(y) & B(z)) ==> PIT(x)",
           "(ADJ(x, y) & ADJ(x, z) & S(y) & S(z)) ==> WUM(x)"]
    # Create an array to hold clauses
    clauses = [aima.utils.expr(s) for s in sen]
    # Create a first-order logic knowledge base (KB) with clauses
    KB = aima.logic.FolKB(clauses)
    # Add rules and facts with tell
    KB.tell(aima.utils.expr('ADJ(A, E)'))
    KB.tell(aima.utils.expr('ADJ(A, C)'))
    KB.tell(aima.utils.expr('B(E)'))
    KB.tell(aima.utils.expr('B(C)'))
    KB.tell(aima.utils.expr('ADJ(A, E)'))
    KB.tell(aima.utils.expr('ADJ(A, C)'))
    KB.tell(aima.utils.expr('S(E)'))
    KB.tell(aima.utils.expr('S(C)'))
    # Get information from the knowledge base with ask
    p = KB.ask(aima.utils.expr('WUM(A)'))
    b = aima.logic.fol_fc_ask(KB, aima.utils.expr('WUM(x)'))
    # Print answers
    print(p)
    print(list(b))


# Tell python to run main method
main()
