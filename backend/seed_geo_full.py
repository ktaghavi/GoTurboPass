from app import create_app
from models import db, County, Court


def seed_geo_full():
    app = create_app()
    with app.app_context():
        print('Seeding full CA counties and courts...')

        # Clear existing
        Court.query.delete()
        County.query.delete()
        db.session.commit()

        counties_by_name = {}

        # Alameda County
        county = County(state='CA', name='Alameda County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Alameda (George E. McDonald Hall of Justice)', dmv_code='01430', legacy_vendor_code='01430'))
        db.session.add(Court(county_id=county.id, name='Berkeley-Albany', dmv_code='01430', legacy_vendor_code='01430'))
        db.session.add(Court(county_id=county.id, name='Dublin (East County Hall of Justice)', dmv_code='01430', legacy_vendor_code='01430'))
        db.session.add(Court(county_id=county.id, name='Fremont Hall of Justice', dmv_code='01430', legacy_vendor_code='01430'))
        db.session.add(Court(county_id=county.id, name='Hayward Hall of Justice', dmv_code='01430', legacy_vendor_code='01430'))
        db.session.add(Court(county_id=county.id, name='Oakland (Wiley W. Manuel Courthouse)', dmv_code='01440', legacy_vendor_code='01440'))

        # Alpine County
        county = County(state='CA', name='Alpine County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Markleeville - Alpine', dmv_code='02100', legacy_vendor_code='02100'))

        # Amador County
        county = County(state='CA', name='Amador County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Jackson - Amador', dmv_code='03610', legacy_vendor_code='03610'))

        # Butte County
        county = County(state='CA', name='Butte County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Chico', dmv_code='04100', legacy_vendor_code='04100'))
        db.session.add(Court(county_id=county.id, name='Gridley', dmv_code='04100', legacy_vendor_code='04100'))
        db.session.add(Court(county_id=county.id, name='Oroville', dmv_code='04100', legacy_vendor_code='04100'))
        db.session.add(Court(county_id=county.id, name='Paradise', dmv_code='04100', legacy_vendor_code='04100'))

        # Calaveras County
        county = County(state='CA', name='Calaveras County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='San Andreas-Calaveras', dmv_code='05100', legacy_vendor_code='05100'))

        # Colusa County
        county = County(state='CA', name='Colusa County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Colusa', dmv_code='06620', legacy_vendor_code='06620'))

        # Contra Costa County
        county = County(state='CA', name='Contra Costa County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Concord', dmv_code='07480', legacy_vendor_code='07480'))
        db.session.add(Court(county_id=county.id, name='Pittsburg', dmv_code='07465', legacy_vendor_code='07465'))
        db.session.add(Court(county_id=county.id, name='Richmond', dmv_code='07460', legacy_vendor_code='07460'))
        db.session.add(Court(county_id=county.id, name='Walnut Creek-Danville', dmv_code='07480', legacy_vendor_code='07480'))

        # Del Norte County
        county = County(state='CA', name='Del Norte County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Crescent City-Del Norte', dmv_code='08100', legacy_vendor_code='08100'))

        # El Dorado County
        county = County(state='CA', name='El Dorado County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Cameron Park', dmv_code='09670', legacy_vendor_code='09670'))
        db.session.add(Court(county_id=county.id, name='Placerville', dmv_code='09670', legacy_vendor_code='09670'))
        db.session.add(Court(county_id=county.id, name='South Lake Tahoe', dmv_code='09660', legacy_vendor_code='09660'))

        # Fresno County
        county = County(state='CA', name='Fresno County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Clovis', dmv_code='10440', legacy_vendor_code='10440'))
        db.session.add(Court(county_id=county.id, name='Coalinga', dmv_code='10440', legacy_vendor_code='10440'))
        db.session.add(Court(county_id=county.id, name='Firebaugh', dmv_code='10440', legacy_vendor_code='10440'))
        db.session.add(Court(county_id=county.id, name='Fowler', dmv_code='10440', legacy_vendor_code='10440'))
        db.session.add(Court(county_id=county.id, name='Fresno', dmv_code='10440', legacy_vendor_code='10440'))
        db.session.add(Court(county_id=county.id, name='Kingsburg', dmv_code='10440', legacy_vendor_code='10440'))
        db.session.add(Court(county_id=county.id, name='Reedley', dmv_code='10440', legacy_vendor_code='10440'))
        db.session.add(Court(county_id=county.id, name='Sanger', dmv_code='10440', legacy_vendor_code='10440'))
        db.session.add(Court(county_id=county.id, name='Selma', dmv_code='10440', legacy_vendor_code='10440'))

        # Glenn County
        county = County(state='CA', name='Glenn County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Orland', dmv_code='11100', legacy_vendor_code='11100'))
        db.session.add(Court(county_id=county.id, name='Willows', dmv_code='11100', legacy_vendor_code='11100'))

        # Humboldt County
        county = County(state='CA', name='Humboldt County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Eureka', dmv_code='12100', legacy_vendor_code='12100'))
        db.session.add(Court(county_id=county.id, name='Garberville', dmv_code='12100', legacy_vendor_code='12100'))
        db.session.add(Court(county_id=county.id, name='Hoopa Tribal', dmv_code='12100', legacy_vendor_code='12100'))

        # Imperial County
        county = County(state='CA', name='Imperial County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Brawley', dmv_code='13420', legacy_vendor_code='13420'))
        db.session.add(Court(county_id=county.id, name='Calexico', dmv_code='13430', legacy_vendor_code='13430'))
        db.session.add(Court(county_id=county.id, name='El Centro', dmv_code='13440', legacy_vendor_code='13440'))
        db.session.add(Court(county_id=county.id, name='Winterhaven', dmv_code='13450', legacy_vendor_code='13450'))

        # Inyo County
        county = County(state='CA', name='Inyo County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Bishop', dmv_code='14660', legacy_vendor_code='14660'))
        db.session.add(Court(county_id=county.id, name='Independence', dmv_code='14660', legacy_vendor_code='14660'))

        # Kern County
        county = County(state='CA', name='Kern County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Arvin-Lamont (South Kern)', dmv_code='15410', legacy_vendor_code='15410'))
        db.session.add(Court(county_id=county.id, name='Bakersfield', dmv_code='15420', legacy_vendor_code='15420'))
        db.session.add(Court(county_id=county.id, name='Delano-McFarland (North Kern)', dmv_code='15430', legacy_vendor_code='15430'))
        db.session.add(Court(county_id=county.id, name='Kern River (East Kern)', dmv_code='15460', legacy_vendor_code='15460'))
        db.session.add(Court(county_id=county.id, name='Maricopa-Taft (South Kern)', dmv_code='15440', legacy_vendor_code='15440'))
        db.session.add(Court(county_id=county.id, name='Mojave (East Kern)', dmv_code='15460', legacy_vendor_code='15460'))
        db.session.add(Court(county_id=county.id, name='Ridgecrest (East Kern)', dmv_code='15470', legacy_vendor_code='15470'))
        db.session.add(Court(county_id=county.id, name='Shafter-Wasco (North Kern)', dmv_code='15445', legacy_vendor_code='15445'))

        # Kings County
        county = County(state='CA', name='Kings County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Avenal', dmv_code='16610', legacy_vendor_code='16610'))
        db.session.add(Court(county_id=county.id, name='Corcoran', dmv_code='16620', legacy_vendor_code='16620'))
        db.session.add(Court(county_id=county.id, name='Hanford', dmv_code='16420', legacy_vendor_code='16420'))
        db.session.add(Court(county_id=county.id, name='Lemoore', dmv_code='16660', legacy_vendor_code='16660'))

        # Lake County
        county = County(state='CA', name='Lake County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Clearlake', dmv_code='17610', legacy_vendor_code='17610'))
        db.session.add(Court(county_id=county.id, name='Lakeport', dmv_code='17100', legacy_vendor_code='17100'))

        # Lassen County
        county = County(state='CA', name='Lassen County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Susanville-Lassen', dmv_code='18675', legacy_vendor_code='18675'))

        # Los Angeles County
        county = County(state='CA', name='Los Angeles County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Airport', dmv_code='19405', legacy_vendor_code='19405'))
        db.session.add(Court(county_id=county.id, name='Alhambra', dmv_code='19410', legacy_vendor_code='19410'))
        db.session.add(Court(county_id=county.id, name='Bellflower', dmv_code='19466', legacy_vendor_code='19466'))
        db.session.add(Court(county_id=county.id, name='Beverly Hills', dmv_code='19420', legacy_vendor_code='19420'))
        db.session.add(Court(county_id=county.id, name='Burbank', dmv_code='19425', legacy_vendor_code='19425'))
        db.session.add(Court(county_id=county.id, name='Catalina', dmv_code='19610', legacy_vendor_code='19610'))
        db.session.add(Court(county_id=county.id, name='Chatsworth', dmv_code='19432', legacy_vendor_code='19432'))
        db.session.add(Court(county_id=county.id, name='Compton', dmv_code='19435', legacy_vendor_code='19435'))
        db.session.add(Court(county_id=county.id, name='Downey', dmv_code='19440', legacy_vendor_code='19440'))
        db.session.add(Court(county_id=county.id, name='East Los Angeles', dmv_code='19443', legacy_vendor_code='19443'))
        db.session.add(Court(county_id=county.id, name='El Monte', dmv_code='19446', legacy_vendor_code='19446'))
        db.session.add(Court(county_id=county.id, name='Glendale', dmv_code='19450', legacy_vendor_code='19450'))
        db.session.add(Court(county_id=county.id, name='Governor George Deukmejian Courthouse', dmv_code='19460', legacy_vendor_code='19460'))
        db.session.add(Court(county_id=county.id, name='Hollywood', dmv_code='19495', legacy_vendor_code='19495'))
        db.session.add(Court(county_id=county.id, name='Huntington Park', dmv_code='19480', legacy_vendor_code='19480'))
        db.session.add(Court(county_id=county.id, name='Inglewood', dmv_code='19455', legacy_vendor_code='19455'))
        db.session.add(Court(county_id=county.id, name='Lancaster (Michael Antonovich Antelope Valley)', dmv_code='19413', legacy_vendor_code='19413'))
        db.session.add(Court(county_id=county.id, name='Long Beach', dmv_code='19460', legacy_vendor_code='19460'))
        db.session.add(Court(county_id=county.id, name='Los Angeles (1945 S. Hill St)', dmv_code='19463', legacy_vendor_code='19463'))
        db.session.add(Court(county_id=county.id, name='Malibu', dmv_code='19472', legacy_vendor_code='19472'))
        db.session.add(Court(county_id=county.id, name='Metropolitan', dmv_code='19463', legacy_vendor_code='19463'))
        db.session.add(Court(county_id=county.id, name='Michael Antonovich Antelope Valley Courthouse', dmv_code='19413', legacy_vendor_code='19413'))
        db.session.add(Court(county_id=county.id, name='Pasadena', dmv_code='19470', legacy_vendor_code='19470'))
        db.session.add(Court(county_id=county.id, name='Pomona', dmv_code='19475', legacy_vendor_code='19475'))
        db.session.add(Court(county_id=county.id, name='San Fernando', dmv_code='19496', legacy_vendor_code='19496'))
        db.session.add(Court(county_id=county.id, name='San Pedro', dmv_code='19497', legacy_vendor_code='19497'))
        db.session.add(Court(county_id=county.id, name='Santa Clarita', dmv_code='19468', legacy_vendor_code='19468'))
        db.session.add(Court(county_id=county.id, name='Santa Monica', dmv_code='19484', legacy_vendor_code='19484'))
        db.session.add(Court(county_id=county.id, name='Torrance', dmv_code='19486', legacy_vendor_code='19486'))
        db.session.add(Court(county_id=county.id, name='Van Nuys', dmv_code='19498', legacy_vendor_code='19498'))
        db.session.add(Court(county_id=county.id, name='West Covina', dmv_code='19430', legacy_vendor_code='19430'))
        db.session.add(Court(county_id=county.id, name='West Los Angeles', dmv_code='19499', legacy_vendor_code='19499'))
        db.session.add(Court(county_id=county.id, name='Whittier', dmv_code='19490', legacy_vendor_code='19490'))

        # Madera County
        county = County(state='CA', name='Madera County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Borden', dmv_code='20640', legacy_vendor_code='20640'))
        db.session.add(Court(county_id=county.id, name='Chowchilla', dmv_code='20100', legacy_vendor_code='20100'))
        db.session.add(Court(county_id=county.id, name='Madera', dmv_code='20100', legacy_vendor_code='20100'))
        db.session.add(Court(county_id=county.id, name='Madera Traffic Division', dmv_code='20620', legacy_vendor_code='20620'))
        db.session.add(Court(county_id=county.id, name='Sierra', dmv_code='20680', legacy_vendor_code='20680'))

        # Marin County
        county = County(state='CA', name='Marin County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Marin-San Rafael', dmv_code='21420', legacy_vendor_code='21420'))

        # Mariposa County
        county = County(state='CA', name='Mariposa County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Mariposa', dmv_code='22650', legacy_vendor_code='22650'))

        # Mendocino County
        county = County(state='CA', name='Mendocino County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Boonville-Anderson', dmv_code='23480', legacy_vendor_code='23480'))
        db.session.add(Court(county_id=county.id, name='Covelo-Round Valley', dmv_code='23480', legacy_vendor_code='23480'))
        db.session.add(Court(county_id=county.id, name='Fort Bragg-Ten Mile', dmv_code='23480', legacy_vendor_code='23480'))
        db.session.add(Court(county_id=county.id, name='Leggett-Long Valley', dmv_code='23480', legacy_vendor_code='23480'))
        db.session.add(Court(county_id=county.id, name='Point Arena', dmv_code='23480', legacy_vendor_code='23480'))
        db.session.add(Court(county_id=county.id, name='Ukiah', dmv_code='23480', legacy_vendor_code='23480'))
        db.session.add(Court(county_id=county.id, name='Willits', dmv_code='23480', legacy_vendor_code='23480'))

        # Merced County
        county = County(state='CA', name='Merced County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Dos Palos', dmv_code='24400', legacy_vendor_code='24400'))
        db.session.add(Court(county_id=county.id, name='Gustine', dmv_code='24400', legacy_vendor_code='24400'))
        db.session.add(Court(county_id=county.id, name='Los Banos', dmv_code='24400', legacy_vendor_code='24400'))
        db.session.add(Court(county_id=county.id, name='Merced', dmv_code='24400', legacy_vendor_code='24400'))

        # Modoc County
        county = County(state='CA', name='Modoc County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Alturas-Modoc', dmv_code='25100', legacy_vendor_code='25100'))

        # Mono County
        county = County(state='CA', name='Mono County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Bridgeport (North County)', dmv_code='26660', legacy_vendor_code='26660'))
        db.session.add(Court(county_id=county.id, name='Mammoth Lakes (South County)', dmv_code='26660', legacy_vendor_code='26660'))

        # Monterey County
        county = County(state='CA', name='Monterey County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='King City', dmv_code='27450', legacy_vendor_code='27450'))
        db.session.add(Court(county_id=county.id, name='Marina', dmv_code='27450', legacy_vendor_code='27450'))
        db.session.add(Court(county_id=county.id, name='Monterey', dmv_code='27450', legacy_vendor_code='27450'))
        db.session.add(Court(county_id=county.id, name='Salinas', dmv_code='27450', legacy_vendor_code='27450'))

        # Napa County
        county = County(state='CA', name='Napa County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Napa', dmv_code='28100', legacy_vendor_code='28100'))

        # Nevada County
        county = County(state='CA', name='Nevada County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Nevada City', dmv_code='29460', legacy_vendor_code='29460'))
        db.session.add(Court(county_id=county.id, name='Truckee', dmv_code='29480', legacy_vendor_code='29480'))

        # Orange County
        county = County(state='CA', name='Orange County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Central Justice Center - Santa Ana', dmv_code='30470', legacy_vendor_code='30470'))
        db.session.add(Court(county_id=county.id, name='Harbor Justice Center - Newport Beach', dmv_code='30470', legacy_vendor_code='30470'))
        db.session.add(Court(county_id=county.id, name='Laguna Hills', dmv_code='30470', legacy_vendor_code='30470'))
        db.session.add(Court(county_id=county.id, name='Laguna Niguel', dmv_code='30470', legacy_vendor_code='30470'))
        db.session.add(Court(county_id=county.id, name='Lamoreaux Justice Center - Orange', dmv_code='30470', legacy_vendor_code='30470'))
        db.session.add(Court(county_id=county.id, name='North Justice Center - Fullerton', dmv_code='30470', legacy_vendor_code='30470'))
        db.session.add(Court(county_id=county.id, name='West Justice Center - Westminster', dmv_code='30470', legacy_vendor_code='30470'))

        # Placer County
        county = County(state='CA', name='Placer County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Auburn', dmv_code='31455', legacy_vendor_code='31455'))
        db.session.add(Court(county_id=county.id, name='Foresthill', dmv_code='31455', legacy_vendor_code='31455'))
        db.session.add(Court(county_id=county.id, name='Lincoln', dmv_code='31455', legacy_vendor_code='31455'))
        db.session.add(Court(county_id=county.id, name='Roseville', dmv_code='31455', legacy_vendor_code='31455'))
        db.session.add(Court(county_id=county.id, name='Tahoe City', dmv_code='31455', legacy_vendor_code='31455'))

        # Plumas County
        county = County(state='CA', name='Plumas County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Chester', dmv_code='32100', legacy_vendor_code='32100'))
        db.session.add(Court(county_id=county.id, name='Greenville', dmv_code='32100', legacy_vendor_code='32100'))
        db.session.add(Court(county_id=county.id, name='Portola', dmv_code='32100', legacy_vendor_code='32100'))
        db.session.add(Court(county_id=county.id, name='Quincy', dmv_code='32100', legacy_vendor_code='32100'))

        # Riverside County
        county = County(state='CA', name='Riverside County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Banning', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Blythe', dmv_code='33450', legacy_vendor_code='33450'))
        db.session.add(Court(county_id=county.id, name='Corona', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Hemet', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Indio - Larson Justice', dmv_code='33450', legacy_vendor_code='33450'))
        db.session.add(Court(county_id=county.id, name='Lake Elsinore', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Moreno Valley', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Murrieta - Southwest Justice', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Palm Springs', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Perris', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Riverside', dmv_code='33460', legacy_vendor_code='33460'))
        db.session.add(Court(county_id=county.id, name='Temecula', dmv_code='33460', legacy_vendor_code='33460'))

        # Sacramento County
        county = County(state='CA', name='Sacramento County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Elk Grove-South Sacramento', dmv_code='34470', legacy_vendor_code='34470'))
        db.session.add(Court(county_id=county.id, name='Galt', dmv_code='34470', legacy_vendor_code='34470'))
        db.session.add(Court(county_id=county.id, name='Sacramento - Carol Miller Justice', dmv_code='34470', legacy_vendor_code='34470'))
        db.session.add(Court(county_id=county.id, name='Sacramento County Superior Court', dmv_code='34470', legacy_vendor_code='34470'))
        db.session.add(Court(county_id=county.id, name='Walnut Grove-Iselton', dmv_code='34470', legacy_vendor_code='34470'))

        # San Benito County
        county = County(state='CA', name='San Benito County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Hollister - San Benito', dmv_code='35100', legacy_vendor_code='35100'))

        # San Bernardino County
        county = County(state='CA', name='San Bernardino County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Barstow', dmv_code='36130', legacy_vendor_code='36130'))
        db.session.add(Court(county_id=county.id, name='Big Bear Lake', dmv_code='36120', legacy_vendor_code='36120'))
        db.session.add(Court(county_id=county.id, name='Chino', dmv_code='36100', legacy_vendor_code='36100'))
        db.session.add(Court(county_id=county.id, name='Fontana (Valley)', dmv_code='36480', legacy_vendor_code='36480'))
        db.session.add(Court(county_id=county.id, name='Joshua Tree (Morongo Basin)', dmv_code='36140', legacy_vendor_code='36140'))
        db.session.add(Court(county_id=county.id, name='Needles', dmv_code='36660', legacy_vendor_code='36660'))
        db.session.add(Court(county_id=county.id, name='Rancho Cucamonga (West Valley)', dmv_code='36110', legacy_vendor_code='36110'))
        db.session.add(Court(county_id=county.id, name='Redlands (East)', dmv_code='36110', legacy_vendor_code='36110'))
        db.session.add(Court(county_id=county.id, name='San Bernardino (Central)', dmv_code='36100', legacy_vendor_code='36100'))
        db.session.add(Court(county_id=county.id, name='Twin Peaks', dmv_code='36100', legacy_vendor_code='36100'))
        db.session.add(Court(county_id=county.id, name='Victorville', dmv_code='36120', legacy_vendor_code='36120'))

        # San Diego County
        county = County(state='CA', name='San Diego County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Central Division', dmv_code='37480', legacy_vendor_code='37480'))
        db.session.add(Court(county_id=county.id, name='Chula Vista (South County)', dmv_code='37485', legacy_vendor_code='37485'))
        db.session.add(Court(county_id=county.id, name='East County Division', dmv_code='37440', legacy_vendor_code='37440'))
        db.session.add(Court(county_id=county.id, name='El Cajon', dmv_code='37440', legacy_vendor_code='37440'))
        db.session.add(Court(county_id=county.id, name='Escondido', dmv_code='37465', legacy_vendor_code='37465'))
        db.session.add(Court(county_id=county.id, name='Kearny Mesa Branch-Clairemont Mesa', dmv_code='37480', legacy_vendor_code='37480'))
        db.session.add(Court(county_id=county.id, name='North County', dmv_code='37465', legacy_vendor_code='37465'))
        db.session.add(Court(county_id=county.id, name='Ramona Branch', dmv_code='37480', legacy_vendor_code='37480'))
        db.session.add(Court(county_id=county.id, name='San Diego', dmv_code='37480', legacy_vendor_code='37480'))
        db.session.add(Court(county_id=county.id, name='San Marcos', dmv_code='37465', legacy_vendor_code='37465'))
        db.session.add(Court(county_id=county.id, name='Vista', dmv_code='37465', legacy_vendor_code='37465'))

        # San Francisco County
        county = County(state='CA', name='San Francisco County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='San Francisco', dmv_code='38460', legacy_vendor_code='38460'))

        # San Joaquin County
        county = County(state='CA', name='San Joaquin County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Lodi', dmv_code='39460', legacy_vendor_code='39460'))
        db.session.add(Court(county_id=county.id, name='Manteca', dmv_code='39460', legacy_vendor_code='39460'))
        db.session.add(Court(county_id=county.id, name='Stockton', dmv_code='39460', legacy_vendor_code='39460'))
        db.session.add(Court(county_id=county.id, name='Tracy', dmv_code='39460', legacy_vendor_code='39460'))

        # San Luis Obispo County
        county = County(state='CA', name='San Luis Obispo County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Grover Beach', dmv_code='40410', legacy_vendor_code='40410'))
        db.session.add(Court(county_id=county.id, name='Paso Robles', dmv_code='40410', legacy_vendor_code='40410'))
        db.session.add(Court(county_id=county.id, name='San Luis Obispo', dmv_code='40410', legacy_vendor_code='40410'))

        # San Mateo County
        county = County(state='CA', name='San Mateo County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='San Mateo-All Court Branches (Central Northern and Southern)', dmv_code='41470', legacy_vendor_code='41470'))

        # Santa Barbara County
        county = County(state='CA', name='Santa Barbara County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Figueroa Division', dmv_code='42460', legacy_vendor_code='42460'))
        db.session.add(Court(county_id=county.id, name='Lompoc', dmv_code='42470', legacy_vendor_code='42470'))
        db.session.add(Court(county_id=county.id, name='Santa Barbara', dmv_code='42460', legacy_vendor_code='42460'))
        db.session.add(Court(county_id=county.id, name='Santa Maria - Miller Division', dmv_code='42465', legacy_vendor_code='42465'))
        db.session.add(Court(county_id=county.id, name='Solvang', dmv_code='42675', legacy_vendor_code='42675'))

        # Santa Clara County
        county = County(state='CA', name='Santa Clara County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Morgan Hill (South County)', dmv_code='43471', legacy_vendor_code='43471'))
        db.session.add(Court(county_id=county.id, name='Palo Alto', dmv_code='43471', legacy_vendor_code='43471'))
        db.session.add(Court(county_id=county.id, name='San Jose', dmv_code='43471', legacy_vendor_code='43471'))
        db.session.add(Court(county_id=county.id, name='Santa Clara', dmv_code='43471', legacy_vendor_code='43471'))
        db.session.add(Court(county_id=county.id, name='Sunnyvale', dmv_code='43471', legacy_vendor_code='43471'))

        # Santa Cruz County
        county = County(state='CA', name='Santa Cruz County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Santa Cruz', dmv_code='44460', legacy_vendor_code='44460'))
        db.session.add(Court(county_id=county.id, name='Watsonville', dmv_code='44460', legacy_vendor_code='44460'))

        # Shasta County
        county = County(state='CA', name='Shasta County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Burney', dmv_code='45670', legacy_vendor_code='45670'))
        db.session.add(Court(county_id=county.id, name='Redding-Shasta', dmv_code='45670', legacy_vendor_code='45670'))

        # Sierra County
        county = County(state='CA', name='Sierra County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Downieville-Sierra', dmv_code='46100', legacy_vendor_code='46100'))

        # Siskiyou County
        county = County(state='CA', name='Siskiyou County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Dorris', dmv_code='47630', legacy_vendor_code='47630'))
        db.session.add(Court(county_id=county.id, name='Happy Camp', dmv_code='47650', legacy_vendor_code='47650'))
        db.session.add(Court(county_id=county.id, name='Weed', dmv_code='47670', legacy_vendor_code='47670'))
        db.session.add(Court(county_id=county.id, name='Yreka', dmv_code='47690', legacy_vendor_code='47690'))

        # Solano County
        county = County(state='CA', name='Solano County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Fairfield', dmv_code='48430', legacy_vendor_code='48430'))
        db.session.add(Court(county_id=county.id, name='Vallejo-Benicia', dmv_code='48480', legacy_vendor_code='48480'))

        # Sonoma County
        county = County(state='CA', name='Sonoma County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Santa Rosa', dmv_code='49460', legacy_vendor_code='49460'))
        db.session.add(Court(county_id=county.id, name='Sonoma', dmv_code='49100', legacy_vendor_code='49100'))

        # Stanislaus County
        county = County(state='CA', name='Stanislaus County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Modesto', dmv_code='50450', legacy_vendor_code='50450'))
        db.session.add(Court(county_id=county.id, name='Turlock', dmv_code='50450', legacy_vendor_code='50450'))

        # Sutter County
        county = County(state='CA', name='Sutter County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Yuba City - Sutter', dmv_code='51460', legacy_vendor_code='51460'))

        # Tehama County
        county = County(state='CA', name='Tehama County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Corning', dmv_code='52660', legacy_vendor_code='52660'))
        db.session.add(Court(county_id=county.id, name='Red Bluff', dmv_code='52660', legacy_vendor_code='52660'))

        # Trinity County
        county = County(state='CA', name='Trinity County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Weaverville - Trinity', dmv_code='53100', legacy_vendor_code='53100'))

        # Tulare County
        county = County(state='CA', name='Tulare County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Dinuba', dmv_code='54490', legacy_vendor_code='54490'))
        db.session.add(Court(county_id=county.id, name='Pixley', dmv_code='54485', legacy_vendor_code='54485'))
        db.session.add(Court(county_id=county.id, name='Porterville', dmv_code='54465', legacy_vendor_code='54465'))
        db.session.add(Court(county_id=county.id, name='Tulare', dmv_code='54490', legacy_vendor_code='54490'))
        db.session.add(Court(county_id=county.id, name='Visalia', dmv_code='54490', legacy_vendor_code='54490'))

        # Tuolumne County
        county = County(state='CA', name='Tuolumne County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Sonora - Tuolumne', dmv_code='55100', legacy_vendor_code='55100'))

        # Ventura County
        county = County(state='CA', name='Ventura County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Simi Valley', dmv_code='56100', legacy_vendor_code='56100'))
        db.session.add(Court(county_id=county.id, name='Ventura', dmv_code='56100', legacy_vendor_code='56100'))

        # Yolo County
        county = County(state='CA', name='Yolo County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Woodland', dmv_code='57420', legacy_vendor_code='57420'))
        db.session.add(Court(county_id=county.id, name='Yolo', dmv_code='57420', legacy_vendor_code='57420'))

        # Yuba County
        county = County(state='CA', name='Yuba County', dmv_code=None, legacy_vendor_code=None)
        db.session.add(county)
        db.session.flush()
        counties_by_name[county.name] = county
        db.session.add(Court(county_id=county.id, name='Marysville - Yuba', dmv_code='58100', legacy_vendor_code='58100'))

        db.session.commit()
        print('Done. Seeded:')
        print('  - Counties:', County.query.count())
        print('  - Courts:', Court.query.count())


if __name__ == '__main__':
    seed_geo_full()
