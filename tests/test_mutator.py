"""Unit tests for agent-ast-mutation-test-generator."""
import unittest
from agent_ast_mutation_test_generator.mutator import ASTMutationGenerator

class TestASTMutator(unittest.TestCase):
    def test_mutate_addition(self):
        code = "def calc(x): return x + 10"
        mutants = ASTMutationGenerator.mutate_code(code)
        self.assertEqual(len(mutants), 1)
        self.assertIn("-", mutants[0][0])

    def test_kill_mutant(self):
        code = "def calc(x): return x + 10"
        def good_test(c):
            loc = {}
            exec(c, {}, loc)
            return loc["calc"](5) == 15
        res = ASTMutationGenerator.evaluate_test_suite(code, good_test)
        self.assertEqual(res.killed_mutants, 1)
        self.assertEqual(res.score, 1.0)

if __name__ == "__main__":
    unittest.main()
