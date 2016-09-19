from api.controllers.muziekcentrum import Identities, Organisations, Carriers
from flask import jsonify


def groepstentoonstellingen_get(organiteitId = None) -> str:
    return 'do some magic!'

def kunst_in_opdracht_get(offset, limit, organiteitId = None, fromDate = None, untilDate = None) -> str:
    return 'do some magic!'

def opleidingen_get(offset, limit, organiteitId = None, fromDate = None, untilDate = None) -> str:
    return 'do some magic!'

def residenties_get(offset, limit, organiteitId = None, fromDate = None, untilDate = None) -> str:
    return 'do some magic!'

def solotentoonstellingen_get(offset, limit, organiteitId = None, fromDate = None, untilDate = None) -> str:
    return 'do some magic!'

def functies_get(offset, limit, organiteitId = None) -> str:
    return 'do some magic!'

def genres_get(offset, limit, activiteitId = None, organiteitTypeId = None) -> str:
    return 'do some magic!'

def locaties_get(offset, limit, activiteitId = None, organiteitId = None) -> str:
    return 'do some magic!'

def locaties_locatie_id_get(locatieId) -> str:
    return 'do some magic!'

def buitenlandse_concerten_get(offset, limit, organiteitId = None, fromDate = None, untilDate = None) -> str:
    return 'do some magic!'

def releases_activiteit_id_get(activiteitId) -> str:
    return 'do some magic!'

def releases_get(offset, limit, from_date = None, until_date = None, organiteit_id = None) -> str:
    if from_date is None and until_date is None and organiteit_id is None:
        count, payload = mcv_carriers.get_full_list_of_carriers(limit, offset)
    elif from_date is not None and until_date is not None and organiteit_id is None:
        count, payload = mcv_carriers.get_list_of_carriers_in_period(from_date, until_date, limit, offset)
    else:
        count = -1
        payload = None
    resp = jsonify(payload)
    resp.headers['x_total_count'] = count

    return resp

def organiteiten_get(offset, limit, organiteitTypeId = None, activiteitId = None, genreId = None, locatieId = None, organiteitId = None) -> str:
    return 'do some magic!'

def organiteiten_organiteit_id_get(organiteitId) -> str:
    return 'do some magic!'

def organiteittypes_get(offset, limit, organiteitId = None) -> str:
    return 'do some magic!'

def podium_producties_podium_productie_id_get(podiumProductieId) -> str:
    return 'do some magic!'

def podiumproducties_get(offset, limit, organiteitId = None, podiumProductieId = None, fromDate = None, untilDate = None) -> str:
    return 'do some magic!'

def podiumvoorstellingen_get(offset, limit, podiumproductieId = None, organiteitId = None, fromDate = None, untilDate = None) -> str:
    return 'do some magic!'


mcv_identities = Identities()
mcv_organisations = Organisations()
mcv_carriers = Carriers()
