import unittest

from src.shape import Shape

class ShapeTest(unittest.TestCase):
    '''
    Unit test for shape class
    '''

    def setUp(self):
        self.valid_shape_codes = ['Q', 'Z', 'S', 'T', 'I', 'L', 'J']
        self.shape_to_expected_map = {'Q': [(0,0),(0,1),(1,0),(1,1)],
                                      'Z': [(0,0),(0,1),(1,1),(1,2)],
                                      'S': [(0,1),(0,2),(1,0),(1,1)],
                                      'T': [(0,0),(0,1),(0,2),(1,1)],
                                      'I': [(0,0),(0,1),(0,2),(0,3)],
                                      'L': [(0,0),(1,0),(2,0),(2,1)],
                                      'J': [(0,1),(1,1),(2,0),(2,1)],
                                      'V': None
                                      }

    def test_valid_shapes(self):
        """ Testing valid shapes per specification, should get no error"""
        for shape_code in self.valid_shape_codes:
            expected_coords = set(self.shape_to_expected_map.get(shape_code))
            self.assertSetEqual(Shape(shape_code).get_shape_coords(), expected_coords)

    def test_fail_shape_v(self):
        """ Testing invalid shape V, should get an exception"""
        with self.assertRaises(Exception) as context:
            Shape('V')
        self.assertTrue('Shape V is not created in configuration' in str(context.exception))