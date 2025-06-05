import os
import yaml

from electricity import computation_logger, compute_electricity, logger
from electricity.compute_electricity import impressions_cost, adcalls_cost, bids_cost
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
    display_size_ko = 100 # the max google ad size and IAB suggested

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
    eu_population_dict = None
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
    eu_rtb_dict = None
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
    video_share = 0.4 #this is just a guess
    display_share = 0.6  # this is just a guess

    per_pop_online = 0.75
    fr_pop = eu_pop_dict["FR"] # this is fine
    daily_rtb = eu_rtb_dict["FR"] # this is fine

    # normalize to find the value per one impression
    video_electricity_direct = ad_campaign["direct_video"].overall_use / 10000 #only want to consider usage
    video_electricity_direct_ds = ad_campaign["direct_video"].kWh_distrib_server.use / 10000 #only want to consider usage
    video_electricity_direct_dn = ad_campaign["direct_video"].kWh_distrib_network.use / 10000 #only want to consider usage
    video_electricity_direct_dt = ad_campaign["direct_video"].kWh_distrib_terminal.use / 10000 #only want to consider usage
    video_electricity_direct_an = ad_campaign["direct_video"].kWh_allocation_network.use / 10000 #only want to consider usage
    video_electricity_direct_as = ad_campaign["direct_video"].kWh_allocation_server.use / 10000 #only want to consider usage
    
    video_electricity_programmatic = ad_campaign["programmatic_video"].overall_use / 10000
    video_electricity_programmatic_ds = ad_campaign["programmatic_video"].kWh_distrib_server.use / 10000
    video_electricity_programmatic_dn = ad_campaign["programmatic_video"].kWh_distrib_network.use / 10000
    video_electricity_programmatic_dt = ad_campaign["programmatic_video"].kWh_distrib_terminal.use / 10000
    video_electricity_programmatic_an = ad_campaign["programmatic_video"].kWh_allocation_network.use / 10000
    video_electricity_programmatic_as = ad_campaign["programmatic_video"].kWh_allocation_server.use / 10000
    
    display_electricity_direct = ad_campaign["direct_display"].overall_use / 10000
    display_electricity_direct_ds = ad_campaign["direct_display"].kWh_distrib_server.use / 10000
    display_electricity_direct_dn = ad_campaign["direct_display"].kWh_distrib_network.use / 10000
    display_electricity_direct_dt = ad_campaign["direct_display"].kWh_distrib_terminal.use / 10000
    display_electricity_direct_an = ad_campaign["direct_display"].kWh_allocation_network.use / 10000
    display_electricity_direct_as = ad_campaign["direct_display"].kWh_allocation_server.use / 10000
    
    display_electricity_programmatic = ad_campaign["programmatic_display"].overall_use / 10000
    display_electricity_programmatic_ds = ad_campaign["programmatic_display"].kWh_distrib_server.use  / 10000
    display_electricity_programmatic_dn = ad_campaign["programmatic_display"].kWh_distrib_network.use  / 10000
    display_electricity_programmatic_dt = ad_campaign["programmatic_display"].kWh_distrib_terminal.use  / 10000
    display_electricity_programmatic_an = ad_campaign["programmatic_display"].kWh_allocation_network.use  / 10000
    display_electricity_programmatic_as = ad_campaign["programmatic_display"].kWh_allocation_server.use  / 10000

    # give weight to consider each value
    programmatic_impression_elec = video_share*video_electricity_programmatic + display_share * display_electricity_programmatic
    programmatic_kWh_distrib_server = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_programmatic_ds + display_share * display_electricity_programmatic_ds)
    programmatic_kWh_distrib_network = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_programmatic_dn + display_share * display_electricity_programmatic_dn)
    programmatic_kWh_distrib_terminal = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_programmatic_dt + display_share * display_electricity_programmatic_dt)
    programmatic_kWh_allocation_server = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_programmatic_an + display_share * display_electricity_programmatic_an)
    programmatic_kWh_allocation_network = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_programmatic_as + display_share * display_electricity_programmatic_as)

    
    direct_impression_elec = video_share*video_electricity_direct + display_share * display_electricity_direct
    direct_kWh_distrib_server = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_direct_ds + display_share * display_electricity_direct_ds)
    direct_kWh_distrib_network = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_direct_dn + display_share * display_electricity_direct_dn)
    direct_kWh_distrib_terminal = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_direct_dt + display_share * display_electricity_direct_dt)
    direct_kWh_allocation_server = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_direct_as + display_share * display_electricity_direct_as)
    direct_kWh_allocation_network = daily_rtb*per_pop_online*fr_pop*365*(video_share*video_electricity_direct_an + display_share * display_electricity_direct_an)

    # calculation for anual consumption for France, need to print and test if it actually works 
    annual_programmatic_elctricity = daily_rtb*per_pop_online*fr_pop*365*programmatic_impression_elec
    annual_direct_electricity = daily_rtb*per_pop_online*fr_pop*365*direct_impression_elec

    print("Programmatic Advertising Campaign Estimates")
    print("--------------------------------------------")
    print(f"prog kWh_distrib_server: {programmatic_kWh_distrib_server}")
    print(f"prog kWh_distrib_network: {programmatic_kWh_distrib_network}")
    print(f"prog kWh_distrib_terminal: {programmatic_kWh_distrib_terminal}")
    print(f"prog kWh_allocation_network:  {programmatic_kWh_allocation_network}")
    print(f"prog kWh_allocation_server: {programmatic_kWh_allocation_server}")
    print(f"Programmatic Impression {programmatic_impression_elec}")
    print(f"Prog Annual programmatic electricity usage in France: {annual_programmatic_elctricity}")
    print("\n")

    print("Direct Advertising Campaign Estimates")
    print("--------------------------------------------")
    print(f"direct kWh_distrib_server: {direct_kWh_distrib_server}")
    print(f"direct kWh_distrib_network: {direct_kWh_distrib_network}")
    print(f"direct kWh_distrib_terminal: {direct_kWh_distrib_terminal}")
    print(f"direct kWh_allocation_network:  {direct_kWh_allocation_network}")
    print(f"direct kWh_allocation_server: {direct_kWh_allocation_server}")
    print(f"Direct Impression {direct_impression_elec}")
    print(f"Annual direct electricity usage in France: {annual_direct_electricity}")





# computations for the EU
def calc_eu(eu_rtb_dict, eu_pop_dict):

    eu_total_direct = 0.
    eu_total_programmatic = 0.

    video_share = 0.3 #this is just a guess
    display_share = 0.7  # this is just a guess
    per_pop_online = 0.9 # percent of each population we assume is online
    print(eu_pop_dict)
    print(eu_rtb_dict)
    for iso, population in eu_pop_dict.items():
        daily_rtb = eu_rtb_dict[iso]
        ad_campaign = generate_campaign(iso)

        video_electricity_direct = ad_campaign["direct_video"].overall_use/ 10000 #only want to consider usage
        video_electricity_programmatic = ad_campaign["programmatic_video"].overall_use / 10000
        display_electricity_direct = ad_campaign["direct_display"].overall_use / 10000
        display_electricity_programmatic = ad_campaign["programmatic_display"].overall_use / 10000

        programmatic_impression_elec = video_share*video_electricity_programmatic + display_share * display_electricity_programmatic
        direct_impression_elec = video_share*video_electricity_direct + display_share * display_electricity_direct

    # calculation for anual consumption for France, need to print and test if it actually works 
        annual_programmatic_elctricity = daily_rtb*per_pop_online*population*365*programmatic_impression_elec
        annual_direct_electricity = daily_rtb*per_pop_online*population*365*direct_impression_elec

        eu_total_direct += annual_direct_electricity
        eu_total_programmatic += annual_programmatic_elctricity
    print(eu_total_direct)
    print(eu_total_programmatic)



def main():
 pop_dict = eu_population()
 rtb_dict = eu_rtb()
 calc_france(rtb_dict,pop_dict)
 #calc_eu(rtb_dict, pop_dict)

 # 4 key factors affecting the output, the 350,100, the percent of SSP and percent of 


main()
