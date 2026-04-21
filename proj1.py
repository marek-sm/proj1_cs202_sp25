#complete your tasks in this file
import sys
import math
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)

# Task 1
@dataclass(frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float

@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str

@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float

# Task 2
nyc_globerect: GlobeRect = GlobeRect(40.5, 41.0, -74.3, -73.4)
nyc_region: Region = Region(nyc_globerect, "New York City", "other")
nyc_region_condition: RegionCondition = RegionCondition(nyc_region, 2020, 20_100_000, 200_000_000.0)

joburg_globerect: GlobeRect = GlobeRect(-26.4, -26.0, 27.8, 28.2)
joburg_region: Region = Region(joburg_globerect, "Johannesburg", "other")
joburg_region_condition: RegionCondition = RegionCondition(joburg_region, 2015, 6_000_000, 30_000_000.0)

gulf_of_mexico_globerect: GlobeRect = GlobeRect(18.0, 31.0, -98.0, -81.0)
gulf_of_mexico_region: Region = Region(gulf_of_mexico_globerect, "Gulf of Mexico", "ocean")
gulf_of_mexico_region_condition: RegionCondition = RegionCondition(gulf_of_mexico_region, 2026, 0, 0.0)

cal_poly_globerect: GlobeRect = GlobeRect(35.0, 35.5, -121.0, -120.3)
cal_poly_region: Region = Region(cal_poly_globerect, "Cal Poly", "other")
cal_poly_region_condition: RegionCondition = RegionCondition(cal_poly_region, 2020, 55_000, 400_000.0)

region_conditions: list[RegionCondition] = [nyc_region_condition, joburg_region_condition, gulf_of_mexico_region_condition, cal_poly_region_condition]

# Task 3
def emissions_per_capita(rc: RegionCondition) -> float:
    # Returns the tons of CO2-equivalent emitted per person in the region per year, given a RegionCondition

    if not isinstance(rc, RegionCondition):
        raise TypeError("rc must be a RegionCondition")
    if rc.pop < 0 or rc.ghg_rate < 0:
        raise ValueError("population and ghg rate must both be at least 0")
    if rc.pop == 0:
        return 0.0

    return rc.ghg_rate / rc.pop

def area(gr: GlobeRect) -> float:
    # Returns the estimated surface area of the region in square kilometers, given a GlobeRect
    
    if not isinstance(gr, GlobeRect):
        raise TypeError("gr must be a GlobeRect")
    
    long_diff: float = gr.east_long - gr.west_long
    if long_diff < 0:
        long_diff += 360
    long_diff_radians: float = math.radians(long_diff)

    lo_lat_radians: float = math.radians(gr.lo_lat)
    hi_lat_radians: float = math.radians(gr.hi_lat)
    
    R: float = 6378.1

    return R ** 2 * long_diff_radians * abs(math.sin(lo_lat_radians) - math.sin(hi_lat_radians))

def emissions_per_square_km(rc: RegionCondition) -> float:
    # Returns the tons of CO2-equivalent per square kilometer, given a RegionCondition
    
    if not isinstance(rc, RegionCondition):
        raise TypeError("rc must be a RegionCondition")
    if rc.ghg_rate < 0:
        raise ValueError("ghg rate must be at least 0")
    
    size: float = area(rc.region.rect)
    if size == 0:
        return 0.0
    
    return rc.ghg_rate / size

def densest(rc_list: list[RegionCondition]) -> str:
    # Returns the name of the region with the highest population density, given a list of RegionCondition values
    if not isinstance(rc_list, list):
        raise TypeError("Not a list of RegionCondition objects")
    if not rc_list:
        raise ValueError("List cannot be empty")
    
    def _helper_densest(rc_list: List[RegionCondition]) -> RegionCondition:
        # Returns the RegionCondition with the highest population density from a non-empty list of RegionCondition values
        head: RegionCondition = rc_list[0]
        if head.pop < 0:
            raise ValueError("Population must be at least 0")
        if len(rc_list) == 1:
            return head
        tail_winner: RegionCondition = _helper_densest(rc_list[1:])
        head_area: float = area(head.region.rect)
        tail_area: float = area(tail_winner.region.rect)
        head_density: float = head.pop / head_area if head_area > 0 else 0.0
        tail_density: float = tail_winner.pop / tail_area if tail_area > 0 else 0.0
        if head_density >= tail_density:
            return head
        return tail_winner
    
    return _helper_densest(rc_list).region.name

# Task 4
def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    # Returns a RegionCondition projected into the future by the given number of years, assuming a constant population growth rate and a constant GHG emissions growth rate
    TERRAIN_GROWTH_RATES: dict[str, float] = {"ocean": 0.0001, "mountains": 0.0005, "forest": -0.00001, "other": 0.0003}

    def _helper_grow_population(pop: float, rate: float, years: int) -> float:
        # Returns the compounded population after a certain amount of years at a certain annual rate
        if years == 0:
            return pop
        return _helper_grow_population(pop * (1 + rate), rate, years - 1)

    if not isinstance(rc, RegionCondition):
        raise TypeError("rc has to be a RegionCondition object")
    if not isinstance(years, int) or isinstance(years, bool):
        raise TypeError("years has to be an int")
    if years < 0:
        raise ValueError("years has to be non-negative")
    if rc.pop < 0 or rc.ghg_rate < 0:
        raise ValueError("Population and ghg rate must both be at least 0")
    if rc.region.terrain not in TERRAIN_GROWTH_RATES:
        raise ValueError(f"terrain must be one of {set(TERRAIN_GROWTH_RATES)}")
    
    rate: float = TERRAIN_GROWTH_RATES[rc.region.terrain]
    new_pop_float: float = _helper_grow_population(float(rc.pop), rate, years)
    new_pop: int = round(new_pop_float)
    
    if rc.pop == 0:
        new_ghg: float = 0.0
    else:
        new_ghg = rc.ghg_rate * (new_pop_float / rc.pop)
    
    return RegionCondition(rc.region, rc.year + years, new_pop, new_ghg)