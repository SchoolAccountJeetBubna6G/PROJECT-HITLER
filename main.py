import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import time
import pyautogui
import random
import command_list
import json

engine = pyttsx3.init()
listener = sr.Recognizer()
listener_for_yt_query = sr.Recognizer()
listener_for_weather_city = sr.Recognizer()
listener_for_option_weather = sr.Recognizer()
listener_for_spotify_song_name = sr.Recognizer()
listener_for_google_search_query = sr.Recognizer()
listener_for_closing_tabs = sr.Recognizer()

engine.setProperty('voice', engine.getProperty('voices')[0].id)#get voices 

engine.say('Hi! How can i help you!')
engine.runAndWait()

setTimer = False

app_names = json.load(open('app_names.json','r'))

def getWeather(city_name):
    API_KEY = "f354c11eb850918547081c684e06e42d"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    city = city_name
    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = round(data["main"]["temp"] - 273.15, 2)

        return weather, temperature
    else:
        return 0

def getTime():
    t = time.localtime()
    current_time = time.strftime("%I,%M", t)
    return current_time

def getDate():
    current_day = time.strftime("%b %d")
    return current_day

def findNumInText(text = ''):
    res = [int(i) for i in text.split() if i.isdigit()]
    return res if len(res) > 0 else 0

def engineSay(speakText):
    engine.say(speakText)
    engine.runAndWait()

# define the countdown func.
def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		timer = '{:02d}:{:02d}'.format(mins, secs)
		print(timer, end="\r")
		time.sleep(1)
		t -= 1
	
	return True

def filter_word_query(list_1 = list, list_2 = list):
    list_1 = str(list_1).split()
    list_1_as_set = set(list_1)
    intersection = list(list_1_as_set.intersection(list_2))
    print(intersection)
    for word in range(len(intersection)):
        list_1.remove(intersection[word])
    return list_1

def list_to_string(list):
    str = ''
    return (str.join(list))

def play_spotify():
    url = 'https://open.spotify.com/'
    webbrowser.get().open(url)
    time.sleep(9)
    pyautogui.press('space')

timer_set = 0



while True:
    '''
    setTimer = countdown(timer_set)
    print(countdown(timer_set))
    '''

    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=1)
        command = listener.listen(source)
        try:
            text = listener.recognize_google(command)
            for i in text:
                i.lower()
            print(text)
            if 'Hitler' in text:
                if 'play' in text:
                    if 'Vivah' not in text:
                        url_youtube = 'https://www.youtube.com/results?search_query='
                        search_query_spotify = str(filter_word_query(text, command_list.commands))
                        if 'spotify' in search_query_spotify:
                            play_spotify()
                        else:
                            engineSay(f'playing: {search_query_spotify}')
                            webbrowser.get().open(url_youtube+search_query_spotify)
                            time.sleep(4)
                            pyautogui.press('tab')  
                            pyautogui.press('enter')

                if 'weather' in text:                    
                    city = 'Bengaluru'
                    weather_list = getWeather(city)
                    if weather_list != 0:
                        engineSay(f'The weather of {city} is {weather_list[0]} and temperature is {weather_list[1]}')
                    else:
                        engineSay('Sorry, city not found')

                if 'stop' in text:
                    False

                if 'time' in text or 'Time' in text:
                    current_time = getTime()
                    engine.say(f'The current time is: {current_time}')
                    engine.runAndWait()
                
                if 'day' in text or 'Day' in text or 'date' in text or 'Date' in text:
                    current_day = getDate()
                    engine.say(f'Today is {current_day}')
                    engine.runAndWait()

                if 'how are you' in text:
                    responses = ['Im good! Thanks for asking! I really appreciate it!',
                    'i am ok! How are you!',
                    'sir, im a robot dont you remember?',
                    'sir, im ok!']
                    engine.say(random.sample(responses, 1))
                    engine.runAndWait()

                if 'I love' in text:
                    responses = ['Oh, is it! Well, who the hell are you and what the hell are you doing here you freaky bozo',
                    'i have no idea how to respond to that as jeet didnt teach me how to flirt',
                    'well, at least you dont like 7 lol, wait you do? as expected']
                    engine.say(random.sample(responses, 1))
                    engine.runAndWait()

                if 'how to' in text or 'why' in text:
                    engine.say(f'Results for: {text}')
                    engine.runAndWait()
                    search_query_google = text
                    url = f'https://www.google.com/search?q={search_query_google}&sxsrf=ALiCzsZcvIpOyLPFaZa_huKZJA0dO5JDhA%3A1662896136188&ei=CMgdY-GQC77y4-EPtP6p2Ac&ved=0ahUKEwjhtPvr0oz6AhU--TgGHTR_CnsQ4dUDCA4&uact=5&oq=how+to+cook&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBQgAEJECMgUIABCRAjIFCAAQkQIyBQgAEJECMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIICAAQgAQQsQM6CggAEEcQ1gQQsAM6BAgAEEdKBQg8EgExSgQIQRgASgQIRhgAULgFWI8HYPAIaAFwAngAgAHtAogB7QKSAQMzLTGYAQCgAQHIAQjAAQE&sclient=gws-wiz'
                    webbrowser.get().open(url)

                if 'open' in text:
                    f = open('app_names.json')
                    data = json.load(f)
                    print('open detected')
                    # print(data)
                    #print(data['apps'][0]['name'])
                    for i in range(len(data)):
                        print('loop')
                        name_app_unfiltered_normal = data['apps'][i]['name']
                        name_app_unfiltered_office = data['apps_tbo'][i]['name']
                        print(name_app_unfiltered_office)
                        if name_app_unfiltered_normal in text:
                            print('App name found')
                            url = data['apps'][i]['url']
                            webbrowser.get().open(url)
                        elif name_app_unfiltered_office in text:
                            print('Office, app!')
                            command = data['apps_tbo'][i]['command']
                            pyautogui.hotkey('win','r')
                            time.sleep(1)
                            pyautogui.typewrite(command)
                            pyautogui.press('enter')
                    
                    print('over')

                if 'exit' in text:
                    engine.say('Closing current tab')
                    engine.runAndWait()
                    pyautogui.hotkey('alt','f4')
                
                if 'volume down' in text:
                    nums_volume_down = findNumInText(text)
                    print(nums_volume_down)
                    if nums_volume_down != 0:
                        volume_to_shift = nums_volume_down[0]
                        engineSay(f'Sure! turning volume down by {volume_to_shift}')
                        num_press_keydown = int(volume_to_shift*1)
                        pyautogui.press('volumedown', num_press_keydown)

                if 'volume up' in text:
                    nums_volume_up = findNumInText(text)
                    print(type(text))
                    print(nums_volume_up)
                    if nums_volume_up != 0:
                        volume_to_shift_up = nums_volume_up[0]
                        engineSay(f'Sure! turning volume up by {volume_to_shift_up}')
                        num_press_volume_up = int(volume_to_shift_up*1)
                        pyautogui.press('volumeup', num_press_volume_up)                

                if 'close' in text and 'tab' in text:
                    num_close_tab = findNumInText(text)
                    if num_close_tab == 0:
                        pyautogui.hotkey('ctrl','w')
                        time.sleep(1)
                    else:
                        for i in range(int(num_close_tab[0])):
                            pyautogui.hotkey('ctrl','w')
                '''
                if  'timer' or 'alarm' in text:
                    time_set = str(filter_word_query(text, command_list.commands))
                    timer_set = findNumInText(time_set)
                    setTimer = True
                '''
        except sr.UnknownValueError:
            print('Sorry, u spoke too bad not my problem hehe')
        except sr.WaitTimeoutError:
            print('Time out error')
        except sr.RequestError:
            print('request error')
 