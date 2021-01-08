import Diabete
from datetime import datetime

d = Diabete.Diabete()

d.newFoodInfo("Banana", 30)
d.newFoodInfo("Dumpling", 8)
d.newFoodInfo("Dumpling", 10)
d.newFoodInfo("Whole Wheat Sandwich", 30)
d.newFoodInfo("Rice", 15)
d.newFoodInfo("Stew", 7)
d.newFoodInfo("Tofu", 0)


d.newLog("glucose", "Fast", {"glucoseLevel":"97", "measuredTime": "2019-12-11 07:00:00"}) 
d.newLog("glucose", "Morning", {"glucoseLevel":"97", "measuredTime": "2019-12-11 10:00:00"}) 
d.newLog("glucose", "Afternoon", {"glucoseLevel":"97", "measuredTime": "2019-12-11 15:00:00"}) 
d.newLog("glucose", "Evening", {"glucoseLevel":"97", "measuredTime": "2019-12-11 21:15:00"}) 


food = d.getFoodInfo("Banana")
if food != -1:
    d.newLog("Meal", "Breakfast", {"food":[food[0]], "consumedTime": "2019-12-11 08:00:00"})

food = d.getFoodInfo("Crackers")
if food != -1:
    d.newLog("Meal", "Snack1", {"food":[food[0]], "consumedTime": "2019-12-11 10:00:00"})

food = d.getFoodInfo("Whole Wheat Sandwich")
if food != -1:
    d.newLog("Meal", "Lunch", {"food":[food[0]], "consumedTime": "2019-12-11 12:00:00"})

food = d.getFoodInfo("Dumpling")
if food != -1:
    d.newLog("Meal", "Snack2", {"food":[food[0]], "consumedTime": "2019-12-11 14:00:00"})
    
dumpling = d.getFoodInfo("Dumpling")
rice = d.getFoodInfo("Rice")
stew = d.getFoodInfo("Stew")
tofu = d.getFoodInfo("Tofu")
consumedTime = "2019-12-11 18:00:00"
if dumpling != -1 and rice != -1 and stew != -1 and tofu != -1:
    d.newLog("Meal", "Dinner", {"food":[dumpling[1], rice[0], stew[0], tofu[0]],
                                "consumedTime": consumedTime})
