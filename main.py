import speech_recognition as sr
import webbrowser #anyoutput will get open through web browser
#it is built in python 
import pyttsx3 #does text to speech whatever we want it to speak
import time #for the duration used 
import musiclib #for playing songs
import requests # library for playing news
from gtts import gTTS #pip install gtts 
#benefits to use gtts is we can control speed and change voice
import pygame #pip install pygame
import os
from google import genai #importing genai libraries
import datetime as dt #importing libraries for weather date and time


'''pip install pockeetsphinx - haven't use this as it not listen properly 
so we have used r.recognize google audio it listens clearly''' #we have install these lib
r = sr.Recognizer() #Recognizer is a class helps in speech recognization functionality me
#help karti hai
engine = pyttsx3.init() #initializing pyttsx
weather_api = "1141efce99bb8830d3362db2b36bf0f7"
newsapi ="f495bd0c56aa4984b708d166dfd02ec0" #is from news api website

# ai_api =
def speak_old(text):     #speak funct which will take input  of text and speak it 
     engine.say(text) #it will speak the text from pyttsx3 weebsite
     engine.runAndWait() #from pyttsx3 website for more

#changing it to old

#funct for ai based output
client=genai.Client(api_key="AIzaSyB5O1RLG7xUnzAnUrTs5FThIkYmH_qB-I4")

def aiProcess(command):
#pip install genai  will install the genai(gemini) libraries
#if you saved the key under a different environment variable name,
#you can do something like:
#here we are setting the response for genai and returning the response
            
            response = client.models.generate_content(model="gemini-2.5-flash",contents=command)      
    
            
            return(response.text) #returns the response text

 
'''use gTTs for larger project as it is more reliable- copying code from gtts website'''
#new speak function from
def speak(text):
    tts = gTTS(text,slow=False) #so that it speaks the text
    tts.save('temp.mp3') #will make mp3 of text
    
    #now we will use chat gpt and ask code for playing mp3 in pygame
    #it will play the sound for the text

    # Initialize mixer
    pygame.mixer.init()

    # Load your mp3 file
    pygame.mixer.music.load("temp.mp3")  # replace with your filename

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running until the music can play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")





def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")

    #now here our friday can open websites and play music and can respond 
    # now we can also add news
    elif("news" in c.lower()):
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}" )
        #these lines from chat gpt that will give the headlines

        if r.status_code==200:
            #parse the JSOM response
            data = r.json()

            #extract the articles
            articles = data.get('articles',[])

            #speak the headlines
            for article in articles:
                speak(article['title']) 
                
                


    elif(c.lower().startswith("play")): #the command starts with play like play doraemon
        song =c.lower().split(" ")[1] #here when we said play doraemon so it will
        #splits the both words after space and return them in list and then select word
        #at index 1 for selecting song
        link =musiclib.music[song] #then search it in music lib
        webbrowser.open(link) #open the link
        
    elif("weather" in c.lower()):
       city_name = c.lower().split()[-1] #returns city name that we speak
       if 'in' in c.lower():
           city_name = c.lower().split('in',1)[1].strip() #grabs all words after 'in' like weather in gkp
       
       
       BASE_URL ="https://api.openweathermap.org/data/2.5/weather?"
       API_KEY ="1141efce99bb8830d3362db2b36bf0f7"
       CITY = f"{city_name}"
        #here we are getting temp in kelvin so we changed it to celsius and fahrenheit
       def kelvin_to_fahrenh_celsius(kelvin):
                celsius = kelvin -273.15
                fahrenheit = celsius*(9/5)+32
                return celsius,fahrenheit
            
       url = BASE_URL+"appid=" +API_KEY +"&q="+CITY
       response = requests.get(url).json() #gather the response of weather from above url
        
        #setting the response in that we changed to above to celcius and all
       temp_kelvin =response['main']['temp'] #will extracts the temp(in kelvin) from the main part of response
       temp_celsius, temp_fahrenheit  = kelvin_to_fahrenh_celsius(temp_kelvin) #converts the teemp
       feels_like_kelvin = response['main']['feels_like'] #extracts feels like from main
       feels_like_celsius, feels_like_fahrenheit = kelvin_to_fahrenh_celsius(feels_like_kelvin) #conveert to celsius and fahre
       wind_speed = response['wind']['speed'] #extracts wind speed from wind section
       humidity = response['main']['humidity'] #gets humidity percentage from main sec of api response
       description =response['weather'][0]['description'] #it is basically a list of weather condition
       #it extracts the decription of weather like "clear sky","light rain"
       sunrise_time =dt.datetime.utcfromtimestamp(response['sys']['sunrise']+ response['timezone'])
       #it adds timezone offset to convert the time to local timezone of the city
       sunset_time =dt.datetime.utcfromtimestamp(response['sys']['sunset']+ response['timezone']) #here the sunrise and sunset timestamps
       #are taken from sys part of response
       #the datetime.utcfromtimestamp() converts the  unix timestamp to oddset to a
       #datetime.obj representing the local sunrise and sunset times as datetime objects

        #setting the response that it will speak for  weather
       speak(f"Temperature in {CITY}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°Fahrenheit") #setting decimal value upto 2 
       speak(f"Temperature in {CITY} feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°Fahrenheit")
       speak(f"humidity in {CITY}: {humidity}%")
       speak(f"Wind speed in {CITY}: {wind_speed} meter per second")
       speak(f"Genral weather in {CITY}: {description}") 
       speak(f"sun rises in {CITY} at {sunrise_time} local time")
       speak(f"sun sets in {CITY} at {sunset_time} local time")






#ab hum isko ai powered karenge ab agr request inme se koi nhi hua
#to hum open ai ke pas jayenge and
    
    else:
        #let genai handle the request
        output=aiProcess(c)
        speak(output)
        



if __name__ =="__main__":
    speak("Initializing Friday...") 
     #now hum chahte hai ki ye ek word sune file kuch response de maybe tone
     #then fir hum bole mai nhi chahta ki ye humesha chalta rahe
     #code sample aap yad nhi rakh sakte ya to ap chatgpt par dekho ya kahi se uthao

    
    while True:  #mtlb ek word k liye listening karta rahe mtlb ye cheez hoti rahe
          #listen for the wake word "jarvis"
          # obtain audio from the microphone
        #r = sr.Recognizer()
       
        '''timeout param - max no. of sec that it will wait for a 
            phrase to start before giving up the output
            phrase_time_limit - max numb of sec this will allow a phrase to continue 
            before stopping and returning the part of phrase processed'''

        print("recognizing....") #as it is taking time to recognize 
            
        # recognize speech using Sphinx
        #we have to keep all this in try other wise error can come
        try:
            with sr.Microphone() as source: #will put this in try hum nhi chahte isme error aye
                print("Listening...")
                
                audio = r.listen(source,timeout =3,phrase_time_limit =1) #listen funct takes two parameter 1. is timeout parameter
                #2. is phrase time parameter so here we set limit  2 sec for timeout parameter
                #means it will listen only for 2 sec
                word = r.recognize_google(audio) #recognize google will help it to detect correct word of what is
                #is being  said
            if(word.lower() == "friday"): #if we speak friday

                speak("sir") #it replies this
                

                #listen for command
                with sr.Microphone() as source:

                    
                    print("Friday Activated....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(f"Command received: {command}")

                    processCommand(command) #this funct will process command
           
        
        except Exception as e:
            print("Error; {0}".format(e))
            

        # recognize speech using Google Speech Recognition