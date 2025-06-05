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
    DEVICES_REPARTITION_VIDEO = {
        "desktop": 1,
        "smart_phone": 0.0,
        "tablet": 0.0,
        "connected_tv": 0.0,
    }

    # AD DISPLAY
    DEVICES_REPARTITION_DISPLAY= {
        "desktop": 0.0,
        "smart_phone": 1.0,
        "tablet": 0.0,
        "connected_tv": 0.0,
    }

    DEVICES_VIDEO = Distribution(weights=DEVICES_REPARTITION_VIDEO)
    DEVICES_DISPLAY = Distribution(weights=DEVICES_REPARTITION_DISPLAY)

### Creative Size Depending on the Creative Type
    
    # base these numbers on Google Ads
#https://support.google.com/google-ads/answer/13547298?hl=en
    video_size_ko = 5000 #256 GB is the upper bound


# https://support.google.com/google-ads/answer/1722096?hl=en
#https://www.iabstandards.be/#/
# https://support.google.com/google-ads/answer/1722096?hl=en#zippy=%2Camphtml-ads-created-in-google-web-designer
# limit suggeted by IAB
    display_size_ko = 150


    impression_count = 1
    video_avg_view_s = 6
    display_avg_view_s = 3
    
    campaign = Framework.load()

    print("Calculations for Direct Allocation:")
    print("____________________________________")
    print("Video Ads")

    results = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="video",
        allocation="direct",
        creative_size_ko= video_size_ko,
        devices_repartition=DEVICES_REPARTITION_VIDEO,
        creative_avg_view_s=video_avg_view_s,
    )

    print(results.shows())

    results = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="display",
        allocation="direct",
        creative_size_ko= display_size_ko,
        devices_repartition=DEVICES_REPARTITION_DISPLAY,
        creative_avg_view_s=display_avg_view_s,
    )

    print(results.shows())

    print("Calculations for Programmatic Allocation:")
    print("____________________________________")
    print("Video Ads")

    results = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="video",
        allocation="programmatic",
        creative_size_ko= video_size_ko,
        devices_repartition=DEVICES_REPARTITION_VIDEO,
        creative_avg_view_s=video_avg_view_s,
    )

    print(results.shows())

    results = compute_electricity.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="display",
        allocation="programmatic",
        creative_size_ko= display_size_ko,
        devices_repartition=DEVICES_REPARTITION_DISPLAY,
        creative_avg_view_s=display_avg_view_s,
    )

    print(results.shows())
