# -*- coding: utf-8 -*-
import re
import urlparse

VCARD_TYPE = 'vcard'
SCHEMA_DOT_ORG_TYPE = 'schema.org'
RDFA_TYPE = 'rdfa'
ADDRESS_ELEMENT_TYPE = 'address'
GOOGLE_MAP_EMBED_TYPE = 'gmap'
GOOGLE_MAP_SHORTENED = 'gmap_short'
GEOTAG_TYPE = 'geotag'
OG_TAG_TYPE = 'og'
OG_BUSINESS_TAG_TYPE = 'og_business'
DATA_LATLON_TYPE = 'data_latlon'

HOPSTOP_MAP_TYPE = 'hopstop.map'
HOPSTOP_ROUTE_TYPE = 'hopstop.route'

MAPPOINT_EMBED_TYPE = 'mappoint.embed'

property_values = {
    'meta': 'content',
    'audio': 'src',
    'embed': 'src',
    'iframe': 'src',
    'img': 'src',
    'source': 'src',
    'video': 'src',
    'a': 'href',
    'area': 'href',
    'link': 'href',
    'object': 'data',
    'time': 'datetime',
}

br_regex = re.compile('<[\s]*br[\s]*/?[\s]*>', re.I)


def br2nl(text):
    return br_regex.sub('\n', text)

latlon_splitter = re.compile('[\s]*;[\s]*')
latlon_comma_splitter = re.compile('[\s]*,[\s]*')

street_props = set(['street_address', 'street', 'address', 'street-address', 'streetaddress'])
latitude_props = set(['latitude', 'lat'])
longitude_props = set(['longitude', 'lon', 'lng', 'long'])
latlon_props = latitude_props | longitude_props

UNINTERESTING_PLACE_TYPES = set(s.lower() for s in [
    'Airport',
    'Airline',
    'AutoRepair',
    'ApartmentComplex',
    'Residence',
    'City',
    'SingleFamilyResidence',
    'Country',
    'SelfStorage',
    'RealEstateAgent',
    'State',
    'AdministrativeArea',
    'Continent',
])

PLACE_SCHEMA_TYPES = dict([(s.lower(), s) for s in [
    'Organization',
    'Corporation',
    'EducationalOrganization',
    'GovernmentOrganization',
    'NGO',
    'PerformingGroup',
    'SportsOrganization',
    'Place',
    'AdministrativeArea',
    'City',
    'Country',
    'State',
    'CivicStructure',
    'Airport',
    'Aquarium',
    'Beach',
    'BusStation',
    'BusStop',
    'Campground',
    'Cemetery',
    'Crematorium',
    'EventVenue',
    'FireStation',
    'GovernmentBuilding',
    'CityHall',
    'Courthouse',
    'DefenceEstablishment',
    'Embassy',
    'LegislativeBuilding',
    'Hospital',
    'MovieTheater',
    'Museum',
    'MusicVenue',
    'Park',
    'ParkingFacility',
    'PerformingArtsTheater',
    'PlaceOfWorship',
    'BuddhistTemple',
    'CatholicChurch',
    'Church',
    'HinduTemple',
    'Mosque',
    'Synagogue',
    'Playground',
    'PoliceStation',
    'RVPark',
    'StadiumOrArena',
    'SubwayStation',
    'TaxiStand',
    'TrainStation',
    'Zoo',
    'Landform',
    'BodyOfWater',
    'Canal',
    'LakeBodyOfWater',
    'OceanBodyOfWater',
    'Pond',
    'Reservoir',
    'RiverBodyOfWater',
    'SeaBodyOfWater',
    'Waterfall',
    'Continent',
    'Mountain',
    'Volcano',
    'LandmarksOrHistoricalBuildings',
    'LocalBusiness',
    'AnimalShelter',
    'AutomotiveBusiness',
    'AutoBodyShop',
    'AutoDealer',
    'AutoPartsStore',
    'AutoRental',
    'AutoRepair',
    'AutoWash',
    'GasStation',
    'MotorcycleDealer',
    'MotorcycleRepair',
    'ChildCare',
    'DryCleaningOrLaundry',
    'EmergencyService',
    'FireStation',
    'Hospital',
    'PoliceStation',
    'EmploymentAgency',
    'EntertainmentBusiness',
    'AdultEntertainment',
    'AmusementPark',
    'ArtGallery',
    'Casino',
    'ComedyClub',
    'MovieTheater',
    'NightClub',
    'FinancialService',
    'AccountingService',
    'AutomatedTeller',
    'BankOrCreditUnion',
    'InsuranceAgency',
    'FoodEstablishment',
    'Bakery',
    'BarOrPub',
    'Brewery',
    'CafeOrCoffeeShop',
    'FastFoodRestaurant',
    'IceCreamShop',
    'Restaurant',
    'Winery',
    'GovernmentOffice',
    'PostOffice',
    'HealthAndBeautyBusiness',
    'BeautySalon',
    'DaySpa',
    'HairSalon',
    'HealthClub',
    'NailSalon',
    'TattooParlor',
    'HomeAndConstructionBusiness',
    'Electrician',
    'GeneralContractor',
    'HVACBusiness',
    'HousePainter',
    'Locksmith',
    'MovingCompany',
    'Plumber',
    'RoofingContractor',
    'InternetCafe',
    'Library',
    'LodgingBusiness',
    'BedAndBreakfast',
    'Hostel',
    'Hotel',
    'Motel',
    'MedicalOrganization',
    'Dentist',
    'DiagnosticLab',
    'Hospital',
    'MedicalClinic',
    'Optician',
    'Pharmacy',
    'Physician',
    'VeterinaryCare',
    'ProfessionalService',
    'AccountingService',
    'Attorney',
    'Dentist',
    'Electrician',
    'GeneralContractor',
    'HousePainter',
    'Locksmith',
    'Notary',
    'Plumber',
    'RoofingContractor',
    'RadioStation',
    'RealEstateAgent',
    'RecyclingCenter',
    'SelfStorage',
    'ShoppingCenter',
    'SportsActivityLocation',
    'BowlingAlley',
    'ExerciseGym',
    'GolfCourse',
    'HealthClub',
    'PublicSwimmingPool',
    'SkiResort',
    'SportsClub',
    'StadiumOrArena',
    'TennisComplex',
    'Store',
    'AutoPartsStore',
    'BikeStore',
    'BookStore',
    'ClothingStore',
    'ComputerStore',
    'ConvenienceStore',
    'DepartmentStore',
    'ElectronicsStore',
    'Florist',
    'FurnitureStore',
    'GardenStore',
    'GroceryStore',
    'HardwareStore',
    'HobbyShop',
    'HomeGoodsStore',
    'JewelryStore',
    'LiquorStore',
    'MensClothingStore',
    'MobilePhoneStore',
    'MovieRentalStore',
    'MusicStore',
    'OfficeEquipmentStore',
    'OutletStore',
    'PawnShop',
    'PetStore',
    'ShoeStore',
    'SportingGoodsStore',
    'TireShop',
    'ToyStore',
    'WholesaleStore',
    'TelevisionStation',
    'TouristInformationCenter',
    'TravelAgency',
    'Residence',
    'ApartmentComplex',
    'GatedResidenceCommunity',
    'SingleFamilyResidence',
    'TouristAttraction',
]])


OG_PLACE_TYPES = set([
    'hotel',
    'company',
    'landmark',
    'place',
    'restaurant',
    'university',
    'non_profit',
    'spot',
    'business.business',
    'bar',
    'school',
    'business',
    'museum',
    'venue',
    'cafe',
    'food store',
    'restaurant.restaurant',
    'location',
    'retail',
    'cinema',
    'salon',
    'cine',
    'destination',
    'chamber of commerce',
    'sight',
    'disco',
    'tapas',
    'club',
    'resort',
    'bares de copas y pubs',
    'businesses',
    'store',
    'accommodations',
    'theater',
    'restaurantes tradicionales',
    'sights',
    'bares',
    'centros comerciales',
    'restaurantes italianos',
    u'cocina mediterránea',
    'theatre',
    u'librerías',
    'park',
    u'asadores y braserías',
    'destinations',
    u'jugueterías',
    'lounge',
    'worship',
    u'zapaterías',
    'hotel/restaurant',
    'nonprofit',
    'discotecas',
    'taxis',
    'churches-places-of-worship',
    'rite-aid',
    u'cafeterías',
    'cocina de mercado',
    'banquet-halls-reception-facilities',
    u'pizzerías',
    'restaurantes vascos',
    'gimnasios',
    'motels',
    'concert_hall',
    'restaurantes  cocina casera',
    u'marisquerías',
    'car-rental',
    'clubs',
    'animal-shelters',
    'police-departments',
    'veterinarians',
    'liquor-stores',
    'beauty shop',
    'police-station',
    'grocery-stores',
    'tiendas de deporte',
    'company.website',
    u'peluquerías',
    'doctor',
    'pharmacies',
    'restaurantes andaluces',
    'government-offices',
    'movie-theaters',
    'centros culturales',
    u'joyerías',
    u'alimentación',
    u'hamburgueserías',
    'churches-interdenominational',
    'comida para llevar',
    'destinazioni',
    'baptist-churches',
    'churches',
    'churches-baptist-general',
    'plumbers',
    'campgrounds-recreational-vehicle-parks',
    u'tiendas de decoración',
    'places',
    'comfort-inn',
    'restaurantes vegetarianos',
    'fire-departments',
    'sheriff-department',
    'martial-arts-instruction',
    'tiendas de muebles',
    'nightlife',
    'catholic-churches',
    'religious-organizations',
    'skiresort',
    'churches-lutheran',
    u'restaurantes de cocina española',
    'walmart-supercenter',
    'truck-rental',
    'conv_center',
    'nail-salons',
    'hair-salons',
    'churches-baptist',
    'florist',
    'churches-pentecostal',
    'lodging',
    'library',
    'banks',
    'concerthall',
    'churches-catholic',
    'parks',
    'churches-roman-catholic',
    'tiendas de antiguedades',
    'sightseeing',
    'shopping center',
    'restaurantes',
    'historical_site',
    u'cervecerías',
    'convenience-stores',
    'restaurantes asturianos',
    u'tiendas de electrodomésticos',
    'police-dept',
    'tour_operators',
    'restaurantes catalanes',
    'black-hair-salons',
    'churches-methodist',
    'resorts',
    u'arrocerías',
    'gas-stations',
    'bed-breakfast-inns',
    'churches-united-methodist',
    'employment-agencies',
    'walmart',
    'pet-grooming',
    'teatros',
    'churches-non-denominational',
    'cvs-pharmacy',
    'guns-gunsmiths',
    'restaurantes castellanos',
    'dentists',
    u'con espectáculo',
    'churches-lutheran-evangelical-lutheran-church-in-america-elca',
    'tattoo-shops',
    'massage-therapists',
    'campgrounds',
    'accommodation',
    'olive-garden',
    'rv-parks',
    'public-swimming-pools',
    'beauty-salons',
    'bank-of-america',
    'churches-various-denominations',
    'churches-bible',
    'parques y jardines',
    u'papelerías',
    'churches-lutheran-evangelical-lutheran-church-in-america',
    'walgreens',
    'target',
    'night_club',
    'roberts-bar',
    'de compras',
    u'campos de fútbol',
    'sprint-store',
    'public-pools',
    'electricians',
    'national-car-rental',
    u'tiendas de vestidos de novia',
    'quilt-shops',
    'cab-service',
    'motel-6',
    'auditorium',
    'non-profit',
    'hvac company',
    'buffet libre',
    'churches-presbyterian-usa',
    'cemeteries',
    'immigration attorney',
    u'centros de estética',
    'automobile-leasing',
    'restaurantes japoneses',
    'museos',
    'hobby-model-shops',
    'hospitals',
    'church',
    'especialidades en carnes',
    u'pastelerías',
    u'tiendas de fotografía',
    'book-stores',
    'recreation-centers',
    'massage',
    'restaurantes de cocina internacional',
    'banquet-halls',
    'hertz',
    'veterinarian-emergency-services',
    'bowling-alley',
    'veterinary-clinics-hospitals',
    'van-rental-leasing',
    'pet-services',
    'restaurantes mexicanos',
    'ymca',
    'social-security-office',
    'restaurantes americanos',
    'chase-bank',
    'polideportivos',
    u'restaurantes asiáticos',
    'gun-shop',
    'day-spas',
    'photo-finishing',
    'hospital',
    'used-furniture',
    'thrift-shops',
    'chinese-food-delivery',
    'attraction',
    'jewellery',
    'bakeries',
    'churches-baptist-southern',
    'mcdonalds',
    'walk-in-clinic',
    'veterinary',
    'retailstore',
    'social-service-organizations',
    'flea-markets',
    'avis-rent-a-car',
    u'cosmética',
    u'telefonía',
    'corporate-lodging',
    u'monumentos históricos',
    'preschools-kindergarten',
    'alamo-car-rental',
    'bicycle-shops',
    u'coctelerías',
    'restaurantes chinos',
    'party-halls',
    'restaurantes argentinos',
    'trailer-renting-leasing',
    'swimming-pools-public',
    'stock-bond-brokers',
    'shell-gas-station',
    'churches-church-of-the-nazarene',
    'golf-courses',
    'holiday-inn-express',
    'martial-arts-schools',
    'veterinary-specialty-services',
    u'casa, jardín y bricolaje',
    'tiendas de disfraces',
    'walmart-pharmacy',
    'laundromat',
    'restaurantes gallegos',
    'fitness-centers',
    'synagogues',
    'winery',
    'amusement-places-arcades',
    'roses-store',
    'kosher-grocery-stores',
    'hair-salon',
    'federaciones y asociaciones deportivas',
    'donut-shops',
    'wells-fargo-bank',
    'talleres y cursos',
    'taverns',
    'budget-car-rental',
    'salas de conciertos',
    'bowling',
    'veterinary-clinics',
    'balnearios',
    'vinos, cavas, cervezas y licores',
    'beautyshop',
    'humane-society',
    'child-care',
    'animal-rescue',
    'hampton-inn',
    'social club',
    'churches-assemblies-of-god',
    'religious-general-interest-schools',
    u'tiendas de audio y vídeo',
    'antiques',
    'bed-and-breakfast',
    'dance_studio',
    'upholstery-fabrics',
    'churches-church-of-god',
    'dentist',
    'architects',
    'mobile-home-dealers',
    'hotel, restaurant',
    'tanning-salons',
    u'galerías de arte',
    'cheap-motels',
    'meat-markets',
    'recycling-centers',
    'panda-express',
    'music-stores',
    'laser tag',
    '24-hour-walgreens',
    u'comida rápida',
    'afterschool',
    'public-schools',
    'camping',
    'bicycle-rental',
    'chauffeur-service',
    'machine-shops',
    'bakery',
    'auto-oil-lube',
    u'floristerías',
    'casinos',
    'jail',
    u'bocaterías',
    'churches-presbyterian',
    'seamstress',
    'churches-community',
    'eye-doctor',
    'delicatessen',
    'pet-boarding-kennels',
    'fabric-shops',
    'penske-truck-rental',
    'mechanical-contractors',
    u'coleccionismo y numismática',
    'yellow-cab',
    'used-car-dealers',
    'marinas',
    'urgent-care',
    'bar-grills',
    'churches-lutheran-lutheran-church-missouri-synod-lcms',
    'holiday-inn',
    'divorce-attorneys',
    'tattoo',
    'churches-evangelical-covenant',
    'museums',
    'transportation-providers',
    'notaries-public',
    'music venue',
    'shooting-range',
    'veterinary-labs',
    'alamo-rent-a-car',
    u'tiendas de artesanía',
    'camps-recreational',
    u'tiendas de artesanía',
    'supermarkets-super-stores',
    'restaurantes arabes',
    u'chocolaterías',
    'ambulance-services',
    'payday-loans',
    'discount-stores',
    'hertz-rent-a-car',
    'asian-massage',
    'business school',
    u'heladerías',
    'drug-stores',
    'videoclubs',
    'health-resorts',
    'emergency-care-facilities',
    'churches-episcopal',
    'resale-shops',
    'hardware-stores',
    'mobile-pet-grooming',
    'pet-sitting',
    u'natación',
    'feed-store',
    'shuttle-service',
    'skin-care',
    'rv-rentals',
    'doctors',
    'churches-christian',
    'fire-dept',
    'water-heater-repair',
    'pet-stores',
    'laundromats',
    'farm',
    'nonprofit_charity',
    'churches-assemblies-of-god-independent',
    'variety-stores',
    'post-office',
    'smoke-shop',
    'boat-dealers',
    'hamburgers-hot-dogs',
    'restaurantes alemanes',
    'theaters',
    'comfort-suites',
    'mexican-latin-american-grocery-stores',
    'hair-braiding',
    u'panaderías',
    'guitar-stores',
    'churches-presbyterian-pca',
    'churches-presbyterian-arp',
    'check-cashing-service',
    'dog-pound',
    'psychics-mediums',
    'gymnasiums',
    'platos combinados',
    'new-car-dealers',
    'temples',
    u'ópticas',
    'lowes',
    'autobody shop',
    'motorcycle-dealers',
    'senior-center',
    'farms',
    'churches-evangelical',
    'campgrounds-parks',
    'lingerie',
    'churches-full-gospel',
    'churches-jehovahs-witnesses',
    'roman-catholic-churches',
    'independent-baptist-churches',
    'churches-baptist-independent',
    'churches-church-of-jesus-christ-of-latter-day-saints',
    'monuments',
    'lutheran-church',
    'private-swimming-pools',
    'stores',
    'cat-grooming',
    'budget-truck-rental',
    '31-flavors',
    'commercial organisation',
    'kinkos',
    'restaurant-delivery-service',
    'kennels',
    'barbers',
    'financial-planners',
    'used-bicycles',
    'rifle-pistol-ranges',
    'stadium',
    'art-instruction-schools',
    'indoor-shooting-range',
    'state-parks',
    'plumbing-contractors-commercial-industrial',
    'roman-catholic-church',
    'dollar-general',
    'spa',
    'restaurantes de alta cocina',
    "farmers' market",
    'car-dealers',
    'post-offices',
    'cinemas',
    'health-clubs',
    'massage-services',
    'driving-school',
    'pub',
    'gym',
    'atv-rentals',
    'preschool',
    'kmart',
    'parque infantiles',
    'costco',
    'courier-delivery-service',
    'localbusiness',
    'clothing-stores',
    'taxi',
    'taxi-cab',
    'ais-taxi-winooski',
    'taxi-service',
    'benways-taxi',
    'champs-taxi',
    'urgent-care-24-hour',
])

