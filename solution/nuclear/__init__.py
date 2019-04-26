"""Nuclear solution model.
   Excel filename: Drawdown-Nuclear_RRS.ES_v1.1_13Jan2019_PUBLIC.xlsm
"""

import pathlib

import numpy as np
import pandas as pd

from model import adoptiondata
from model import advanced_controls
from model import ch4calcs
from model import co2calcs
from model import customadoption
from model import emissionsfactors
from model import firstcost
from model import helpertables
from model import operatingcost
from model import s_curve
from model import unitadoption
from model import vma
from model.advanced_controls import SOLUTION_CATEGORY

from model import tam
from solution import rrs

DATADIR = str(pathlib.Path(__file__).parents[2].joinpath('data'))
THISDIR = pathlib.Path(__file__).parents[0]

REGIONS = ['World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)', 'Middle East and Africa',
           'Latin America', 'China', 'India', 'EU', 'USA']

scenarios = {
  'PDS-12p2050-Plausible (Book Ed. 1)': advanced_controls.AdvancedControls(
      # Plausible Scenario; Based on the evaluation of ambitious scenarios from four
      # global energy systems models, this scenario follows a high growth trajectory of
      # the adoption cases.

      # general
      solution_category='REPLACEMENT', 
      report_start_year=2020, report_end_year=2050, 

      # adoption
      soln_ref_adoption_basis='Custom', 
      soln_ref_adoption_custom_name='Custom REF Adoption mirroring decline in nuclear in Plausible SCenario', 
      soln_ref_adoption_regional_data=False, soln_pds_adoption_regional_data=False, 
      soln_pds_adoption_basis='Existing Adoption Prognostications', 
      soln_pds_adoption_prognostication_source='Ambitious Cases', 
      soln_pds_adoption_prognostication_trend='3rd Poly', 
      soln_pds_adoption_prognostication_growth='High', 
      source_until_2014='ALL SOURCES', 
      ref_source_post_2014='Baseline Cases', 
      pds_source_post_2014='Drawdown TAM: Drawdown TAM - Post Integration - Plausible Scenario', 
      pds_base_adoption=[('World', 2417.0), ('OECD90', 2067.538596846472), ('Eastern Europe', 337.7907984353286), ('Asia (Sans Japan)', 422.9280547381077), ('Middle East and Africa', 19.434007595770563), ('Latin America', 34.286204887889326), ('China', 186.72565568543357), ('India', 81.7511387032866), ('EU', 911.5844464681002), ('USA', 822.7334922881862)], 
      pds_adoption_final_percentage=[('World', 0.0), ('OECD90', 0.0), ('Eastern Europe', 0.0), ('Asia (Sans Japan)', 0.0), ('Middle East and Africa', 0.0), ('Latin America', 0.0), ('China', 0.0), ('India', 0.0), ('EU', 0.0), ('USA', 0.0)], 

      # financial
      pds_2014_cost=4680.011875, ref_2014_cost=4680.011875, 
      conv_2014_cost=2010.0317085196398, 
      soln_first_cost_efficiency_rate=0.03, 
      conv_first_cost_efficiency_rate=0.02, 
      soln_first_cost_below_conv=True, 
      npv_discount_rate=0.094, 
      soln_lifetime_capacity=358697.6666666667, soln_avg_annual_use=7173.953333333334, 
      conv_lifetime_capacity=182411.2757676607, conv_avg_annual_use=4946.8401873420025, 

      soln_var_oper_cost_per_funit=0.014706279999999999, soln_fuel_cost_per_funit=0.00341387997268896, 
      soln_fixed_oper_cost_per_iunit=46.870000000000005, 
      conv_var_oper_cost_per_funit=0.003752690403548987, conv_fuel_cost_per_funit=0.0731, 
      conv_fixed_oper_cost_per_iunit=32.951404311078015, 

      # emissions
      ch4_is_co2eq=True, n2o_is_co2eq=True, 
      co2eq_conversion_source='AR5 with feedback', 
      soln_indirect_co2_per_iunit=16830.0, 
      conv_indirect_co2_per_unit=0.0, 
      conv_indirect_co2_is_iunits=False, 
      ch4_co2_per_twh=0.0, n2o_co2_per_twh=0.0, 

      soln_energy_efficiency_factor=0.0, 
      soln_annual_energy_used=0.0, conv_annual_energy_used=0.0, 
      conv_fuel_consumed_per_funit=0.0, soln_fuel_efficiency_factor=0.0, 
      conv_fuel_emissions_factor=0.0, soln_fuel_emissions_factor=0.0, 

      emissions_grid_source='Meta-Analysis', emissions_grid_range='Mean', 
      emissions_use_co2eq=True, 
      conv_emissions_per_funit=0.0, soln_emissions_per_funit=0.0, 

    ),
  'PDS-10p2050-Drawdown Scenario': advanced_controls.AdvancedControls(
      # Drawdown Scenario, It is assumed that because of the higher adoption of other
      # renewable energy systems, such as wind and solar, the need for new nuclear
      # energy facilities will decline. This scenario is built upon the same
      # trajectories as the Plausible Scenario, but presents a medium growth trajectory,
      # dipping below the Reference Scenario in 2041. It also uses the Default REF.

      # general
      solution_category='REPLACEMENT', 
      report_start_year=2020, report_end_year=2050, 

      # adoption
      soln_ref_adoption_basis='Default', 
      soln_ref_adoption_regional_data=False, soln_pds_adoption_regional_data=False, 
      soln_pds_adoption_basis='Existing Adoption Prognostications', 
      soln_pds_adoption_prognostication_source='Ambitious Cases', 
      soln_pds_adoption_prognostication_trend='3rd Poly', 
      soln_pds_adoption_prognostication_growth='Medium', 
      source_until_2014='ALL SOURCES', 
      ref_source_post_2014='Baseline Cases', 
      pds_source_post_2014='Drawdown TAM: Drawdown TAM - Post Integration - Drawdown Scenario', 
      pds_base_adoption=[('World', 2417.0), ('OECD90', 2067.538596846472), ('Eastern Europe', 337.7907984353286), ('Asia (Sans Japan)', 422.9280547381077), ('Middle East and Africa', 19.434007595770563), ('Latin America', 34.286204887889326), ('China', 186.72565568543357), ('India', 81.7511387032866), ('EU', 911.5844464681002), ('USA', 822.7334922881862)], 
      pds_adoption_final_percentage=[('World', 0.0), ('OECD90', 0.0), ('Eastern Europe', 0.0), ('Asia (Sans Japan)', 0.0), ('Middle East and Africa', 0.0), ('Latin America', 0.0), ('China', 0.0), ('India', 0.0), ('EU', 0.0), ('USA', 0.0)], 

      # financial
      pds_2014_cost=4680.011875, ref_2014_cost=4680.011875, 
      conv_2014_cost=2010.0317085196398, 
      soln_first_cost_efficiency_rate=0.03, 
      conv_first_cost_efficiency_rate=0.02, 
      soln_first_cost_below_conv=True, 
      npv_discount_rate=0.094, 
      soln_lifetime_capacity=358697.6666666667, soln_avg_annual_use=7173.953333333334, 
      conv_lifetime_capacity=182411.2757676607, conv_avg_annual_use=4946.8401873420025, 

      soln_var_oper_cost_per_funit=0.014706279999999999, soln_fuel_cost_per_funit=0.00341387997268896, 
      soln_fixed_oper_cost_per_iunit=46.870000000000005, 
      conv_var_oper_cost_per_funit=0.003752690403548987, conv_fuel_cost_per_funit=0.0731, 
      conv_fixed_oper_cost_per_iunit=32.951404311078015, 

      # emissions
      ch4_is_co2eq=True, n2o_is_co2eq=True, 
      co2eq_conversion_source='AR5 with feedback', 
      soln_indirect_co2_per_iunit=16830.0, 
      conv_indirect_co2_per_unit=0.0, 
      conv_indirect_co2_is_iunits=False, 
      ch4_co2_per_twh=0.0, n2o_co2_per_twh=0.0, 

      soln_energy_efficiency_factor=0.0, 
      soln_annual_energy_used=0.0, conv_annual_energy_used=0.0, 
      conv_fuel_consumed_per_funit=0.0, soln_fuel_efficiency_factor=0.0, 
      conv_fuel_emissions_factor=0.0, soln_fuel_emissions_factor=0.0, 

      emissions_grid_source='Meta-Analysis', emissions_grid_range='Mean', 
      emissions_use_co2eq=True, 
      conv_emissions_per_funit=0.0, soln_emissions_per_funit=0.0, 

    ),
  'PDS-0p2050-Optimum (Book Ed.1)': advanced_controls.AdvancedControls(
      # Optimum Scenario, with the target of 100 percent electricity generation from no-
      # regrets, renewable energy sources in 2050, this scenario shows the peak in
      # nuclear energy by 2023 following REFpol Ampere (max generation; after is
      # followed by a decline to zero in 2050.

      # general
      solution_category='REPLACEMENT', 
      report_start_year=2020, report_end_year=2050, 

      # adoption
      soln_ref_adoption_basis='Default', 
      soln_ref_adoption_regional_data=False, soln_pds_adoption_regional_data=False, 
      soln_pds_adoption_basis='Fully Customized PDS', 
      soln_pds_adoption_custom_name='Optimum Nuclear reduces to 0% of TAM by 2050, based on AMPERE RefPol Scenario (2014) till peaking', 
      pds_adoption_use_ref_years=[2015], 
      source_until_2014='ALL SOURCES', 
      ref_source_post_2014='Baseline Cases', 
      pds_source_post_2014='Drawdown TAM: Drawdown TAM - Post Integration - Optimum Scenario', 
      pds_base_adoption=[('World', 2417.0), ('OECD90', 2067.538596846472), ('Eastern Europe', 337.7907984353286), ('Asia (Sans Japan)', 422.9280547381077), ('Middle East and Africa', 19.434007595770563), ('Latin America', 34.286204887889326), ('China', 186.72565568543357), ('India', 81.7511387032866), ('EU', 911.5844464681002), ('USA', 822.7334922881862)], 
      pds_adoption_final_percentage=[('World', 0.0), ('OECD90', 0.0), ('Eastern Europe', 0.0), ('Asia (Sans Japan)', 0.0), ('Middle East and Africa', 0.0), ('Latin America', 0.0), ('China', 0.0), ('India', 0.0), ('EU', 0.0), ('USA', 0.0)], 

      # financial
      pds_2014_cost=4680.011875, ref_2014_cost=4680.011875, 
      conv_2014_cost=2010.0317085196398, 
      soln_first_cost_efficiency_rate=0.03, 
      conv_first_cost_efficiency_rate=0.02, 
      soln_first_cost_below_conv=True, 
      npv_discount_rate=0.094, 
      soln_lifetime_capacity=358697.6666666667, soln_avg_annual_use=7173.953333333334, 
      conv_lifetime_capacity=182411.2757676607, conv_avg_annual_use=4946.8401873420025, 

      soln_var_oper_cost_per_funit=0.014706279999999999, soln_fuel_cost_per_funit=0.00341387997268896, 
      soln_fixed_oper_cost_per_iunit=46.870000000000005, 
      conv_var_oper_cost_per_funit=0.003752690403548987, conv_fuel_cost_per_funit=0.0731, 
      conv_fixed_oper_cost_per_iunit=32.951404311078015, 

      # emissions
      ch4_is_co2eq=True, n2o_is_co2eq=True, 
      co2eq_conversion_source='AR5 with feedback', 
      soln_indirect_co2_per_iunit=16830.0, 
      conv_indirect_co2_per_unit=0.0, 
      conv_indirect_co2_is_iunits=False, 
      ch4_co2_per_twh=0.0, n2o_co2_per_twh=0.0, 

      soln_energy_efficiency_factor=0.0, 
      soln_annual_energy_used=0.0, conv_annual_energy_used=0.0, 
      conv_fuel_consumed_per_funit=0.0, soln_fuel_efficiency_factor=0.0, 
      conv_fuel_emissions_factor=0.0, soln_fuel_emissions_factor=0.0, 

      emissions_grid_source='Meta-Analysis', emissions_grid_range='Mean', 
      emissions_use_co2eq=True, 
      conv_emissions_per_funit=0.0, soln_emissions_per_funit=0.0, 

    ),
}

class Nuclear:
  name = 'Nuclear'
  units = {
    "implementation unit": "TW",
    "functional unit": "TWh",
    "first cost": "US$B",
    "operating cost": "US$B",
  }

  def __init__(self, scenario=None):
    if scenario is None:
      scenario = 'PDS-12p2050-Plausible (Book Ed. 1)'
    self.scenario = scenario
    self.ac = scenarios[scenario]

    # TAM
    tamconfig_list = [
      ['param', 'World', 'PDS World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)',
       'Middle East and Africa', 'Latin America', 'China', 'India', 'EU', 'USA'],
      ['source_until_2014', self.ac.source_until_2014, self.ac.source_until_2014,
       'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES',
       'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES'],
      ['source_after_2014', self.ac.ref_source_post_2014, self.ac.pds_source_post_2014,
       'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES',
       'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES'],
      ['trend', '3rd Poly', '3rd Poly',
       '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly',
       '3rd Poly', '3rd Poly', '3rd Poly'],
      ['growth', 'Medium', 'Medium', 'Medium', 'Medium',
       'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium'],
      ['low_sd_mult', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
      ['high_sd_mult', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
    tamconfig = pd.DataFrame(tamconfig_list[1:], columns=tamconfig_list[0], dtype=np.object).set_index('param')
    tam_ref_data_sources = {
      'Baseline Cases': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
      },
      'Conservative Cases': {
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
      },
      'Ambitious Cases': {
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
      },
      '100% RES2050 Case': {
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
      },
      'Region: OECD90': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
      'Region: Eastern Europe': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
      'Region: Asia (Sans Japan)': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
      'Region: Middle East and Africa': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
      'Region: Latin America': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
      'Region: China': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
      'Region: India': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
      'Region: EU': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
      'Region: USA': {
        'Data sets': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
          'Based on: Greenpeace 2015 Reference': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Reference.csv'),
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('tam_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('tam_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
          'Based on: Greenpeace 2015 Energy Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Energy_Revolution.csv'),
          'Based on: Greenpeace 2015 Advanced Revolution': THISDIR.joinpath('tam_based_on_Greenpeace_2015_Advanced_Revolution.csv'),
        },
      },
    }
    self.tm = tam.TAM(tamconfig=tamconfig, tam_ref_data_sources=tam_ref_data_sources,
      tam_pds_data_sources=rrs.tam_pds_data_sources)
    ref_tam_per_region=self.tm.ref_tam_per_region()
    pds_tam_per_region=self.tm.pds_tam_per_region()

    adconfig_list = [
      ['param', 'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)',
       'Middle East and Africa', 'Latin America', 'China', 'India', 'EU', 'USA'],
      ['trend', self.ac.soln_pds_adoption_prognostication_trend, '3rd Poly',
       '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly',
       '3rd Poly', '3rd Poly', '3rd Poly'],
      ['growth', self.ac.soln_pds_adoption_prognostication_growth, 'Medium',
       'Medium', 'Medium', 'Medium', 'Medium', 'Medium',
       'Medium', 'Medium', 'Medium'],
      ['low_sd_mult', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
      ['high_sd_mult', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
    adconfig = pd.DataFrame(adconfig_list[1:], columns=adconfig_list[0], dtype=np.object).set_index('param')
    ad_data_sources = {
      'Baseline Cases': {
          'Based on: IEA ETP 2016 6DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_6DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
      },
      'Conservative Cases': {
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
      },
      'Ambitious Cases': {
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
      },
      '100% Case': {
          'Based on Greenpeace Advanced Revolution Scenario': THISDIR.joinpath('ad_based_on_Greenpeace_Advanced_Revolution_Scenario.csv'),
      },
      'Region: OECD90': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
      'Region: Eastern Europe': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
      'Region: Asia (Sans Japan)': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
      'Region: Middle East and Africa': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
      'Region: Latin America': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
      'Region: China': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
      'Region: India': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
      'Region: EU': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
      'Region: USA': {
        'Baseline Cases': {
          'Based on: AMPERE 2014 MESSAGE MACRO Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_Reference.csv'),
          'Based on: AMPERE 2014 GEM E3 Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_Reference.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER Reference': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_Reference.csv'),
        },
        'Conservative Cases': {
          'Based on: IEA ETP 2016 4DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_4DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_550.csv'),
          'Based on: AMPERE 2014 GEM E3 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_550.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 550': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_550.csv'),
        },
        'Ambitious Cases': {
          'Based on: IEA ETP 2016 2DS': THISDIR.joinpath('ad_based_on_IEA_ETP_2016_2DS.csv'),
          'Based on: AMPERE 2014 MESSAGE MACRO 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_MESSAGE_MACRO_450.csv'),
          'Based on: AMPERE 2014 GEM E3 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_GEM_E3_450.csv'),
          'Based on: AMPERE 2014 IMAGE TIMER 450': THISDIR.joinpath('ad_based_on_AMPERE_2014_IMAGE_TIMER_450.csv'),
        },
      },
    }
    self.ad = adoptiondata.AdoptionData(ac=self.ac, data_sources=ad_data_sources,
        adconfig=adconfig)

    # Custom PDS Data
    ca_pds_data_sources = [
      {'name': 'Project Drawdown High Growth, Ambitious Cases, adjusted', 'include': True,
          'filename': THISDIR.joinpath('ca_pds_data', 'custom_pds_ad_Project_Drawdown_High_Growth_Ambitious_Cases_adjusted.csv')},
      {'name': 'Project Drawdown High Growth, Conservative Cases, adjusted, smoothed curve', 'include': True,
          'filename': THISDIR.joinpath('ca_pds_data', 'custom_pds_ad_Project_Drawdown_High_Growth_Conservative_Cases_adjusted_smootha648ec7d.csv')},
      {'name': 'Optimum Nuclear reduces to 0% of TAM by 2050, based on AMPERE RefPol Scenario (2014) till peaking', 'include': True,
          'filename': THISDIR.joinpath('ca_pds_data', 'custom_pds_ad_Optimum_Nuclear_reduces_to_0_of_TAM_by_2050_based_on_AMPERE_Refa766969f.csv')},
    ]
    self.pds_ca = customadoption.CustomAdoption(data_sources=ca_pds_data_sources,
        soln_adoption_custom_name=self.ac.soln_pds_adoption_custom_name,
        high_sd_mult=1.0, low_sd_mult=1.0,
        total_adoption_limit=pds_tam_per_region)

    # Custom REF Data
    ca_ref_data_sources = [
      {'name': 'Custom REF Adoption mirroring decline in nuclear in Plausible SCenario', 'include': False,
          'filename': THISDIR.joinpath('ca_ref_data', 'custom_ref_ad_Custom_REF_Adoption_mirroring_decline_in_nuclear_in_Plausible_S8b57661b.csv')},
    ]
    self.ref_ca = customadoption.CustomAdoption(data_sources=ca_ref_data_sources,
        soln_adoption_custom_name=self.ac.soln_ref_adoption_custom_name,
        high_sd_mult=1.0, low_sd_mult=1.0,
        total_adoption_limit=ref_tam_per_region)

    if self.ac.soln_ref_adoption_basis == 'Custom':
      ref_adoption_data_per_region = self.ref_ca.adoption_data_per_region()
    else:
      ref_adoption_data_per_region = None

    if False:
      # One may wonder why this is here. This file was code generated.
      # This 'if False' allows subsequent conditions to all be elif.
      pass
    elif self.ac.soln_pds_adoption_basis == 'Fully Customized PDS':
      pds_adoption_data_per_region = self.pds_ca.adoption_data_per_region()
      pds_adoption_trend_per_region = self.pds_ca.adoption_trend_per_region()
      pds_adoption_is_single_source = None
    elif self.ac.soln_pds_adoption_basis == 'Existing Adoption Prognostications':
      pds_adoption_data_per_region = self.ad.adoption_data_per_region()
      pds_adoption_trend_per_region = self.ad.adoption_trend_per_region()
      pds_adoption_is_single_source = self.ad.adoption_is_single_source()

    ht_ref_adoption_initial = pd.Series(
      [2417.0, 2067.538596846472, 337.7907984353286, 422.9280547381077, 19.434007595770563,
       34.286204887889326, 186.72565568543357, 81.7511387032866, 911.5844464681002, 822.7334922881862],
       index=REGIONS)
    ht_ref_adoption_final = ref_tam_per_region.loc[2050] * (ht_ref_adoption_initial / ref_tam_per_region.loc[2014])
    ht_ref_datapoints = pd.DataFrame(columns=REGIONS)
    ht_ref_datapoints.loc[2014] = ht_ref_adoption_initial
    ht_ref_datapoints.loc[2050] = ht_ref_adoption_final.fillna(0.0)
    ht_pds_adoption_initial = ht_ref_adoption_initial
    ht_regions, ht_percentages = zip(*self.ac.pds_adoption_final_percentage)
    ht_pds_adoption_final_percentage = pd.Series(list(ht_percentages), index=list(ht_regions))
    ht_pds_adoption_final = ht_pds_adoption_final_percentage * pds_tam_per_region.loc[2050]
    ht_pds_datapoints = pd.DataFrame(columns=REGIONS)
    ht_pds_datapoints.loc[2014] = ht_pds_adoption_initial
    ht_pds_datapoints.loc[2050] = ht_pds_adoption_final.fillna(0.0)
    self.ht = helpertables.HelperTables(ac=self.ac,
        ref_datapoints=ht_ref_datapoints, pds_datapoints=ht_pds_datapoints,
        pds_adoption_data_per_region=pds_adoption_data_per_region,
        ref_adoption_limits=ref_tam_per_region, pds_adoption_limits=pds_tam_per_region,
        ref_adoption_data_per_region=ref_adoption_data_per_region,
        pds_adoption_trend_per_region=pds_adoption_trend_per_region,
        pds_adoption_is_single_source=pds_adoption_is_single_source)

    self.ef = emissionsfactors.ElectricityGenOnGrid(ac=self.ac)

    self.ua = unitadoption.UnitAdoption(ac=self.ac,
        ref_tam_per_region=ref_tam_per_region, pds_tam_per_region=pds_tam_per_region,
        soln_ref_funits_adopted=self.ht.soln_ref_funits_adopted(),
        soln_pds_funits_adopted=self.ht.soln_pds_funits_adopted(),
        bug_cfunits_double_count=True)
    soln_pds_tot_iunits_reqd = self.ua.soln_pds_tot_iunits_reqd()
    soln_ref_tot_iunits_reqd = self.ua.soln_ref_tot_iunits_reqd()
    conv_ref_tot_iunits = self.ua.conv_ref_tot_iunits()
    soln_net_annual_funits_adopted=self.ua.soln_net_annual_funits_adopted()

    self.fc = firstcost.FirstCost(ac=self.ac, pds_learning_increase_mult=2,
        ref_learning_increase_mult=2, conv_learning_increase_mult=2,
        soln_pds_tot_iunits_reqd=soln_pds_tot_iunits_reqd,
        soln_ref_tot_iunits_reqd=soln_ref_tot_iunits_reqd,
        conv_ref_tot_iunits=conv_ref_tot_iunits,
        soln_pds_new_iunits_reqd=self.ua.soln_pds_new_iunits_reqd(),
        soln_ref_new_iunits_reqd=self.ua.soln_ref_new_iunits_reqd(),
        conv_ref_new_iunits=self.ua.conv_ref_new_iunits(),
        fc_convert_iunit_factor=rrs.TERAWATT_TO_KILOWATT)

    self.oc = operatingcost.OperatingCost(ac=self.ac,
        soln_net_annual_funits_adopted=soln_net_annual_funits_adopted,
        soln_pds_tot_iunits_reqd=soln_pds_tot_iunits_reqd,
        soln_ref_tot_iunits_reqd=soln_ref_tot_iunits_reqd,
        conv_ref_annual_tot_iunits=self.ua.conv_ref_annual_tot_iunits(),
        soln_pds_annual_world_first_cost=self.fc.soln_pds_annual_world_first_cost(),
        soln_ref_annual_world_first_cost=self.fc.soln_ref_annual_world_first_cost(),
        conv_ref_annual_world_first_cost=self.fc.conv_ref_annual_world_first_cost(),
        single_iunit_purchase_year=2017,
        soln_pds_install_cost_per_iunit=self.fc.soln_pds_install_cost_per_iunit(),
        conv_ref_install_cost_per_iunit=self.fc.conv_ref_install_cost_per_iunit(),
        conversion_factor=rrs.TERAWATT_TO_KILOWATT)

    self.c4 = ch4calcs.CH4Calcs(ac=self.ac,
        soln_net_annual_funits_adopted=soln_net_annual_funits_adopted)

    self.c2 = co2calcs.CO2Calcs(ac=self.ac,
        ch4_ppb_calculator=self.c4.ch4_ppb_calculator(),
        soln_pds_net_grid_electricity_units_saved=self.ua.soln_pds_net_grid_electricity_units_saved(),
        soln_pds_net_grid_electricity_units_used=self.ua.soln_pds_net_grid_electricity_units_used(),
        soln_pds_direct_co2_emissions_saved=self.ua.soln_pds_direct_co2_emissions_saved(),
        soln_pds_direct_ch4_co2_emissions_saved=self.ua.soln_pds_direct_ch4_co2_emissions_saved(),
        soln_pds_direct_n2o_co2_emissions_saved=self.ua.soln_pds_direct_n2o_co2_emissions_saved(),
        soln_pds_new_iunits_reqd=self.ua.soln_pds_new_iunits_reqd(),
        soln_ref_new_iunits_reqd=self.ua.soln_ref_new_iunits_reqd(),
        conv_ref_new_iunits=self.ua.conv_ref_new_iunits(),
        conv_ref_grid_CO2_per_KWh=self.ef.conv_ref_grid_CO2_per_KWh(),
        conv_ref_grid_CO2eq_per_KWh=self.ef.conv_ref_grid_CO2eq_per_KWh(),
        soln_net_annual_funits_adopted=soln_net_annual_funits_adopted,
        fuel_in_liters=False)

    self.r2s = rrs.RRS(total_energy_demand=ref_tam_per_region.loc[2014, 'World'],
        soln_avg_annual_use=self.ac.soln_avg_annual_use,
        conv_avg_annual_use=self.ac.conv_avg_annual_use)
