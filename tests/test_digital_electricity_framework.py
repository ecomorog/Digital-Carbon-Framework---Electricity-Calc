import unittest

from electricity import digital_electricity_framework
from electricity.compute_electricity import ElectricityCost, impressions_cost

DEVICES_REPARTITION = digital_electricity_framework.Distribution(
    weights={
        "desktop": 10,
        "smart_phone": 20,
        "tablet": 5,
        "connected_tv": 20,
    }
)


class DigitalCarbonTest(unittest.TestCase):
    def test_co2_full_direct(self):
        campaign = digital_electricity_framework.Framework.load()
        self.assertAlmostEqual(
            impressions_cost(
                campaign,
                nb_impressions=10000,
                creative_type="video",
                allocation="direct",
                creative_size_ko=1200,
                devices_repartition=DEVICES_REPARTITION,
                creative_avg_view_s=5,
            ).overall.total,
            ElectricityCost(use=0.2562733391548535, manufacturing=0.5793029714657473).total,
        )

    def test_co2_full_programmatic(self):
        campaign = digital_electricity_framework.Framework.load()
        self.assertAlmostEqual(
            impressions_cost(
                campaign,
                nb_impressions=10000,
                creative_type="display",
                allocation="programmatic",
                creative_size_ko=1200,
                devices_repartition=DEVICES_REPARTITION,
                creative_avg_view_s=5,
            ).overall.total,
            ElectricityCost(use=7.323631186960354, manufacturing=3.2045569703363834).total,
        )

    def test_change_target_country(self):
        campaign = digital_electricity_framework.Framework.load()
        campaign.change_target_country(alpha_code="FR")
        self.assertAlmostEqual(
            impressions_cost(
                campaign,
                nb_impressions=10000,
                creative_type="display",
                allocation="programmatic",
                creative_size_ko=1200,
                devices_repartition=DEVICES_REPARTITION,
                creative_avg_view_s=5,
            ).overall.total,
            ElectricityCost(use=7.83829675080798, manufacturing=3.2045569703363834).total,
        )
