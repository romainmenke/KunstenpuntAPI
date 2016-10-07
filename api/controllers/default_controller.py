from api.controllers.muziekcentrum import MCV, Identities, Organisations, Carriers
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

def releases_activiteit_id_get(activiteit_id) -> str:
    activiteit_id_str = str(activiteit_id)
    if int(activiteit_id_str[0]) == mcv_carriers.db_id and int(activiteit_id_str[1]) == mcv_carriers.table_id:
        return mcv_carriers.get_release_with_id(int(activiteit_id_str[2:]))
    else:
        return {}

def releases_get(offset, limit, from_date = None, until_date = None, organiteit_id = None) -> str:
#TODO globale ID strategie nog niet geimplementeerd
#     if str(organiteit_id)[0] != mcv.db_id:
#        organiteit_id = GET MCV ORGANITEIT UIT DATA.KUNSTEN.BE veld

    if from_date is None and until_date is None and organiteit_id is None:
        count, payload = mcv_carriers.get_full_list_of_carriers(limit, offset)
    elif from_date is not None and until_date is not None and organiteit_id is None:
        count, payload = mcv_carriers.get_list_of_carriers_in_period(from_date, until_date, limit, offset)
    elif organiteit_id is not None and from_date is None and until_date is None:
        local_id = str(organiteit_id)[2:]
        if int(str(organiteit_id)[1]) == mcv_identities.table_id:
            count, payload = mcv_carriers.get_list_of_carriers_by_identity(local_id, limit, offset)
        elif int(str(organiteit_id)[1]) == mcv_organisations.table_id:
            count, payload = mcv_carriers.get_list_of_carriers_by_organisation(local_id, limit, offset)
    else:
        count = -1
        payload = None
    resp = jsonify(payload)
    resp.headers['x_total_count'] = count

    return resp

def organiteiten_get(offset, limit, organiteitTypeId = None, activiteit_id = None, genreId = None, locatieId = None, organiteitId = None) -> str:
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
