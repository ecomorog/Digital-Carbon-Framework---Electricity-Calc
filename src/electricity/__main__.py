from electricity import computation_logger, compute_electricity, logger
from electricity.compute_electricity import ElectricityCost
from electricity.digital_electricity_framework import Framework
from electricity.utils import Distribution

if __name__ == "__main__":

    # Initialization of logging info
    logger.setLevel("INFO")
    computation_logger.setLevel("INFO")

    # Device Repartion: Provides the weighing for each target device type:
    # Types include : Smartphones, Desktop, TV, and Tablets. 

    ######## VIDEO AD ##########
    # AD Video Displayed on Desktop
    #DEVICES_REPARTITION = {
    #   "desktop": 18,
    #    "smart_phone": 61,
    #    "tablet": 4,
    #    "connected_tv": 17,
    #}



    DEVICES = Distribution(weights=DEVICES_REPARTITION)

### Creative Size Depending on the Creative Type
    
# base these numbers on Google Ads
#https://support.google.com/google-ads/answer/13547298?hl=en
    video_size_ko = 4000 #256 GB is the upper bound


# https://support.google.com/google-ads/answer/1722096?hl=en
#https://www.iabstandards.be/#/
# https://support.google.com/google-ads/answer/1722096?hl=en#zippy=%2Camphtml-ads-created-in-google-web-designer
# limit suggeted by IAB
    display_size_ko = 100 # the max google


    impression_count = 10000
    video_avg_view_s = 6
    display_avg_view_s = 3
    
    campaign = Framework.load()
    campaign.change_target_country("FR")

    print("Calculations for Direct Allocation:")
    print("____________________________________")
    print("Video Direct Ads")

    results = compute_electricity.impressions_cost(
        campaign,
        nb_impressions= impression_count,
        creative_type="video",
        allocation="direct",
        creative_size_ko= video_size_ko,
        devices_repartition=DEVICES,
        creative_avg_view_s=video_avg_view_s,
    )

    print(results.shows())

    print("Display Direct Ads")

    results = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=impression_count,
        creative_type="display",
        allocation="direct",
        creative_size_ko= display_size_ko,
        devices_repartition=DEVICES,
        creative_avg_view_s=display_avg_view_s,
    )

    print(results.shows())

    print("Calculations for Programmatic Allocation:")
    print("____________________________________")
    print("Video Prog Ads")

    results_prog = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=impression_count,
        creative_type="video",
        allocation="programmatic",
        creative_size_ko= video_size_ko,
        devices_repartition=DEVICES,
        creative_avg_view_s=video_avg_view_s,
    )

    print(results_prog.shows())

    print("Display Prog Ads")
    results = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=impression_count,
        creative_type="display",
        allocation="programmatic",
        creative_size_ko= display_size_ko,
        devices_repartition=DEVICES,
        creative_avg_view_s=display_avg_view_s,
    )

    print(results.shows())
