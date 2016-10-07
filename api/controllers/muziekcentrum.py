from configparser import ConfigParser
from pymysql import connect


class MCV:
    def __init__(self, table_id):
        self.db_id = 1
        self.table_id = table_id
        mcv_settings = ConfigParser()
        mcv_settings.read('db.cfg')
        mcv = connect(host=mcv_settings['Muziekcentrum']['host'],
                      user=mcv_settings['Muziekcentrum']['user'],
                      passwd=mcv_settings['Muziekcentrum']['pass'],
                      db=mcv_settings['Muziekcentrum']['db'],
                      sql_mode="ALLOW_INVALID_DATES")
        self.mcv_cur = mcv.cursor()


class Identities(MCV):
    def __init__(self):
        super(Identities, self).__init__(1)


class Organisations(MCV):
    def __init__(self):
        super(Organisations, self).__init__(2)


class Carriers(MCV):
    def __init__(self):
        super(Carriers, self).__init__(5)

    def _make_list_payload_item(self, row):
        toonnaam = row[1] if row[2] is None else row[1] + '(' + row[2] + ')'
        id = int(str(self.db_id) + str(self.table_id) + str(row[0]))
        payload_item = {
            "id": id,
            "toonnaam": toonnaam,
            "datum": str(row[3]),
            "rol": str(row[4]) if len(row) > 4 else None
        }
        return payload_item

    def _get_count_and_payload(self, sql_payload, sql_count):
        self.mcv_cur.execute(sql_payload)
        payload = [self._make_list_payload_item(row) for row in self.mcv_cur.fetchall()]
        self.mcv_cur.execute(sql_count)
        count = self.mcv_cur.fetchone()[0]
        return count, payload

    def get_full_list_of_carriers(self, limit, offset):
        sql_payload = """SELECT ID, Title, VersionInfo, ReleaseDate
                         FROM carriers
                         ORDER BY ReleaseDate DESC
                         LIMIT {0} OFFSET {1};""".format(str(limit), str(offset))
        sql_count = "SELECT count(ID) FROM carriers;"
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_list_of_carriers_in_period(self, from_date, until_date, limit, offset):
        sql_payload = """SELECT ID, Title, VersionInfo, ReleaseDate
                         FROM carriers
                         WHERE ReleaseDate > '{2}' AND ReleaseDate < '{3}'
                         ORDER BY ReleaseDate DESC
                         LIMIT {0} OFFSET {1};""".format(str(limit), str(offset), from_date, until_date)
        sql_count = """SELECT count(ID)
                       FROM carriers
                       WHERE ReleaseDate > '{0}' AND ReleaseDate < '{1}';""".format(from_date, until_date)
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_list_of_carriers_by_identity(self, organiteit_id, limit, offset):
        sql_payload = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate, mac.Name
                         FROM carriers c
                         LEFT JOIN carriermembers cm ON cm.CarrierID=c.ID
                         LEFT JOIN carriermainartists cma ON cma.CarrierID=c.ID
                         LEFT JOIN mainartistcontext mac ON cma.ContextID=mac.ID
                         WHERE (cm.IdentityID={0} OR cma.IdentityID={0}) AND c.Hidden=0 AND ((c.Filter & 2) = 2)
                         ORDER BY ReleaseDate DESC
                         LIMIT {1} OFFSET {2}""".format(str(organiteit_id), str(limit), str(offset))
        sql_count = """SELECT DISTINCT count(c.ID)
                       FROM carriers c
                        LEFT JOIN carriermembers cm ON cm.CarrierID=c.ID
                        LEFT JOIN carriermainartists cma ON cma.CarrierID=c.ID
                        WHERE (cm.IdentityID={0} OR cma.IdentityID={0})
                          AND c.Hidden=0 AND ((c.Filter & 2) = 2)""".format(str(organiteit_id))
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_list_of_carriers_by_organisation(self, organiteit_id, limit, offset):
        sql_payload = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate, l.LinkCategory
                         FROM carriers c
                         INNER JOIN dblinking l
                         ON l.LinkType=3 AND
                            l.ObjectID=c.ID AND
                            l.ObjectType=5 AND
                            l.LinkCategory IN (46, 24, 23)
                         WHERE l.LinkID={0} AND
                               ((c.Filter & 2) = 2) AND
                               c.Hidden=0
                         ORDER BY ReleaseDate DESC
                         LIMIT {1} OFFSET {2}""".format(str(organiteit_id), str(limit), str(offset))
        sql_count = """SELECT DISTINCT count(c.ID)
                       FROM carriers c
                       INNER JOIN dblinking l
                       ON l.LinkType=3 AND
                          l.ObjectID=c.ID AND
                          l.ObjectType=5 AND
                          l.LinkCategory IN (46, 24, 23)
                       WHERE l.LinkID={0} AND
                             ((c.Filter & 2) = 2) AND
                             c.Hidden=0""".format(str(organiteit_id))
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_release_with_id(self, release_id):
        payload = {}
        # statische gegevens
        sql = """SELECT c.*, ct.Name AS CountryName, cf.Name AS Format, cc.Name AS Concept
                 FROM carriers c
                 LEFT OUTER JOIN carrierformats cf ON cf.ID = c.Format
                 LEFT OUTER JOIN carrierconcepts cc ON cc.ID = c.Concept
                 LEFT OUTER JOIN countries ct ON ct.ID = c.CountryID
                 WHERE c.ID={0}""".format(str(release_id))
        self.mcv_cur.execute(sql)
        statische_gegevens = self.mcv_cur.fetchone()
        payload['id'] = int(str(self.db_id) + str(self.table_id) + str(statische_gegevens[0]))
        payload['toonnaam'] = statische_gegevens[1]
        payload['versie_info'] = statische_gegevens[4]
        payload['ondertitel'] = statische_gegevens[3]
        payload['drager_formaat'] = statische_gegevens[45]
        payload['drager_concept'] = statische_gegevens[46]
        payload['catalogus_nummer'] = statische_gegevens[5]
        payload['release_datum'] = statische_gegevens[28]
        payload['land'] = statische_gegevens[44]
        payload['beschrijving_nl'] = statische_gegevens[20]
        payload['beschrijving_en'] = statische_gegevens[21]
        payload['officiele_perstekst_nl'] = statische_gegevens[23]
        payload['officiele_perstekst_en'] = statische_gegevens[24]

        # beeldmateriaal
        payload['beeldmateriaal'] = None

        # tracklist
        payload['tracks'] = {'plat': statische_gegevens[25]}
        payload['tracks']['lijst'] = self._get_rich_tracklist_for_release_id(release_id)

        return payload

    def _get_rich_tracklist_for_release_id(self, release_id):
        sql = """SELECT phonograms.ID AS ID,
                        phonograms.Title, phonograms.VersionInfo, carrierphonograms.TrackNumber AS TrackNumber,
                        CONCAT(
                          LPAD(
                            LEFT(
                              carrierphonograms.TrackNumber, INSTR(carrierphonograms.TrackNumber, '-') - 1
                            ),
                            3, '0'
                          ),
                          LPAD(
                            RIGHT(
                              carrierphonograms.TrackNumber, CHAR_LENGTH(carrierphonograms.TrackNumber) -
                              INSTR(carrierphonograms.TrackNumber, '-')
                            ), 3, '0'
                          )
                        ) AS TrackOrder
                 FROM phonograms
                 INNER JOIN carrierphonograms
                 ON phonograms.ID = carrierphonograms.PhonogramID
                 WHERE carrierphonograms.CarrierID={}
                 ORDER BY TrackOrder""".format(str(release_id))
        self.mcv_cur.execute(sql)
        tracklijst_raw = self.mcv_cur.fetchall()
        tracklijst = []
        for row in tracklijst_raw:
            nummer = row[3]
            rangschikking = row[4]
            toonnaam = str(row[1]) if row[2] is None else row[1] + '(' + row[2] + ')'
            mainartists = self._get_main_artist_on_track(row[0])
            tracklijst.append({"rank": rangschikking, "nummer": nummer, "toonnaam": toonnaam, "mainartists": mainartists})
        return tracklijst

    def _get_main_artist_on_track(self, track_id):
        ident = Identities()
        sql = """SELECT i.ID, i.FullName, i.Nationality, i.Filter, mc.Name AS Context
                 FROM identities i
                 INNER JOIN phonogrammainartists pm
                 ON pm.IdentityID=i.ID
                 LEFT JOIN mainartistcontext mc
                 ON pm.ContextID=mc.ID
                 WHERE pm.PhonogramID={0}
                 ORDER BY pm.Ranking, i.FullName""".format(str(track_id))
        self.mcv_cur.execute(sql)
        mainartists = self.mcv_cur.fetchall()
        return [{"id": int(str(self.db_id) + str(ident.table_id) + str(row[0])),
                 "toonnaam": row[1]
                 } for row in mainartists]
