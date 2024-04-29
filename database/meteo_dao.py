from database.DB_connect import DBConnect
from model.situazione import Situazione

class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_umidita(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                            FROM situazione s 
                            WHERE MONTH(s.Data) = %s """
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        print(result)
        return result

    @staticmethod
    def get_umidita_giorno(mese, giorno, citta):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """SELECT s.Umidita FROM situazione s WHERE MONTH(s.Data) = %s AND DAY(s.Data) = %s AND s.Localita = %s """
            cursor.execute(query, (mese, giorno, citta))
            result = cursor.fetchall()[0][0]
            cursor.close()
            cnx.close()
        return result