from bs4 import BeautifulSoup
import requests


def getHTML(countryName):
	url = "https://www.citypopulation.de/en/" + countryName + "/cities/"
	result = requests.get(url)

	if result.status_code == 404:
		url = "https://www.citypopulation.de/en/" + countryName + "/"
		result = requests.get(url)

	if result.status_code == 404:
		countryName = countryName.capitalize()
		url = "https://www.citypopulation.de/" + countryName + ".html"
		result = requests.get(url)


	return result


def getCities(countryName):
	result = getHTML(countryName)

	doc = BeautifulSoup(result.text, "html.parser")
	cities = doc.find(id="citysection")
	locations = cities.find_all("a")
	names = []

	for location in locations:
		if (location.find("span")):
			names.append(location.string)

	return names


def getCityState(countryName):
	result = getHTML(countryName)

	doc = BeautifulSoup(result.text, "html.parser")
	locations = doc.find(id="citysection")
	locations = locations.find("tbody")
	locations = locations.find_all(class_="radm")
	states = []

	for location in locations:
		states.append(location.string)

	return states


def getCityPopulations(countryName):
	result = getHTML(countryName)

	doc = BeautifulSoup(result.text, "html.parser")
	locations = doc.find(id="citysection")
	locations = locations.find("tbody")
	locations = locations.find_all(class_="rpop prio1")
	populations = []

	for location in locations:
		populations.append(location.string)

	return populations


def getCityInfo(countryName, choice):
	def swap(arr, i):
		temp = arr[i];
		arr[i] = arr[i + 1]
		arr[i + 1] = temp

	names = getCities(countryName)
	populations = getCityPopulations(countryName)
	states = getCityState(countryName)
	cities = []

	if (not (len(names) == len(populations) == len(states))):
		print("Lists of cities/populations/states have unequal length.")
		return;

	if choice == 'p':
		for i in range(len(populations) - 1):
			for j in range(len(populations) - 1):
				if populations[j].replace(",", "").isdigit():
					if populations[j + 1].replace(",", "").isdigit():
						if int(populations[j].replace(",", "")) > int(populations[j + 1].replace(",", "")):
							swap(names, j)
							swap(populations, j)
							swap(states, j)
					else:
						swap(names, j)
						swap(populations, j)
						swap(states, j)

	for i in range(len(names)):
		cities.append((names[i], populations[i], states[i]))

	return cities


info = getCityInfo("nauru", 'p')
for i in range(len(info)):
	for x in range(3):
		print(info[i][x])
	print()

"""
Check how to fix countries such as Nauru without abbreviations, or South Africa with false population/abbrev.
Could be done by checking if the current location has a correponding string, if not, adding ... as blank space.
"""