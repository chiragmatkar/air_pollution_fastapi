#from functions.variables import *
#from functions.calculate_on_ref_Ro import calculate_on_ref_Ro

##mq2_ref_lpg_ppm = calculate_on_ref_Ro(int(112.22),MQ2_RL,MQ2_Ref_#Ro,MQ2_LPGCurve)
#print(mq2_ref_lpg_ppm)
import sys
from app.database import get_collection
collection=get_collection()

country="India"
for x in collection.find({},{"country":country}):
  print(x)
