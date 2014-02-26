import os
import datetime
import sqlite3

from serveus.models import *

if os.path.isfile('cs198pythontest.db'):
	os.remove('cs198pythontest.db')

if os.path.isfile('updated.db'):
	os.remove('updated.db')

db.create_all()

OUTPUT_LOG = True
def log(s):
	if OUTPUT_LOG:
		print 'Added', str(s)

# DEFAULT VALUES

# Database
temp = Database()
db.session.add(temp)
db.session.commit()
log(temp)

# Updated database
conn = sqlite3.connect('updated.db')
c = conn.cursor()
c.execute('''CREATE TABLE user (id INTEGER NOT NULL, username VARCHAR(80), password VARCHAR(80), PRIMARY KEY (id), UNIQUE (username))''')
conn.commit()
conn.close()

# User types
user_types = ['Administrator', 'Validator', 'Medical Technician']
for user_type in user_types:
	temp = UserType(user_type)
	db.session.add(temp)
	log(temp)

# Locations

locations = """Region I (Ilocos Region)
	Ilocos Norte
		Adams
		Bacarra
		Badoc
		Bangui
		Banna (Espiritu)
		Burgos
		Carasi
		City Of Batac
		Currimao
		Dingras
		Dumalneg
		Laoag City
		Marcos
		Nueva Era
		Pagudpud
		Paoay
		Pasuquin
		Piddig
		Pinili
		San Nicolas
		Sarrat
		Solsona
		Vintar
	Ilocos Sur
		Alilem
		Banayoyo
		Bantay
		Burgos
		Cabugao
		Caoayan
		Cervantes
		City Of Candon
		City Of Vigan
		Galimuyod
		Gregorio Del Pilar (Concepcion)
		Lidlidda
		Magsingal
		Nagbukel
		Narvacan
		Quirino (Angkaki)
		Salcedo (Baugen)
		San Emilio
		San Esteban
		San Ildefonso
		San Juan (Lapog)
		San Vicente
		Santa
		Santa Catalina
		Santa Cruz
		Santa Lucia
		Santa Maria
		Santiago
		Santo Domingo
		Sigay
		Sinait
		Sugpon
		Suyo
		Tagudin
	La Union
		Agoo
		Aringay
		Bacnotan
		Bagulin
		Balaoan
		Bangar
		Bauang
		Burgos
		Caba
		City Of San Fernando
		Luna
		Naguilian
		Pugo
		Rosario
		San Gabriel
		San Juan
		Santo Tomas
		Santol
		Sudipen
		Tubao
	Pangasinan
		Agno
		Aguilar
		Alcala
		Anda
		Asingan
		Balungao
		Bani
		Basista
		Bautista
		Bayambang
		Binalonan
		Binmaley
		Bolinao
		Bugallon
		Burgos
		Calasiao
		City Of Alaminos
		City Of Urdaneta
		Dagupan City
		Dasol
		Infanta
		Labrador
		Laoac
		Lingayen
		Mabini
		Malasiqui
		Manaoag
		Mangaldan
		Mangatarem
		Mapandan
		Natividad
		Pozzorubio
		Rosales
		San Carlos City
		San Fabian
		San Jacinto
		San Manuel
		San Nicolas
		San Quintin
		Santa Barbara
		Santa Maria
		Santo Tomas
		Sison
		Sual
		Tayug
		Umingan
		Urbiztondo
		Villasis
Region II (Cagayan Valley)
	Batanes
		Basco
		Itbayat
		Ivana
		Mahatao
		Sabtang
		Uyugan
	Cagayan
		Abulug
		Alcala
		Allacapan
		Amulung
		Aparri
		Baggao
		Ballesteros
		Buguey
		Calayan
		Camalaniugan
		Claveria
		Enrile
		Gattaran
		Gonzaga
		Iguig
		Lal-Lo
		Lasam
		Pamplona
		Penablanca
		Piat
		Rizal
		Sanchez-Mira
		Santa Ana
		Santa Praxedes
		Santa Teresita
		Santo Nino (Faire)
		Solana
		Tuao
		Tuguegarao City
	Isabela
		Alicia
		Angadanan
		Aurora
		Benito Soliven
		Burgos
		Cabagan
		Cabatuan
		City Of Cauayan
		City Of Santiago
		Cordon
		Delfin Albano (Magsaysay)
		Dinapigue
		Divilacan
		Echague
		Gamu
		Ilagan
		Jones
		Luna
		Maconacon
		Mallig
		Naguilian
		Palanan
		Quezon
		Quirino
		Ramon
		Reina Mercedes
		Roxas
		San Agustin
		San Guillermo
		San Isidro
		San Manuel
		San Mariano
		San Mateo
		San Pablo
		Santa Maria
		Santo Tomas
		Tumauini
	Nueva Vizcaya
		Alfonso Castaneda
		Ambaguio
		Aritao
		Bagabag
		Bambang
		Bayombong
		Diadi
		Dupax Del Norte
		Dupax Del Sur
		Kasibu
		Kayapa
		Quezon
		Santa Fe
		Solano
		Villaverde
	Quirino
		Aglipay
		Cabarroguis
		Diffun
		Maddela
		Nagtipunan
		Saguday
Region III (Central Luzon)
	Angeles City
		Angeles City
	Aurora
		Baler
		Casiguran
		Dilasag
		Dinalungan
		Dingalan
		Dipaculao
		Maria Aurora
		San Luis
	Bataan
		Abucay
		Bagac
		City Of Balanga
		Dinalupihan
		Hermosa
		Limay
		Mariveles
		Morong
		Orani
		Orion
		Pilar
		Samal
	Bulacan
		Angat
		Balagtas (Bigaa)
		Baliuag
		Bocaue
		Bulacan
		Bustos
		Calumpit
		City Of Malolos
		City Of Meycauayan
		City Of San Jose Del Monte
		Dona Remedios Trinidad
		Guiguinto
		Hagonoy
		Marilao
		Norzagaray
		Obando
		Pandi
		Paombong
		Plaridel
		Pulilan
		San Ildefonso
		San Miguel
		San Rafael
		Santa Maria
	Nueva Ecija
		Aliaga
		Bongabon
		Cabanatuan City
		Cabiao
		Carranglan
		City Of Gapan
		Cuyapo
		Gabaldon (Bitulok & Sabani)
		General Mamerto Natividad
		General Tinio (Papaya)
		Guimba
		Jaen
		Laur
		Licab
		Llanera
		Lupao
		Nampicuan
		Palayan City
		Pantabangan
		Penaranda
		Quezon
		Rizal
		San Antonio
		San Isidro
		San Jose City
		San Leonardo
		Santa Rosa
		Santo Domingo
		Science City Of Munoz
		Talavera
		Talugtug
		Zaragoza
	Olangapo City
		Olongapo City
	Pampanga
		Apalit
		Arayat
		Bacolor
		Candaba
		City Of San Fernando
		Floridablanca
		Guagua
		Lubao
		Mabalacat
		Macabebe
		Magalang
		Masantol
		Mexico
		Minalin
		Porac
		San Luis
		San Simon
		Santa Ana
		Santa Rita
		Santo Tomas
		Sasmuan (Sexmoan)
	Tarlac
		Anao
		Bamban
		Camiling
		Capas
		City Of Tarlac
		Concepcion
		Gerona
		La Paz
		Mayantoc
		Moncada
		Paniqui
		Pura
		Ramos
		San Clemente
		San Jose
		San Manuel
		Santa Ignacia
		Victoria
	Zambales
		Botolan
		Cabangan
		Candelaria
		Castillejos
		Iba
		Masinloc
		Palauig
		San Antonio
		San Felipe
		San Marcelino
		San Narciso
		Santa Cruz
		Subic
Region IV-A (Calabarzon)
	Batangas
		Agoncillo
		Alitagtag
		Balayan
		Balete
		Batangas City
		Bauan
		Calaca
		Calatagan
		City Of Tanauan
		Cuenca
		Ibaan
		Laurel
		Lemery
		Lian
		Lipa City
		Lobo
		Mabini
		Malvar
		Mataasnakahoy
		Nasugbu
		Padre Garcia
		Rosario
		San Jose
		San Juan
		San Luis
		San Nicolas
		San Pascual
		Santa Teresita
		Santo Tomas
		Taal
		Talisay
		Taysan
		Tingloy
		Tuy
	Cavite
		Alfonso
		Amadeo
		Bacoor
		Carmona
		Cavite City
		City Of Dasmarinas
		Gen. Mariano Alvarez
		General Emilio Aguinaldo
		General Trias
		Imus
		Indang
		Kawit
		Magallanes
		Maragondon
		Mendez (Mendez-Nunez)
		Naic
		Noveleta
		Rosario
		Silang
		Tagaytay City
		Tanza
		Ternate
		Trece Martires City
	Laguna
		Alaminos
		Bay
		Cabuyao
		Calauan
		Cavinti
		City Of Binan
		City Of Calamba
		City Of Santa Rosa
		Famy
		Kalayaan
		Liliw
		Los Banos
		Luisiana
		Lumban
		Mabitac
		Magdalena
		Majayjay
		Nagcarlan
		Paete
		Pagsanjan
		Pakil
		Pangil
		Pila
		Rizal
		San Pablo City
		San Pedro
		Santa Cruz
		Santa Maria
		Siniloan
		Victoria
	Lucena City
		Lucena City
	Quezon
		Agdangan
		Alabat
		Atimonan
		Buenavista
		Burdeos
		Calauag
		Candelaria
		Catanauan
		City Of Tayabas
		Dolores
		General Luna
		General Nakar
		Guinayangan
		Gumaca
		Infanta
		Jomalig
		Lopez
		Lucban
		Macalelon
		Mauban
		Mulanay
		Padre Burgos
		Pagbilao
		Panukulan
		Patnanungan
		Perez
		Pitogo
		Plaridel
		Polillo
		Quezon
		Real
		Sampaloc
		San Andres
		San Antonio
		San Francisco (Aurora)
		San Narciso
		Sariaya
		Tagkawayan
		Tiaong
		Unisan
	Rizal
		Angono
		Baras
		Binangonan
		Cainta
		Cardona
		City Of Antipolo
		Jala-Jala
		Morong
		Pililla
		Rodriguez (Montalban)
		San Mateo
		Tanay
		Taytay
		Teresa
Region IV-B (Mimaropa)
	Marinduque
		Boac
		Buenavista
		Gasan
		Mogpog
		Santa Cruz
		Torrijos
	Occidental Mindoro
		Abra De Ilog
		Calintaan
		Looc
		Lubang
		Magsaysay
		Mamburao
		Paluan
		Rizal
		Sablayan
		San Jose
		Santa Cruz
	Oriental Mindoro
		Baco
		Bansud
		Bongabong
		Bulalacao (San Pedro)
		City Of Calapan
		Gloria
		Mansalay
		Naujan
		Pinamalayan
		Pola
		Puerto Galera
		Roxas
		San Teodoro
		Socorro
		Victoria
	Palawan
		Aborlan
		Agutaya
		Araceli
		Balabac
		Bataraza
		Brooke's Point
		Busuanga
		Cagayancillo
		Coron
		Culion
		Cuyo
		Dumaran
		El Nido (Bacuit)
		Kalayaan
		Linapacan
		Magsaysay
		Narra
		Quezon
		Rizal (Marcos)
		Roxas
		San Vicente
		Sofronio Espanola
		Taytay
	Puerto Princesa City
		Puerto Princesa City
	Romblon
		Alcantara
		Banton
		Cajidiocan
		Calatrava
		Concepcion
		Corcuera
		Ferrol
		Looc
		Magdiwang
		Odiongan
		Romblon
		San Agustin
		San Andres
		San Fernando
		San Jose
		Santa Fe
		Santa Maria (Imelda)
Region V (Bicol)
	Albay
		Bacacay
		Camalig
		City Of Ligao
		City Of Tabaco
		Daraga (Locsin)
		Guinobatan
		Jovellar
		Legazpi City
		Libon
		Malilipot
		Malinao
		Manito
		Oas
		Pio Duran
		Polangui
		Rapu-Rapu
		Santo Domingo (Libog)
		Tiwi
	Camarines Norte
		Basud
		Capalonga
		Daet
		Jose Panganiban
		Labo
		Mercedes
		Paracale
		San Lorenzo Ruiz (Imelda)
		San Vicente
		Santa Elena
		Talisay
		Vinzons
	Camarines Sur
		Baao
		Balatan
		Bato
		Bombon
		Buhi
		Bula
		Cabusao
		Calabanga
		Camaligan
		Canaman
		Caramoan
		Del Gallego
		Gainza
		Garchitorena
		Goa
		Iriga City
		Lagonoy
		Libmanan
		Lupi
		Magarao
		Milaor
		Minalabac
		Nabua
		Naga City
		Ocampo
		Pamplona
		Pasacao
		Pili
		Presentacion (Parubcan)
		Ragay
		Sagnay
		San Fernando
		San Jose
		Sipocot
		Siruma
		Tigaon
		Tinambac
	Catanduanes
		Bagamanoc
		Baras
		Bato
		Caramoran
		Gigmoto
		Pandan
		Panganiban (Payo)
		San Andres (Calolbon)
		San Miguel
		Viga
		Virac
	Masbate
		Aroroy
		Baleno
		Balud
		Batuan
		Cataingan
		Cawayan
		City Of Masbate
		Claveria
		Dimasalang
		Esperanza
		Mandaon
		Milagros
		Mobo
		Monreal
		Palanas
		Pio V. Corpuz (Limbuhan)
		Placer
		San Fernando
		San Jacinto
		San Pascual
		Uson
	Sorsogon
		Barcelona
		Bulan
		Bulusan
		Casiguran
		Castilla
		City Of Sorsogon
		Donsol
		Gubat
		Irosin
		Juban
		Magallanes
		Matnog
		Pilar
		Prieto Diaz
		Santa Magdalena
Region VI (Western Visayas)
	Aklan
		Altavas
		Balete
		Banga
		Batan
		Buruanga
		Ibajay
		Kalibo
		Lezo
		Libacao
		Madalag
		Makato
		Malay
		Malinao
		Nabas
		New Washington
		Numancia
		Tangalan
	Antique
		Anini-Y
		Barbaza
		Belison
		Bugasong
		Caluya
		Culasi
		Hamtic
		Laua-An
		Libertad
		Pandan
		Patnongon
		San Jose
		San Remigio
		Sebaste
		Sibalom
		Tibiao
		Tobias Fornier (Dao)
		Valderrama
	Bacolod City
		Bacolod City
	Capiz
		Cuartero
		Dao
		Dumalag
		Dumarao
		Ivisan
		Jamindan
		Ma-Ayon
		Mambusao
		Panay
		Panitan
		Pilar
		Pontevedra
		President Roxas
		Roxas City
		Sapi-An
		Sigma
		Tapaz
	Guimaras
		Buenavista
		Jordan
		Nueva Valencia
		San Lorenzo
		Sibunag
	Iloilo
		Ajuy
		Alimodian
		Anilao
		Badiangan
		Balasan
		Banate
		Barotac Nuevo
		Barotac Viejo
		Batad
		Bingawan
		Cabatuan
		Calinog
		Carles
		City Of Passi
		Concepcion
		Dingle
		Duenas
		Dumangas
		Estancia
		Guimbal
		Igbaras
		Janiuay
		Lambunao
		Leganes
		Lemery
		Leon
		Maasin
		Miagao
		Mina
		New Lucena
		Oton
		Pavia
		Pototan
		San Dionisio
		San Enrique
		San Joaquin
		San Miguel
		San Rafael
		Santa Barbara
		Sara
		Tigbauan
		Tubungan
		Zarraga
	Iloilo City
		Iloilo City
	Negros Occidental
		Bago City
		Binalbagan
		Cadiz City
		Calatrava
		Candoni
		Cauayan
		City Of Escalante
		City Of Himamaylan
		City Of Kabankalan
		City Of Sipalay
		City Of Talisay
		City Of Victorias
		Enrique B. Magalona (Saravia)
		Hinigaran
		Hinoba-An (Asia)
		Ilog
		Isabela
		La Carlota City
		La Castellana
		Manapla
		Moises Padilla (Magallon)
		Murcia
		Pontevedra
		Pulupandan
		Sagay City
		Salvador Benedicto
		San Carlos City
		San Enrique
		Silay City
		Toboso
		Valladolid
Region VII (Central Visayas)
	Bohol
		Alburquerque
		Alicia
		Anda
		Antequera
		Baclayon
		Balilihan
		Batuan
		Bien Unido
		Bilar
		Buenavista
		Calape
		Candijay
		Carmen
		Catigbian
		Clarin
		Corella
		Cortes
		Dagohoy
		Danao
		Dauis
		Dimiao
		Duero
		Garcia Hernandez
		Guindulman
		Inabanga
		Jagna
		Jetafe
		Lila
		Loay
		Loboc
		Loon
		Mabini
		Maribojoc
		Panglao
		Pilar
		Pres. Carlos P. Garcia (Pitogo)
		Sagbayan (Borja)
		San Isidro
		San Miguel
		Sevilla
		Sierra Bullones
		Sikatuna
		Tagbilaran City
		Talibon
		Trinidad
		Tubigon
		Ubay
		Valencia
	Cebu
		Alcantara
		Alcoy
		Alegria
		Aloguinsan
		Argao
		Asturias
		Badian
		Balamban
		Bantayan
		Barili
		Boljoon
		Borbon
		Carmen
		Catmon
		City Of Bogo
		City Of Carcar
		City Of Naga
		City Of Talisay
		Compostela
		Consolacion
		Cordoba
		Daanbantayan
		Dalaguete
		Danao City
		Dumanjug
		Ginatilan
		Liloan
		Madridejos
		Malabuyoc
		Medellin
		Minglanilla
		Moalboal
		Oslob
		Pilar
		Pinamungahan
		Poro
		Ronda
		Samboan
		San Fernando
		San Francisco
		San Remigio
		Santa Fe
		Santander
		Sibonga
		Sogod
		Tabogon
		Tabuelan
		Toledo City
		Tuburan
		Tudela
	Cebu City
		Cebu City
	Lapu-Lapu City
		Lapu-Lapu City (Opon)
	Mandaue City
		Mandaue City
	Negros Oriental
		Amlan (Ayuquitan)
		Ayungon
		Bacong
		Bais City
		Basay
		Bindoy (Payabon)
		Canlaon City
		City Of Bayawan (Tulong)
		City Of Guihulngan
		City Of Tanjay
		Dauin
		Dumaguete City
		Jimalalud
		La Libertad
		Mabinay
		Manjuyod
		Pamplona
		San Jose
		Santa Catalina
		Siaton
		Sibulan
		Tayasan
		Valencia (Luzurriaga)
		Vallehermoso
		Zamboanguita
	Siquijor
		Enrique Villanueva
		Larena
		Lazi
		Maria
		San Juan
		Siquijor
Region VIII (Eastern Visayas)
	Biliran
		Almeria
		Biliran
		Cabucgayan
		Caibiran
		Culaba
		Kawayan
		Maripipi
		Naval
	Eastern Samar
		Arteche
		Balangiga
		Balangkayan
		Can-Avid
		City Of Borongan
		Dolores
		General Macarthur
		Giporlos
		Guiuan
		Hernani
		Jipapad
		Lawaan
		Llorente
		Maslog
		Maydolong
		Mercedes
		Oras
		Quinapondan
		Salcedo
		San Julian
		San Policarpo
		Sulat
		Taft
	Leyte
		Abuyog
		Alangalang
		Albuera
		Babatngon
		Barugo
		Bato
		Burauen
		Calubian
		Capoocan
		Carigara
		City Of Baybay
		Dagami
		Dulag
		Hilongos
		Hindang
		Inopacan
		Isabel
		Jaro
		Javier (Bugho)
		Julita
		Kananga
		La Paz
		Leyte
		Macarthur
		Mahaplag
		Matag-Ob
		Matalom
		Mayorga
		Merida
		Ormoc City
		Palo
		Palompon
		Pastrana
		San Isidro
		San Miguel
		Santa Fe
		Tabango
		Tabontabon
		Tacloban City
		Tanauan
		Tolosa
		Tunga
		Villaba
	Northern Samar
		Allen
		Biri
		Bobon
		Capul
		Catarman
		Catubig
		Gamay
		Laoang
		Lapinig
		Las Navas
		Lavezares
		Lope De Vega
		Mapanas
		Mondragon
		Palapag
		Pambujan
		Rosario
		San Antonio
		San Isidro
		San Jose
		San Roque
		San Vicente
		Silvino Lobos
		Victoria
	Samar (Western)
		Almagro
		Basey
		Calbayog City
		Calbiga
		City Of Catbalogan
		Daram
		Gandara
		Hinabangan
		Jiabong
		Marabut
		Matuguinao
		Motiong
		Pagsanghan
		Paranas (Wright)
		Pinabacdao
		San Jorge
		San Jose De Buan
		San Sebastian
		Santa Margarita
		Santa Rita
		Santo Nino
		Tagapul-An
		Talalora
		Tarangnan
		Villareal
		Zumarraga
	Southern Leyte
		Anahawan
		Bontoc
		City Of Maasin
		Hinunangan
		Hinundayan
		Libagon
		Liloan
		Limasawa
		Macrohon
		Malitbog
		Padre Burgos
		Pintuyan
		Saint Bernard
		San Francisco
		San Juan (Cabalian)
		San Ricardo
		Silago
		Sogod
		Tomas Oppus
Region IX (Zamboanga Peninsula)
	Basilan
		City Of Isabela
	Zamboanga City
		Zamboanga City
	Zamboanga Sibugay
		Alicia
		Buug
		Diplahan
		Imelda
		Ipil
		Kabasalan
		Mabuhay
		Malangas
		Naga
		Olutanga
		Payao
		Roseller Lim
		Siay
		Talusan
		Titay
		Tungawan
	Zamboanga del Norte
		Bacungan (Leon T. Postigo)
		Baliguian
		Dapitan City
		Dipolog City
		Godod
		Gutalac
		Jose Dalman (Ponot)
		Kalawit
		Katipunan
		La Libertad
		Labason
		Liloy
		Manukan
		Mutia
		Pinan (New Pinan)
		Polanco
		Pres. Manuel A. Roxas
		Rizal
		Salug
		Sergio Osmena Sr.
		Siayan
		Sibuco
		Sibutad
		Sindangan
		Siocon
		Sirawai
		Tampilisan
	Zamboanga del Sur
		Aurora
		Bayog
		Dimataling
		Dinas
		Dumalinao
		Dumingag
		Guipos
		Josefina
		Kumalarang
		Labangan
		Lakewood
		Lapuyan
		Mahayag
		Margosatubig
		Midsalip
		Molave
		Pagadian City
		Pitogo
		Ramon Magsaysay (Liargo)
		San Miguel
		San Pablo
		Sominot (Don Mariano Marcos)
		Tabina
		Tambulig
		Tigbao
		Tukuran
		Vincenzo A. Sagun
Region X (Northern Mindanao)
	Bukidnon
		Baungon
		Cabanglasan
		City Of Malaybalay
		City Of Valencia
		Damulog
		Dangcagan
		Don Carlos
		Impasug-Ong
		Kadingilan
		Kalilangan
		Kibawe
		Kitaotao
		Lantapan
		Libona
		Malitbog
		Manolo Fortich
		Maramag
		Pangantucan
		Quezon
		San Fernando
		Sumilao
		Talakag
	Cagayan de Oro City
		Cagayan De Oro City
	Camiguin
		Catarman
		Guinsiliban
		Mahinog
		Mambajao
		Sagay
	Iligan City
		Iligan City
	Lanao del Norte
		Bacolod
		Baloi
		Baroy
		Kapatagan
		Kauswagan
		Kolambugan
		Lala
		Linamon
		Magsaysay
		Maigo
		Matungao
		Munai
		Nunungan
		Pantao Ragat
		Pantar
		Poona Piagapo
		Salvador
		Sapad
		Sultan Naga Dimaporo (Karomatan)
		Tagoloan
		Tangcal
		Tubod
	Misamis Occidental
		Aloran
		Baliangao
		Bonifacio
		Calamba
		Clarin
		Concepcion
		Don Victoriano Chiongbian (Don Mariano Marcos)
		Jimenez
		Lopez Jaena
		Oroquieta City
		Ozamis City
		Panaon
		Plaridel
		Sapang Dalaga
		Sinacaban
		Tangub City
		Tudela
	Misamis Oriental
		Alubijid
		Balingasag
		Balingoan
		Binuangan
		City Of El Salvador
		Claveria
		Gingoog City
		Gitagum
		Initao
		Jasaan
		Kinoguitan
		Lagonglong
		Laguindingan
		Libertad
		Lugait
		Magsaysay (Linugos)
		Manticao
		Medina
		Naawan
		Opol
		Salay
		Sugbongcogon
		Tagoloan
		Talisayan
		Villanueva
Region XI (Davao Region)
	Compostela Valley
		Compostela
		Laak (San Vicente)
		Mabini (Dona Alicia)
		Maco
		Maragusan (San Mariano)
		Mawab
		Monkayo
		Montevista
		Nabunturan
		New Bataan
		Pantukan
	Davao City
		Davao City
	Davao Oriental
		Baganga
		Banaybanay
		Boston
		Caraga
		Cateel
		City Of Mati
		Governor Generoso
		Lupon
		Manay
		San Isidro
		Tarragona
	Davao del Norte
		Asuncion (Saug)
		Braulio E. Dujali
		Carmen
		City Of Panabo
		City Of Tagum
		Island Garden City Of Samal
		Kapalong
		New Corella
		San Isidro
		Santo Tomas
		Talaingod
	Davao del Sur
		Bansalan
		City Of Digos
		Don Marcelino
		Hagonoy
		Jose Abad Santos (Trinidad)
		Kiblawan
		Magsaysay
		Malalag
		Malita
		Matanao
		Padada
		Santa Cruz
		Santa Maria
		Sarangani
		Sulop
Region XII (Soccsksargen)
	Cotabato (North C.)
		Alamada
		Aleosan
		Antipas
		Arakan
		Banisilan
		Carmen
		City Of Kidapawan
		Kabacan
		Libungan
		M'Lang
		Magpet
		Makilala
		Matalam
		Midsayap
		Pigkawayan
		Pikit
		President Roxas
		Tulunan
	Cotabato City
		Cotabato City
	General Santos City
		General Santos City (Dadiangas)
	Sarangani
		Alabel
		Glan
		Kiamba
		Maasim
		Maitum
		Malapatan
		Malungon
	South Cotabato
		Banga
		City Of Koronadal
		Lake Sebu
		Norala
		Polomolok
		Santo Nino
		Surallah
		T'Boli
		Tampakan
		Tantangan
		Tupi
	Sultan Kudarat
		Bagumbayan
		City Of Tacurong
		Columbio
		Esperanza
		Isulan
		Kalamansig
		Lambayong (Mariano Marcos)
		Lebak
		Lutayan
		Palimbang
		President Quirino
		Sen. Ninoy Aquino
Region XIII (Caraga)
	Agusan del Norte
		Buenavista
		Carmen
		City Of Cabadbaran
		Jabonga
		Kitcharao
		Las Nieves
		Magallanes
		Nasipit
		Remedios T. Romualdez
		Santiago
		Tubay
	Agusan del Sur
		Bunawan
		City Of Bayugan
		Esperanza
		La Paz
		Loreto
		Prosperidad
		Rosario
		San Francisco
		San Luis
		Santa Josefa
		Sibagat
		Talacogon
		Trento
		Veruela
	Butuan City
		Butuan City
	Dinagat Islands
		Basilisa (Rizal)
		Cagdianao
		Dinagat
		Libjo (Albor)
		Loreto
		San Jose
		Tubajon
	Surigao del Norte
		Alegria
		Bacuag
		Burgos
		Claver
		Dapa
		Del Carmen
		General Luna
		Gigaquit
		Mainit
		Malimono
		Pilar
		Placer
		San Benito
		San Francisco (Anao-Aon)
		San Isidro
		Santa Monica (Sapao)
		Sison
		Socorro
		Surigao City
		Tagana-An
		Tubod
	Surigao del Sur
		Barobo
		Bayabas
		Cagwait
		Cantilan
		Carmen
		Carrascal
		City Of Bislig
		City Of Tandag
		Cortes
		Hinatuan
		Lanuza
		Lianga
		Lingig
		Madrid
		Marihatag
		San Agustin
		San Miguel
		Tagbina
		Tago
ARMM - Autonomous Region of Muslim Mindanao
	Basilan
		Akbar
		Al-Barka
		City Of Lamitan
		Hadji Mohammad Ajul
		Hadji Muhtamad
		Lantawan
		Maluso
		Sumisip
		Tipo-Tipo
		Tuburan
		Ungkaya Pukan
	Lanao del Sur
		Bacolod-Kalawi (Bacolod Grande)
		Balabagan
		Balindong (Watu)
		Bayang
		Binidayan
		Buadiposo-Buntong
		Bubong
		Bumbaran
		Butig
		Calanogas
		Ditsaan-Ramain
		Ganassi
		Kapai
		Kapatagan
		Lumba-Bayabao (Maguing)
		Lumbaca-Unayan
		Lumbatan
		Lumbayanague
		Madalum
		Madamba
		Maguing
		Malabang
		Marantao
		Marawi City
		Marogong
		Masiu
		Mulondo
		Pagayawan (Tatarikan)
		Piagapo
		Picong (Sultan Gumander)
		Poona Bayabao (Gata)
		Pualas
		Saguiaran
		Sultan Dumalondong
		Tagoloan Ii
		Tamparan
		Taraka
		Tubaran
		Tugaya
		Wao
	Maguindanao
		Ampatuan
		Barira
		Buldon
		Buluan
		Datu Abdullah Sangki
		Datu Anggal Midtimbang
		Datu Blah T. Sinsuat
		Datu Odin Sinsuat (Dinaig)
		Datu Paglas
		Datu Piang
		Datu Saudi-Ampatuan
		Datu Unsay
		Gen. S. K. Pendatun
		Guindulungan
		Kabuntalan (Tumbao)
		Mamasapano
		Mangudadatu
		Matanog
		Northern Kabuntalan
		Pagagawan
		Pagalungan
		Paglat
		Pandag
		Parang
		Rajah Buayan
		Shariff Aguak (Maganoy)
		South Upi
		Sultan Kudarat (Nuling)
		Sultan Mastura
		Sultan Sa Barongis (Lambayong)
		Talayan
		Talitay
		Upi
	Sulu
		Hadji Panglima Tahil (Marunggas)
		Indanan
		Jolo
		Kalingalan Caluang
		Lugus
		Luuk
		Maimbung
		Old Panamao
		Omar
		Pandami
		Panglima Estino (New Panamao)
		Pangutaran
		Parang
		Pata
		Patikul
		Siasi
		Talipao
		Tapul
		Tongkil
	Tawi-tawi
		Bongao
		Languyan
		Mapun (Cagayan De Tawi-Tawi)
		Panglima Sugala (Balimbing)
		Sapa-Sapa
		Sibutu
		Simunul
		Sitangkai
		South Ubian
		Tandubas
		Turtle Islands
CAR - Cordillera Administrative Region
	Abra
		Bangued
		Boliney
		Bucay
		Bucloc
		Daguioman
		Danglas
		Dolores
		La Paz
		Lacub
		Lagangilang
		Lagayan
		Langiden
		Licuan-Baay (Licuan)
		Luba
		Malibcong
		Manabo
		Penarrubia
		Pidigan
		Pilar
		Sallapadan
		San Isidro
		San Juan
		San Quintin
		Tayum
		Tineg
		Tubo
		Villaviciosa
	Apayao
		Calanasan (Bayag)
		Conner
		Flora
		Kabugao
		Luna
		Pudtol
		Santa Marcela
	Baguio City
		Baguio City
	Benguet
		Atok
		Bakun
		Bokod
		Buguias
		Itogon
		Kabayan
		Kapangan
		Kibungan
		La Trinidad
		Mankayan
		Sablan
		Tuba
		Tublay
	Ifugao
		Aguinaldo
		Alfonso Lista (Potia)
		Asipulo
		Banaue
		Hingyon
		Hungduan
		Kiangan
		Lagawe
		Lamut
		Mayoyao
		Tinoc
	Kalinga
		Balbalan
		City Of Tabuk
		Lubuagan
		Pasil
		Pinukpuk
		Rizal (Liwan)
		Tanudan
		Tinglayan
	Mountain Province
		Barlig
		Bauko
		Besao
		Bontoc
		Natonin
		Paracelis
		Sabangan
		Sadanga
		Sagada
		Tadian
NCR - National Capital Region (Metro Manila)
	First District
		Binondo
		Ermita
		Intramuros
		Malate
		Paco
		Pandacan
		Port Area
		Quiapo
		Sampaloc
		San Miguel
		San Nicolas
		Santa Ana
		Santa Cruz
		Tondo I / II
	Fourth District
		Las Pinas, City of
		Makati, City of
		Muntinlupa, City of
		Paranaque, City of
		Pasay City
		Pateros
		Taguig City
	Second District
		Mandaluyong, City of
		Marikina, City of
		Pasig, City of
		Quezon City
		San Juan, City of
	Third District
		Caloocan City
		Malabon, City of
		Navotas, City of
		Valenzuela, City of"""

order_string = """010000000	Region I (Ilocos Region)	San Fernando City	13,012.60	3,550,642	4,200,478	4,748,372
020000000	Region II (Cagayan Valley)	Tuguegarao City	28,228.83	2,340,545	2,813,159	3,229,163
030000000	Region III (Central Luzon)	City of San Fernando	22,014.63	6,338,590	8,204,742	10,137,737
040000000	Region IV-A (Calabarzon)	Calamba City	16,873.31	6,349,452	9,320,629	12,609,803
170000000	Region IV-B (Mimaropa)	Calapan City	29,620.87	1,774,074	2,299,229	2,744,671
050000000	Region V (Bicol)	Legazpi City	18,155.82	3,910,001	4,686,669	5,420,411
060000000	Region VI (Western Visayas)	Iloilo City	20,794.18	5,393,333	6,211,038	7,102,438
070000000	Region VII (Central Visayas)	Cebu City	15,885.97	4,594,124	5,706,953	6,800,180
080000000	Region VIII (Eastern Visayas)	Tacloban City	23,251.10	3,054,490	3,610,355	4,101,322
090000000	Region IX (Zamboanga Peninsula)	Pagadian City	17,046.64	2,281,064	2,831,412	3,407,353
100000000	Region X (Northern Mindanao)	Cagayan de Oro City	20,496.02	2,811,646	3,505,708	4,297,323
110000000	Region XI (Davao Region)	Davao City	20,357.42	2,933,743	3,676,163	4,468,563
120000000	Region XII (Soccsksargen)	Koronadal City	22,513.30	2,399,953	3,222,169	4,109,571
160000000	Region XIII (Caraga)	Butuan City	21,478.35	1,764,297	2,095,367	2,429,224
150000000	ARMM - Autonomous Region of Muslim Mindanao	Cotabato City	21,065.30	2,108,061	2,803,045	3,256,140
140000000	CAR - Cordillera Administrative Region	Baguio City	19,422.03	1,146,191	1,365,412	1,616,867
130000000	NCR - National Capital Region (Metro Manila)	Manila	633.11	7,948,392	9,932,560	11,855,975"""

order = [line.split('\t')[1] for line in order_string.split('\n')]

d = {}
for line in locations.split('\n'):
	count = line.count('\t')
	data = line.replace('\t','')
	if count == 0:
		region = data
		d[region] = {}
	elif count == 1:
		province = data
		d[region][province] = []
	else:
		municipality = data
		d[region][province].append(municipality)

for region in order:
	provinces = d[region]
	db_region = Region(name=region)
	db.session.add(db_region)
	for province, municipalities in sorted(provinces.iteritems()):
		db_province = Province(name=province)
		db_province.region = db_region
		db.session.add(db_province)
		for municipality in sorted(municipalities):
			db_municipality = Municipality(name=municipality)
			db_municipality.province = db_province
			db.session.add(db_municipality)

db.session.commit()


# DUMMY DATA

log('dummy data')

# Users
x = []
x.append(User('Rodolfo', 'Kirong', 'rodolfo', User.hash_password('genius123'), '0912-345-6789', 'rodolfo@mailinator.com'))
x[-1].usertype_id = 1
x.append(User('Noel', 'Sison', 'noel', User.hash_password('qwert'), '0912-345-6789', 'noel@mailinator.com'))
x[-1].usertype_id = 2
x.append(User('Juancho', 'Coronel', 'juancho', User.hash_password('12345'), '0912-345-6789', 'juancho@mailinator.com'))
x[-1].usertype_id = 1
x.append(User('Marven', 'Sanchez', 'marven', User.hash_password('asd'), '0912-345-6789', 'marven@mailinator.com'))
x[-1].usertype_id = 3
x.append(User('Jasper', 'Cacbay', 'jasper', User.hash_password('asd'), '0912-345-6789', 'jasper@mailinator.com'))
x[-1].usertype_id = 2
x.append(User('Cat', 'Angangco', 'cat', User.hash_password('asd'), '0912-345-6789', 'cat@mailinator.com'))
x[-1].usertype_id = 1
x.append(User('Pros', 'Naval', 'pcnaval', User.hash_password('genius123'), '0917-865-8452', 'pros@mailinator.com'))
x[-1].usertype_id = 1
for i in x:
    db.session.add(i)

# Cases

x = Case(datetime.date(2010,5,15),'Vivax','Description',11.2,119.41,True)
x.user_id = 1
db.session.add(x)

x = Case(datetime.date(2005,8,26),'Vivax','Description',11.2,119.41,True)
x.user_id = 2
db.session.add(x)

x = Case(datetime.date(2010,5,15),'Falciparum','Description',10.49,119.31,True)
x.user_id = 3
db.session.add(x)

x = Case(datetime.date(2007,1,5),'Ovale','Description',9.17,118.25,True)
x.user_id = 4
db.session.add(x)

x = Case(datetime.date(2009,9,9),'No Disease','Description',10.42,119.2,True)
x.user_id = 5
db.session.add(x)

x = Case(datetime.date(2011,9,9),'Malariae','Description',8.4,117.2,True)
x.user_id = 6
db.session.add(x)

x = Case(datetime.date(2008,9,9),'No Disease','Description',9.25,118.05,True)
x.user_id = 1
db.session.add(x)

x = Case(datetime.date(2012,9,9),'Malariae','Description',9.26,118.33,True)
x.user_id = 2
db.session.add(x)

x = Case(datetime.date(2013,1,10),'Falciparum','Description',10.32,119.17,True)
x.user_id = 3
db.session.add(x)

x = Case(datetime.date(2013,9,10),'Ovale','Description',10.32,119.46,True)
x.user_id = 4
db.session.add(x)

x = Case(datetime.date(2011,5,15),'No Disease','Description',8.47,117.5,True)
x.user_id = 5
db.session.add(x)

x = Case(datetime.date(2012,5,9),'Vivax','Description',10.51,121.0, True)
x.user_id = 6
db.session.add(x)

# Manila
x = Case(datetime.date(2014,2,19),'Malariae','Severe',14.565454,120.993973, True)
x.user_id = 6
db.session.add(x)

# Manila
x = Case(datetime.date(2014,2,19),'Malariae','Severe',14.565454,120.993973,True)
x.user_id = 6
db.session.add(x)

# Manila
x = Case(datetime.date(2014,2,10),'Malariae','Severe',14.565454,120.993973, True)
x.user_id = 6
db.session.add(x)

# QC
x = Case(datetime.date(2014,2,17),'Malariae','Severe',14.64836399, 121.0684764, True)
x.user_id = 6
db.session.add(x)

# QC
x = Case(datetime.date(2014,2,18),'Malariae','Severe',14.64836399, 121.0684764, True)
x.user_id = 6
db.session.add(x)

# QC
x = Case(datetime.date(2014,2,19),'Malariae','Severe',14.64836399, 121.0684764, True)
x.user_id = 6
db.session.add(x)

# QC
x = Case(datetime.date(2014,2,19),'Malariae','Severe',14.639946,121.0781, True)
x.user_id = 6
db.session.add(x)

# Images
for i in xrange(1,9):
    tmp = Image()
    tmp.create_image('reset_images/' + str(i) + '.jpg', None)
    tmp.case_id = i
    db.session.add(tmp)
log('images')    

# TODO: remove when keys are synced with accounts
"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

private_key = RSA.generate(1024)
public_key = private_key.publickey()
private_key = private_key.exportKey()
public_key = public_key.exportKey().replace('-----BEGIN PUBLIC KEY-----','').replace('-----END PUBLIC KEY-----','').replace('\n','')
db.session.add(Key(private_key, public_key))
"""
#public_key = """MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbMiQNyj/Nzj7QQBj8nAx3WKPy4r72Onnw/E9KQY1gUwepRtCKYgJz9typvvfi7zNROFp5o8OBL5mVWFShxMIh57entYRpZUGtTZtb7YT5Bx3ZM5FPKQzHcJDyPJFloJW6V0+jmmZSosvM4nrZknVW3DABdmiVadGXtdy9DNevyQIDAQAB"""
public_key = """009b32240dca3fcdce3ed04018fc9c0c7758a3f2e2bef63a79f0fc4f4a418d605307a946d08a620273f6dca9bef7e2ef3351385a79a3c3812f99955854a1c4c221e7b7a7b584696541ad4d9b5bed84f9071dd933914f290cc77090f23c9165a095ba574fa39a6652a2cbcce27ad9927556dc300176689569d197b5dcbd0cd7afc9"""
private_key = """-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQCbMiQNyj/Nzj7QQBj8nAx3WKPy4r72Onnw/E9KQY1gUwepRtCK\nYgJz9typvvfi7zNROFp5o8OBL5mVWFShxMIh57entYRpZUGtTZtb7YT5Bx3ZM5FP\nKQzHcJDyPJFloJW6V0+jmmZSosvM4nrZknVW3DABdmiVadGXtdy9DNevyQIDAQAB\nAoGAF7J9TNnAClXew3+2EQRm5uZTCmhTDlf5fLGaDdWal8W12sQkXaz/gOOF6Clv\nwmgR5un67q3x0U0KX4KAUb8wgS2wlkWYlT062+mE7cYKZh07ZxCFy+yrfM6qRrvA\nHJPa60TTAQTRXSeoX9DrWHld+JVKml74vV3oQSThdgj70d0CQQC1Ei48dhfmCurY\nsVPjHR6Sx0URqtHvZMHJrW1eMa0X0QHSs9iSXFZmQGD5qprQBjNmMrQe8zd4Uwto\ntPMnPSxjAkEA22rd7deGlaWaaTosMF12ikzMd1KP42IK+BWMIh6HfoXcxj7H1pQ7\nS7oSNgqqIojgGLZfIc9bKfa0sSp6GE+c4wJBAKd2vRRmFAxKJJFsz6zJDbGqYpLI\nbYj+osunffMT9oaEYy8/7hjPFYlUGVxPEQc79OWcF0JYpwC9rVuVnxy3UwkCQQCw\nnCk8OyGyLFTIZDGTUHeMxFpDpSn6PT1VCIr+H5KyLW9SBtB1kGTWBFSKOTVOjNvM\nKGcUYMIhWdmBTQ5vqQ0/AkAx2XcV90V/6i89F2SElT3OcQsjznPJ58TupP5Ckr6l\n3i8SY+/pip4zPV0/gdS21VbaOEvwxaVOUcm1anNmBmRs\n-----END RSA PRIVATE KEY-----"""
db.session.add(Key(private_key, public_key))

# COMMIT
db.session.commit()
