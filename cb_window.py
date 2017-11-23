
# Calculate the height of an office tall building where only the number window
# http://www.ctbuh.org/HighRiseInfo/TallestDatabase/Criteria/HeightCalculator/tabid/1007/language/en-GB/Default.aspx
# This caluculation does not include any factors for spires or any other major projections at the roof plane, due to the wide ranging nature of these.
from array import array
import sys
# Factor for increased ground level floor-to-floor height = 3.9m
# Factor for increased mechanical levels floor-to-floor height = 3.9m x (s/20)
# Factor for roof level mechanical systems / parapets / roof features = 7.8m
def hOfficeCalculate(window):
    return ((3.9*window) + 11.7 + (3.9*(window/20))) * 3.28


# Height of building = number of stories x floor-to-floor height = 3.1s
# Factor for increased ground level floor-to-floor height = 1.55m
# Factor for increased mechanical levels floor-to-floor height = 1.55m x (s/30)
# Factor for roof level mechanical systems / parapets / roof features = 6.2m
def hResidentialHotelTallCalculate(window):
	return ((3.1*window) + 7.75 + (1.55*(window/30))) * 3.28


# Height of building = number of stories x floor-to-floor height = 3.5s
# Factor for increased ground level floor-to-floor height = 2.625m
# Factor for increased mechanical levels floor-to-floor height = 2.625m x (s/25)
# Factor for roof level mechanical systems / parapets / roof features = 7.0m
def mixedUseTallBuildingCalculate(window):
	return ((3.5*window) + 9.625 + (2.625*(window/25))) * 3.28


# function that converts a String array to int array
# accepts a list
# returns a list
def convertArrayStrToInt(array):
	newArray = list();
	for i in array:
		newArray.append(int(i))	
	return newArray

def findTheBottomMostWindow(arrayWindows):
	bottomMostWindow = None
	temp1 = arrayWindows[0]
	temp1 = temp1.split()
	temp1 = convertArrayStrToInt(temp1)

	bottomXCoordinate = temp1[1] + temp1[4]

	for wind in arrayWindows:
		windowLocation = wind.split()
		newArrayWindows = convertArrayStrToInt(windowLocation)

		temp2 = (newArrayWindows[1] + newArrayWindows[4])
		if bottomXCoordinate <= temp2:
			bottomXCoordinate = temp2
			bottomMostWindow = wind

	return bottomMostWindow


#.  xbbox/frameW	ybbox/frameH   bboxwidth/frameW. bbHeight/frameH
#10 0.403636363636 0.229508196721 0.0436363636364 0.0765027322404
with open('adobe.txt') as f:

	#car: 1,
    #truck: 2,
    #semi: 3,
    #streetsign: 4, #ex.stop sign
    #trafficlight: 5, #red,yellow,green
    #streetlight: 6,
    #firehydrant: 7,
    #person: 8,
    #door: 9,
    #window: 10,
    #building: 11
    arrayCars = list()
    arrayTrucks = list()
    arraySemis = list()
    arrayStreetsigns = list()
    arrayTrafficlights = list()
    arrayStreetlights = list()
    arrayFirehydrants = list()
    arrayPersons = list()
    arrayDoors = list()
    arrayWindows = list()
    arrayBuildings = list()
    
    content = f.readlines()
    content = [x.strip() for x in content]

    for line in content:
		temp = line.split()
		print(line)
		if temp[0] == '1':
			arrayCars.append(line)
		elif temp[0] == '2':
			arrayTrucks.append(line)
		elif temp[0] == '3':
			arraySemis.append(line)
		elif temp[0] == '4':
			arrayStreetsigns.append(line)
		elif temp[0] == '5':
			arrayTrafficlights.append(line)
		elif temp[0] == '6':
			arrayStreetlights.append(line)
		elif temp[0] == '7':
			arrayFirehydrants.append(line)
		elif temp[0] == '8':
			arrayPersons.append(line)
		elif temp[0] == '9':
			arrayDoors.append(line)
		elif temp[0] == '10':
			arrayWindows.append(line)
		elif temp[0] == '11':		
			arrayBuildings.append(line)
		else:
			print("else")

#1 we collect all windows that are within the building
windInBuild = list()
buildingTopic = arrayBuildings[0]#only one building is in the picture
buildingTopic = buildingTopic.split()

buildingTopic = convertArrayStrToInt(buildingTopic)

buildTopLeft = buildingTopic[1]
buildTopRight = buildingTopic[3] + buildingTopic[1]
buildBottomLeft = buildingTopic[4] + buildingTopic[1]
buildBottomRight = buildBottomLeft + buildTopRight


#print(buildTopLeft, buildTopRight, buildBottomLeft, buildBottomRight)

print("\n")
#0-object 1-x 2-y 3-width 4-height
windowsInsideBuilding = list()
for wind in arrayWindows:

	windowLocation = wind.split()
	newArrayWindows = convertArrayStrToInt(windowLocation)

	windowTopLeft = newArrayWindows[1]
	windowTopRight = newArrayWindows[3] + newArrayWindows[1]
	windowBottomLeft = newArrayWindows[4] + newArrayWindows[1]
	windowBottomRight = windowBottomLeft + newArrayWindows[3]

	print(buildTopLeft, windowTopLeft, buildBottomLeft, windowBottomLeft)
	print(buildTopRight, windowTopRight, buildBottomRight, windowBottomRight)
	print("\n")
	if (buildTopLeft <= windowTopLeft) and (buildBottomLeft >= windowBottomLeft):
		if (buildTopRight >= windowTopRight) and (buildBottomRight >= windowBottomRight):
			windowsInsideBuilding.append(wind)

print("Windows inside the building")
print(len(windowsInsideBuilding))
for values in windowsInsideBuilding:
	print(values)
print("\n")

#2 we find a door and count windows from there up

#we need to make sure that the door is inside the building of interest
filterDoor = list()
for door in arrayDoors:
	doorLocation = door.split()

	#convert each line to be in int array
	newArrayDoors = convertArrayStrToInt(doorLocation)

	#here we extract all door coordinate 
	doorTopLeft = newArrayDoors[1]
	doorTopRight = newArrayDoors[3] + newArrayDoors[1]
	doorBottomLeft = newArrayDoors[4] + newArrayDoors[1]
	doorBottomRight = doorBottomLeft + newArrayDoors[3]

	#we need to filter the right door, which must be inside the building
	if (buildTopLeft <= doorTopLeft) and (buildBottomLeft >= doorBottomLeft):
		if (buildTopRight >= doorTopRight) and (buildBottomRight >= doorBottomRight):
			filterDoor.append(door)

windowsSameXCoordinate = list()

if filterDoor != None:
	doorFirst = filterDoor[0]
	doorFirst = doorFirst.split()
	doorLeftBound = int(doorFirst[1])
	doorRightBound = doorLeftBound + int(doorFirst[3])

	doorLeftBound = doorLeftBound - 50
	doorRightBound = doorRightBound + 50
	print("doorLeftBound" + str(doorLeftBound) + " doorRightBound" + str(doorRightBound))
	for wind in windowsInsideBuilding:
		windowLocation = wind.split()
		newArrayWindows = convertArrayStrToInt(windowLocation)

		windowLeftBound = newArrayWindows[1]
		windowRightBound = windowLeftBound + int(newArrayWindows[3]) #xCoor + width

		#print(windowLeftBound , newArrayWindows[3], doorRightBound, windowLeftBound + newArrayWindows[3])
		windowLocation = wind.split()
		newArrayWindows = convertArrayStrToInt(windowLocation)

		windowTopLeft = newArrayWindows[1]
		windowTopRight = newArrayWindows[3] + newArrayWindows[1]
		windowBottomLeft = newArrayWindows[4] + newArrayWindows[1]
		windowBottomRight = windowBottomLeft + newArrayWindows[3]

		#this is where we filter the windows 
		#windows that are align with the door

		#window x leftCoordinate must be inside doorLeftBound
		#window x rightCoordinate myst be inside doorRightBound
		
		print(doorLeftBound, windowLeftBound, doorRightBound, windowRightBound)
		#print(buildTopLeft, windowTopLeft, windowTopRight, buildTopRight)
		if (doorLeftBound <= windowLeftBound) and (doorRightBound >= windowRightBound):
			windowsSameXCoordinate.append(wind)
			#if (buildTopLeft <= windowTopLeft) and (windowTopRight <= buildTopRight):
				#if(buildBottomLeft >= windowBottomLeft) and (buildBottomRight >= windowBottomRight):
					#windowsSameXCoordinate.append(wind)
	
else:
	print("No door in the building")

print("\n")
print(len(windowsSameXCoordinate))
print("\nWindows within door x coordinate")
for values in windowsSameXCoordinate:
	print(values)
print("\n")



#1 find windows that are on the same x coordinate

# find window that is all the way down
'''bottomMostWindow = findTheBottomMostWindow(windowsInsideBuilding)
print(bottomMostWindow)
bottomMostWindowLocation = bottomMostWindow.split()
newBottomMostWindowLocation = convertArrayStrToInt(bottomMostWindowLocation)

xCoordinateBottomMostWindLeftBound = newBottomMostWindowLocation[1]
xCoordinateBottomMostWindRightBound = xCoordinateBottomMostWindLeftBound + newBottomMostWindowLocation[3]

xLMinus = xCoordinateBottomMostWindLeftBound - 8
xRPlus = xCoordinateBottomMostWindRightBound + 8


#then we collect all windows that have the same (close) x-coordinate with bottomMostWindow
filterWindows = list()
for wind in arrayWindows:
	windowLocation = wind.split()
	newArrayWindows = convertArrayStrToInt(windowLocation)

	windowLeftBound = newArrayWindows[1]
	windowRightBound = windowLeftBound + newArrayWindows[3]

	if (xLMinus < windowLeftBound) and (xRPlus > windowRightBound): 
		filterWindows.append(wind)

print("\nFiltered")
for values in filterWindows:
	print(values)
'''





#print(temp[1])



f.close()
# 
#10 0.545454545455 0.306010928962 0.0472727272727 0.0765027322404


# 1 mter = 3.28 ft or 39.37 inches
# San Jose Hilton = 246.06 ft 		floors = 18 above ground

# Adobe Systems = 259 16 floors
print(len(windowsSameXCoordinate))
numWindows = len(windowsSameXCoordinate)
print("Number of floors:", numWindows)
#buildingType is either office, residential/hotel, or mixed 
buildingType = "office"

if buildingType == "office":
	print(str(hOfficeCalculate(numWindows)) + " feet")
elif buildingType == "residential":
	print(str(hResidentialHotelTallCalculate(numWindows)) + " feet")
else:#mixed
	print(str(mixedUseTallBuildingCalculate(numWindows)) +  " feet")

print("\n")
