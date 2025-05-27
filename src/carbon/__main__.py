from carbon import computation_logger, compute_footprints, logger
from carbon.compute_footprints import Co2Cost
from carbon.digital_carbon_framework import Framework
from carbon.utils import Distribution

# if __name__ == "__main__":
#     logger.setLevel("INFO")
#     computation_logger.setLevel("INFO")

#     DEVICES_REPARTITION = {
#         "desktop": 60.0,
#         "smart_phone": 20.0,
#         "tablet": 0.0,
#         "connected_tv": 20.0,
#     }

#     DEVICES = Distribution(weights=DEVICES_REPARTITION)
#     campaign = Framework.load()

#     results = compute_footprints.impressions_cost(
#         campaign,
#         nb_impressions=10000,
#         creative_type="video",
#         allocation="direct",
#         creative_size_ko=1200,
#         devices_repartition=DEVICES,
#         creative_avg_view_s=5,
#     )

#     print(results.shows())

#     results = compute_footprints.impressions_cost(
#         campaign,
#         nb_impressions=10000,
#         creative_type="display",
#         allocation="programmatic",
#         creative_size_ko=1200,
#         devices_repartition=DEVICES,
#         creative_avg_view_s=5,
#     )
#     print(results.shows())

#     campaign.change_target_country("DE")  # Changed from France to Germany
#     results = compute_footprints.impressions_cost(
#         campaign,
#         nb_impressions=10000,
#         creatifrom carbon import computation_logger, compute_footprints, logger
# from carbon.compute_footprints import Co2Cost
# from carbon.digital_carbon_framework import Framework
# from carbon.utils import Distribution

# if __name__ == "__main__":
#     logger.setLevel("INFO")
#     computation_logger.setLevel("INFO")

#     DEVICES_REPARTITION = {
#         "desktop": 60.0,
#         "smart_phone": 20.0,
#         "tablet": 0.0,
#         "connected_tv": 20.0,
#     }

#     DEVICES = Distribution(weights=DEVICES_REPARTITION)
#     campaign = Framework.load()

#     results = compute_footprints.impressions_cost(
#         campaign,
#         nb_impressions=10000,
#         creative_type="video",
#         allocation="direct",
#         creative_size_ko=1200,
#         devices_repartition=DEVICES,
#         creative_avg_view_s=5,
#     )

#     print(results.shows())

#     results = ve_type="display",
#         allocation="programmatic",
#         creative_size_ko=1200,
#         devices_repartition=DEVICES,
#         creative_avg_view_s=5,
#     )
#     print(results.shows())

#     test = Co2Cost(use=0.1, manufacturing=0.2)

#     a = compute_footprints.bids_cost(campaign, nb_bids=1000)
#     print(a.shows())

#     a = compute_footprints.adcalls_cost(
#         campaign, nb_ad_calls=1000, creative_type="video"
#     )

#     print(a.shows())

if __name__ == "__main__":

    # Initialization of logging info
    logger.setLevel("INFO")
    computation_logger.setLevel("INFO")

    # Device Repartion: Provides the weighing for each target device type:
    # Types include : Smartphones, Desktop, TV, and Tablets. 

    ######## VIDEO AD ##########
    # AD Video Displayed on Desktop
    DEVICES_REPARTITION_VIDEO = {
        "desktop": 0.5,
        "smart_phone": 0.5,
        "tablet": 0.0,
        "connected_tv": 0.0,
    }

    # AD DISPLAY
    DEVICES_REPARTITION_DISPLAY= {
        "desktop": 0.5,
        "smart_phone": 0.5,
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

    results = compute_footprints.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="video",
        allocation="direct",
        creative_size_ko= video_size_ko,
        devices_repartition=DEVICES_VIDEO,
        creative_avg_view_s=video_avg_view_s,
    )

    print(results.shows())

    print("Display Ads")

    results = compute_footprints.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="display",
        allocation="direct",
        creative_size_ko= display_size_ko,
        devices_repartition=DEVICES_DISPLAY,
        creative_avg_view_s=display_avg_view_s,
    )

    print(results.shows())

    print("Calculations for Programmatic Allocation:")
    print("____________________________________")
    print("Video Ads")

    results = compute_footprints.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="video",
        allocation="programmatic",
        creative_size_ko= video_size_ko,
        devices_repartition=DEVICES_VIDEO,
        creative_avg_view_s=video_avg_view_s,
    )

    print(results.shows())

    print("Display Ads")
    results = compute_footprints.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="display",
        allocation="programmatic",
        creative_size_ko= display_size_ko,
        devices_repartition=DEVICES_DISPLAY,
        creative_avg_view_s=display_avg_view_s,
    )

    print(results.shows())
