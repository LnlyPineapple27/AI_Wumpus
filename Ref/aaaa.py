# Import libraries
import aima.utils
import aima.logic
# The main entry point for this module
def main():
    # Create an array to hold clauses
    clauses = []
    # Add first-order logic clauses (rules and fact)
    clauses.append(aima.utils.expr("(ADJ(x, y) & ADJ(x, z) & B(y) & B(z)) ==> PIT(x)"))
    # Create a first-order logic knowledge base (KB) with clauses
    KB = aima.logic.FolKB(clauses)
    # Add rules and facts with tell
    KB.tell(aima.utils.expr('ADJ(A, E)'))
    KB.tell(aima.utils.expr('ADJ(A, C)'))
    KB.tell(aima.utils.expr('B(E)'))
    KB.tell(aima.utils.expr('B(C)'))
    # Get information from the knowledge base with ask
    p = KB.ask(aima.utils.expr('PIT(A)'))
    b = aima.logic.fol_fc_ask(KB, aima.utils.expr('PIT(x)'))
    # Print answers
    print(list(p))
# Tell python to run main method
if __name__ == "__main__": main()