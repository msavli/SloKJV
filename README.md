# SloKJV
## Sveto pismo kralja Jakoba (1769) v slovenščini

![Knjiga](slike/Slika_knjige_v_perspektivi_transparent_400.png?raw=true "400e")

## *Slovensko / Slovenščina*

Projekt prevoda **Svetega pisma kralja Jakoba** iz angleškega v slovenski jezik je potekal od maja 2010 do maja 2022. Prevedenih je 66 knjig. Sedaj poteka lektoriranje in odprava napak.

Prevedene knjige: Geneza do Malahija in celotna Nova Zaveza.

### Posebnosti prevoda:
 - dodane opombe in reference iz KJV 1611,
 - dodane približne letnice dogodkov; KJV Oxford 1769,
 - »nagnjene« besede so dodane izvirnem KJV besedilu,
 - »<sup>a</sup>« opombe KJV 1611 in opombe prevajalca,
 - »<sub>b</sub>« sklici na druge dela besedila,
 - »[ ]« dodala prevajalca, ni v originalu KJV,
 - »§« razlika besedila SloKJV od ostalih slovenskih prevodov,
 - Jezusove besede izpisane z rdečo (Android verzija).
 
Viri: [Angleško besedilo](http://www.crosswire.org/~dmsmith/kjv2006/), [Opombe in reference](https://www.kingjamesbibleonline.org/Genesis-Chapter-1_Original-1611-KJV/) in [biblija.net](http://www.biblija.net/biblija.cgi?m=&id13=1&id7=1&pos=0&set=6&l=sl).

Prevajanje je potekalo v programu [Notepad++](https://notepad-plus-plus.org/) kjer je slovensko besedilo in pod njim angleško. Potem se s skripto to pretvori v OSIS obliko - XML datoteko, ki je objavljena na tej strani. XML datoteko se potem pretvori v Sword modul, ki je dostopen na spletni strani [Crosswire.org](http://www2.crosswire.org/sword/modules/).

### Datoteke programi in naprave:
Sveto pismo lahko berete s pomočjo enega izmed teh naprav ali programov:
 - [Preglednica programov na crosswire.org za Windows, Mac, Linux, Andorid, iPhone, iPad](http://wiki.crosswire.org/Choosing_a_SWORD_program)
 #### Izvorna datoteka 
 - [`SloKJV_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloKJV_sword.xml) (glavna datoteka s prevodom; XML SWORD oblika za [Crosswire.org](https://crosswire.org/sword/modules/ModInfo.jsp?modName=SloKJV))
 - [`slokjv.conf`](https://github.com/msavli/SloKJV/blob/master/slokjv.conf) (konfiguracija za [`SloKJV_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloKJV_sword.xml))
 #### Windows
 - [Xiphos](https://xiphos.org/)
 - [Windows e-sword](https://www.e-sword.net/) ([`SloKJV.bblx`](https://github.com/msavli/SloKJV/blob/master/SloKJV.bblx) odložiti v mapo: c:\Program Files (x86)\e-Sword)
 #### Android
 - [AndBible](https://play.google.com/store/apps/details?id=net.bible.android.activity) namestitev je avtomatična. Za ročno namestitev datoteko [`Android_data_net.bible.android.activity_files.zip`](https://github.com/msavli/SloKJV/blob/master/Android_data_net.bible.android.activity_files.zip) razpakirati v mapo `\\Android\data\net.bible.android.activity\files`)
 - [Mysword for Android](https://www.mysword.info/download-mysword) ([`SloKJV.bbl.mybible`](https://github.com/msavli/SloKJV/blob/master/SloKJV.bbl.mybible) odložiti v mapo [`/storage/emulated/0/mysword/bibles`])
 - [MyBible](https://mybible.zone/) ([`SloKJV.sqlite3`](https://github.com/msavli/SloKJV/blob/master/SloKJV.sqlite3) je potrebno ročno namestiti)
 #### iPhone
 -  [PocketSword](https://apps.apple.com/us/app/pocketsword/id341046078)
 #### Java telefoni
 -  [GoBible](https://github.com/msavli/SloKJV/blob/master/slokjv.jar) (Za stare Java MIDP 2.0 telefone; SLO-ENG KJV z opombami in referencami; datoteki [`slokjv.jad`](https://github.com/msavli/SloKJV/blob/master/slokjv.jad) in [`slokjv.jar`](https://github.com/msavli/SloKJV/blob/master/slokjv.jar) je potrebno ročno namestiti)
 #### Palm
 - [Palm Bible+](https://palmbibleplus.sourceforge.net/) ([`SloKJV.pdb`](https://github.com/msavli/SloKJV/blob/master/SloKJV.pdb) je potrebno ročno namestiti)
 #### ePUB
 - [`SloKJV.epub`](https://github.com/msavli/SloKJV/blob/master/SloKJV.epub) (Kindle, KoboPDF, e-bralniki)
 #### VideoPsalm
 - [VideoPsalm](https://myvideopsalm.weebly.com/) [`SloEngKJV_VideoPsalm_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloEngKJV_VideoPsalm_sword.xml) uvoziti v program VideoPsalm, ki se uporablja za prezentacijo na platno v cerkvah. Vsaka biblijska vrstica je v slovenščini in pod njo še v angleščini
 #### Online (ni vedno zadnja verzija SloKJV)
 - [Aionianbible.org](https://www.aionianbible.org/Bibles/Slovene---Slovene-Savli-Bible)
 - [StepBible.org](https://www.stepbible.org/version.jsp?version=SloKJV)
 #### PDF
 - [PDF - en stolpec]( https://github.com/msavli/SloKJV/blob/master/SloKJV.pdf) ([Stephan Kreutzer](https://skreutzer.de/) je s svojim projektom [Free Scriptures](http://www.free-scriptures.org/index.php?page=downloads), [ver: 2019_07_31](http://www.free-scriptures.org/downloads/free-scriptures_gnu_20190731.zip) pomagal narediti prvo PDF verzijo.)
 - `SloKJV*.pdf` (PDF datoteke za tisk)

### Papirni izvod SloKJV
![Knjiga](slike/Slika_knjige_v_perspektivi_transparent_150.png?raw=true "150e")
 Sveto pismo je tiskano z digitalnim tiskom na 60g papir z broširano vezavo. Sta dva založnika, toda isti digitalni stroji, na katerih se 800 stranska Sveta pisma tiskajo (lulu.com).
  - Hojkar-Šavli: Do meseca meseca maja 2024 bo predvidoma dobava stekla. Naročite ga s [klikom](mailto:marjan.savli@gmail.com?subject=SloKJV–Narocilo&body=%0ASpostovani%21%0A%0ANa%20voljo%20so%20brosirane%20vezave%3A%0A%0A%20%2D%20%281%29%20SloKJV%20%28A4%2C%20%20trde%20%20platnice%2C%20velikost%20pisave%2012%2C5%29%0A%20%2D%20%282%29%20SloKJV%20%28A4%2C%20%20mehke%20platnice%2C%20velikost%20pisave%2012%2C5%29%0A%20%2D%20%283%29%20SloKJV%20%28A5%2B%2C%20trde%20%20platnice%2C%20velikost%20pisave%2010%29%0A%20%2D%20%284%29%20SloKJV%20%28A5%2B%2C%20mehke%20platnice%2C%20velikost%20pisave%2010%29%0A%20%2D%20%285%29%20SloKJV%20%28A5%2C%20%20mehke%20platnice%2C%20velikost%20pisave%209%2C4%29%0A%20%2D%20%286%29%20SloKJV%20%28A5%2C%20%20mehke%20%20platnice%2C%20velikost%20pisave%209%2C4%29%0A%20%2D%20%287%29%20SloKJV%20Ps%2BNz%20%28A5%2C%20mehke%20platnice%2C%20velikost%20pisave%209%2C4%29%0A%20%2D%20%288%29%20SloKJV%20Ps+NZ%20%28A5%2C%20trde%20%20platnice%2C%20velikost%20pisave%209%2C4%29%0A%0A%20Narocam%201%20%28en%29%20kos%20papirni%20izvod%20SloKJV%20z%20zaporedno%20stevilko%3A%20%5F%5F%5F%5F%5F%2C%20s%20ceno%200%20EUR%20%28cena%20vkljucuje%20dostavo%29%2E%0A%20%0A%20%20Moj%20naslov%3A%0A%20%20%5F%5F%5F%5F%5F%5F%5F%5F%0A%20%20%5F%5F%5F%5F%5F%5F%5F%5F%0A%20%20%5F%5F%5F%5F%5F%5F%5F%5F%0A%0A%0A%0AHvala%20za%20narocilo%2E%0AKmalu%20boste%20na%20e%2Dmail%20prejeli%20potrditev%20posiljanja%20paketa%20in%20potem%20prejmete%20se%20paket%2E%0A%0AJezus%20je%20GOSPOD%2E%0A%0AMarjan%20Savli%20in%20Barbara%20Hojkar%20Savli%0AMestni%20trg%2011%0ASI%2D4220%20Skofja%20Loka%OASlovenia%2FEurope%0Aemail%3A%20marjan%2Esavli%40gmail%2Ecom).
 - [Nainoia Inc.](https://nainoia-inc.signedon.net/) Anionian verzija z [mehkimi platnicami](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769/paperback/product-1y5gpyry.html), s [trdimi platnicami](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769/hardcover/product-j25j7z.html) in [Nova Zaveza z mehkimi platnicami](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769-new-testament/paperback/product-6k4jeq.html).

### Predlogi za izboljšavo
 Če ste v prevodu našli kako napako ali predlog za izboljšavo, jo lahko [sporočite](mailto:marjan.savli@gmail.com?subject=SloKJV–predlog&body=Predlagam...).


## *English*

## The King James Version Bible (1769) translated from English to Slovenian language

Translation project **King James Version** Bible in to Slovenian language since May 2010 to May 2022. 66 books have been translated. Since then, proofreading and corrections have been made.

Translated books: Old Testament (Genesis to Malachi) and whole New Testament.

 ### Translation features:

 - added notes and references from KJV 1611,
 - added approximate years of events; KJV Oxford 1769,
 - The "italicized" words are added to the original KJV text,
 - "<sup>a</sup>" KJV 1611 notes and translator's notes,
 - "<sub>b</sub>" references to other parts of the text,
 - "[ ]" added by the translator, not in the original KJV,
 - "§" is the difference between the SloKJV text and other Slovenian translations.
 - Jesus' words written in red (Android version)
 
Sources: [English text](http://www.crosswire.org/~dmsmith/kjv2006/), [Notes and references](https://www.kingjamesbibleonline.org/Genesis-Chapter-1_Original-1611-KJV/) and [biblija.net](http://www.biblija.net/biblija.cgi?m=&id13=1&id7=1&pos=0&set=6&l=sl).
 
Translation takes place in [Notepad++](https://notepad-plus-plus.org/) where the Slovenian text is below the English text for each verse. Then with a script this is converted to OSIS format - the XML file that is published on this page. The XML file is then converted into a Sword module, which is accessible on the [Crosswire.org](http://www2.crosswire.org/sword/modules/). 

### Files programs and devices:
You can read the Bible using one of these devices or programs:
  - [Crosswire.org list of programs for Windows, Mac, Linux, Andorid, iPhone, iPad](http://wiki.crosswire.org/Choosing_a_SWORD_program)
  #### Source file
  - [`SloKJV_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloKJV_sword.xml) (master translation file; XML SWORD format for [Crosswire.org](https://crosswire .org/sword/modules/ModInfo.jsp?modName=SloKJV))
  - [`slokjv.conf`](https://github.com/msavli/SloKJV/blob/master/slokjv.conf) (config for [`SloKJV_sword.xml`](https://github.com/msavli/ SloKJV/blob/master/SloKJV_sword.xml))
  #### Windows
  - [Xiphos](https://xiphos.org/)
  - [Windows e-sword](https://www.e-sword.net/) ([`SloKJV.bblx`](https://github.com/msavli/SloKJV/blob/master/SloKJV.bblx) put in the folder: c:\Program Files (x86)\e-Sword)
  #### Android
  - [AndBible](https://play.google.com/store/apps/details?id=net.bible.android.activity) installation is automatic. For manual installation, unpack the file [`Android_data_net.bible.android.activity_files.zip`](https://github.com/msavli/SloKJV/blob/master/Android_data_net.bible.android.activity_files.zip) into the folder `\\ Android\data\net.bible.android.activity\files`)
  - [Mysword for Android](https://www.mysword.info/download-mysword) ([`SloKJV.bbl.mybible`](https://github.com/msavli/SloKJV/blob/master/SloKJV. bbl.mybible) put in folder [`/storage/emulated/0/mysword/bibles`])
  - [MyBible](https://mybible.zone/) ([`SloKJV.sqlite3`](https://github.com/msavli/SloKJV/blob/master/SloKJV.sqlite3) needs to be installed manually)
  #### iPhone
  - [PocketSword](https://apps.apple.com/us/app/pocketsword/id341046078)
  #### Java Phones
  - [GoBible](https://github.com/msavli/SloKJV/blob/master/slokjv.jar) (For old Java MIDP 2.0 phones; SLO-ENG KJV with notes and references; files [`slokjv.jad`] (https://github.com/msavli/SloKJV/blob/master/slokjv.jad) and [`slokjv.jar`](https://github.com/msavli/SloKJV/blob/master/slokjv.jar) must be installed manually)
  #### Palms
  - [Palm Bible+](https://palmbibleplus.sourceforge.net/) ([`SloKJV.pdb`](https://github.com/msavli/SloKJV/blob/master/SloKJV.pdb) must be manually installed )
  #### ePUB
  - [`SloKJV.epub`](https://github.com/msavli/SloKJV/blob/master/SloKJV.epub) (Kindle, KoboPDF, e-readers)
  #### VideoPsalm
  - [VideoPsalm](https://myvideopsalm.weebly.com/) [`SloEngKJV_VideoPsalm_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloEngKJV_VideoPsalm_sword.xml) import into the VideoPsalm program, which is used for screen presentation in churches. Each Bible line is in Slovenian and below it in English
  #### Online (not always the latest SloKJV version)
  - [Aionianbible.org](https://www.aionianbible.org/Bibles/Slovene---Slovene-Savli-Bible)
  - [StepBible.org](https://www.stepbible.org/version.jsp?version=SloKJV)
  #### PDF
  - [PDF - one column]( https://github.com/msavli/SloKJV/blob/master/SloKJV.pdf) ([Stephan Kreutzer](https://skreutzer.de/) with his project [Free Scriptures ](http://www.free-scriptures.org/index.php?page=downloads), [ver: 2019_07_31](http://www.free-scriptures.org/downloads/free-scriptures_gnu_20190731.zip) helped make the first PDF version.)
  - `SloKJV*.pdf` (printable PDF files)
 
 ### SloKJV paper copy
 ![Knjiga](slike/Slika_knjige_v_perspektivi_transparent_150.png?raw=true "150e")
 The Bible is digitally printed on 60g paper with a paperback binding. There are two publishers, but the same digital presses on which the 800-page Bibles are printed (lulu.com).
 - Hojkar-Šavli: Delivery is expected to start by May 2024. To order it, [click](mailto:marjan.savli@gmail.com?subject=SloKJV–Order&body=%0AFarewell%21%20%0A%0ABrossed%20bindings%20are%20available%3A%20%0A%0A%20%2D%20%281%29%20SloKJV%20%28A4%2C%20hard%20cover%2C%20font%20size%2012%2C5%29%20%0A%20%2D%20%282%29%20SloKJV%20%28A4%2C%20soft%20cover%2C%20font%20size%2012%2C5%29%20%0A%20%2D%20%283%29%20SloKJV%20%28A5%2B%2C%20hard%20cover%2C%20font%20size%2010%29%20%0A%20%2D%20%284%29%20SloKJV%20%28A5%2B%2C%20soft%20cover%2C%20font%20size%2010%29%20%0A%20%2D%20%285%29%20SloKJV%20%28A5%2C%20soft%20cover%2C%20font%20size%209%2C4%29%20%0A%20%2D%20%286%29%20SloKJV%20%28A5%2C%20soft%20cover%2C%20font%20size%209%2C4%29%20%0A%20%2D%20%287%29%20SloKJV%20Ps%2BNz%20%28A5%2C%20soft%20cover%2C%20font%20size%209%2C4%29%20%0A%20%2D%20%288%29%20SloKJV%20Ps%2BNZ%20%28A5%2C%20hard%20cover%2C%20font%20size%209%2C4%29%20%0A%20%0A%20I%20am%20ordering%201%20%28one%29%20paper%20copy%20of%20the%20SloKJV%20with%20the%20sequence%20number%3A%20_____%2C%20at%20a%20price%20of%20EUR%200%20%28price%20includes%20delivery%29%2E%0A%20%20%0A%20%20My%20address%3A%20%0A%20%20________%20%0A%20%20________%20%0A%20%20________%20%0A%0A%0A%0AThank%20you%20for%20your%20order%2E%20%0AYou%20will%20receive%20a%20confirmation%20e%2Dmail%20shortly%20and%20then%20you%20will%20receive%20your%20package%2E%20%0A%0AJesus%20is%20LORD%2E%20%0A%0AMarjan%20Savli%20and%20Barbara%20Hojkar%20Savli%20%0AMestni%20trg%2011%20%0ASI%2D4220%20Skofja%20Loka%20%0ASlovenia%2FEurope%20%0Aemail%3A%20marjan%2Esavli%40gmail%2Ecom).
 - [Nainoia Inc.](https://nainoia-inc.signedon.net/) Anionian version: [Paperback](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769/paperback/product-1y5gpyry.html), [Hardcover](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769/hardcover/product-j25j7z.html) and [Paperback New Testament](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769-new-testament/paperback/product-6k4jeq.html) 

 ### Suggestions for improvement
 If you find an error or suggestion for improvement in the translation, you can [report it](mailto:marjan.savli@gmail.com?subject=SloKJV–suggestion&body=Suggestion...).

*License*

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
