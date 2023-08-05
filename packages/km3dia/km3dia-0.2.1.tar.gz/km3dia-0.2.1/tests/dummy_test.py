#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import km3dia as kia


class test_reader_CSK(unittest.TestCase):
    def setUp(self):
        self.DB = kia.DBManager()

    def test_df(self):
        assert isinstance(self.DB, kia.DBManager)
