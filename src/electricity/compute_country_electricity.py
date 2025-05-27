import os
from typing import Literal
import yaml

from electricity import computation_logger, compute_electricity, logger
from electricity.compute_electricity import ElectricityCost
from electricity.digital_electricity_framework import Framework
from electricity.utils import Distribution

# generates general ad campaign 
def generate_campaign(iso): # generates a campaign based on country
    logger.setLevel("INFO")
    computation_logger.setLevel("INFO")

    #based on iab partition assumptions
    DEVICES_REPARTITION = {
        "desktop": 18,
        "smart_phone": 61,
        "tablet": 4,
        "connected_tv": 17,
    }

    DEVICES = Distribution(weights=DEVICES_REPARTITION)

    #https://support.google.com/google-ads/answer/13547298?hl=en
    video_size_ko = 4000 #256 GB is the upper bound


    # https://support.google.com/google-ads/answer/1722096?hl=en
    #https://www.iabstandards.be/#/
    # https://support.google.com/google-ads/answer/1722096?hl=en#zippy=%2Camphtml-ads-created-in-google-web-designer
    # limit suggeted by IAB
    display_size_ko = 150 # the max google ad size and IAB suggested

    impression_count = 10000 # scales linearly
    video_avg_view_s = 6 # based on 5 second as skip
    display_avg_view_s = 3 # overestimate by IAB
    
    campaign = Framework.load()
    campaign.change_target_country(iso)

    result = {}

    direct_video_campaign = compute_electricity.impressions_cost(
        campaign,
        nb_impressions= impression_count,
        creative_type="video",
        allocation="direct",
        creative_size_ko= video_size_ko,
        devices_repartition=DEVICES,
        creative_avg_view_s=video_avg_view_s,
    )

    result["direct_video"] = direct_video_campaign

    direct_display_campaign = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=impression_count,
        creative_type="display",
        allocation="direct",
        creative_size_ko= display_size_ko,
        devices_repartition=DEVICES,
        creative_avg_view_s=display_avg_view_s,
    )
    result["direct_display"] = direct_display_campaign

    programmatic_video_campaign= compute_electricity.impressions_cost(
        campaign,
        nb_impressions=impression_count,
        creative_type="video",
        allocation="programmatic",
        creative_size_ko= video_size_ko,
        devices_repartition=DEVICES,
        creative_avg_view_s=video_avg_view_s,
    )
    result["programmatic_video"] = programmatic_video_campaign

    programmatic_display_campaign = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=impression_count,
        creative_type="display",
        allocation="programmatic",
        creative_size_ko= display_size_ko,
        devices_repartition=DEVICES,
        creative_avg_view_s=display_avg_view_s,
    )
    result["programmatic_display"] = programmatic_display_campaign

    return result # maps the string to the result for readability

# read in the eu population yml
def eu_population() -> dict:
    eu_population_dict = {}
    if eu_population_dict is None:
        with open(
            os.path.join(os.path.dirname(__file__), "pop_eu.yml"), "r"
        ) as yaml_file:
           eu_population_dict = yaml.safe_load(yaml_file)
    else:
        eu_population_dict = eu_population_dict
    return eu_population_dict


# read in the rtb data yml
def eu_rtb() -> dict:
    eu_rtb_dict = {}
    if eu_rtb_dict is None:
        with open(
            os.path.join(os.path.dirname(__file__), "rtb_eu.yml"), "r"
        ) as yaml_file:
           eu_rtb_dict = yaml.safe_load(yaml_file)
    else:
        eu_rtb_dict = eu_rtb_dict
    return eu_rtb_dict


# computations for France

# calc electricity consumption
def calc_france(eu_rtb_dict, eu_pop_dict):

    ad_campaign = generate_campaign("FR")

    # give weight to both the video and display share in consideration for 1 RTB
    video_share = 0.3 #this is just a guess
    display_share = 0.7  # this is just a guess

    per_pop_online = 0.9
    fr_pop = eu_pop_dict["FR"]
    daily_rtb = eu_rtb_dict["FR"]

    # normalize to find the value per one impression
    video_electricity_direct = (ad_campaign["direct_video"].overall()) / 10000 #only want to consider usage
    video_electricity_programmatic = (ad_campaign["programmatic_video"].overall()) / 10000
    display_electricity_direct = (ad_campaign["direct_display"].overall()) / 10000
    display_electricity_programmatic = (ad_campaign["programmatic_display"].overall()) / 10000

    # give weight to consider each value
    programmatic_impression_elec = video_share*video_electricity_programmatic + display_share * display_electricity_programmatic
    direct_impression_elec = video_share*video_electricity_direct + display_share * display_electricity_direct

    # calculation for anual consumption for France, need to print and test if it actually works 
    annual_programmatic_elctricity = daily_rtb*per_pop_online*fr_pop*365*programmatic_impression_elec
    annual_direct_electricity = daily_rtb*per_pop_online*fr_pop*365*direct_impression_elec


# computations for the EU
#def calc_eu():

# campaign.change_target_country("DE")
# Algo: 
# Iterate through all of the country codes in the pop eu and rtb
# generate an model ad campaign in that country
# extract the electricity output for that single impression
# calc: 
#       RTB_broadcasts_per_day × 365 × Online_population_fraction × Populatation × Electricity_per_impression
#       Electricity_per_impression = ((Electricity_Consum_Vid_Prog_Per_imp) (1 - %of Display Impressions) + 
#       (Electricity_Consum_Disp_Prog_Per_Imp)(%of Disp Impressions))
#       do a running sum of all of this to calc just for the EU

# things to recalc: energy conversions that are extracted by dividing by the carbon emission factor
#                   local share vs the global share of servers
#                   fixed vs mobile network usage

# do the same for a direct ad campaign


def main():
 pop_dict = eu_population()
 rtb_dict = eu_rtb()
 calc_france(pop_dict, rtb_dict)

main()
