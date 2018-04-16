# -*- coding: utf-8 -*-

import json
import locale
import requests
from datetime import datetime
from calendar import TimeEncoding, month_name

url = "http://bibliotecadigital.planejamento.gov.br/rest"
login_header = {'Content-Type': 'application/x-www-form-urlencoded'}
login_url = url + "/login"


def get_month_name(month_no, locale):
    with TimeEncoding(locale) as encoding:
        s = month_name[month_no]
        if encoding is not None:
            s = s.decode(encoding)
        return s

# print get_month_name(3, "nb_NO.UTF-8")

def upload_panmacro(email, password, filename):
    locale.setlocale(locale.LC_ALL, 'pt_BR')

    #login_data = {'email':'alex.pereira@planejamento.gov.br', 'password':'@Lex2017'}
    login_data = {'email': email, 'password': password}
    r = requests.post(login_url, data=login_data, headers=login_header)
    print r.status_code

    headers = {'Content-type': 'application/xml', 'Accept': 'application/json'}
    date = datetime.today() #'2018-04-01'
    ##mes = get_month_name(date.strftime("%m"), "pt_BR.UTF-8")  #u'Março'
    mes = date.strftime("%B")
    ano = date.strftime("%Y")
    mes_ano = u'{0}/{1}'.format(mes,ano)

    data=u'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?> <item> 
       <metadata> <key>dc.contributor.author</key> <value>Brasil. Ministério do Planejamento, Desenvolvimento e Gestão (MP).</value> <language>pt_BR</language> </metadata> 
       <metadata> <key>dc.subject</key> <value>Economia</value> <language>pt_BR</language> </metadata> 
       <metadata> <key>dc.description.abstract</key> <value>Variáveis Macroeconomicas do mês de {0} de {1}</value> <language>pt_BR</language> </metadata> 
       <metadata> <key>dc.title</key> <value>Pan Macro de {2}</value> <language>pt_BR</language> </metadata> 
       <metadata> <key>dc.date.issued</key> <value>{3}</value> <language>pt_BR</language> </metadata>
       <metadata> <key>dc.type</key> <value>Apresentação</value> <language>pt_BR</language> </metadata> 
       <metadata> <key>dc.rights</key> <value>Isento de Licenciamento</value> <language>pt_BR</language> </metadata> 
       <metadata> <key>dc.language.iso</key> <value>Português (Brasil)</value> <language>pt_BR</language> </metadata> </item>'''.format(mes, ano, mes_ano, date)

    post_item_url = url + '/collections/{0}/items'.format("514baa86-9334-40aa-9e62-7279f09b84a9")
    r2 = requests.post(post_item_url, data=data.encode('utf-8'), headers=headers, cookies=r.cookies)
    print r2.status_code
    json_data = r2.json()
    upload_url = url + '/items/{0}/bitstreams'.format(json_data['uuid'])
    upload_header = {'Accept': 'application/xml'}

    with open(filename, 'rb') as f:
        r3 = requests.post(upload_url, files={filename: f}, headers=upload_header, cookies=r.cookies)

    print r3
    # curl -v -X POST --data "email=admin@dspace.org&password=mypass" https://dspace.myu.edu/rest/login
    # curl -k -4 --silent --cookie "JSESSIONID=AF457CA04FBB62C1167D384AEAEF46EF"
    # -H "accept: application/xml" -H "Content-Type: application/xml"
    # -X POST http://bibliotecadigital.planejamento.gov.br/rest/collections/514baa86-9334-40aa-9e62-7279f09b84a9/items
