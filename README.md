# driverData
This code is for the Root internship application. Involves reading two different commands from a text file and storing / manipulating read data accordingly and return total distance and average speed for each driver.

The problem solving process is as follows:
1) Understand how the supplied data is structured in the text file
2) Read the data into some structure (list) to keep it all together and ensure ease of manipulation
3) Split data into lines, then split lines further into words or (char sequences separated by spaces)
4) Determine if the first word is one of the two expected commands (Drive or Trip)
5) If Drive, save next word into dictionary as key and initialize a nested dictionary as its value
6) Initialize the remaining words in Trip list to their respective purposes (start time, end time, miles)
7) Create methods for finding total driving time for trip and finding speed for trip
8) Ensure name is in dictionary
  9) Call distance and speed methods
  10) if driver has data, pull apart by key and value and update
  11) if driver has no data, initialize data
12) If command is unknown, delete driver
13) Sort list of drivers by total distance

A noteworthy decision in this process was choosing to implement a nested dictionary. To keep each driver's data with that driver, a dictionary was made with the driver's name as the key and his/her data in the value--stored with a label as the key and the value being the numeric value associated with that label (i.e. {'Alex', {"total_distance": 42, "total_time": 1.25, "avg_speed": 34}}). The dictionary was a good option because it allowed for making the driver an object. The dictionary also makes keeping track of each object's different characteristics and working with the values easy.
