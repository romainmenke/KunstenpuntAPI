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
                      db=mcv_settings['Muziekcentrum']['db'])
        self.mcv_cur = mcv.cursor()


class Identities(MCV):
    def __init__(self):
        super(Identities, self).__init__(1)


class Organisations(MCV):
    def __init__(self):
        super(Organisations, self).__init__(2)


class Carriers(MCV):
    def __init__(self):
        super(Carriers, self).__init__(3)

    def _make_list_payload_item(self, row):
        toonnaam = row[1] if row[2] is None else row[1] + '(' + row[2] + ')'
        id = str(self.db_id) + str(self.table_id) + str(row[0])
        payload_item = {
            "id": id,
            "toonnaam": toonnaam,
            "datum": str(row[3])
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

    def get_list_of_carriers_by_identity_as_main_artist(self, organiteit_id, limit, offset):
        sql_payload = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate
                         FROM carriers c
                         INNER JOIN carriermainartists cm ON cm.CarrierID=c.ID
                         WHERE cm.IdentityID={0} AND
                               cm.ContextID IN (1,3,4,5,6) AND
                               ((c.Filter & 2)=2) AND c.Hidden=0
                         ORDER BY ReleaseDate DESC
                         LIMIT {1} OFFSET {2}""".format(str(organiteit_id), str(limit), str(offset))
        sql_count = """SELECT DISTINCT count(c.ID)
                       FROM carriers c
                       INNER JOIN carriermainartists cm ON cm.CarrierID=c.ID
                       WHERE cm.IdentityID={0} AND
                             cm.ContextID IN (1,3,4,5,6) AND
                             ((c.Filter & 2)=2) AND c.Hidden=0""".format(str(organiteit_id))
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_list_of_carriers_by_identity_as_member(self, organiteit_id, limit, offset):
        sql_payload = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate
                         FROM carriers c
                         INNER JOIN carriermembers cm ON cm.CarrierID=c.ID
                         WHERE cm.IdentityID={0} AND c.Hidden=0
                         ORDER BY ReleaseDate DESC
                         LIMIT {1} OFFSET {2}""".format(str(organiteit_id), str(limit), str(offset))
        sql_count = """SELECT DISTINCT count(c.ID)
                       FROM carriers c
                       INNER JOIN carriermembers cm ON cm.CarrierID=c.ID
                       WHERE cm.IdentityID={0} AND c.Hidden=0""".format(str(organiteit_id))
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_list_of_carriers_by_identity_as_composer(self, organiteit_id, limit, offset):
        sql_payload = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate
                         FROM carriers c INNER JOIN carriermainartists cm ON cm.CarrierID=c.ID
                         WHERE cm.IdentityID={0} AND
                               cm.ContextID=2 AND
                               ((c.Filter & 2)=2) AND c.Hidden=0
                         ORDER BY ReleaseDate DESC
                         LIMIT {1} OFFSET {2}""".format(str(organiteit_id), str(limit), str(offset))
        sql_count = """SELECT DISTINCT count(c.ID)
                       FROM carriers c INNER JOIN carriermainartists cm ON cm.CarrierID=c.ID
                       WHERE cm.IdentityID={0} AND
                             cm.ContextID=2 AND
                             ((c.Filter & 2)=2) AND c.Hidden=0""".format(str(organiteit_id))
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_list_of_carriers_by_organisation_as_label(self, organiteit_id, limit, offset):
        sql_payload = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate
                         FROM carriers c
                         INNER JOIN dblinking l
                         ON l.LinkType=3 AND
                            l.ObjectID=c.ID AND
                            l.ObjectType=5 AND
                            l.LinkCategory=46
                         WHERE l.LinkID={0} AND
                               ((c.Filter & 2) = 2) AND
                               c.Hidden=0
                         ORDER BY ReleaseDate DESC
                         LIMIT {1} OFFSET {2}""".format(str(organiteit_id), str(limit, str(offset)))
        sql_count = """SELECT DISTINCT count(c.ID)
                       FROM carriers c
                       INNER JOIN dblinking l
                       ON l.LinkType=3 AND
                          l.ObjectID=c.ID AND
                          l.ObjectType=5 AND
                          l.LinkCategory=46
                       WHERE l.LinkID={0} AND
                             ((c.Filter & 2) = 2) AND
                             c.Hidden=0""".format(str(organiteit_id))
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_list_of_carriers_by_organisation_as_publisher(self, organiteit_id, limit, offset):
        sql_payload = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate
                         FROM carriers c
                         INNER JOIN dblinking l
                         ON l.LinkType=3 AND
                            l.ObjectID=c.ID AND
                            l.ObjectType=5 AND
                            l.LinkCategory=24
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
                          l.LinkCategory=24
                       WHERE l.LinkID={0} AND
                             ((c.Filter & 2) = 2) AND
                             c.Hidden=0""".format(str(organiteit_id))
        return self._get_count_and_payload(sql_payload, sql_count)

    def get_list_of_carriers_by_organisation_as_distributor(self, organiteit_id, limit, offset):
        sql_payload = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate
                         FROM carriers c
                         INNER JOIN dblinking l
                         ON l.LinkType=3 AND
                            l.ObjectID=c.ID AND
                            l.ObjectType=5 AND
                            l.LinkCategory=23
                         WHERE l.LinkID={0} AND
                               ((c.Filter & 2) = 2) AND
                               c.Hidden=0
                         ORDER BY ReleaseDate DESC
                         LIMIT {1} OFFSET {2}""".format(str(organiteit_id), str(limit), str(offset))
        sql_count = """SELECT DISTINCT c.ID, c.Title, c.VersionInfo, c.ReleaseDate
                       FROM carriers c
                       INNER JOIN dblinking l
                       ON l.LinkType=3 AND
                          l.ObjectID=c.ID AND
                          l.ObjectType=5 AND
                          l.LinkCategory=23
                       WHERE l.LinkID={0} AND
                             ((c.Filter & 2) = 2) AND
                             c.Hidden=0""".format(str(organiteit_id))
        return self._get_count_and_payload(sql_payload, sql_count)
