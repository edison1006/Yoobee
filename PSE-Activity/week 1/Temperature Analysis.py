import numpy as np
Temperature = np.array([18.5,19.20,25.0,2,30,13.9])
print("The average temperature is:", np.mean(Temperature))
print("The bigest temperature is:", np.max(Temperature))
print("The smallest temperature is:", np.min(Temperature))
for t in Temperature:
    Fahrenheit = (t * 9/5) + 32
    print("The temperature in Fahrenheit is:", Fahrenheit)
for i in range(len(Temperature)):
    if Temperature[i] > 20:
        print("Day with temperatures exceeded 20°C is", i+1)