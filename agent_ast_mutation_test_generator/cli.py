"""CLI for agent-ast-mutation-test-generator."""
import sys
import argparse
from .mutator import ASTMutationGenerator

def main():
    parser = argparse.ArgumentParser(description="Agent AST Mutation Test Generator CLI")
    parser.add_argument("--demo", action="store_true", help="Run AST mutation generator demo")
    args = parser.parse_args()

    if args.demo:
        code = "def add(a, b): return a + b"
        mutants = ASTMutationGenerator.mutate_code(code)
        print(f"[+] Mutated code: {mutants[0][0]} ({mutants[0][1]})")
        # Test function that catches the mutation
        def strict_test(c):
            loc = {}
            exec(c, {}, loc)
            return loc["add"](2, 3) == 5

        res = ASTMutationGenerator.evaluate_test_suite(code, strict_test)
        print(f"[+] Mutation score: {res.score * 100}% (Killed {res.killed_mutants}/{res.total_mutants})")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
