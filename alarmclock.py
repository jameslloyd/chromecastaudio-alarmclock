import time
import pychromecast # https://github.com/balloob/pychromecast
import urllib
import pyowm  # https://github.com/csparpa/pyowm
import json

owmapikey = 'XXXXXXX'
chromecasttarget = 'XXXXXXX'
location = 'XXXXXXXX'
radiostation = 'radio2'

# get weather
owm = pyowm.OWM(owmapikey)
#establish time constant
in3hours = pyowm.timeutils.next_three_hours()
#Retreive daily forecast
forecast = owm.daily_forecast(location)
#Retrieve forecast at location in 3 hours
latertoday = forecast.get_weather_at(in3hours)
decoded_later = json.loads(latertoday.to_JSON()) #its easier to load it into JSON and decode it!
detailed_status_later = decoded_later['detailed_status'] #detailed status in 3 hours
# Search for current weather
observation = owm.weather_at_place(location)
#observation = owm.weather_at_coords(-33.73, 150.998)
w = observation.get_weather()
decoded_w = json.loads(w.to_JSON())
detailed_status = decoded_w['detailed_status']
#Create String to Print
loc = location.split(',')
weathermessage = 'The weather today in ' + loc[0] + ', ' + detailed_status.title() + ' (later expect ' + detailed_status_later.title() + ') from ' + str(w.get_temperature('celsius')['temp_min']) + ' degrees C to ' + str(w.get_temperature('celsius')['temp_max']) + ' degrees C, and a humidity of ' + str(decoded_w['humidity']) + '% '

chromecasts = pychromecast.get_chromecasts()

cast = next(cc for cc in chromecasts if cc.device.friendly_name == chromecasttarget)
#set the volume to not scare the crap out me in the morning
cast.set_volume(0.1)
cast.wait()
mc = cast.media_controller
radio = {}
radio['radio1'] = 'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_p'
radio['radio2'] = 'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio2_mf_p'

def tts_url(say):
	url = 'http://translate.google.com/translate_tts?ie=UTF-8&total=1&idx=0&textlen=22&client=tw-ob&q=' + say + '&tl=En-gb'
	return url

if not cast.is_idle:
    print("Killing current running app")
    cast.quit_app()
    time.sleep(5)
wakeup = 'Good Morning!, this is your alarm.' + weathermessage + '. I\'ll now turn on the radio'
mc.play_media(tts_url(wakeup), 'audio/mp3')
mc.block_until_active()
time.sleep(21)
mc.play_media(radio[radiostation], 'audio/mp3')
time.sleep(30)
cast.set_volume(0.15)
time.sleep(60)
cast.set_volume(0.2)
time.sleep(10)
mc.play_media(tts_url('switching off Alarm!, have a good day!.'), 'audio/mp3')

mc.stop()

