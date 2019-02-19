from app.api.v2.db import db
class Office:
    """ The office model """
    def __init__(self):
        self.db=db()

    def create_office(self, name, officeType):
        """ Create a office method """
        office = {
            "name": name,
            "officeType": officeType
        }
        query = """INSERT INTO offices(name, type) VALUES(%(name)s, %(officeType)s)"""
        cursor = self.db.cursor()
        cursor.execute(query, office)
        self.db.commit()
        return office   

    def get_all_offices(self):
        """ Get all parties method """
        cursor = self.db.cursor()
        cursor.execute("""SELECT id, name, type FROM offices""")
        data=cursor.fetchall()
        offices=[]
        for i, items in enumerate(data):
            id, name, officeType=items
            office=dict(
                id=int(id),
                name=name,
                officeType=officeType
            )
            offices.append(office)
        return offices

    def get_specific_office(self, id):
        """ Get all parties method """
        cursor = self.db.cursor()
        cursor.execute("""SELECT id, name, type FROM offices WHERE id={}""".format(id))
        data=cursor.fetchall()
        offices=[]
        for i, items in enumerate(data):
            id, name, officeType=items
            office=dict(
                id=int(id),
                name=name,
                officeType=officeType
            )
            offices.append(office)
        return offices 

    def search(self, name):
        """ This function returns True if an office exists in the database."""
        cursor=self.db.cursor()
        cursor.execute("""SELECT * FROM offices WHERE name='%s'"""%(name))
        data=cursor.fetchall()
        if len(data)>0:
            return True
