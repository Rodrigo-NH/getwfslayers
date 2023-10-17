from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pathlib, os
import zipfile
from time import sleep

servicelink = 'https://geoserver.meioambiente.mg.gov.br/master/IDE/ows'
workingdir = r'D:\wfstest'
layersToDownload = 'layersToDownload.txt'
mode = 1

def main():
	page = getWFS(servicelink + '?SERVICE=WFS&REQUEST=GetCapabilities')
	layers = getLayers(page)

	if mode == 1:
		getTitles(layers, workingdir + r'\layerNames.txt')
	elif mode == 2:
		downloadGroup(layers, workingdir + r'\\' + layersToDownload)

def downloadGroup(layers, file):
	grupo = open(file, 'r', encoding='utf-8')
	gl = grupo.readlines()
	dir =  pathlib.Path(gl[0].strip()).absolute()
	dir2 = dir.joinpath('zipcopies')
	try:
		os.mkdir(dir)
	except Exception as e:
		print(e)
	try:
		os.mkdir(dir2)
	except Exception as e:
		print(e)
	for t in range(1, len(gl)):
		layern = gl[t].strip()
		if layern != '':
			for each in layers:
				title = each[2].strip()
				if title == layern:
					print(title)
					print(each[1])
					downloadLayer(each, dir2)
					basename = each[2].strip().replace('/', '_')
					filename = str(dir2) + '\\' + basename.replace(' ', '_') + '.zip'
					print("===========")
					print(filename)
					zipdata = zipfile.ZipFile(filename)
					zipinfos = zipdata.infolist()
					for zipinfo in zipinfos:
						fexte = zipinfo.filename.split('.')[1]
						zipinfo.filename = basename + '.' + fexte
						zipdata.extract(zipinfo, dir)

def downloadLayer(layer, dir2):
	downshapeurl = servicelink + '?service=WFS&version=1.0.0&srsName=epsg:'
	downshape = downshapeurl + layer[0] + '&request=GetFeature&typeName=' + layer[1] + '&outputFormat=SHAPE-ZIP'
	response = requests.get(downshape)
	filename = str(dir2) + '\\' + layer[2].strip().replace(' ','_') + '.zip'
	filename = filename.replace('/', '_')
	open(filename, "wb").write(response.content)
	# sleep = Just being (super) cool to the server as my intervention dont cause any issues to other users. You can comment this out if you want
	sleep(3)


def getTitles(layers, outputfile):
	parse = open(outputfile, 'w', encoding='utf-8')
	for each in layers:
		parse.write(each[2] + '\n')
	parse.close()

def getWFS(url):
	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
	page = requests.get(url, timeout=5, headers=header)
	return page

def getLayers(page):
	soup = BeautifulSoup(page.text, features="xml")
	takeaways = soup.findAll('FeatureType')
	layers = []
	for each in takeaways:
		print(each)
		li = []
		li.append(each.DefaultCRS.string.split('::')[1]) # urn:ogc:def:crs:EPSG::4674
		li.append(each.Name.string.split('IDE:')[1]) # ide_1601_mg_indice_umidade_thornthwaite_pol
		li.append(each.Title.string) # Índice de umidade
		layers.append(li)
	return layers

if __name__ == "__main__":
	main()