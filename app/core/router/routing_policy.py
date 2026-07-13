
from enum import Enum


class RoutingPolicy(str, Enum):
    BEST_SCORE = "best_score"

    ROUND_ROBIN = "round_robin"

    LOWEST_COST = "lowest_cost"

    LOWEST_LATENCY = "lowest_latency"

    RANDOM = "random"

    FAILOVER = "failover"