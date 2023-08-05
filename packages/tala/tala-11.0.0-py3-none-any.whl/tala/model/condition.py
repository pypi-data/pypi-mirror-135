class Condition():

    HAS_VALUE = "HasValue"
    IS_TRUE = "IsTrue"
    HAS_SHARED_VALUE = "HasSharedValue"
    HAS_PRIVATE_VALUE = "HasPrivateValue"
    HAS_SHARED_OR_PRIVATE_VALUE = "HasSharedOrPrivateValue"
    IS_SHARED_COMMITMENT = "IsSharedCommitment"
    IS_PRIVATE_BELIEF = "IsPrivateBelief"
    IS_PRIVATE_BELIEF_OR_SHARED_COMMITMENT = "IsPrivateBeliefOrSharedCommitment"

    def __init__(self, type):
        self._type = type

    @property
    def condition_type(self):
        return self._type

    def is_has_value_condition(self):
        return self.condition_type in [
            self.HAS_VALUE, self.HAS_SHARED_VALUE, self.HAS_PRIVATE_VALUE, self.HAS_SHARED_OR_PRIVATE_VALUE
        ]

    def is_is_true_condition(self):
        return self.condition_type in [
            self.IS_TRUE, self.IS_SHARED_COMMITMENT, self.IS_PRIVATE_BELIEF, self.IS_PRIVATE_BELIEF_OR_SHARED_COMMITMENT
        ]

    def is_true_given_proposition_set(self, _):
        return False

    def __eq__(self, other):
        try:
            return self.condition_type == other.condition_type
        except AttributeError:
            return False

    def __repr__(self):
        return "Condition()"


class HasValue(Condition):
    def __init__(self, predicate, type=Condition.HAS_VALUE):
        super().__init__(type)
        self._predicate = predicate

    @property
    def predicate(self):
        return self._predicate

    def is_true_given_proposition_set(self, proposition_set):
        for proposition in proposition_set:
            try:
                if proposition.get_predicate() == self.predicate:
                    return True
            except AttributeError:
                pass
        return False

    def __eq__(self, other):
        try:
            equality = super().__eq__(other) and self.predicate == other.predicate
            return equality
        except AttributeError:
            return False

    def __repr__(self):
        return "{}({})".format(self.condition_type, self.predicate)


class HasSharedValue(HasValue):
    def __init__(self, predicate):
        super().__init__(predicate, self.HAS_SHARED_VALUE)

    def is_true_given_tis(self, tis):
        return super().is_true_given_proposition_set(tis.shared.com)


class HasPrivateValue(HasValue):
    def __init__(self, predicate):
        super().__init__(predicate, self.HAS_PRIVATE_VALUE)

    def is_true_given_tis(self, tis):
        return super().is_true_given_proposition_set(tis.private.bel)


class HasSharedOrPrivateValue(HasValue):
    def __init__(self, predicate):
        super().__init__(predicate, self.HAS_SHARED_OR_PRIVATE_VALUE)

    def is_true_given_tis(self, tis):
        return super().is_true_given_proposition_set(tis.private.bel) or super().is_true_given_proposition_set(tis.shared.com)


class IsTrue(Condition):
    def __init__(self, proposition, type=Condition.IS_TRUE):
        super().__init__(type)
        self._proposition = proposition

    @property
    def proposition(self):
        return self._proposition

    def is_true_given_proposition_set(self, proposition_set):
        return self.proposition in proposition_set

    def __eq__(self, other):
        try:
            return super().__eq__(other) and self.proposition == other.proposition
        except AttributeError:
            return False

    def __repr__(self):
        return "{}({})".format(self.condition_type, self.proposition)


class IsSharedCommitment(IsTrue):
    def __init__(self, proposition):
        super().__init__(proposition, self.IS_SHARED_COMMITMENT)

    def is_true_given_tis(self, tis):
        return super().is_true_given_proposition_set(tis.shared.com)


class IsPrivateBelief(IsTrue):
    def __init__(self, proposition):
        super().__init__(proposition, self.IS_PRIVATE_BELIEF)

    def is_true_given_tis(self, tis):
        return super().is_true_given_proposition_set(tis.private.bel)


class IsPrivateBeliefOrSharedCommitment(IsTrue):
    def __init__(self, proposition):
        super().__init__(proposition, self.IS_PRIVATE_BELIEF_OR_SHARED_COMMITMENT)

    def is_true_given_tis(self, tis):
        return super().is_true_given_proposition_set(tis.private.bel) or super().is_true_given_proposition_set(tis.shared.com)
