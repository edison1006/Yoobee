import numpy as np
rainfall = np.array([0.0,5.2,3.1,0.0,12.4,0.0,7.5])
print("Total rainfall:", np.sum(rainfall))
print("Average rainfall:", np.mean(rainfall))
no_rain_days = np.sum(rainfall == 0)
print("The number of days without rain is:", no_rain_days)
for i in range(len(rainfall)):
    if rainfall[i] > 5:
        print("Day with rainfall more than 5 mm is", i+1)
print("The 75th percentile of the rainfall data is:", np.percentile(rainfall, 75))