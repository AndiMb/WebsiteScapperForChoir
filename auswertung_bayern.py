import csv
import configparser

# Read Config File
config = configparser.ConfigParser()
config.read('config.ini')
bundesland = config['General']['Bundesland']

datadir = config[bundesland]['datadir']

schooltyp_column=1
url_column=6
choirlinksnum_column=8

with open(datadir + '/schools.csv', 'r') as csvfile:
    schoolreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = next(schoolreader, None)

    schultypen=['Grund- u. Mittelschule',
                'Realschule',
                'Gymnasium']
    
    schultanzahl = {'Gesamt': 0,
                    'sonstigeSchulen': 0}
    
    schultanzahl_mitChor = {'Gesamt': 0,
                            'sonstigeSchulen': 0}
    
    schultanzahl_mitWebsite = {'Gesamt': 0,
                            'sonstigeSchulen': 0}
    
    for schultyp in schultypen:
        schultanzahl[schultyp] = 0
        schultanzahl_mitChor[schultyp] = 0
        schultanzahl_mitWebsite[schultyp] = 0

    for row in schoolreader:
        
        schultypStr = row[schooltyp_column]

        found = False
        schultanzahl['Gesamt'] += 1
        if int(row[choirlinksnum_column]) > 0:
            schultanzahl_mitChor['Gesamt'] += 1
        if len(row[url_column]) > 0:
            schultanzahl_mitWebsite['Gesamt'] += 1
        for schultyp in schultypen:
            if str(schultyp) in schultypStr:
                schultanzahl[schultyp] += 1
                if int(row[choirlinksnum_column]) > 0:
                    schultanzahl_mitChor[schultyp] += 1
                if len(row[url_column]) > 0:
                    schultanzahl_mitWebsite[schultyp] += 1
                found = True
        if not found: # sonstige Schule z.B. Förderschulen
            schultanzahl['sonstigeSchulen'] += 1
            if int(row[choirlinksnum_column]) > 0:
                schultanzahl_mitChor['sonstigeSchulen'] += 1
            if len(row[url_column]) > 0:
                schultanzahl_mitWebsite['sonstigeSchulen'] += 1


    print('Schulen', schultanzahl['Gesamt'],schultanzahl_mitWebsite['Gesamt'],schultanzahl_mitChor['Gesamt'])
    for schultyp in schultypen:
        print(schultyp.replace(" ",""), schultanzahl[schultyp],schultanzahl_mitWebsite[schultyp],schultanzahl_mitChor[schultyp])
    print('sonst.Schulen', schultanzahl['sonstigeSchulen'],schultanzahl_mitWebsite['sonstigeSchulen'],schultanzahl_mitChor['sonstigeSchulen'])
    print('\n\n\n')

    print(';Alle;Grund-u.Mittelschule;Realschule;Gymnasium')
    print('mitChor;'+str(schultanzahl_mitChor['Gesamt'])+';'+str(schultanzahl_mitChor['Grund- u. Mittelschule'])+';'+str(schultanzahl_mitChor['Realschule'])+';'+str(schultanzahl_mitChor['Gymnasium']))
    print('ohneChor;'+
          str(schultanzahl_mitWebsite['Gesamt']-schultanzahl_mitChor['Gesamt'])+';'+
          str(schultanzahl_mitWebsite['Grund- u. Mittelschule']-schultanzahl_mitChor['Grund- u. Mittelschule'])+';'+
          str(schultanzahl_mitWebsite['Realschule']-schultanzahl_mitChor['Realschule'])+';'+
          str(schultanzahl_mitWebsite['Gymnasium']-schultanzahl_mitChor['Gymnasium']))
    
    print(';Alle;Grund-u.Mittelschule;Realschule;Gymnasium')
    print('mit Chor;'+str(schultanzahl_mitChor['Gesamt'])+';'+str(schultanzahl_mitChor['Grund- u. Mittelschule'])+';'+str(schultanzahl_mitChor['Realschule'])+';'+str(schultanzahl_mitChor['Gymnasium']))
    print('ohne Chor;'+
          str(schultanzahl_mitWebsite['Gesamt']-schultanzahl_mitChor['Gesamt'])+';'+
          str(schultanzahl_mitWebsite['Grund- u. Mittelschule']-schultanzahl_mitChor['Grund- u. Mittelschule'])+';'+
          str(schultanzahl_mitWebsite['Realschule']-schultanzahl_mitChor['Realschule'])+';'+
          str(schultanzahl_mitWebsite['Gymnasium']-schultanzahl_mitChor['Gymnasium']))
    print('mit Website;'+
          str(schultanzahl_mitWebsite['Gesamt'])+';'+
          str(schultanzahl_mitWebsite['Grund- u. Mittelschule'])+';'+
          str(schultanzahl_mitWebsite['Realschule'])+';'+
          str(schultanzahl_mitWebsite['Gymnasium']))
    print('alle;'+
          str(schultanzahl['Gesamt'])+';'+
          str(schultanzahl['Grund- u. Mittelschule'])+';'+
          str(schultanzahl['Realschule'])+';'+
          str(schultanzahl['Gymnasium']))
    
    print(';Alle;Grund-u.Mittelschule;Realschule;Gymnasium')
    print('mitChor;'+
          str(schultanzahl_mitChor['Gesamt']/schultanzahl_mitWebsite['Gesamt'])+';'+
          str(schultanzahl_mitChor['Grund- u. Mittelschule']/schultanzahl_mitWebsite['Grund- u. Mittelschule'])+';'+
          str(schultanzahl_mitChor['Realschule']/schultanzahl_mitWebsite['Realschule'])+';'+
          str(schultanzahl_mitChor['Gymnasium']/schultanzahl_mitWebsite['Gymnasium']))
    print('ohneChor;'+
          str((schultanzahl_mitWebsite['Gesamt']-schultanzahl_mitChor['Gesamt'])/schultanzahl_mitWebsite['Gesamt'])+';'+
          str((schultanzahl_mitWebsite['Grund- u. Mittelschule']-schultanzahl_mitChor['Grund- u. Mittelschule'])/schultanzahl_mitWebsite['Grund- u. Mittelschule'])+';'+
          str((schultanzahl_mitWebsite['Realschule']-schultanzahl_mitChor['Realschule'])/schultanzahl_mitWebsite['Realschule'])+';'+
          str((schultanzahl_mitWebsite['Gymnasium']-schultanzahl_mitChor['Gymnasium'])/schultanzahl_mitWebsite['Gymnasium']))