import requests

d = {'duration': 14.933333, 
	'height': 1080,
	'poolID': '13',
	'raspberryPiID': '10000000d7e78654',
	'utcTime': 1696566874.5745802,
	'width': 1920,
	'wristbandID': '1880610'}

r = requests.post("http://52.20.31.145:5000/api/upload", timeout=240)

response = r.json()

print(response)
