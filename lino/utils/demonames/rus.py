# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.utils import Cycler


def splitter1(s):
    for ln in s.splitlines():
        ln = ln.strip()
        if len(ln) > 1 and ln[0] != '#':
            yield ln

LAST_NAMES_RUSSIA = u"""
A
Abezgauz 
Aleksandrov 
Altukhov 
Alvang 
Ankundinov 
Arent 
Arnold 
Arshan 
Arshun 
Artemieva 
Astafurov 

B
Bardzecki 
Bartoszewicz 
Bashmakov 
Baskov 
Bek-Murzin 
Belskaia 
Berendt 
Berndt 
Bernt 
Berthner 
Bilinskii 
Bleiwas 
Bobrov 
Bogaevskaia 
Bogdanjwa 
Bogdanovich 
Bolokhovskis 
Bondar 
Borenstein 
Borodinskii 
Borovsky 
Borowski 
Botkina 
Budberg 
Budian 
Budkovskiy 
Budliavski 
Burdzecki 
Burundukov 
Buryshkin 
Burzeckaia 

C
Chepelskii 
Cheremisinova 
Cherevin 
Cherkesov 
Cherlin 
Cherlina 
Chernikova 
Cherstvennikov 
Chirkoff 
Chopiak 
Chubinskii 
Chuchin 
Chuzhoi 

D
Dauksza 
Dikau 
Dmitriev 
Domashevich 
Dombrovski 
Dotsenko 
Dvorkin 
Dvorzhetskii 
Dzhigit 

E
Elout 
Entin 

F
Feldberg 
Fialkovskii 
Fiialkov 
Flits 
Frinovskii 

G
Garder 
Gaunshtein 
Gavlik 
Gavrikov 
Gavronskii 
Gelb 
Gepfner 
Gerasimova 
Gerburt 
Gershan 
Gikalov 
Gise 
Giunter 
Glazov 
Glinka 
Glubonin 
Golender 
Golovkin 
Gontmakher 
Gorchakov 
Gorenshtein 
Grabianko 
Gundobin 
Gunter 
Gusarov 
Gutelmakher 
Gutemovskii 
Gutenmakher 
Guttenmakher 

H
Holender 

I
Ialovskaia 
Ialovskii 
Iavlenskaia 
Ioksimovich 
Ioselovich 
Iskander 
Istomin 
Iunter 
Iushkevich 
Ivanov 

K
Kalandarishvili 
Kamarauskas 
Kasianenko 
Kenin 
Khanina 
Khavin 
Kheifets 
Khitrovo 
Khmelnitskii 
Khodkevich 
Khripunov 
Khripunova 
Kintsel 
Kiselow 
Kitaev 
Klopov 
Koliabskaia 
Kologrivov 
Kologrivova 
Komarnitskaia 
Komarov 
Komarovski 
Komarovskii 
Komerovskaia 
Konchin 
Konfer 
Konkin 
Konn 
Konstantinov 
Konstantinova 
Korchagina 
Korchinskaia 
Kosmachevskaia 
Kosovskaia 
Kotko 
Kovalevski 
Kozerskaia 
Kozerski 
Kozlow 
Kozyrskii 
Kriukov 
Kulikovskaia 
Kunitskaia 
Kupchenko 
Kuzmin 

L
Lebel 
Lempitskaia 
Lenevski 
Leontiev 
Lerche 
Levanda 
Levinson 
Levitan 
Levkov 
Levkova 
Likharev 
Likhareva 
Lipinskii 
Lishin 
Lisitskaia 
Lisovskii 
Lukowskaia 

M
Magnovska 
Mahkno 
Maier 
Makarova 
Maklakov 
Maksimov 
Malakhovskii 
Maletski 
Maletskii 
Malinovskii 
Maliszewski 
Maliszkewicz 
Malitzka 
Malitzkii 
Malygin 
Markevich 
Masalsky 
Maslov 
Massalsky 
Matsevich 
Matsevichus 
Matskevich 
Mattel 
Matulevich 
Mayer 
Medvedev 
Medvedeva 
Meier 
Melnikov 
Menshutkin 
Menzhinskii 
Mezentsov 
Mezentsova 
Mikhailov 
Milaszewicz 
Milaszewska 
Milaszewski 
Milkovich 
Milodanovich 
Milosz 
Miloszinski 
Mionchinskaia 
Mirskii 
Misostov 
Miziukov 
Molchanov 
Molotkoff 
Morozov 
Mosalsky 
Moskvin 
Moszynski 
Mozheika 

N
Nazilevskii 
Nebogatov 
Negnevitskii 
Nevelskoi 
Nikonechnaia 
Nisselovich 

O
Oborskaia 
Oborski 
Okecka 
Okkerman 
Olendzskaia 

P
Pankov 
Panushkis 
Parnes 
Parolow 
Paulson 
Pavlovskii 
Pechatnoff 
Petrov 
Petrovskaia 
Petrovskii 
Petrowa 
Piotrovskii 
Pletner 
Plotnitskaia 
Pogoretskaia 
Pogorzelski 
Polivanov 
Polovinkin 
Ponomarev 
Popova 
Popovtsev 
Posiet 
Potemkin 
Pravdin 
Priselkov 
Prokofiev 
Prokopchenko 
Prokopovich 
Pruszynski 
Pumpianskii 
Putilina 

R
Rakhmelevich 
Reikhman 
Reznikov 
Reznikova 
Rodwalski 
Rogusskii 
Rokitskaia 
Roschin 
Rosenthal 
Rowan 
Rusakov 
Rusakova 

S
Saburova 
Seidin 
Semenov 
Shalberov 
Shchepetov 
Shcherbatov 
Shereshevski 
Sheridan 
Shikov 
Shiritlokov 
Shkarov 
Shponarskaia 
Shtadler 
Shtein 
Shubovich 
Shuliakovskii 
Shulkovskii 
Shumakher 
Shvarts 
Siegel 
Simonovich 
Simson 
Siniakov 
Sipiagin 
Sivortsova 
Skipetroff 
Skipetrova 
Slavin 
Slavina 
Smolenskaia 
Smolenskii 
Sobeskaia 
Sobetskaia 
Sokolovskii 
Solomon 
Soloviev 
Somov 
Somova 
Sotravits 
Spektor 
Speshiloff 
Stanevich 
Steinhauer 
Steinheil 
Stenghel 
Stepunin 
Sukhodolskaia 
Sverzhenskii 

T
Talkovskaia 
Tamashevska 
Tereshchenko 
Tetiukov 
Tokmakoff 
Tomilin 
Topczewski 
Topezuvjw 
Topezuvjwa 
Trambetskaia 
Treshchev 
Trombetskaia 
Trubachev 
Trzemin 
Trzheminska 
Tsarev 
Tselikova 
Tsert 
Tsitov 
Turets 
Turetskii 

U
Ukhtomskii 
Umanskii 

V
Vans 
Vargunin 
Vasiliev 
Veis 
Veksler 
Verbukh 
Verden 
Veretennikov 
Vershvovski 
Vikentieva 
Vladimirskii 
Volynski 
Vorobiev 

W
Weinstein 
Werner 
Wittenburg 
Wolkowicz 
Wolowitz 
Worden 

Y
Yakunun 
Yunter 

Z
Zalesskii 
Zalicker 
Zeif 
Zelecker 
Zelichonok 
Zhalobovskaia 
Zheldak 
Zhelobovskaia 
Zilberman 
Zubkin 
Zukov 
Zukowskaia 
Zukowski
"""

FEMALE_FIRST_NAMES_RUSSIA = u"""

Adla
Adleida
Adlesha
Adleta
Adviga
Afanasiia
Afanasiya
Afimia
Afonaseva
Agafia
Agafiia
Agafiya
Agafokliia
Agafonika
Agafya
Agapiia
Agasha
Agashka
Aglaia
Aglaida
Aglaya
Agna
Agnessa
Agnia
Agniia
Agrafena
Agrafina
Agramakova
Agripena
Agripina
Agrippa
Agrippina
Aitugan
Aizdiakova
Akillina
Akiulina
Aksana
Aksinya
Alasa
Albena
Albina
Aleksandra
Alena
Alenka
Alexandra
Alexcia
Alexia
Alexis
Alina
Alma
Alona
Alyssa
Alzbeta
Amelfa
Ampliia
Ana
Anastasia
Anastasiia
Anastasija
Anatassia
Andreea
Andreeva
Andreiana
Andrievicha
Anechka
Aneska
Anfiia
Anfoma
Anfusa
Angelika
Angelina
Angusta
Ania
Animaida
Animaisa
Anina
Anisia
Anisiia
Anisiya
Anisya
Anitchka
Anitsa
Anizka
Anja
Anje
Anjelica
Anjelika
Anka
Ann
Anna
Annastasija
Antonidka
Antonina
Anusia
Anya
Anzhela
Apfiia
Apolinaria
Apolinariia
Apoloniada
Apolosakifa
Ariadna
Arina
Arkhipa
Arkhippa
Artemeva
Artemiia
Asenka
Askitreia
Askitriia
Asya
Augusta
Avdeeva
Avdiushka
Avdotia
Avgusta
Avramova
Baialyn
Baibichia
Bakhteiarova
Balbara
Barbara
Bazhena
Bedche
Bela
Beleka
Belgukovna
Belka
Bella
Belukha
Benka
Bezruchka
Bezubaia
Bezui
Biana
Biata
Bibishkina
Biiata
Biriuta
Blanka
Blausa
Bogdana
Bogukhvala
Bogumezt
Bogumila
Boguslava
Bohdana
Bohumile
Boika
Bolce
Boldina
Bolemila
Boleslava
Bolgarina
Bolgarynia
Bona
Borisova
Boriuta
Bozena
Bozhana
Bozhitsa
Bragina
Branislava
Branizlawa
Bratomila
Bratromila
Bratrumila
Bruna
Budisla
Budizla
Budshka
Budska
Bukhval
Calina
Catarina
Caterina
Catherine
Catina
Catreen
Catrin
Catrina
Catrinia
Catriona
Catryn
Cecislava
Charlotta
Chebotova
Chekhina
Chekhyna
Cheliadina
Chemislava
Chenka
Chernavka
Chernislava
Chernka
Chesislava
Chimislava
Chiona
Chiudka
Chobotova
Chynica
Ciernislava
Clavdia
Cyzarine
Czarina
Czeimislawa
Dalida
Daliunda
Dama
Danilova
Daria
Darina
Daritsa
Darja
Daromila
Darya
Dasha
Datja
Davyd
Davyzha
Davyzheia
Debora
Deda
Dedenia
Dekava
Dekhova
Demidova
Denicha
Deretka
Derska
Derzhena
Derzhka
Desa
Desha
Despa
Dessa
Desta
Detana
Detava
Deva
Devka
Devochka
Devochkina
Devora
Dikana
Dima
Dimitra
Dimut
Dina
Dinah
Dinara
Dmitreeva
Dmitrieva
Dmitrovna
Dobegneva
Dobislava
Dobka
Dobra
Dobrava
Dobreva
Dobromila
Dobroslava
Dobrowest
Dobryna
Doda
Domaslava
Dominika
Domka
Domna
Domnika
Domnikiia
Domnina
Domona
Dorofeia
Doroteya
Dosya
Dounia
Dozene
Dozhene
Draginia
Dragomira
Dragoslawa
Dragushla
Draia
Drga
Drosida
Druzhinina
Dubrava
Dubravka
Duklida
Dunya
Dunyasha
Duscha
Dusha
Dusya
Dvora
Ecatarina
Ecatrinna
Eda
Edviga
Edviva
Efdokia
Effimia
Efimia
Efiopskaia
Efrasiia
Efrosenia
Efrossina
Ekatarina
Ekaterina
Ekatrinna
Ekzuperiia
Elacha
Eleena
Elen
Eleni
Elenya
Elga
Elgiva
Eliaksha
Elikonida
Elina
Elisava
Elisaveta
Elissa
Elizabeth
Elizarova
Elizaveta
Ella
Ellena
Ellina
Elonka
Elzbeta
Elzhbeta
Ennafa
Epestemiia
Epikhariia
Epistima
Eretiia
Ermolina
Erotiida
Ertugana
Esineeva
Euafina
Eufemia
Eugenia
Euprakseia
Eupraksiia
Eva
Evanova
Evdokeia
Evdokia
Evdokiia
Evdokiya
Evdokseia
Evdoksiia
Evelina
Evfaliia
Evfrasiia
Evfroseniia
Evfrosinya
Evgenia
Evgeniia
Evgeniya
Evgenya
Evginia
Evguenia
Evpraksi
Evpraksiia
Evrosena
Evseevskaia
Evsegniia
Evseveia
Evseviia
Evstoliia
Evtropiia
Faina
Fanaila
Fanya
Fatianova
Fausta
Favsta
Fayina
Fedia
Fedka
Fedkina
Fedora
Fedoritsa
Fedorka
Fedorova
Fedosia
Fedosiia
Fedosya
Fedotia
Fedotiia
Fedya
Feia
Feiniia
Fekla
Feklitsa
Fenia
Feodora
Feodosia
Feodosiia
Feoduliia
Feofana
Feoklita
Feoktista
Feona
Feonilla
Feopimta
Feopista
Feopistiia
Feozva
Ferfufiia
Ferufa
Fesalonikiia
Fetenia
Fetinia
Fetiniia
Fevronia
Filikitata
Filippiia
Filitsata
Filofei
Filofinaia
Filonilla
Fimochka
Fiva
Fiveia
Foimina
Fokina
Fomina
Fotina
Fotiniia
Fovro
Fovroneia
Frolova
Frosiniia
Gadina
Gaianiia
Gala
Galenka
Gali
Galina
Galina
Galine
Galochka
Galya
Galyna
Gamana
Gana
Gananiia
Gandaza
Ganna
Gasha
Gema
Genka
Georgieva
Gertruda
Ginechka
Giurgevaia
Gizheurann
Gizla
Glafira
Glasha
Glebovicha
Glikeriia
Glikeriya
Glukeriia
Glukheria
Godava
Golindukha
Goltiaeva
Golubitsa
Gordislava
Gorislava
Gorshedna
Gostena
Gostenia
Gostiata
Gostimira
Goulislava
Govdela
Gravriia
Grekina
Grekinia
Grekyna
Grifina
Grigoreva
Grigorevna
Grigorieva
Groza
Gruba
Grunya
Grusha
Halyna
Helen
Helena
Helenka
Helga
Hema
Henka
Hinezka
Hinica
Hodawa
Hora
Horina
Hosche
Hostena
Hruoza
Iadviga
Iakova
Iakovleva
Iakovlevskaia
Iakun
Iakunova
Iakunovaia
Ianevaia
Ianisha
Ianishe
Ianka
Iarche
Iarena
Iarina
Iarogned
Iaroia
Iarokhna
Iaroslava
Iarshek
Iasynia
Ieliaia
Iev
Ievlia
Ifrosenia
Ignateva
Ignatevskaia
Igoshkova
Iia
Ilariia
Ilia
Ilina
Ilya
Inessa
Inkena
Inna
Ioanna
Iona
Iosifova
Iovilla
Ira
Iraida
Irena
Irene
Irina
Irinia
Irinka
Irisa
Irodia
Irodiia
Isakova
Isidora
Ismagrad
Itka
Iudita
Iuliana
Iuliania
Iulianiia
Iuliia
Iulita
Iulitta
Iuniia
Iurevna
Iustina
Ivana
Ivanova
Ivanovskaia
Iveska
Ivonne
Iziaslava
Izmaragd
Janna
Jarena
Jarene
Jarohna
Jekaterina
Jelena
Jelena
Jelizaveta
Jenica
Jeremia
Jevdokija
Jitka
Julia
Kace
Kacha
Kache
Kachka
Kala
Kaleria
Kaleriia
Kalia
Kalisa
Kalisfena
Kalista
Kalitina
Kallisfeniia
Kallista
Kamenka
Kamle
Kandaza
Kapetolina
Kaptelina
Karen
Karina
Karine
Karinna
Karolina
Karpova
Karpovskaia
Karrine
Karyna
Kasha
Kashka
Kata
Katalena
Katareena
Katarina
Kateena
Katerina
Katerinka
Katherina
Katherine
Katia
Katina
Katinka
Katiya
Katja
Katlina
Katreen
Katreena
Katrene
Katria
Katrien
Katrina
Katrine
Katrusha
Katrya
Katryn
Katryna
Kattrina
Kattryna
Katunia
Katuscha
Katya
Katyenka
Katyushka
Katyuska
Kazdoia
Kerkira
Kharesa
Khariessa
Kharitaniia
Kharitina
Kharitona
Kharitonova
Kheoniia
Khioniia
Khlopyreva
Khovra
Khrana
Khrisiia
Khristeen
Khristen
Khristianova
Khristin
Khristina
Khristine
Khristyana
Khristyna
Khrstina
Khrystina
Khrystyn
Khrystyne
Khvalibud
Khynika
Kikiliia
Kilikeia
Kilikiia
Kiprilla
Kira
Kiraanna
Kiriakiia
Kiriena
Kirilla
Kirilovskaia
Kisa
Kiska
Kitsa
Kittiana
Kiuprila
Kiuriakiia
Kiza
Klasha
Klavdiia
Kleopatra
Klychikha
Knikki
Kogorshed
Koia
Koika
Kolomianka
Konchaka
Konchasha
Konkordiia
Konstantiia
Konstiantina
Konstiantinova
Kora
Koretskaia
Korina
Korotkaia
Korotkova
Korotsek
Korotskovaia
Kosa
Kosenila
Kostenka
Kostya
Kostyusha
Kotik
Kovan
Kovana
Kowan
Kozma
Kozmina
Krabava
Krasa
Krestiia
Kristina
Krivulinaia
Krunevichovna
Krushka
Ksafipa
Ksana
Ksanfippa
Ksanochka
Ksenia
Kseniia
Kseniya
Ksenya
Kshtovtovna
Ksnia
Ksniatintsa
Kudra
Kuna
Kunei
Kunka
Kunko
Kunku
Kuntse
Kuriana
Kuznetsova
Kvasena
Kvetava
Kzhna
Lacey
Lacey
Lada
Laikina
Lala
Lanassa
Lanka
Lara
Lari
Larina
Larisa
Larissa
Larissa
Larochka
Larra
Laryssa
Latskaia
Leia
Leka
Lelik
Lena
Lenina
Lenochka
Lenora
Lenusy
Lenusya
Leonilla
Leonteva
Lepa
Lera
Lerka
Leva
Liba
Libania
Libusa
Lida
Lidena
Lidia
Lidiia
Lidija
Lidiy
Lidiya
Lidka
Lidmila
Lidocha
Lidochka
Lieba
Lila
Lilac
Lilia
Liolya
Lipa
Lisa
Lisanka
Lisaveta
Liseetsa
Lishka
Lisil
Liska
Lisotianka
Liuba
Liubchanina
Liubka
Liubokhna
Liubone
Liubusha
Liudena
Liudmila
Liunharda
Liutarda
Liutsilla
Liza
Lizabeta
Lizanka
Lizette
Ljudmila
Ljudmilla
Lolya
Lotta
Luba
Lubachitsa
Lubmila
Lubmilla
Lubohna
Lubov
Lubusha
Luda
Ludiia
Ludmia
Ludmila
Ludmilla
Ludomia
Luka
Lukeria
Lukerina
Lukerya
Lukiia
Lukina
Lukiria
Lukoianova
Lvovicha
Lyalechka
Lyalya
Lybed
Lydia
Lyeta
Lyuba
Lyubochka
Lyubonka
Lyubov
Lyudmila
Lyudmilla
Lyuha
Lyutsiana

Machko
Machna
Magdalina
Magmeteva
Maiya
Makhna
Makrina
Maksimina
Maksimova
Malana
Malania
Maliusha
Maliuta
Malka
Malona
Malonia
Maluchka
Malusha
Mamelfa
Mamika
Mana
Manechka
Manka
Manya
Mara
Marana
Maremiana
Marfa
Marfutka
Margarita
Margo
Maria
Marian
Marianna
Marianne
Marianskaia
Maricha
Marichinich
Mariia
Marimiana
Marina
Marinka
Marinochka
Marinskaia
Marionilla
Marisha
Maritanna
Maritsa
Marjka
Marka
Markiana
Marnie
Marous
Marta
Martemianova
Marufa
Marulia
Marusya
Marya
Mascha
Masha
Mashenka
Matfeitsa
Matrena
Matrona
Matruna
Matryoshka
Mavra
Maya
Mazcho
Melania
Melaniia
Meletina
Melita
Melitina
Menshikova
Mergivana
Merkureva
Miesha
Mika
Mikhaila
Mikhailova
Mikitina
Mikula
Mikulina
Mila
Milakhna
Milana
Milata
Milava
Milehva
Milekha
Milena
Milenia
Milesa
Mileva
Miliia
Milika
Militsa
Milka
Milleise
Milohna
Milokhna
Miloslava
Miloushka
Miluska
Minodora
Mira
Mirena
Mironova
Miropiia
Miroslava
Mirozlava
Mirra
Misha
Mitrodora
Mizinovskaia
Mlada
Moiko
Morava
Morawa
Mounya
Mousia
Mozyr
Mstislava
Mstislavliaia
Mudri
Muniia
Mura
Muroniia
Muza
Myrra
Myshka
Myslna
Nadeek
Nadeekovaia
Nadejda
Nadenka
Nadia
Nadie
Nadine
Nadiya
Nadja
Nadjenka
Nadya
Nadyenka
Nadysha
Nadyuiska
Naglaya
Na'Kesha
Nakita
Narkissa
Nastasia
Nastasich
Nastasiia
Nastasja
Nastassia
Nastenka
Nastia
Nastiona
Nastionka
Nastiusha
Nastka
Natachia
Natacia
Natalia
Nataliia
Natalja
Natalka
Natalya
Natascha
Natasha
Natashenka
Natashia
Natasia
Natassia
Nathasha
Nazarova
Nebracha
Nebraga
Neda
Nedana
Nedelia
Nekrasa
Nekrasia
Neliuba
Nemilka
Nemka
Neonila
Nesdits
Nesha
Nessa
Nesy
Neta
Netka
Neva
Neza
Nezhatok
Nezhdakha
Nezhka
Nifantova
Nika
Niki
Nikiforova
Nikita
Nikitina
Nikkylia
Nikolena
Niksha
Nimfodora
Nina
Ninel
Ninockha
Ninotchka
Nitasha
Nitca
Nona
Nonna
Nostasia
Nunekhiia
Nyura
Nyusha
Obrezkova
Odigitriia
Odintsova
Ofce
Ofimia
Ogafia
Ogafitsa
Ogashka
Ografena
Ogrifina
Ogrofena
Ogrufena
Ogrufina
Okinfieva
Oksana
Oksana
Oksanochka
Okseniia
Oksinia
Oksiutka
Oktyabrina
Okulina
Olechka
Oleksandra
Olena
Olenitsa
Olenka
Olfereva
Olga
Olginitsa
Olgirdovna
Olgov
Olimpiada
Olisava
Olivera
Olkha
Olya
Olzhbeta
Omelfa
Ondreiana
Onoslava
Ontonia
Ontsiforova
Ontsyforova
Oprosiniia
Orenka
Oria
Orina
Orlenda
Orlitza
Orsha
Orshinaia
Ortemeva
Orya
Osipova
Osliabia
Ostafia
Ostankova
Ostashkova
Osyenya
Ovdeeva
Ovdiukha
Ovdokea
Ovdotia
Ovdotitsa
Ovtsa
Oxana
Paladia
Palasha
Panfilova
Pansemna
Pantislava
Pantyslawa
Panya
Paraaha
Paramona
Parasha
Parasia
Paraskova
Paraskovga
Paraskovgiia
Paraskovia
Paraskoviia
Paroskova
Pasha
Patrova
Paula
Paulina
Pauline
Pavel
Pavla
Pavlova
Pavloveia
Pavlusha
Pchuneia
Pechta
Pelaga
Pelageia
Pelageya
Pelagiia
Perchta
Peredeslava
Perkhta
Perkhte
Perpetuia
Petronila
Petrova
Petrovna
Petsa
Peza
Pheodora
Piama
Piina
Piminova
Pirueva
Plakida
Platonida
Pokinaria
Poladia
Polazhitsa
Polia
Polikseniia
Polinaria
Poliuzhaia
Poloneika
Polotsk
Polotska
Poloudnitsa
Polovinova
Pomnislavka
Pompliia
Ponaria
Popliia
Popova
Poroskova
Poved
Praskovja
Praskovya
Prebrana
Predslava
Predyslava
Preia
Preksedys
Premislava
Prepedigna
Presthlava
Priba
Pribyslava
Priia
Prikseda
Priskilla
Priskula
Proksha
Proniakina
Prosdoka
Proskudiia
Przhibislava
Przybyslawa
Pukhleriia
Pulkheriia
Puna
Puteshineia
Putok
Putokoveia
Rada
Radia
Radivilovna
Radka
Rado
Radok
Radokhna
Radokovaia
Radonia
Radosha
Radoslava
Radosta
Radoste
Radozte
Radslava
Ragneda
Ragosna
Rahil
Raina
Raisa
Raiza
Rajna
Rakhiel
Ratka
Ratslava
Raya
Rechkina
Reicza
Reshunda
Richca
Richica
Richika
Richikha
Richtca
Richza
Riksa
Rima
Ripsimia
Rislava
Rita
Rogned
Roksana
Romanovna
Roscislawa
Roslava
Rossitza
Rostislava
Roza
Rozalia
Rozgneda
Rozhneva
Rufina
Rulza

Rusa
Rusna
Ryska
Sabina
Sacha
Sahsha
Samarina
Sanya
Sapozhnika
Sascha
Sashah
Sashana
Sashenka
Sashenka
Sashia
Sashka
Sausha
Savastian
Savastianova
Sbyslava
Selianka
Selivankov
Selivankova
Semenova
Semenovskaia
Semislava
Senia
Senny
Serafima
Sevastianiia
Sevastiiana
Severina
Sfandra
Shasha
Shcastna
Shchastna
Shedra
Shelovlevaya
Shiriaeva
Shkonka
Shura
Shushanika
Shvakova
Sidorova
Sima
Sina
Sinklitikiia
Siny
Sira
Siuiunbek
Siuiunbeka
Siuiunbuka
Siunbek
Siunbeka
Skameikina
Skonka
Slava
Slavna
Smils
Smina
Smirenka
Snanduliia
Snigurka
Sobina
Sofeia
Sofia
Sofiia
Sofiya
Sonaya
Sonechka
Sonia
Sonia
Sonja
Sonya
Sonyuru
Sonyusha
Sonyushka
Sophi
Sophia
Soroka
Sosanna
Sosfena
Sosipatra
Spasenieva
Spera
Spitoslava
Spitsislava
Stana
Stanislava
Stanka
Starsha
Stasy
Stasya
Stefanida
Stefanidka
Stefanova
Stefanya
Stepanida
Stepanova
Stephania
Stepka
Stesha
Stolma
Stolpolcha
Stopolcha
Stranizlava
Stratka
Strezhena
Strezhislava
Strezislava
Sudehna
Sudekhna
Sudila
Sulislava
Sumorokova
Sunklitikiia
Susana
Svakhna
Svatata
Svatava
Svatochna
Svatohna
Sveisla
Sveta
Svetlana
Svetocha
Svetokhna
Sviatata
Sviatokhna
Sviatoslava
Svoda
Swachnina
Swatawa
Symislava
Syp
Sypovaia
Tacha
Tachia
Tachiana
Tachianna
Tahn
Tahna
Tahnia
Tahniya
Tahnya
Tahsha
Taidula
Taina
Taisha
Taishineia
Taisiia
Tamara
Tamary
Tamera
Tamra
Tamryn
Tana
Tanalia
Tanasha
Tanaya
Tandula
Tanea
Tanechka
Taneya
Tania
Tanija
Tanita
Taniya
Tanja
Tanka
Tanna
Tannia
Tannis
Tanniya
Tannya
Tanya
Tasenka
Tasha
Tashana
Tashia
Tashiana
Tashianna
Tashina
Tashira
Tashiya
Tassa
Tasya
Tata
Tatiana
Tatianka
Tatianna
Tatiiana
Tatjana
Tatsa
Tatyana
Taunia
Taunya
Tavlunbeka
Tawnia
Tayna
Tazia
Teha
Tekh
Tekha
Tekusa
Tesheia
Teshka
Tetka
Tevkel
Tferianka
Thais
Thasha
Tiaga
Tina
Tishka
Tishkina
Titania
Titka
Tiutcheva
Tomila
Tomislava
Tonasha
Tonaya
Tonechka
Tonia
Tonja
Tonniya
Tonnya
Tonya
Torokanova
Toshiana
Tretiakovskaia
Troika
Trpena
Trufena
Tsaritsa
Tsvetkova
Tulna
Tutana
Tvoislava
Tvoyzlava
Ualentina
Uirko
Ulana
Uleia
Ulen'ka
Ulia
Uliaanitsa
Uliana
Ulianiia
Ulianka
Ulianushka
Uliasha
Uliiana
Ulita
Ulyana
Unefiia
Unka
Upritsa
Urshila
Ursula
Ustenia
Ustiniia
Vakhneva
Vakhtina
Valenta
Valentina
Valya
Vania
Vanmra
Vanya
Varenka
Varka
Varsonofia
Vartsislava
Varushka
Varvara
Varya
Varyusha
Vasileva
Vasilevna
Vasilevskaia
Vasilida
Vasilievaia
Vasilii
Vasilina
Vasilisa
Vasilissa
Vasilista
Vasisa
Vassa
Vassillissa
Vasya
Vaviia
Velika
Velislava
Ventseslava
Vera
Verochka
Veronika
Veronikeia
Vershina
Veruschka
Vetenega
Veveia
Viachenega
Victoria
Vida
Vika
Vikashenka
Viktoria
Viktoriya
Vila
Vilena
Vilenina
Vilma
Vilna
Virineia
Vironikiia
Vishemila
Vitalya
Vitasa
Vitko
Vitla
Vitoslava
Vivka
Vlada
Vladaia
Vladilena
Vladilenaova
Vladimira
Vladisava
Vladka
Vladlena
Vlaikha
Vlastika
Vlcena
Vlschet
Vogna
Voina
Voislava
Volodimerna
Volotka
Volotkoveia
Volotok
Vonda
Voyzlava
Vrata
Vratislava
Vrkhuslava
Vrotsislava
Vrsanka
Vseslava
Vukosava
Vukoslava
Vyesna
Vysheslava
Vyshia
Wannon
Warvara
Wava
Welislawa
Wierga
Wissa
Witoslava
Wiwka
Wladyka
Woina
Wrata
Wratislava
Wrocislawa
Xenia
Yalena
Yalenchka
Yalens
Yekaterina
Yelena
Yeva
Yevdokiya
Yevfrosinya
Yevgenya
Yogenya
Yovanka
Yulenka
Yulia
Yulianiya
Yulika
Yuliy
Yuliya
Yulya
Yusmara
Zabela
Zakharia
Zakharieva
Zakharina
Zamiatina
Zaneta
Zaritsa
Zasha
Zavidovicha
Zavorokhina
Zbina
Zbinka
Zbiska
Zbynek
Zbynko
Zbyshka
Zdena
Zdeslava
Zdislava
Zdzislaba
Zena
Zenaida
Zenaide
Zenechka
Zenochka
Zeny
Zenya
Zhanna
Zhdana
Zhena
Zhenya
Zhirava
Zhivana
Zhona
Zhonka
Zima
Zina
Zinaida
Zinerva
Zinoviia
Znata
Zofeia
Zoia
Zoika
Zoya
Zoyenka
Ztrezena
Zvatata
Zvenislava


"""

MALE_FIRST_NAMES_RUSSIA = u"""
Adrik
Akim
Alek
Aleksandr
Aleksi
Aleksis
Alexei
Alik
Aloyoshenka
Aloysha
Anatolii
Andrei
Andrusha
Andrya
Anstice
Antinko
Anton
Antosha
Arman
Avel
Bogdashha
Bohdan
Bolodenka
Boris
Boris
Boris
Borya
Boryenka
Brends
Brody
Burian
Cheslav
Czar
Danya
Demyan
Dima
Dimitri
Edik
Eduard
Egor
Egor
Evgenii
Fabi
Faddei
Fadey
Fadeyka
Fedor
Fedya
Fedyenka
Feliks
Filip
Fjodor
Fjodor
Foma
Fredek
Fyodor
Ganya
Gav
Gavrel
Gavrie
Gavril
Gavril
Gavrilovich
Gennadi
Gregori
Grigor
Grigori
Grigorii
Grisha
Hedeon
Helge
Igor
Igoryok
Ilya
Ioakim
Iov
Ivan
Ivano
Jascha
Jasha
Jeirgif
Jermija
Jov
Jurg
Karolek
Kiril
Kirill
Kliment
Konstantin
Konstantine
Kostya
Laurente
Leonide
Lev
Levka
Luka
Lukyan
Maks
Maksim
Maksimillian
Marko
Markov
Matvey
Matysh
Maxim
Michail
Mikhail
Mikhail
Misha
Mishe
Moriz
Motka
Naum
Nicolai
Nikolai
Oleg
Oleg
Olezka
Ony
Oral
Orel
Orell
Oriel
Orrel
Osip
Pabiyan
Pavel
Pavel
PavIpv
Pavlik
Pavlo
Pavlusha
Pavlushka
Pavlya
Petenka
Petrov
Petya
Pyotr
Roman
Romochka
Rurik
Rurik
Sacha
Sacha
Sanya
Sasha
Semyon
Serge
Sergei
Serguei
Seriozha
Seriozhenka
Sevastian
Shashenka
Shura
Shurik
Shurochka
Slavik
Stanislov

Stefan
Stephan
Stepka
Tamryn
Tasha
Tolenka
Tolya
Tosya
Tusya
Uri
Uriah
Urie
Ustin
Vadim
Valerii
Valerik
Vanechka
Vanya
Vanyusha
Vas
Vasilii
Vasily
Vassi
Vassily
Vasya
Viktor
Vitaliy
Vitenka
Vladik
Vladilen
Vladilen
Vladislav
Vladmir
Vladmiri
Vladya
Volody
Vyacheslav
Yakov
Yaremka
Yasha
Yefrem
Yerik
Yevgeni
Yura
Yuri
Yurii
Yurik
Yurochka
Zhenechka
Zhenya
Zhorah
Ziven
Zivon
Zory
"""

LAST_NAMES_RUSSIA = Cycler(splitter1(LAST_NAMES_RUSSIA))
MALE_FIRST_NAMES_RUSSIA = Cycler(splitter1(MALE_FIRST_NAMES_RUSSIA))
FEMALE_FIRST_NAMES_RUSSIA = Cycler(splitter1(FEMALE_FIRST_NAMES_RUSSIA))

