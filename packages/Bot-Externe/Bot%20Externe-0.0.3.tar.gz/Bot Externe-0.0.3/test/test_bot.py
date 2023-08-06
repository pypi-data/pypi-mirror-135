# -*- coding: utf-8 -*-
import unittest
from context import Bot, COMMAND_LIST, HELP_FILE, Request


class TestBot(unittest.TestCase):

    def setUp(self) -> None:
        self.true_command_list = COMMAND_LIST
        self.false_command_list_1 = ["/", "/help", "inutile", "/zarbi"]
        self.message_1 = Request("/help")
        self.message_2 = ["/cine", "namur"]

    def test_init(self):
        pass

    def test_get_help(self):
        # self.assertEqual(len(Bot(Request("/help"), self.true_command_list).get_help(HELP_FILE)), 913)
        pass

    def test_process_request(self):
        self.assertEqual(len(Bot(Request("/itinerary louvain-la-neuve ottignies"), self.true_command_list).process_request(Request("/itinerary louvain-la-neuve ottignies").get_message(self.true_command_list))), 1201)
        self.assertEqual(len(Bot(Request("/cine namur"), self.true_command_list).process_request(Request("/cine namur").get_message(self.true_command_list))), 187)
        self.assertEqual(len(Bot(Request("/news basket"), self.true_command_list).process_request(Request("/news basket").get_message(self.true_command_list))), 89)
        self.assertEqual(len(Bot(Request("/resto gembloux"), self.true_command_list).process_request(Request("/resto gembloux").get_message(self.true_command_list))), 84)


if __name__ == "__main__":
    unittest.main()