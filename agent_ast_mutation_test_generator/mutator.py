"""AST mutation test generator and mutation score evaluator."""
import ast
from typing import Dict, List, Optional, Tuple, Any, Callable

class MutationResult:
    def __init__(self, total_mutants: int, killed_mutants: int, score: float, survived_mutants: List[str]):
        self.total_mutants = total_mutants
        self.killed_mutants = killed_mutants
        self.score = score
        self.survived_mutants = survived_mutants

class BinaryOpMutator(ast.NodeTransformer):
    def __init__(self):
        self.mutation_applied = False
        self.mutation_desc = ""

    def visit_Add(self, node: ast.Add):
        if not self.mutation_applied:
            self.mutation_applied = True
            self.mutation_desc = "Replaced Add (+) with Sub (-)"
            return ast.Sub()
        return node

    def visit_Lt(self, node: ast.Lt):
        if not self.mutation_applied:
            self.mutation_applied = True
            self.mutation_desc = "Replaced Lt (<) with Gt (>)"
            return ast.Gt()
        return node

class ASTMutationGenerator:
    """Injects syntax-tree mutations and checks if test suites kill them."""

    @staticmethod
    def mutate_code(source_code: str) -> List[Tuple[str, str]]:
        tree = ast.parse(source_code)
        mutants = []

        mutator = BinaryOpMutator()
        mutated_tree = mutator.visit(tree)
        if mutator.mutation_applied:
            ast.fix_missing_locations(mutated_tree)
            mutated_code = ast.unparse(mutated_tree)
            mutants.append((mutated_code, mutator.mutation_desc))

        return mutants

    @staticmethod
    def evaluate_test_suite(source_code: str, test_func: Callable[[str], bool]) -> MutationResult:
        mutants = ASTMutationGenerator.mutate_code(source_code)
        if not mutants:
            return MutationResult(0, 0, 1.0, [])

        killed = 0
        survived = []
        for code, desc in mutants:
            passed = test_func(code)  # If test passes on mutated code, mutant survived (bad!)
            if not passed:
                killed += 1
            else:
                survived.append(desc)

        score = killed / len(mutants)
        return MutationResult(len(mutants), killed, round(score, 4), survived)
