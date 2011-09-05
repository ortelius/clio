from django.test import TestCase

class PopulationTest(TestCase):

    # Date Tests
    def test_empty_dates(self):
        """
        Tests that the search form *and* pagination works if no dates are specified 
        """
        pass

    def test_after_date(self):
        """
        Tests that the search form *and* pagination works if only a start date is specified.
        Results should be strictly _after_ the specified start date
        """
        pass
        
    def test_before_date(self):
        """
        Tests that the search form *and* pagination works if only an end date is specified.
        Results should be strictly _before_ the specified end date
        """
        pass

    def test_valid_dates(self):
        """
        Tests that the search form *and* pagination works if a valid date range is given. 
        Results should be strictly _between_ the specified start and end dates.
        """
        pass

    def test_invalid_dates(self):
        """
        Tests that the search form returns an appropriate error of an invalid date range is given 
        """
        pass

    # Location Tests
     
