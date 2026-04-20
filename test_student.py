import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade. 
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        # Basic globerect/region/region_condition
        self.sydney_globerect: GlobeRect = GlobeRect(-34.1, -33.6, 150.5, 151.3)
        sydney_region: Region = Region(self.sydney_globerect, "Sydney", "other")
        self.sydney_region_condition: RegionCondition = RegionCondition(sydney_region, 2020, 5_300_000, 25_000_000.0)

        # Zero population region_condition
        caribbean_sea_globerect: GlobeRect = GlobeRect(9, 22, -89, -60)
        caribbean_sea_region: Region = Region(caribbean_sea_globerect, "Caribbean Sea", "ocean")
        self.caribbean_sea_region_condition: RegionCondition = RegionCondition(caribbean_sea_region, 2026, 0, 0.0)

        # Negative population / ghg_rate
        invalid_pop_globerect: GlobeRect = GlobeRect(5, 10, -5, -10)
        invalid_pop_region: Region = Region(invalid_pop_globerect, "Invalid Population", "other")
        self.invalid_pop_region_condition: RegionCondition = RegionCondition(invalid_pop_region, 2026, -5_000, 1_984.4)

        invalid_ghg_globerect: GlobeRect = GlobeRect(5, 10, -5, -10)
        invalid_ghg_region: Region = Region(invalid_ghg_globerect, "Invalid GHG Rate", "other")
        self.invalid_ghg_region_condition: RegionCondition = RegionCondition(invalid_ghg_region, 2026, 7_500, -768.4)

    def test_emissions_per_capita_basic(self) -> None:
        self.assertAlmostEqual(emissions_per_capita(self.sydney_region_condition), 4.7170, places=4)

    def test_emissions_per_capita_zero_pop(self) -> None:
        self.assertEqual(emissions_per_capita(self.caribbean_sea_region_condition), 0.0)

    def test_emissions_per_capita_wrong_type(self) -> None:
        with self.assertRaises(TypeError):
            emissions_per_capita("Not a RegionCondition")
    
    def test_emissions_per_capita_negative_input(self) -> None:
        with self.assertRaises(ValueError):
            emissions_per_capita(self.invalid_pop_region_condition)
        with self.assertRaises(ValueError):
            emissions_per_capita(self.invalid_ghg_region_condition)

    def test_area_basic(self) -> None:
        self.assertAlmostEqual(area(self.sydney_globerect), 4116.5647, places=4)

    def test_area_wrap_around(self) -> None:
        gr: GlobeRect = GlobeRect(0, 10, 170, -170)
        self.assertGreater(area(gr), 0)
        equivalent: GlobeRect = GlobeRect(0, 10, 0, 20)
        self.assertAlmostEqual(area(gr), area(equivalent), delta=1.0)

    def test_area_zero_width(self) -> None:
        gr: GlobeRect = GlobeRect(0, 10, 50, 50)
        self.assertAlmostEqual(area(gr), 0.0, places=4)

    def test_area_full_globe(self) -> None:
        gr: GlobeRect = GlobeRect(-90, 90, -180, 180)
        self.assertAlmostEqual(area(gr), 511_201_962, delta=100)

    def test_area_high_latitude_smaller_than_equator(self) -> None:
        equator: GlobeRect = GlobeRect(0, 1, 0, 1)
        polar: GlobeRect = GlobeRect(85, 86, 0, 1)
        self.assertLess(area(polar), area(equator))

    def test_area_wrong_type(self) -> None:
        with self.assertRaises(TypeError):
            area("Not a GlobeRect")

    def test_emissions_per_square_km_basic(self) -> None:
        self.assertAlmostEqual(emissions_per_square_km(self.sydney_region_condition), 6073.0249, places=4)

    def test_emissions_per_square_km_zero_ghg(self) -> None:
        self.assertEqual(emissions_per_square_km(self.caribbean_sea_region_condition), 0.0)

    def test_emissions_per_square_km_wrong_type(self) -> None:
        with self.assertRaises(TypeError):
            emissions_per_square_km("Not a RegionCondition")

    def test_emissions_per_square_km_negative_ghg(self) -> None:
        with self.assertRaises(ValueError):
            emissions_per_square_km(self.invalid_ghg_region_condition)

    def test_densest(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
