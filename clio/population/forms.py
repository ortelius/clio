from django import forms
from clio.common.forms import GeneralSearchForm

import models

class MainPopulationQueryForm(GeneralSearchForm):
  location = forms.ModelMultipleChoiceField(queryset = models.Location.objects, required = False, label = 'Location')
  begin_date = forms.DateField(required = False, label = "From Date")
  end_date = forms.DateField(required = False, label = "To Date")
  count_type = forms.MultipleChoiceField(required = False, label = "Count Type", choices = (('all', 'All'), ('individ', 'Individuals'), ('fam', 'Families'), ('males', 'Males'), ('females', 'Females')), initial = 'all', widget = forms.CheckboxSelectMultiple)
