import typing

import pandas as pd

from electricity import logger
from electricity.compute_electricity import Distribution
from electricity.digital_electricity_framework import Framework


def get_impressions_cost_aggregator(
    campaign_param: Framework,
) -> typing.Callable[[typing.Mapping[str, typing.Any]], float]:
    from electricity.compute_electricity import impressions_cost

    def impressions_cost_aggregator(row: typing.Mapping[str, typing.Any]) -> float:
        return impressions_cost(
            campaign_param,
            nb_impressions=row["nb_impressions"],
            creative_type=row["creative_type"],
            allocation=row["allocation"],
            creative_size_ko=row["creative_size_ko"],
            creative_avg_view_s=row["creative_avg_view_s"],
            devices_repartition=Distribution(
                weights={
                    k: row[k]
                    for k in (
                        "desktop",
                        "smart_phone",
                        "tablet",
                        "connected_tv",
                    )
                }
            ),
        ).overall.total

    return impressions_cost_aggregator


def impressions_cost(df: "pd.DataFrame", campaign_param: Framework) -> "pd.Series":
    """Compute the kWh usage for a number of impressions."""
    logger.info("Starting impressions cost")
    return df.aggregate(
        get_impressions_cost_aggregator(campaign_param),
        axis="columns",
    )


def get_bids_cost_aggregator(
    campaign_param: Framework,
) -> typing.Callable[[typing.Mapping[str, typing.Any]], float]:
    from electricity.compute_electricity import bids_cost

    def bids_cost_aggregator(row: typing.Mapping[str, typing.Any]) -> float:
        return bids_cost(
            campaign_param,
            nb_bids=row["nb_bids"],
        ).overall.total

    return bids_cost_aggregator


def bids_cost(df: "pd.DataFrame", campaign_param: Framework) -> "pd.Series":
    """Compute the bids kwH usage per row."""
    logger.info("Starting bids cost")
    return df.aggregate(
        get_bids_cost_aggregator(campaign_param),
        axis="columns",
    )
