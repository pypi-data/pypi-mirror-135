# -*- coding: utf-8 -*-
import Bot.config as config
import requests


class ParameterException(Exception):
    pass


class Itinerary:
    def __init__(self, origin_address="louvain-la-neuve", destination_address=""):
        self.__origin_address = origin_address
        self.__destination_address = destination_address

        if not self.__destination_address:
            raise ParameterException("Erreur de paramètre")

        self.__url_address_origin = config.itinerary_link(origin_address)
        self.__url_address_destination = config.itinerary_link(destination_address)

        self.__response = {}

    @property
    def origin_address(self):
        return self.__origin_address

    @property
    def destination_address(self):
        return self.__destination_address

    @property
    def url_address_origin(self):
        return self.__url_address_origin

    @property
    def url_address_destination(self):
        return self.__url_address_destination

    @property
    def response(self):
        return self.__response

    def process_request(self, lon_o, lat_o, lon_d, lat_d):
        self.__response = requests.get(
            config.open_street_link + '&start=' + lon_o + ',' +
            lat_o + '&end=' + lon_d + ',' + lat_d,
            headers=config.headers).json()

    def get_itinerary(self):
        """
        Renvoie un itinéraire

        PRE : "/itinerary"
        POST : liste d'étapes retraçant l'itinéraire souhaité
        RAISES : Exception : si pas de réponse à la requête

        """

        response_origin = requests.get(self.url_address_origin).json()

        response_destination = requests.get(self.url_address_destination).json()

        self.process_request(response_origin[0]["lon"], response_origin[0]["lat"],
                             response_destination[0]["lon"], response_destination[0]["lat"])

        steps = self.response["features"][0]["properties"]["segments"][0]["steps"]

        way = ""
        for i in range(len(steps)):
            way += f"etape {i}:"
            way += f"{steps[i]['instruction']} --> Distance : {steps[i]['distance']} m\n\n"
        return way
