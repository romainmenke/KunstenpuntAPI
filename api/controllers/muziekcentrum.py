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

    @staticmethod
    def _make_list_payload_item(row):
        toonnaam = row[1] if row[2] is None else row[1] + '(' + row[2] + ')'
        id = '13' + str(row[0])
        payload_item = {
            "id": id,
            "toonnaam": toonnaam,
            "datum": str(row[3])
        }
        return payload_item

    def get_full_list_of_carriers(self, limit, offset):
        sql = """SELECT ID, Title, VersionInfo, ReleaseDate
                 FROM carriers
                 ORDER BY ReleaseDate DESC
                 LIMIT {0} OFFSET {1};""".format(str(limit), str(offset))

        self.mcv_cur.execute(sql)
        payload = [self._make_list_payload_item(row)for row in self.mcv_cur.fetchall()]

        sql = "SELECT count(ID) FROM carriers;"
        self.mcv_cur.execute(sql)
        count = self.mcv_cur.fetchone()[0]

        return count, payload

    def get_list_of_carriers_in_period(self, from_date, until_date, limit, offset):
        sql = """SELECT ID, Title, VersionInfo, ReleaseDate
                 FROM carriers
                 WHERE ReleaseDate > '{2}' AND ReleaseDate < '{3}'
                 ORDER BY ReleaseDate DESC
                 LIMIT {0} OFFSET {1};""".format(str(limit), str(offset), from_date, until_date)

        self.mcv_cur.execute(sql)
        payload = [self._make_list_payload_item(row) for row in self.mcv_cur.fetchall()]

        sql = """SELECT count(ID)
                 FROM carriers
                 WHERE ReleaseDate > '{2}' AND ReleaseDate < '{3}'
                 ORDER BY ReleaseDate DESC
                 LIMIT {0} OFFSET {1};""".format(str(limit), str(offset), from_date, until_date)
        self.mcv_cur.execute(sql)
        count = self.mcv_cur.fetchone()[0]

        return count, payload