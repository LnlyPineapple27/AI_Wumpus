# Import libraries
import utils
import logic
# The main entry point for this module
def main():
    # Create an array to hold clauses
    clauses = []
    # Add first-order logic clauses (rules and fact)
    clauses.append(utils.expr("(ADJ(x, y) & ADJ(x, z) & B(y) & B(z)) ==> PIT(x)"))
    # Create a first-order logic knowledge base (KB) with clauses
    KB = logic.FolKB(clauses)
    # Add rules and facts with tell
    KB.tell(utils.expr('ADJ(A, E)'))
    KB.tell(utils.expr('ADJ(A, C)'))
    KB.tell(utils.expr('B(E)'))
    KB.tell(utils.expr('B(C)'))
    # Get information from the knowledge base with ask
    p = KB.ask(utils.expr('PIT(A)'))
    b = logic.fol_fc_ask(KB, utils.expr('PIT(x)'))
    # Print answers
    print(list(p))
# Tell python to run main method
if __name__ == "__main__": main()