#!/usr/bin/python3

import databaseconfig as cfg
import mysql.connector

class DiabeteDB:
    """DiabeteDB
    Class that manages the data for the Diabete database.
    Every method in this class that is related to grabbing data from database will return the result
    in the form of {"result": "success/fail", "data": [list of grabbed data]}
    Every method in this class that is related to adding data to database will return the result in the
    form of {"result": "success/fail", "data": "Id of last insert"}
    """

    def __init__(self):
        """DiabeteDB class constructor
        Creates connection for diabete database by using the database configuration.
        This configuration is saved in databaseconfig.py
        """
        self.conn = mysql.connector.connect(user=cfg.mysql["user"], password=cfg.mysql["passwd"], database=cfg.mysql["db"])

    def __del__(self):
        """DiabeteDB class destructor
        Destroy connection for the diabete database.
        """
        self.conn.close()

    def getEntry(self, id):
        """getEntry
        @param entryId
        Getter for entries table.
        It only grabs one entry out of table
        """

        cursor = self.conn.cursor()
        cursor.execute(""" SELECT id, type FROM entries where id = %s
        """, (id,))
        row = cursor.fetchone()

        if row is None:
            return {"result": "failed", "data": []}

        entryId = row[0]
        entryType = row[1]
        cursor.close()
        
        return {"result": "success", 
                "data": [{"id": entryId, "type": entryType}]}

    def addEntry(self, entryType, name):
        """addEntry
        @param entryName
        @param entryType
        Add new entry to entries table.
        If insert was successful, it returns true, else false.
        """

        cursor = self.conn.cursor()
        cursor.execute(""" INSERT INTO entries
        (name, type) VALUES (%s, %s)
        """, (name, entryType))

        entryId = cursor.lastrowid
        self.conn.commit()
        cursor.close()

        if entryId is None:
            return {"result": "failed", "data": []}
        
        return {"result": "success", "data": {"entryId": entryId}}

    def getFoodInfoByName(self, name):
        """getFoodInfoByName
        @param foodName
        Find and return the food information in foodInfo table by using name.
        """

        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, name, carb FROM foodInfo WHERE name = %s
        """, (name.lower(), ))
        rows = cursor.fetchall()

        if len(rows) == 0 :
            return {"result": "failed", "data": []}

        result = []
        for row in rows:
            foodId = row[0]
            name = row[1]
            carb = row[2]
            result.append({"id": foodId, "name":name, "carb":carb})

        cursor.close()

        return {"result": "success", "data": result}
    
    def addFoodInfo(self, name, carb):
        """addFoodInfo
        @param foodName
        @param carb
        Add food information to the foodInfo table. This does not check for duplicate
        """

        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO foodInfo
        (name, carb) VALUES (%s, %s)""", (name, carb))

        foodInfoId = cursor.lastrowid
        self.conn.commit()
        cursor.close()

        if foodInfoId is None:
            return {"result": "failed", "data": []}

        return {"result": "success", "data": {"foodInfoId": foodInfoId}}

    def getFoodConsumed(self, entryId):

        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, entryId, foodId, consumedTime FROM foodConsumed WHERE entryId = %s
        """, (entryId, ))
        rows = cursor.fetchall()

        if len(rows) == 0:
            return {"result": "failed", "data": []}

        result = []
        for row in rows:
            consumedId = row[0]
            entryId = row[1]
            foodId = row[2]
            consumedTime = row[3]
            result.append({"id": consumedId, "entryId": entryId, "foodId": foodId, "consumedTime": consumedTime})

        cursor.close()

        return {"result":"success", "data": result}

    def addFoodConsume(self, entryId, foodId, consumedTime):
        
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO foodConsumed
        (entryId, foodId, consumedTime) VALUES (%s, %s, %s)""", (entryId, foodId, consumedTime))

        consumeId = cursor.lastrowid
        self.conn.commit()
        cursor.close()

        if consumeId is None:
            return {"result": "failed", "data": []}

        return {"result": "success", "data": {"consumeId": consumeId}}
        
    def getGlucose(self, entryId):
        
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, entryId, glucoseLevel, measuredTime FROM glucose WHERE entryId = %s
        """, (entryId, ))
        row = cursor.fetchone()

        if row is None:
            return {"result": "failed", "data": []}

        glucoseId = row[0]
        entryId = row[1]
        glucoseLevel = row[2]
        measuredTime = row[3]

        cursor.close()

        return {"result": "success",
                "data"  : [ {"id"           : glucoseId,
                            "entryId"       : entryId,
                            "glucoseLevel"  : glucoseLevel,
                            "measuredTime"  : measruedTime
                            }
                          ]
                }

    def addGlucose(self, entryId, glucoseLevel, measuredTime):

        cursor = self.conn.cursor()
        cursor.execute(""" INSERT INTO glucose (entryId, glucoseLevel, measuredTime) 
        VALUES (%s, %s, %s)""", (entryId, glucoseLevel, measuredTime))

        glucoseId = cursor.lastrowid
        self.conn.commit()
        cursor.close()

        if glucoseId is None:
            return {"result": "failed", "data": []}

        return {"result": "success", "data": {"glucoseId": glucoseId}}
