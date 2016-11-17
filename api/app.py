#!/usr/bin/env python3

import connexion

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'Deze API biedt een geïntegreerd zicht op de praktijkbeschrijvende databanken van het Kunstenpunt, die de podiumkunsten, beeldende kunsten en muziek in Vlaanderen en Brussel omvatten.'})
    app.run(port=8080)
