"""
Contains functions to compute the Electricity cost of bids only, and of ad calls.
"""

import sys
import typing

from pydantic import BaseModel

from electricity import computation_logger
from electricity.utils import Distribution

# This function is fine
class ElectricityCost(BaseModel):
    """Represents the Electricity cost of a component of the programmatic chain"""

    use: float = 0
    """Electricity cost associated to the utilisation of the component"""
    manufacturing: float = 0
    """Electricity cost associated to the fabrication, use and life cycle of the component"""

    def __add__(self, other: "ElectricityCost"):
        return ElectricityCost(
            use=self.use + other.use,
            manufacturing=self.manufacturing + other.manufacturing,
        )

    @property
    def total(self):
        """
        Return the total kWh cost of a ElectricityCost object.

        :return: Return the total kWh cost of a ElectricityCost object.
        :rtype: float

        """
        return self.use + self.manufacturing

# Printing function, this is fine
class _ShowMixin(BaseModel):
    """Mixin to pretty print costs."""

    @property
    def overall(self) -> ElectricityCost:
        raise NotImplementedError

    def show(self, file=sys.stdout):
        print(self.shows(), file=file)

    def shows(self) -> str:
        lines = []
        lines.append(f"This is a {type(self).__name__} object.")

        for k, v in dict(self).items():
            if isinstance(v, ElectricityCost):
                use = f"{v.use:.4f}"
                man = f"{v.manufacturing:.4f}"
                lines.append(f"{k:>32s}: \tuse: {use:>8s} \t manufacture: {man:>8s}")
        use = f"{self.overall.use:.4f}"
        man = f"{self.overall.manufacturing:.4f}"
        lines.append(f"{'Overall':>32s}: \tuse: {use:>8s} \t manufacture: {man:>8s}")
        return "\n".join(str(s) for s in lines)

class ElectricityCampaignCost(_ShowMixin, BaseModel):
    """Class summarizing the Electricity cost of the different elements of the programmatic chain, as the total cost of the campaign."""

    kWh_distrib_server: ElectricityCost
    """Electricity cost associated to server usage, for the distribution."""
    kWh_distrib_network: ElectricityCost
    """Electricity cost associated to network usage, for the distribution."""
    kWh_distrib_terminal: ElectricityCost
    """Electricity cost associated to terminal usage, for the distribution."""
    kWh_allocation_network: ElectricityCost
    """Electricity cost associated to network usage, for the allocation."""
    kWh_allocation_server: ElectricityCost
    """Electricity cost associated to server usage, for the allocation."""

    @property
    def overall(self) -> ElectricityCost:
        """
        ElectricityCost: return a ElectricityCost object combining the Electricity emissions of the 5 attributes.
        """
        return (
            self.kWh_distrib_server
            + self.kWh_distrib_network
            + self.kWh_distrib_terminal
            + self.kWh_allocation_network
            + self.kWh_allocation_server
        )
    @property
    def overall_use(self) -> ElectricityCost:
        """
        ElectricityCost: return a ElectricityCost object combining the Electricity emissions of the use of 5 attributes.
        """
        return (
            self.kWh_distrib_server.use
            + self.kWh_distrib_network.use
            + self.kWh_distrib_terminal.use
            + self.kWh_allocation_network.use
            + self.kWh_allocation_server.use
        )

# This is fine
class BidCost(_ShowMixin, BaseModel):
    """Represents the Electricity costs of bids."""

    kWh_allocation_network: ElectricityCost
    """Electricity cost associated to network usage"""
    kWh_allocation_server: ElectricityCost
    """Electricity cost associated to server usage"""

    @property
    def overall(self) -> ElectricityCost:
        return self.kWh_allocation_network + self.kWh_allocation_server

class AdcallCost(_ShowMixin, BaseModel):
    """Represents the Electricity costs of ad calls."""

    kWh_allocation_network: ElectricityCost
    """Electricity cost associated to network usage"""
    kWh_allocation_server: ElectricityCost
    """Electricity cost associated to server usage"""

    @property
    def overall(self) -> ElectricityCost:
        return self.kWh_allocation_network + self.kWh_allocation_server

def bids_cost(framework, nb_bids: int) -> BidCost:
    """
    Return the kWh cost of a number of bids.
    A single bid can be approximated as direct buying process. However, due to internal process and calls when bidding, we estimate the number of paths activated to be 4.

    Args:
        framework (Framework): Framework object
        nb_bids (int): number of bids.

    Return:
        BidCost: a BidCost object containing the Electricity cost of a number of bids.

    """
    computation_logger.info(f"Starting bids_cost for {nb_bids} bids.")

    allocation_factor = 4 
    bid_cost = BidCost(
        kWh_allocation_network=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_allocation_network, allocation_factor * nb_bids
            ).dict()
        ),
        kWh_allocation_server=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_allocation_server, allocation_factor * nb_bids
            ).dict()
        ),
    )

    computation_logger.info(bid_cost)
    return bid_cost


def adcalls_cost(
    framework, nb_ad_calls: int, creative_type: typing.Literal["video", "display"]
) -> AdcallCost:
    """
    Return the kWh cost of a number of ad calls.
    We approximate the number of SSPs connected to be 10 on average for each prebid auction.
    The Framework defines a number of paths activated at each bid: 1 for direct auction, 100 for video ad, 350 for display ad.
    Thus, each adcall activates 10 paths for a video ad, 35 for a display ad.

    Args:
        framework (Framework): Framework object
        nb_ad_calls (int): number of ad calls
        creative_type (typing.Literal[&quot;video&quot;, &quot;display&quot;]): Type of the creative

    Returns:
        AdcallCost: a AdcallCost object containing the Electricity cost of a number of ad calls.

    """
    computation_logger.info(
        f"Starting adcall_cost for {nb_ad_calls} ad calls. Creative type is {creative_type}"
    )

    allocation_factor = (
        framework.allocation_network_servers.nb_paths_video
        if creative_type == "video"
        else framework.allocation_network_servers.nb_paths_display
    ) / 10

    computation_logger.debug(f"Allocation factor is set to {allocation_factor}.")

    adcall_cost = AdcallCost(
        kWh_allocation_network=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_allocation_network, allocation_factor * nb_ad_calls
            ).dict()
        ),
        kWh_allocation_server=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_allocation_server, allocation_factor * nb_ad_calls
            ).dict()
        ),
    )
    computation_logger.info(adcall_cost)
    return adcall_cost


def impressions_cost(
    framework,
    nb_impressions: int,
    creative_type: typing.Literal["video", "display"],
    allocation: typing.Literal["direct", "programmatic"],
    creative_size_ko: float,
    devices_repartition: Distribution,
    creative_avg_view_s: float = 3,
) -> ElectricityCampaignCost:
    """Return the kWh cost of an advertising campaign.

    Args:
        nb_impressions (int): Total number of impressions
        creative_type (typing.Literal[&quot;video&quot;, &quot;display&quot;]): Type of the creative
        allocation (typing.Literal[&quot;direct&quot;, &quot;programmatic&quot;]): Campaign allocation type
        creative_size_ko (float): Size of the creative, in ko (kB)
        devices_repartition (Distribution): Device delivery repartition
        creative_avg_view_s (float, optional): average duration view of the creative, in seconds. Mandatory for a display creative. Defaults to 3.

    Returns:
        ElectricityCampaignCost: electricity cost of the campaign
    """

    computation_logger.info(
        f"Starting impression_costs for {nb_impressions} impressions."
    )
    computation_logger.debug("Asserting creative_type either video or display")
    assert (creative_type == "display") or (
        creative_type == "video"
    ), "creative_type is either 'display' or 'video' "
    computation_logger.debug("creative_type field: correct")

    computation_logger.debug("Asserting allocation either direct or programmatic")
    assert (allocation == "programmatic") or (
        allocation == "direct"
    ), "allocation is either 'programmatic' or 'direct' "
    computation_logger.debug("allocation field: correct")

    if creative_type == "display":
        assert (
            creative_avg_view_s > 0.0
        ), "creative_avg_view_s is mandatory for creative_type='display' "

    computation_logger.debug("Setting allocation_factor")
    if allocation == "direct":
        allocation_factor = 1
    else:
        allocation_factor = (
            framework.allocation_factor
            * framework.allocation_network_servers.nb_paths_video # nb_pontential_paths * percent_active_paths
            if creative_type == "video"
            else framework.allocation_factor
            * framework.allocation_network_servers.nb_paths_display # nb_pontential_paths * percent_active_paths
        )
    computation_logger.debug(f"allocation_factor setted to {allocation_factor}")

    electricity_campaign_cost = ElectricityCampaignCost(
        kWh_distrib_server=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_distrib_server, creative_size_ko * nb_impressions
            ).dict()
        ),
        kWh_distrib_network=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_distrib_network, creative_size_ko * nb_impressions
            ).dict()
        ),
        kWh_distrib_terminal=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_distrib_terminal(devices_repartition),
                creative_avg_view_s * nb_impressions,
            ).dict()
        ),
        kWh_allocation_network=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_allocation_network, allocation_factor * nb_impressions
            ).dict()
        ),
        kWh_allocation_server=ElectricityCost(
            **framework.multiply_attributes(
                framework.kWh_allocation_server, allocation_factor * nb_impressions
            ).dict()
        ),
    )
    computation_logger.info(electricity_campaign_cost)
    return electricity_campaign_cost