# driverData
This code is for an internship application. Involves reading two different commands from a text file and storing / manipulating read data accordingly and return total distance and average speed.

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
  10) if driver has data, pull apart by key and value (nested dictionary) and update
  11) if driver has no data, initialize data
