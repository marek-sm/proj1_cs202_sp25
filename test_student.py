import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade. 
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        # Negative population
        invalid_pop_globerect: GlobeRect = GlobeRect(5, 10, -5, -10)
        invalid_pop_region: Region = Region(invalid_pop_globerect, "Invalid Population", "other")
        self.invalid_pop_region_condition: RegionCondition = RegionCondition(invalid_pop_region, 2026, -5_000, 1_984.4)

        # Negative GHG rate
        invalid_ghg_globerect: GlobeRect = GlobeRect(5, 10, -5, -10)
        invalid_ghg_region: Region = Region(invalid_ghg_globerect, "Invalid GHG Rate", "other")
        self.invalid_ghg_region_condition: RegionCondition = RegionCondition(invalid_ghg_region, 2026, 7_500, -768.4)

    def test_emissions_per_capita_basic(self) -> None:
        self.assertAlmostEqual(emissions_per_capita(nyc_region_condition), 9.9502, places=4)

    def test_emissions_per_capita_zero_pop(self) -> None:
        self.assertEqual(emissions_per_capita(gulf_of_mexico_region_condition), 0.0)

    def test_emissions_per_capita_wrong_type(self) -> None:
        with self.assertRaises(TypeError):
            emissions_per_capita("Not a RegionCondition")
    
    def test_emissions_per_capita_negative_input(self) -> None:
        with self.assertRaises(ValueError):
            emissions_per_capita(self.invalid_pop_region_condition)
        with self.assertRaises(ValueError):
            emissions_per_capita(self.invalid_ghg_region_condition)

    def test_area_basic(self) -> None:
        self.assertAlmostEqual(area(joburg_globerect), 1778.9920, places=4)

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

    def test_area_reversed_latitude(self) -> None:
        normal: float = area(GlobeRect(10, 20, 0, 10))
        reversed: float = area(GlobeRect(20, 10, 0, 10))
        self.assertAlmostEqual(normal, reversed, places=4)

    def test_emissions_per_square_km_basic(self) -> None:
        self.assertAlmostEqual(emissions_per_square_km(cal_poly_region_condition), 112.9339, places=4)

    def test_emissions_per_square_km_zero_ghg(self) -> None:
        self.assertEqual(emissions_per_square_km(gulf_of_mexico_region_condition), 0.0)

    def test_emissions_per_square_km_wrong_type(self) -> None:
        with self.assertRaises(TypeError):
            emissions_per_square_km("Not a RegionCondition")

    def test_emissions_per_square_km_negative_ghg(self) -> None:
        with self.assertRaises(ValueError):
            emissions_per_square_km(self.invalid_ghg_region_condition)

    def test_densest_basic(self) -> None:
        self.assertEqual(densest(region_conditions), "New York City")

    def test_densest_empty_list(self) -> None:
        with self.assertRaises(ValueError):
            densest([])

    def test_densest_wrong_type(self) -> None:
        with self.assertRaises(TypeError):
            densest("Not a list of RegionCondition")

    def test_densest_negative_population(self) -> None:
        with self.assertRaises(ValueError):
            densest([self.invalid_pop_region_condition])

    def test_densest_winner_not_first(self) -> None:
        self.assertEqual(densest([cal_poly_region_condition, nyc_region_condition]), "New York City")

if __name__ == '__main__':
    unittest.main()
