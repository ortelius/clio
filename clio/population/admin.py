from clio.population.models import MainDataEntry, PopulationCondition, Occupation
from clio.sources.models import Table
from clio.common.admin import BaseSubmitAdmin, BaseMergeableCategoryAdmin, BaseMainDataEntryAdmin
from django.contrib import admin

class MainDataEntryAdmin(BaseMainDataEntryAdmin) :
  fieldsets = [
      (None,
        {'fields' : ['active', 'submitted_by', 'datetime_created', ]}),

      ('Location Information', 
        {'fields' : ['location', 'original_location_name', 'alternate_location_name']}),
      
      ('Date Range', 
        {'fields' : ['begin_date', 'end_date', 'circa']}),

      ('Population Characteristics', 
        {'fields' : ['religion', 'race', 'ethnicity', 'ethnic_origin', 'age_start', 'age_end', 'population_condition', 'occupation']}),

      ('Population Statistics', 
        {'fields' : ['individ_fam', 'population_gender', 'population_value', 'value_unit', 'is_total', 'value_precision']}),

      ('Source Information', 
        {'fields' : ['source', 'page_num', 'primary_source_obj', 'primary_source_text']}),

      ('Other Information', 
        {'fields' : ['remarks', ]}),
  ]

  radio_fields = { 'value_precision' : admin.HORIZONTAL, 'individ_fam' : admin.HORIZONTAL, 'population_gender' : admin.HORIZONTAL, 'value_unit' : admin.HORIZONTAL, }

  autocomplete_fields = BaseMainDataEntryAdmin.autocomplete_fields 
  autocomplete_fields.update({ 'religion' : ('name', ), })

  activate_perm = 'population.activate_main_data_entry'

class PopulationConditionAdmin(BaseMergeableCategoryAdmin) :
  activate_perm = 'population.activate_population_condition'
  merge_perm = 'population.merge_population_condition'

class OccupationAdmin(BaseMergeableCategoryAdmin):
  activate_perm = 'population.activate_occupation'
  merge_perm = 'population.merge_occupation'

admin.site.register(MainDataEntry, MainDataEntryAdmin)
admin.site.register(PopulationCondition, PopulationConditionAdmin)
admin.site.register(Occupation, OccupationAdmin)
