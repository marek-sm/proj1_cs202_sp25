from dataclasses import dataclass

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