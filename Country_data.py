import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
my_key = '07e6be11058f287f345016199616cd77'
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDb.db'
db.init_app(app)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    countryName = db.Column(db.String, unique = True, nullable = False)
    offName = db.Column(db.String)
    nativeName = db.Column(db.String)
    currenciesName = db.Column(db.String)
    curSymbol = db.Column(db.String)
    capital = db.Column(db.String, unique = True)
    region = db.Column(db.String)
    subregion = db.Column(db.String)
    language = db.Column(db.String)
    population = db.Column(db.Integer)
    area = db.Column(db.Integer)
    flags = db.Column(db.Integer)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('123.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    print(request.form)
    country_input = request.form['country']
    countryName = country_input.capitalize()

    if Country.query.filter_by(countryName = countryName).first() is None:
        url = 'https://restcountries.com/v3.1/name/' + country_input
        r = requests.get(url)

        if r.status_code == 404:
            return error()

        countData = r.json()[0]
        offName = countData['name']['official']
        nativeName = countData['name']['nativeName'][list(countData['name']['nativeName'].keys())[0]]['official']
        currenciesName = countData['currencies'][list(countData['currencies'].keys())[0]]['name']
        curSymbol = countData['currencies'][list(countData['currencies'].keys())[0]]['symbol']
        capital = countData['capital'][0]
        region = countData['region']
        subregion = countData['subregion']
        language = ', '.join(list(countData['languages'].values()))
        population = int(countData['population'])
        area = int(countData['area'])
        flags = countData['flags']['png']

        data = Country(countryName=countryName,
                       offName=offName,
                       nativeName=nativeName,
                       currenciesName=currenciesName,
                       curSymbol=curSymbol,
                       capital=capital,
                       region=region,
                       subregion=subregion,
                       language=language,
                       population=population,
                       area=area,
                       flags=flags)
        db.session.add(data)
        db.session.commit()

    else:
        v = Country.query.filter_by(countryName = countryName).first()
        offName = v.offName
        nativeName = v.nativeName
        currenciesName = v.currenciesName
        curSymbol = v.curSymbol
        capital = v.capital
        region = v.region
        subregion = v.subregion
        language = v.language
        population = v.population
        area = v.area
        flags = v.flags

    url1 = 'https://api.openweathermap.org/data/2.5/weather?q=' + capital + '&units=metric' + '&appid=' + my_key
    re = requests.get(url1)
    tempData = re.json()
    icon = tempData['weather'][0]['icon']
    urlPng = 'http://openweathermap.org/img/wn/' + icon + '@2x.png'
    weather = tempData['main']['temp']

    return render_template('result.html',
                           offName = offName,
                           nativeName = nativeName,
                           weather=weather,
                           flags = flags,
                           currenciesName = currenciesName,
                           curSymbol = curSymbol,
                           capital = capital,
                           subregion = subregion,
                           region =region,
                           language = language,
                           area = area,
                           population = population,
                           urlPng=urlPng)

if __name__ == '__main__':
    app.run(debug=True)
