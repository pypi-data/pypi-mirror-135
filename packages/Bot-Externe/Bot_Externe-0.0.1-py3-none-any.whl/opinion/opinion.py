# -*- coding: utf-8 -*-
import sys
from pymongo import MongoClient
from src.data.config import CERTIFICATE_FILE


class ParameterException(Exception):
    pass


class MongoConnector:
    def __init__(self):
        uri = "mongodb+srv://cluster0.5i6qo.gcp.mongodb.net/ephecom-2TM2?authSource=%24external&authMechanism=MONGODB" \
              "-X509&retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE"

        client = MongoClient(uri,
                             tls=True,
                             tlsCertificateKeyFile=CERTIFICATE_FILE)
        self.db = client["ephecom-2TM2"]

    def __enter__(self):
        return self

    def __exit__(self):
        self.db.close()


class Opinion(MongoConnector):
    def __init__(self, is_positif, message=""):
        super().__init__()
        self.score = is_positif
        self.message = message
        self.id = 0
        self.error = "Choisissez plutôt un nombre entre 0 et 5 svp."

        try:
            with MongoConnector() as connector:
                self.collection = connector.db["users"]
                res = self.collection.findOne()
                print(res)
        except Exception as e:
            print(e)

    def set_opinion(self):
        """
        Permet à l'utilisateur de laisser une cote et un commentaire'

        PRE : "/opinion"
        POST : Une chaîne de caractères d'accusé de réception
        RAISES : Exception : si pas de réponse à la requête

        """
        if 0 <= int(self.score) <= 5:
            for elem in self.collection.find():
                self.id = elem["_id"] + 1

            self.collection.insert_one({"_id": self.id})
            self.collection.update_one({"_id": self.id}, {"$set": {"opinion": self.score}})
            self.collection.update_one({"_id": self.id}, {"$set": {"message": self.message}})
            return "Votre avis a bien été envoyé. Nous en tiendrons compte !"
        else:
            return self.error
