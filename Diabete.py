import DiabeteDB as db

import json

class Diabete:
    """Diabete class
    """

    def __init__(self):
        self.db = db.DiabeteDB()

    def newLog(self, entryType, name, entry):
        """newLog
        @param entryType
        @param entryInfo
        newEntry takes in string parameter entryType and json parameter entry.
        It enters the new entry into database first and use the resulting entry id to add new log
        into appropriate table according to the entry type.
        If adding new log into the appropriate table fails, it del the previously added entry since
        it won't be used anymore.
        """
        # Add entry
        entryRes = self.newEntry(entryType, name)
        if entryRes["result"] == "failed":
            return res
        entryId = entryRes["data"]["entryId"]

        # Add glucose
        if entryType == "glucose":
            glucoseRes = self.newGlucose(entryId, entry)
            if glucoseRes["result"] == "failed":
                self.delEntry(entryId)
            return glucoseRes

        elif entryType == "meal":
            foodRes = self.newFoodConsumed(entryId, entry)
            if foodRes["result"] == "failed":
                self.delEntry(entryId)
            return foogRes

        else:
            return {"result": "failed", "message": "No such entry type found"}

    def newEntry(self, entryType, name):

        res = self.db.addEntry(entryType, name)
        if res["result"] == "failed":
            return {"result": "failed", "message": "failed to enter new Entry"}
        return res

    def newGlucose(self, entryId, entry):
        """newGlcose
        @param entryId
        @param entry
        newGlucose takes in entryId and json entry.
        It will confirm that entry holds key glucoseLevel and measruedTime and
        add new Glucose into databse
        """

        try:
            json.dumps(entry)
        except:
            return {"result": "failed", "message": "invalid message format"}

        if "glucoseLevel" in entry and "measuredTime" in entry:
            res = self.db.addGlucose(entryId, entry["glucoseLevel"], entry["measuredTime"])
            if res["result"] == "failed":
                return {"result": "failed", "message": "failed to enter new Glucose"}
            
            return {"result": "success"}
        return {"result" : "failed", "message": "Invalid glucose info"}

    def newFoodConsumed(self, entryId, entry):
        """newFoodConsumed
        @param entryId
        @param entry
        newFoodConsumed takes in entryId and json entry
        It will confirm that entry's food value is list and iterate through the food list
        and add to the new foodConsumed into database.
        """

        if isinstance(entry["food"], list) and "consumedTime" in entry:
            for food in entry["food"]:
                if "id" in food:
                    res = self.db.addFoodConsumed(entryId, food["id"], entry["consumedTime"])
                    if res["result"] == "failed":
                        return {"result": "failed", "message": "failed to add new FoodConsumed"}
                return {"result": "failed", "message": "invalid consumed food info"}

            return {"result": "success"}
        
        return {"result": "failed", "message": "invalid entry data"}

    def editLog(self, entryId, entry):
       entryRes = self.db.getEntry(entryId)
       if entryRes["result"] == "failed":
           return {"result": "failed", "message": "Entry doesn't exist!"}

       if entryRes["data"]["type"] == "glucose":
           self.db.deleteGlucoseByEntry(entryId)
           return newGlucose(entryRes["id"],entry)

       elif entryRes["data"]["type"] == "food":
           self.db.deleteFoodConsumedByEntry(entryId)
           return newFoodConsumed(entryRes["id"], entry)

       else:
           return {"result": "failed", "message": "Unknown entry type"}

    #def getFoodInfo(self, name):
    #def newFoodInfo(self, name, carb):
