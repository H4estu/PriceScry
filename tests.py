"""tests.py

Testing Module

At a minimum, the following should be tested:


Searches failing to return any cards
Both sides of dual-face cards are rendered
"""

from pricescry import CardGetter


class TestSearches:
    getter = CardGetter()

    def test_ambiguous_search(self):
        """Searches returning too many results (ambiguous search string)."""
        ambiguous_string = "Portal"
        result = self.getter.search_card(ambiguous_string)
        assert (result["object"], result["type"]) == ("error", "ambiguous")

    def test_card_not_found(self):
        unknown_card = "this_card_does_not_3X$1$T"
        result = self.getter.search_card(unknown_card)
        assert (result["object"], result["status"]) == ("error", 404)
