from bs4 import BeautifulSoup
import requests
import json
import os
import re

directory='./FFd20Spells'
path='.\\'
output=[]


#generic pull the entire page
def get_html(url,path):
    response = requests.get(url)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(response.text)

#Function to update saved spell list with most recent changes
def update_spells():
    get_html("https://www.finalfantasyd20.com/magic/spells/", path+'spell_list.html' )
    with open('spell_list.html','r',encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    content = list(soup.find_all(['a']))
    cleanedlinks={}
    
    for a in content:    
        if 'https://www.finalfantasyd20.com/magic/spells/' in a['href'] and a.text not in 'Spells':
            cleanedlinks[a.text] = a['href']

    for link in cleanedlinks:
        #could break out targetpath into separate function in too many characters need replacing
        targetpath=path+'FFd20Spells\\' + str(link).replace(' ','_').replace('/','').replace('__','_').replace('?','x')+'.html'
        get_html(cleanedlinks[link], targetpath)
        #time.sleep(1) --to be polite we add sleep. Might remove since script doesn't appear to spam even without it

#construct a dictionary to be output as json for each spell
#left in just in case someone needs this format, but v2 format is used for roll20 mod
def construct_dict(id,name,school,level,casting,range,target,area,effect,duration,saving,resistance,description):
    new_dic = {id:{}}
    values = [{'name':name}
              ,{'school':school}
              ,{'level':level}
              ,{'castingTime':casting}
              ,{'range':range}
              ,{'target':target}
              ,{'area':area}
              ,{'effect':effect}
              ,{'duration':duration}
              ,{'savingThrow':saving}
              ,{'spellResistance':resistance}
              ,{'description':description}]
    for val in values:
        new_dic[id].update(val)
    return new_dic
#alt format to be more callable in javascript/roll20
def construct_dictv2(id,name,school,level,casting,range,target,area,effect,duration,saving,resistance,description):

    new_dic={
        'name':name
        ,'school':school
        ,'level':level
        ,'castingTime':casting
        ,'range':range
        ,'target':target
        ,'area':area
        ,'effect':effect
        ,'duration':duration
        ,'savingThrow':saving
        ,'spellResistance':resistance
        ,'description':description
    }
    return new_dic

def unicode_fixer(input):
    output=input.replace('\u2019','\'')   
    output=output.replace('\u00a0',' ')
    output=output.replace('\u2014','-')
    output=output.replace('\u2013','-')
    output=output.replace('\u201c','\"')
    output=output.replace('\u201d','\"')
    output=output.replace('\u00d7','x')
    output=output.replace('\u2018','\'')
    #try and clean everything up
    output=output.replace('\n','\\n')
    #output=output.replace(r'\\','')
    #output=output.replace(r'\"','')
    output=output.replace('\"','\\"')
    #output=output.replace('\\','')
    output=re.sub('[\u0080-\uFFFF]','',output)

    return str(output).strip()

update_spells()

for filename in os.listdir(directory):
    f = os.path.join(directory,filename)
    if os.path.isfile(f):
        with open(f,'r',encoding='utf-8') as file:
            html=file.read()
        soup = BeautifulSoup(html,'html.parser')
        content=soup.find('div',class_='page-content')
        #assign name early on while page content is full
        name=soup.find(class_='page-title').string
        #unwrap a and span tags and leave text content behind
        for tag in content.find_all('a'):
            tag.unwrap()
        for tag in content.find_all('span'):
            tag.unwrap() 
        #convert content to string, then reparse into Soup as the unwrapped tags are still treated like individual elements
        strcontent=str(content)
        cleancontent=BeautifulSoup(strcontent,'html.parser')
        
        #if something breaks, last printed spell name's html page probably had something to do with it
        print(name)

        school=cleancontent.find(string=re.compile(r'(\s*)School(\s*)'))
        if school != None :
            school=str(school.next.get_text())
            school=school.replace(';','').strip()
        else : 
            school='N/A'

        level=cleancontent.find(string=re.compile(r'(\s*)Level(\s*)'))
        if level != None :
            level=str(level.next).strip()
        else : 
            level='N/A'
                
        casting=cleancontent.find(string=re.compile(r'(\s*)Casting(\s*)Time(\s*)'))
        if casting != None:
            casting=str(casting.next)
            casting=casting.strip()
        else :
            casting='N/A'

        range=cleancontent.find(string=re.compile(r'(\s*)Range(\s*)'))
        if range != None :
            range=str(range.next).strip()
        else : 
            range='N/A'

        area = cleancontent.find(string=re.compile(r'(\s*)Area(\s*)'))
        if area != None :
            area=str(area.next).strip()
        else :
            area='N/A'
        
        target = cleancontent.find(string=re.compile(r'(\s*)Target(\s*)'))
        if target != None :
            target=str(target.next).strip()
        else :
            target='N/A'


        effect = cleancontent.find(string=re.compile(r'(\s*)Effect(\s*)'))
        if effect != None :
            effect=str(effect.next).strip()
        else :
            effect='N/A'

        duration=cleancontent.find(string=re.compile(r'(\s*)Duration(\s*)'))
        if duration != None :
            duration=str(duration.next).strip()
        else :
            duration='N/A'

        saving=cleancontent.find(string=re.compile(r'(\s*)Saving(\s*)Throw(\s*)'))
        if saving != None :
            saving=str(saving.next).replace(';','').strip()
        else :
            saving='N/A'

        resistance=cleancontent.find(string=re.compile(r'(\s*)Spell(\s*)Resistance(\s*)'))
        if resistance != None :
            resistance=str(resistance.next).strip()
        else :
            resistance='N/A'

        description=cleancontent.find(string=re.compile(r'(\s*)DESCRIPTION(\s*)'))
        if description != None :
            description=""
            h5 = soup.find('h5',string='DESCRIPTION')
            for sibling in h5.next_siblings:
                description+=sibling.text
                description+='\n'
            description=description.strip()
        else :
            description='N/A'

        output.append(construct_dictv2(#unicode_fixer(str(filename).replace('.html',''))
                                     unicode_fixer(name)
                                     ,unicode_fixer(name)
                                     ,unicode_fixer(school)
                                     ,unicode_fixer(level)
                                     ,unicode_fixer(casting)
                                     ,unicode_fixer(range)
                                     ,unicode_fixer(target)
                                     ,unicode_fixer(area)
                                     ,unicode_fixer(effect)
                                     ,unicode_fixer(duration)
                                     ,unicode_fixer(saving)
                                     ,unicode_fixer(resistance)
                                     ,unicode_fixer(description)
                                    ))

with open(path+'spell_reference.json', 'w') as outfile:
    json.dump(output, outfile,indent=4)





