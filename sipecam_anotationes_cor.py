import os
import psycopg2
from dotenv import load_dotenv
import requests
import uuid
from datetime import datetime
import json
import pysolr


load_dotenv()

dbname = os.getenv('POSTGRES_DB')
dbuser = os.getenv('POSTGRES_USER')
dbpass = os.getenv('POSTGRES_PASSWORD')
dbhost = os.getenv('POSTGRES_HOST')
dbport = os.getenv('POSTGRES_PORT')
mgdt_output = os.getenv('MGDT_OUTPUT')
threshold_score = float(os.getenv('THRESHOLD_SCORE'))
solr_url = os.getenv('SOLR_URL')

url_osm = 'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json'

ecosystems_d = {
    '1': 'Bosques templados',
    '2': 'Bosques mesofilos',
    '3': 'Selvas humedas',
    '4': 'Selvas secas',
    '5': 'Matorrales xerofilos',
    '6': 'Pastizales',
    '7': 'Manglar',
}
labels_d = {
    '1': 'animal', 
    '2': 'person', 
    '3': 'vehicle'
}

mgdt_output = json.loads(open(mgdt_output, 'r').read())['images']
mgdt_output = {item['file']:item for item in mgdt_output}

conn = psycopg2.connect(f'dbname={dbname} user={dbuser} password={dbpass} host={dbhost} port={dbport}')

sql = f'select file_id, longitude, latitude, node_name, filepath, cumulus_name, b.creation_date, b.last_modified \
from delivery.kobo_zendro_assoc as a \
left join delivery.file as b on a.file_id=b.id \
where b.extension_id in (3,6,10,11,12,24,25,26,27,32) and a.cumulus_name is not null and longitude is not null \
order by file_id limit 10'

cur = conn.cursor()
cur.execute(sql)
rows = cur.fetchall()
cur.close()
conn.close()

print(len(rows))

solr_sipecam = pysolr.Solr(f'{solr_url}/sipecam', always_commit=True)
solr_anotaciones = pysolr.Solr(f'{solr_url}/anotaciones', always_commit=True)

i = 1
for row in rows:
    print(i)
    i+=1
    url = url_osm.format(lat=row[2], lon=row[1])
    res_osm = requests.get(url, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'}).json()
    node_name_l = row[3].split('_')
    relative_path = row[4].replace('/LUSTRE/sacmod/audio/raw_media/entregas_sipecam/', '')
    
    if not 'address' in res_osm.keys():
        print(url_osm.format(lat=row[2], lon=row[1]))
        print('\n')
        continue

    if 'county' in res_osm['address'].keys():
        city_or_county = res_osm['address']['county']
    elif 'city' in res_osm['address'].keys():
        city_or_county = res_osm['address']['city']
    else:
        city_or_county = res_osm['address']['village']

    item_d = {
        'estado_str': res_osm['address']['state'],
        'estado':  res_osm['address']['state'],
        'integridad_nodo': 'Degradado' if node_name_l[2] == '0' else 'Integro',
        'ruta': relative_path,
        'ecosistema': ecosystems_d[node_name_l[0]],
        'ecosistema_str': ecosystems_d[node_name_l[0]],
        'municipio': city_or_county,
        'municipio_str': city_or_county,
        'nomenclatura_nodo': row[3],
        'coord_longitud': float(row[1]),
        'cumulo': row[5],
        'fecha_foto': row[6].strftime('%Y-%m-%d %H:%M:%S'),
        'coord_latitud': float(row[2]),
        'ultima_modificacion': row[7].strftime('%Y-%m-%d %H:%M:%S'),
        'id': str(row[0]),
        'labeled': False,
        'new_deliveries': True
    }
    solr_sipecam.add([item_d])
    #print(item_d)

    mgdt_results = mgdt_output[relative_path]
    #print(mgdt_results['detections'])
    for mgdt_result in mgdt_results['detections']:
        score = mgdt_result['conf'] * 100
        if score < threshold_score:
            continue
        item_d = {
            'id': str(uuid.uuid4()),
            'ftrampa_id': str(row[0]),
            'nivel_anotador': "algoritmo",
            'ultima_modificacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_anotacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'coleccion': 'sipecam',
            'modelo_id': 'megadetector_v5a',
            'anotador_id': 34,
            'probabilidad_modelo': score,
            'rect_x': str(mgdt_result['bbox'][0]),
            'rect_y': str(mgdt_result['bbox'][1]),
            'rect_width': str(mgdt_result['bbox'][2]),
            'rect_height': str(mgdt_result['bbox'][3]),
            'tipo_anotacion': 'especimen',
            'etiqueta': labels_d[mgdt_result['category']]
            ,
            'new_deliveries': True
        }
        solr_anotaciones.add([item_d])
        #print(item_d)
