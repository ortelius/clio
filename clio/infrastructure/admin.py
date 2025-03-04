from clio.infrastructure.models import MainDataEntry, MotorVehicleType, PostalItemType, MerchantShipType
from clio.common.models import SpatialAreaUnit, Currency
from clio.sources.models import Table
from clio.common.admin import BaseSubmitAdmin, BaseMergeableCategoryAdmin, BaseMainDataEntryAdmin
from django.contrib import admin

class MainDataEntryAdmin(BaseMainDataEntryAdmin) :
  fieldsets = [
      (None,
        {'fields' : ['active', 'submitted_by', 'datetime_created', ]}),

      ('Location Information', 
        {'fields' : ['location', 'original_location_name', 'alternate_location_name', ]}),
      
      ('Date Range', 
        {'fields' : ['begin_date', 'end_date', 'circa']}),

      ('Currency',
        {'fields' : ['currency', 'currency_exchange_rate']}),

      ('Railroad',
        {'fields' : ['railroad_revenue', 'railroad_expenditure', 'railroad_length', 'railroad_length_unit', 'railroad_num_passengers', 
                     'railroad_num_passengers_value_unit', 'railroad_passenger_km', 'railroad_passenger_km_value_unit', 'railroad_freight', 
                     'railroad_freight_value_unit', 'railroad_freight_unit', 'railroad_freight_ton_km', 'railroad_freight_ton_km_value_unit' ]}),

      ('Road',
        {'fields' : ['road_revenue', 'road_expenditure', 'road_length', 'road_length_unit', 'num_motor_vehicles', 'num_motor_vehicles_value_unit', 
                     'motor_vehicles_type', ]}),

      ('Telephones/Telegraph/Television',
        {'fields' : ['num_telephones', 'telegraph_length', 'telegraph_length_unit', 'telegraph_num_stations', 'telegraph_num_sent', 'telegraph_num_sent_value_unit' ]}),

      ('Postal',
        {'fields' : ['postal_revenue', 'postal_expenditure', 'postal_num_stations', 'postal_num_items', 'postal_num_items_value_unit', 'postal_items_type', 'postal_num_boxes', 'postal_num_staff',  ]}),

      ('Ships',
        {'fields' : ['ships_all_num', 'ships_motor_num', 'ships_sail_num', 'ships_steam_num', 'ships_steammotor_num',
                     'ships_all_ton', 'ships_all_ton_value_unit', 'ships_motor_ton', 'ships_motor_ton_value_unit', 
                     'ships_sail_ton', 'ships_sail_ton_value_unit', 'ships_steam_ton', 'ships_steam_ton_value_unit', 'ships_steammotor_ton',
                     'ships_steammotor_ton_value_unit',
                     'merchant_ships_num', 'merchant_ships_type', 'merchant_ships_cargo', 'merchant_ships_cargo_unit', ]}),

      ('Aviation',
        {'fields' : ['air_cargo', 'air_cargo_unit', 'air_cargo_ton_km','air_cargo_ton_km_value_unit', 'air_passenger_km', 'air_passenger_km_value_unit' ]}),

      ('Source Information', 
        {'fields' : ['source', 'page_num', 'primary_source_obj', 'primary_source_text']}),

      ('Other Information', 
        {'fields' : ['remarks', ]}),
  ]

  radio_fields = { 
                   "railroad_num_passengers_value_unit" : admin.HORIZONTAL,
                   "railroad_passenger_km_value_unit" : admin.HORIZONTAL,
                   "railroad_freight_value_unit" : admin.HORIZONTAL,
                   "railroad_freight_ton_km_value_unit" : admin.HORIZONTAL,
                   "num_motor_vehicles_value_unit" : admin.HORIZONTAL,
                   "telegraph_num_sent_value_unit" : admin.HORIZONTAL,
                   "postal_num_items_value_unit" : admin.HORIZONTAL,
                   "ships_all_ton_value_unit" : admin.HORIZONTAL,
                   "ships_motor_ton_value_unit" : admin.HORIZONTAL,
                   "ships_sail_ton_value_unit" : admin.HORIZONTAL,
                   "ships_steam_ton_value_unit" : admin.HORIZONTAL,
                   "ships_steammotor_ton_value_unit" : admin.HORIZONTAL,
                   "air_cargo_ton_km_value_unit" : admin.HORIZONTAL,
                   "air_passenger_km_value_unit" : admin.HORIZONTAL,
                 }

  activate_perm = 'infrastructure.activate_maindataentry'

class MotorVehicleTypeAdmin(BaseMergeableCategoryAdmin):
  activate_perm = 'infrastructure.activate_mvehicletype'
  merge_perm = 'infrastructure.merge_mvehicletype'

class PostalItemTypeAdmin(BaseMergeableCategoryAdmin):
  activate_perm = 'infrastructure.activate_postalitemtype'
  merge_perm = 'infrastructure.merge_postalitemtype'

class MerchantShipTypeAdmin(BaseMergeableCategoryAdmin):
  activate_perm = 'infrastructure.activate_mshiptype'
  merge_perm = 'infrastructure.merge_mshiptype'

admin.site.register(MainDataEntry, MainDataEntryAdmin)
admin.site.register(MotorVehicleType, MotorVehicleTypeAdmin)
admin.site.register(PostalItemType, PostalItemTypeAdmin)
admin.site.register(MerchantShipType, MerchantShipTypeAdmin)
