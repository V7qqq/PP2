def check(name):
    for i in movies:
        if i['name'] == name:
            if i['imdb'] > 5.5:
                return True
    
    return False
       
def sublist():
    sublist = []
    for i in movies:
        if i['imdb'] > 5.5:
            sublist.append(i['name'])

    print(sublist)

def category(name):
    for i in movies:
        if i['category'] == name:
            print(i['name'])

def average():
    count = 0.0
    d = 0
    for i in movies:
        count += i['imdb']
        d +=1
    
    return count / d

def average_category(name):
    count = 0.0
    d = 0
    for i in movies:
        if name == i['category']:
            count += i['imdb']
            d +=1
    
    return count / d

movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]




print(check('We Two'))
print(check('Exam'))
sublist()
category('Romance')
print(average())
print(average_category('Romance'))
