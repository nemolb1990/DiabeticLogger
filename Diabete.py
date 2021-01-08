import DiabeteDB as db

import json

class Diabete:
    """Diabete class
    Controller that verifies and add, delete, edit the appropriate data to the database.
    """

    def __init__(self):
        """
        Constructor for Diabete class
        """
        self.errorMsg = ""
        self.db = db.DiabeteDB()

    def getErrorMsg(self):
        """ getErrorMsg
        @returns last error message. It will be empty if there was no error since the class
        was first created
        """
        return self.errorMsg

    def newLog(self, entryType, name, entry):
        """newLog
        @param entryType (String)
        @param entryInfo (JSON)
        @returns -1 on fail, id of the last foodConsumed added on success

        newLog enters the new entry into database first and use the resulting entry id to add new log
        into appropriate table according to the entry type.
        If adding new log into the appropriate table fails, it del the previously added entry since
        it won't be used anymore.
        """
        # Add entry
        entryRes = self.newEntry(entryType, name)
        if entryRes == -1:
            return -1
        entryId = entryRes["data"]["entryId"]

        # Add glucose
        if entryType.lower() == "glucose":
            glucoseRes = self.newGlucose(entryId, entry)
            if glucoseRes == -1:
                self.delEntry(entryId)
            return glucoseRes
        # Add meal
        elif entryType.lower() == "meal":
            foodRes = self.newFoodConsumed(entryId, entry)
            if foodRes == -1:
                self.delEntry(entryId)
            return foodRes

        else:
            self.errorMsg("Invalid entryType")
            return -1

    def newEntry(self, entryType, name):
        """newEntry
        @param entryType (String)
        @param name (String)
        @return -1 on fail else, entryId on success

        newEntry adds the new entry data to the database and returns the id of the new entry
        """
        res = self.db.addEntry(entryType, name)
        if res["result"] == "failed":
            self.errorMsg = "Failed to add entry"
            return -1
        return res

    def delEntry(self, entryId):
        """delEntry
        @param entryId (int)
        @return -1 on fail, 0 on success
        
        delEntry deletes the entry from the database based on the entryId
        """
        res = self.db.delEntry(entryId)
        if res["result"] == "failed":
            self.errorMsg="Failed to delete entry"
            return -1
        return 0

    def newGlucose(self, entryId, entry):
        """newGlcose
        @param entryId (int)
        @param entry (JSON)
        @return -1 on fail, added glucoseId on success

        newGlucose will confirm entry is a JSON that entry holds key glucoseLevel and measruedTime 
        then add new Glucose into databse
        """

        # is this JSON?
        try:
            json.dumps(entry)
        except:
            return -1

        # Confirm Keys and add
        if "glucoseLevel" in entry and "measuredTime" in entry:
            res = self.db.addGlucose(entryId, entry["glucoseLevel"], entry["measuredTime"])
            if res["result"] == "failed":
                self.errorMsg = "Failed to add Glucose"
                return -1
            
            return res["data"]["glucoseId"]
        self.errorMsg = "Invalid Glucose entry"
        return -1

    def newFoodConsumed(self, entryId, entry):
        """newFoodConsumed
        @param entryId (int)
        @param entry (JSON)
        @return -1 on fail, last added foodConsumedId on success

        newFoodConsumed will confirm that entry's food value is list and iterate through the list
        to add the new foodConsumed into database
        """

        if isinstance(entry["food"], list) and "consumedTime" in entry:
            for food in entry["food"]:
                if "id" in food:
                    res = self.db.addFoodConsumed(entryId, food["id"], entry["consumedTime"])
                    if res["result"] == "failed":
                        self.errorMsg = "Failed to add FoodConsumed"
                        return -1
                else: 
                    self.errorMsg = "Invalid foodFormat"
                    return -1

            return res["data"]["consumedId"]
        print("Invalid list")
        self.errorMsg = "Invalid list"
        return -1

    def editLog(self, entryId, entry):
        """editLog
        @param entryId (int)
        @param entry (JSON)
        @return -1 on fail, last added glucoseId/foodConsumed on success

        editLog will find the entry based on the entry ID and attempts to replace the entry
        """
        entryRes = self.db.getEntry(entryId)
        if entryRes["result"] == "failed":
            self.errorMsg="There's no entry by the Id provided"
            return -1

        if entryRes["data"]["type"] == "glucose":
            self.db.deleteGlucoseByEntry(entryId)
            return newGlucose(entryRes["id"],entry)

        elif entryRes["data"]["type"] == "meal":
            self.db.deleteFoodConsumedByEntry(entryId)
            return newFoodConsumed(entryRes["id"], entry)

        else:
            self.errorMsg="invalid entry type"
            return -1

    def getFoodInfo(self, name):
        """getFoodInfo
        @param name (string)
        @return -1 on fail, list of JSON food info on success

        getFoodInfo takes the name of the food and returns the list of the food found in database.
        """

        if name is None:
            self.errorMsg = "Invalid food name"
            return -1

        res = self.db.getFoodInfoByName(name)

        if res["result"] == "failed":
            self.errorMsg = "Failed to grab food Info"
            return -1

        return res["data"]

    def newFoodInfo(self, name, carb):
        """newFoodInfo
        @param name (string)
        @param carb (int)
        @return -1 on fail, last added foodId on success

        newFoodInfo takes name and carb info and add the info to the database
        """

        if name is None or carb is None or carb < 0:
            self.errorMsg = "Invalid carb or food name"
            return -1

        res = self.db.addFoodInfo(name, carb)
        if res["result"] == "failed":
            self.errorMsg = "Failed to add food Info"
            return -1
        
        return res["data"]["foodInfoId"]

    #TODO: Maybe some way to print/return summarization will be nice too in the future
