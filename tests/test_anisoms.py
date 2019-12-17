#!/usr/bin/python3

import anisoms
import os
import unittest


class TestAnisoms(unittest.TestCase):

    def test_directions_from_asc_directions(self):

        def get_directions(filename, system):
            def round_in_tuples(x):
                return tuple(map(lambda t: tuple(map(round, t)), x))
            dir_sets = anisoms.directions_from_asc_directions(
                        test_file(filename), system)
            return tuple((name, round_in_tuples(ds.to_decinc_tuples()))
                         for name, ds in dir_sets.items())

        expected_mwd12_specimen = \
            (("MWD1241.1", ((339, 45), ( 90, 19), (196, 38))),
             ("MWD1241.2", ((331, 44), ( 88, 26), (198, 35))),
             ("MWD1241.3", ((315, 48), ( 93, 34), (199, 22))),
             ("MWD1242.1", ((59,   0), (329, 16), (149, 74))),
             ("MWD1242.2", ((334, 42), (100, 33), (213, 30))),
             ("MWD1242.3", ((298, 17), ( 48, 49), (195, 37))),
             ("MWD1243.1", ((318, 18), ( 82, 60), (220, 23))),
             ("MWD1243.2", ((14,  30), (107,  5), (205, 60))),
             ("MWD1244.1", ((125, 24), (239, 43), ( 15, 37))),
             ("MWD1244.2", ((123, 14), (216,  9), (338, 73))),
             ("MWD1244.3", ((107, 26), ( 13,  8), (266, 63))))
        self.assertTupleEqual(expected_mwd12_specimen,
                              get_directions("MWD12.ASC", "Specimen"))

        expected_mwd12_geograph = \
            (('MWD1241.1', ((222,  5), (131, 12), (333, 77))),
             ('MWD1241.2', ((215,  3), (125, 14), (318, 75))),
             ('MWD1241.3', (( 27,  5), (119, 22), (286, 67))),
             ('MWD1242.1', ((307, 24), (203, 29), ( 71, 51))),
             ('MWD1242.2', ((219,  7), (125, 27), (322, 62))),
             ('MWD1242.3', ((179, 10), ( 87,  6), (326, 78))),
             ('MWD1243.1', ((190, 13), ( 89, 38), (295, 49))),
             ('MWD1243.2', ((243,  9), (151, 15), (  5, 73))),
             ('MWD1244.1', ((160, 40), (337, 50), ( 69,  1))),
             ('MWD1244.2', ((166, 31), (284, 38), ( 49, 37))),
             ('MWD1244.3', ((144, 30), (251, 28), ( 15, 47))))
        self.assertTupleEqual(expected_mwd12_geograph,
                              get_directions("MWD12.ASC", "Geograph"))

        expected_d_200_specimen = \
            (('FQD01012', ((189, 23), (43, 62), (285, 14))),
             ('FQD01024', ((189, 37), (61, 40), (303, 29))),
             ('FQD01032', ((182, 28), (76, 28), (309, 48))),
             ('FQD01042', ((190, 32), (60, 46), (298, 27))),
             ('FQD02092', ((188, 27), (290, 22), (54, 54))),
             ('FQD02102', ((188, 24), (54, 58), (287, 21))),
             ('FQD02111', ((180, 28), (296, 41), (67, 37))),
             ('FQD02122', ((183, 26), (70, 39), (297, 40))),
             ('FQD03052', ((186, 39), (81, 17), (333, 46))),
             ('FQD03071', ((183, 43), (311, 34), (63, 29))),
             ('FQD03082', ((198, 32), (90, 26), (330, 46))))
        self.assertTupleEqual(expected_d_200_specimen,
                              get_directions("D_200.ASC", "Specimen"))

        expected_d_200_geograph = \
            (('FQD01012', ((345, 82), (96, 3), (187, 8))),
             ('FQD01024', ((329, 83), (108, 6), (199, 5))),
             ('FQD01032', ((300, 87), (136, 3), (46, 1))),
             ('FQD01042', ((347, 82), (106, 4), (197, 7))),
             ('FQD02092', ((327, 81), (217, 3), (127, 9))),
             ('FQD02102', ((321, 80), (121, 9), (211, 3))),
             ('FQD02111', ((274, 83), (54, 5), (144, 4))),
             ('FQD02122', ((295, 81), (148, 8), (57, 5))),
             ('FQD03052', ((1, 86), (155, 4), (246, 2))),
             ('FQD03071', ((310, 86), (56, 1), (146, 4))),
             ('FQD03082', ((341, 74), (155, 16), (245, 2))))
        self.assertTupleEqual(expected_d_200_geograph,
                              get_directions("D_200.ASC", "Geograph"))


def test_file(leafname):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "..",
                        "test_data", leafname)
