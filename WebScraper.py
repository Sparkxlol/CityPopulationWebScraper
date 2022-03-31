from bs4 import BeautifulSoup
import requests


def getCities(countryName):
	url = "https://www.citypopulation.de/en/" + countryName + "/cities/"

	result = requests.get(url)
	doc = BeautifulSoup(result.text, "html.parser")
	cities = doc.find(id="citysection")
	locations = cities.find_all("a")
	names = []

	for location in locations:
		if (location.find("span")):
			names.append(location.string)

	return names


def getCityState(countryName):
	url = "https://www.citypopulation.de/en/" + countryName + "/cities/"

	result = requests.get(url)
	doc = BeautifulSoup(result.text, "html.parser")
	locations = doc.find(id="citysection")
	locations = locations.find("tbody")
	locations = locations.find_all(class_="radm")
	states = []

	for location in locations:
		states.append(location.string)

	return states


def getCityPopulations(countryName):
	url = "https://www.citypopulation.de/en/" + countryName + "/cities/"

	result = requests.get(url)
	doc = BeautifulSoup(result.text, "html.parser")
	locations = doc.find(id="citysection")
	locations = locations.find("tbody")
	locations = locations.find_all(class_="rpop prio1")
	populations = []

	for location in locations:
		populations.append(location.string)

	return populations

def getCityInfo(countryName):	
	names = getCities(countryName)
	populations = getCityPopulations(countryName)
	states = getCityState(countryName)
	cities = []

	if (not (len(names) == len(populations) == len(states))):
		print("Lists of cities/populations/states have unequal length.")
		return;

	for i in range(len(names)):
		cities.append((names[i], populations[i], states[i]))

	return cities


info = getCityInfo("uk")
for i in range(len(info)):
	for x in range(3):
		print(info[i][x])
	print()



