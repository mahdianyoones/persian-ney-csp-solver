import unittest

class test_CASE_RUNNER(unittest.TestCase):

    def assert_constraint(self, csp, sut, mth, given, expect):
        csp.unassign_all()
        # arrange
        D = csp.get_domains()
        if "D" in given:
            for var, domain in given["D"].items():
                csp.update_domain(var, domain)
        if "A" in given:
            for var, val in given["A"].items():
                csp.assign(var, val)
        # act
        participants = given["participants"]
        if mth == "propagate":
            out = sut.propagate(csp, given["reduced_vars"], participants)
        else:
            out = sut.establish(csp, given["curvar"], given["value"], participants)
        # assess
        self.assertEqual(out, expect["out"])
        if "D" in expect:
            for var, domain in expect["D"].items():
                self.assertEqual(D[var], expect["D"][var])
        return out