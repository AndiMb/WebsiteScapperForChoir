import csv
import configparser

# Read Config File
config = configparser.ConfigParser()
config.read('config.ini')
bundesland = config['General']['Bundesland']

datadir = config[bundesland]['datadir']

with open(datadir + '/schools.csv', 'r') as csvfile:
    schoolreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = next(schoolreader, None)

    schultypen = ['Grundschule',
                  'Regelschule',
                  'Gymnasium',]
    
    schultanzahl = {'Gesamt': 0,
                    'Grundschule': 0,
                    'Regelschule': 0,
                    'Gymnasium': 0,
                    'sonstigeSchulen': 0}
    
    schultanzahl_mitChor = {'Gesamt': 0,
                            'Grundschule': 0,
                            'Regelschule': 0,
                            'Gymnasium': 0,
                            'sonstigeSchulen': 0}
    
    schultanzahl_mitWebsite = {'Gesamt': 0,
                            'Grundschule': 0,
                            'Regelschule': 0,
                            'Gymnasium': 0,
                            'sonstigeSchulen': 0}

    for row in schoolreader:
        
        schultypStr = row[4]

        found = False
        schultanzahl['Gesamt'] += 1
        if int(row[12]) > 0:
            schultanzahl_mitChor['Gesamt'] += 1
        if len(row[11]) > 0:
            schultanzahl_mitWebsite['Gesamt'] += 1
        for schultyp in schultypen:
            if str(schultyp) in schultypStr:
                schultanzahl[schultyp] += 1
                if int(row[12]) > 0:
                    schultanzahl_mitChor[schultyp] += 1
                if len(row[11]) > 0:
                    schultanzahl_mitWebsite[schultyp] += 1
                found = True
        if not found: # sonstige Schule z.B. Förderschulen
            schultanzahl['sonstigeSchulen'] += 1
            if int(row[12]) > 0:
                schultanzahl_mitChor['sonstigeSchulen'] += 1
            if len(row[11]) > 0:
                schultanzahl_mitWebsite['sonstigeSchulen'] += 1


    print('Schulen', schultanzahl['Gesamt'],schultanzahl_mitWebsite['Gesamt'],schultanzahl_mitChor['Gesamt'])
    for schultyp in schultypen:
        print(schultyp, schultanzahl[schultyp],schultanzahl_mitWebsite[schultyp],schultanzahl_mitChor[schultyp])
    print('sonst.Schulen', schultanzahl['sonstigeSchulen'],schultanzahl_mitWebsite['sonstigeSchulen'],schultanzahl_mitChor['sonstigeSchulen'])
    print('\n\n\n')

    print(';Alle;Grundschule;Regelschule;Gymnasium')
    print('mitChor;'+str(schultanzahl_mitChor['Gesamt'])+';'+str(schultanzahl_mitChor['Grundschule'])+';'+str(schultanzahl_mitChor['Regelschule'])+';'+str(schultanzahl_mitChor['Gymnasium']))
    print('ohneChor;'+
          str(schultanzahl_mitWebsite['Gesamt']-schultanzahl_mitChor['Gesamt'])+';'+
          str(schultanzahl_mitWebsite['Grundschule']-schultanzahl_mitChor['Grundschule'])+';'+
          str(schultanzahl_mitWebsite['Regelschule']-schultanzahl_mitChor['Regelschule'])+';'+
          str(schultanzahl_mitWebsite['Gymnasium']-schultanzahl_mitChor['Gymnasium']))
    
    print(';Alle;Grundschule;Regelschule;Gymnasium')
    print('mit Chor;'+str(schultanzahl_mitChor['Gesamt'])+';'+str(schultanzahl_mitChor['Grundschule'])+';'+str(schultanzahl_mitChor['Regelschule'])+';'+str(schultanzahl_mitChor['Gymnasium']))
    print('ohne Chor;'+
          str(schultanzahl_mitWebsite['Gesamt']-schultanzahl_mitChor['Gesamt'])+';'+
          str(schultanzahl_mitWebsite['Grundschule']-schultanzahl_mitChor['Grundschule'])+';'+
          str(schultanzahl_mitWebsite['Regelschule']-schultanzahl_mitChor['Regelschule'])+';'+
          str(schultanzahl_mitWebsite['Gymnasium']-schultanzahl_mitChor['Gymnasium']))
    print('mit Website;'+
          str(schultanzahl_mitWebsite['Gesamt'])+';'+
          str(schultanzahl_mitWebsite['Grundschule'])+';'+
          str(schultanzahl_mitWebsite['Regelschule'])+';'+
          str(schultanzahl_mitWebsite['Gymnasium']))
    print('alle;'+
          str(schultanzahl['Gesamt'])+';'+
          str(schultanzahl['Grundschule'])+';'+
          str(schultanzahl['Regelschule'])+';'+
          str(schultanzahl['Gymnasium']))
    
    print(';Alle;Grundschule;Regelschule;Gymnasium')
    print('mitChor;'+
          str(schultanzahl_mitChor['Gesamt']/schultanzahl_mitWebsite['Gesamt'])+';'+
          str(schultanzahl_mitChor['Grundschule']/schultanzahl_mitWebsite['Grundschule'])+';'+
          str(schultanzahl_mitChor['Regelschule']/schultanzahl_mitWebsite['Regelschule'])+';'+
          str(schultanzahl_mitChor['Gymnasium']/schultanzahl_mitWebsite['Gymnasium']))
    print('ohneChor;'+
          str((schultanzahl_mitWebsite['Gesamt']-schultanzahl_mitChor['Gesamt'])/schultanzahl_mitWebsite['Gesamt'])+';'+
          str((schultanzahl_mitWebsite['Grundschule']-schultanzahl_mitChor['Grundschule'])/schultanzahl_mitWebsite['Grundschule'])+';'+
          str((schultanzahl_mitWebsite['Regelschule']-schultanzahl_mitChor['Regelschule'])/schultanzahl_mitWebsite['Regelschule'])+';'+
          str((schultanzahl_mitWebsite['Gymnasium']-schultanzahl_mitChor['Gymnasium'])/schultanzahl_mitWebsite['Gymnasium']))