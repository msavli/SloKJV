# SloKJV
## Sveto pismo kralja Jakoba (1769) v slovenščini

[![Knjiga](slike/Slika_knjige_v_perspektivi_transparent_400.png?raw=true "SloKJV")](https://slokjv.si/)

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
 - »§« razlika med besedilom SloKJV in ostalimi slovenskimi prevodi,
 - Jezusove besede izpisane z rdečo (Android verzija).
 
Viri: [Angleško besedilo](http://www.crosswire.org/~dmsmith/kjv2006/), [Opombe in reference](https://www.kingjamesbibleonline.org/Genesis-Chapter-1_Original-1611-KJV/) in [biblija.net](http://www.biblija.net/biblija.cgi?m=&id13=1&id7=1&pos=0&set=6&l=sl).

Prevajanje je potekalo v programu [Notepad++](https://notepad-plus-plus.org/) kjer je slovensko besedilo in pod njim angleško. Potem se s skripto to pretvori v OSIS obliko - XML datoteko, ki je objavljena na tej strani. XML datoteko se potem pretvori v Sword modul, ki je dostopen na spletni strani [Crosswire.org](http://www2.crosswire.org/sword/modules/).

### [Beri SloKJV na spletu](https://slokjv.si/index.php) (vedno zadnja verzija)

### Datoteke, programi in naprave:
Sveto pismo lahko berete s pomočjo enega izmed teh naprav ali programov:
 - [Preglednica programov na crosswire.org za Windows, Mac, Linux, Andorid, iPhone, iPad](http://wiki.crosswire.org/Choosing_a_SWORD_program)
 #### Izvorna datoteka 
 - [`SloKJV_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloKJV_sword.xml) (glavna datoteka s prevodom; XML SWORD oblika za [Crosswire.org](https://crosswire.org/sword/modules/ModInfo.jsp?modName=SloKJV))
 - [`slokjv.conf`](https://github.com/msavli/SloKJV/blob/master/slokjv.conf) (konfiguracija za [`SloKJV_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloKJV_sword.xml))
 #### Windows
 - [Xiphos](https://xiphos.org/)
 - [Windows e-sword](https://www.e-sword.net/) ([`SloKJV.bblx`](https://slokjv.si/bin/SloKJV.bblx) odložiti v mapo: "c:\Program Files (x86)\e-Sword" Tej mapi je potrebno dodati 'write' pravice, da se sploh lahko datoteko vanjo shrani.)
 #### Android
 - [AndBible](https://play.google.com/store/apps/details?id=net.bible.android.activity) namestitev je avtomatična. Za ročno namestitev datoteko [`Android_data_net.bible.android.activity_files.zip`](https://slokjv.si/bin/Android_data_net.bible.android.activity_files.zip) razpakirati v mapo `\\Android\data\net.bible.android.activity\files`)
 - [Mysword for Android](https://www.mysword.info/download-mysword) ([`SloKJV.bbl.mybible`](https://slokjv.si/bin/SloKJV.bbl.mybible) odložiti v mapo [`/storage/emulated/0/mysword/bibles`])
 - [MyBible](https://mybible.zone/) ([`SloKJV.sqlite3`](https://slokjv.si/bin/SloKJV.sqlite3) je potrebno ročno namestiti)
 #### iPhone
 -  [Bishop](https://itunes.apple.com/us/app/the-sword-project-for-apple/id1399921911?mt=8)
 #### Java telefoni
 -  [GoBible](https://slokjv.si/bin/slokjv.jar) (Za stare Java MIDP 2.0 telefone; SLO-ENG KJV z opombami in referencami; datoteki [`slokjv.jad`](https://slokjv.si/bin/slokjv.jad) in [`slokjv.jar`](https://slokjv.si/bin/slokjv.jar) je potrebno ročno namestiti)
 #### Palm
 - [Palm Bible+](https://palmbibleplus.sourceforge.net/) ([`SloKJV.pdb`](https://slokjv.si/bin/SloKJV.pdb) je potrebno ročno namestiti)
 #### ePUB
 - [`SloKJV.epub`](https://slokjv.si/bin/SloKJV.epub) (Kindle, KoboPDF, e-bralniki) Dodana preprosta navigacija med kazalom in poglavji.
 #### VideoPsalm (predstavitev za cerkve na PC računalnikih)
 - [VideoPsalm](https://myvideopsalm.weebly.com/) [`SloEngKJV_VideoPsalm_sword.xml`](https://slokjv.si/bin/SloEngKJV_VideoPsalm_sword.xml) uvoziti v program VideoPsalm, ki se uporablja za prezentacijo na platno v cerkvah. Vsaka biblijska vrstica je v slovenščini in pod njo še v angleščini
 #### OpenLP (predstavitev za cerkve na Apple računalnikih)
 - [OpenLP](https://openlp.org/) File > Import > Bible > OSIS [`SloEngKJV_OpenLP.osis`](https://slokjv.si/bin/SloEngKJV_OpenLP.osis) > Open > Next
 #### Online (ni vedno zadnja verzija SloKJV)
 - [Aionianbible.org](https://www.aionianbible.org/Bibles/Slovene---Slovene-Savli-Bible)
 - [StepBible.org](https://www.stepbible.org/version.jsp?version=SloKJV)
 #### PDF
 - [PDF - 1 stolpec](https://slokjv.si/bin/SloKJV.pdf) ([Stephan Kreutzer](https://skreutzer.de/) je s svojim projektom [Free Scriptures](http://www.free-scriptures.org/index.php?page=downloads), [ver: 2019_07_31](http://www.free-scriptures.org/downloads/free-scriptures_gnu_20190731.zip) pomagal narediti prvo PDF verzijo.)
 - [PDF - 2 stolpca](https://k00.fr/odqgcju1) tiskano na Pretore/NL, 6/2025
 #### Pregled datotek
 - [Vpogled v mapo z binarnimi datotekami](https://slokjv.si/folder_bin.php)
 #### MP3
 - Avdio SloKJV ([MP3](https://k00.fr/SloKJV))
   - Stara zaveza (1,6 Gb, 67 ur)
   - Nova zaveza (0,5 Gb, 20 ur)
   - posamezne knjige

### Papirni izvod SloKJV
[![Knjiga](slike/Slika_knjige_v_perspektivi_transparent_150.png?raw=true "SloKJV")](https://slokjv.si/knjige/#sveto-pismo-kralja-jakoba)
 Sveto pismo je tiskano z digitalnim tiskom na 60g papir z broširano vezavo. Sta dva založnika, toda isti digitalni stroji, na katerih se 800 stranska Sveta pisma tiskajo (lulu.com).
  - Hojkar-Šavli: Papirne izvode SloKJV Svetih pisem in ostale knjige lahko naročite v ([spletni trgovini.](https://slokjv.si/knjige/))
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

### [Read SloKJV on web](https://slokjv.si/index.php) (always last version)

### Files, programs and devices:
You can read the Bible using one of these devices or programs:
  - [Crosswire.org list of programs for Windows, Mac, Linux, Andorid, iPhone, iPad](http://wiki.crosswire.org/Choosing_a_SWORD_program)
  #### Source file
  - [`SloKJV_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloKJV_sword.xml) (master translation file; XML SWORD format for [Crosswire.org](https://crosswire.org/sword/modules/ModInfo.jsp?modName=SloKJV))
  - [`slokjv.conf`](https://github.com/msavli/SloKJV/blob/master/slokjv.conf) (config for [`SloKJV_sword.xml`](https://github.com/msavli/SloKJV/blob/master/SloKJV_sword.xml))
  #### Windows
  - [Xiphos](https://xiphos.org/)
  - [Windows e-sword](https://www.e-sword.net/) ([`SloKJV.bblx`](https://slokjv.si/bin/SloKJV.bblx) put in the folder: "c:\Program Files (x86)\e-Sword" It is necessary to add 'write' permission to this folder in order for the file to be saved.)
  #### Android
  - [AndBible](https://play.google.com/store/apps/details?id=net.bible.android.activity) installation is automatic. For manual installation, unpack the file [`Android_data_net.bible.android.activity_files.zip`](https://slokjv.si/bin/Android_data_net.bible.android.activity_files.zip) into the folder `\\ Android\data\net.bible.android.activity\files`)
  - [Mysword for Android](https://www.mysword.info/download-mysword) ([`SloKJV.bbl.mybible`](https://slokjv.si/bin/SloKJV.bbl.mybible) put in folder [`/storage/emulated/0/mysword/bibles`])
  - [MyBible](https://mybible.zone/) ([`SloKJV.sqlite3`](https://slokjv.si/bin/SloKJV.sqlite3) needs to be installed manually)
  #### iPhone
  -  [Bishop](https://itunes.apple.com/us/app/the-sword-project-for-apple/id1399921911?mt=8)
  #### Java Phones
  - [GoBible](https://slokjv.si/bin/slokjv.jar) (For old Java MIDP 2.0 phones; SLO-ENG KJV with notes and references; files [`slokjv.jad`] (https://slokjv.si/bin/slokjv.jad) and [`slokjv.jar`](https://slokjv.si/bin/slokjv.jar) must be installed manually)
  #### Palms
  - [Palm Bible+](https://palmbibleplus.sourceforge.net/) ([`SloKJV.pdb`](https://slokjv.si/bin/SloKJV.pdb) must be manually installed )
  #### ePUB
  - [`SloKJV.epub`](https://slokjv.si/bin/SloKJV.epub) (Kindle, KoboPDF, e-readers) Easy navigation between the table of contents and chapters added.
  #### VideoPsalm (presentation for churches on PCs)
  - [VideoPsalm](https://myvideopsalm.weebly.com/) [`SloEngKJV_VideoPsalm_sword.xml`](https://slokjv.si/bin/SloEngKJV_VideoPsalm_sword.xml) import into the VideoPsalm program, which is used for presentation on screens in churches. Each Bible verse is in Slovenian, followed by the English translation.
  #### OpenLP (presentation for churches on Apple computers)
 - [OpenLP](https://openlp.org/) File > Import > Bible > OSIS [`SloEngKJV_OpenLP.osis`](https://slokjv.si/bin/SloEngKJV_OpenLP.osis) > Open > Next
  #### Online (not always the latest SloKJV version)
  - [Aionianbible.org](https://www.aionianbible.org/Bibles/Slovene---Slovene-Savli-Bible)
  - [StepBible.org](https://www.stepbible.org/version.jsp?version=SloKJV)
  #### PDF
  - [PDF - 1 column](https://slokjv.si/bin/SloKJV.pdf) ([Stephan Kreutzer](https://skreutzer.de/) with his project [Free Scriptures ](http://www.free-scriptures.org/index.php?page=downloads), [ver: 2019_07_31](http://www.free-scriptures.org/downloads/free-scriptures_gnu_20190731.zip) helped make the first PDF version.)
  - [PDF - 2 columns](https://k00.fr/odqgcju1) printed by Pretore/NL, 6/2025
  #### Viewing files
 - [Access the binary files folder](https://slokjv.si/folder_bin.php)
  #### MP3
   - Audio SloKJV ([MP3](https://k00.fr/SloKJV))
   - Old Testament (1.6 Gb, 67 hours)
   - New Testament (0.5 Gb, 20 hours)
   - individual books
 
  ### SloKJV paper copy
 [![Knjiga](slike/Slika_knjige_v_perspektivi_transparent_150.png?raw=true "SloKJV")](https://slokjv.si/knjige/#sveto-pismo-kralja-jakoba)
 The Bible is digitally printed on 60g paper with a paperback binding. There are two publishers, but the same digital presses on which the 800-page Bibles are printed (lulu.com).
 - Hojkar-Šavli: Paper copies of the SloKJV Bibles and other books can be ordered from the ([online shop](https://slokjv.si/knjige/))
 - [Nainoia Inc.](https://nainoia-inc.signedon.net/) Anionian version: [Paperback](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769/paperback/product-1y5gpyry.html), [Hardcover](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769/hardcover/product-j25j7z.html) and [Paperback New Testament](https://www.lulu.com/shop/-nainoia-inc/holy-bible-aionian-edition-slovene-king-james-bible-1769-new-testament/paperback/product-6k4jeq.html) 

 ### Suggestions for improvement
 If you find an error or suggestion for improvement in the translation, you can [report it](mailto:marjan.savli@gmail.com?subject=SloKJV–suggestion&body=Suggestion...).

*License*

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
