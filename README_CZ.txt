KOMENTÁŘ K SEMESTRÁLNÍ PRÁCI

Semestrální práce se skládá z
	README.txt - komentář k sem. práci (který právě čtete)
	brainx.py - soubor se třídy BrainFuck, BrainLoller, BrainCopter pro zpracování jazyků z rodiny BrainFucku, WhichBrainxPic pro rozpoznání druhu brainloller vs. braincopter
	image_png.py - soubor se třídy PngReader, PNGWriter, vyjímky pro zpracování PNG souborů
	convertor.py - třídy BrainFuck2BrainLoller, BrainFuck2BrainCopter a funkce bf2bl, bl2bf, bf2bc, bl2bc, bc2bl pro konverze
	test.py - sadu testů
	gitlog.txt - výstup z příkazu "git log" projektu
	test_data/ - testovací data


=============================
POUŽITÍ INTERPRETERU 
=============================
Interpreter spouštíme příkazem:
 > python3 brainx.py src

 - src: zdrojový kód BrainFucku, .txt nebo .b soubor se zdrojovým kódem BrainFucku nebo .png soubor BrainCopteru nebo BrainLolleru, není třeba specifikovat typ jazyka

Spuštení bez argumentu src: 
 > python3 brainx.py
	
	usage: brainx.py [-h] src
	brainx.py: error: the following arguments are required: src

Spuštění nápovědy přepínačem -h:
 > python3 brainx.py -h

 	usage: brainx.py [-h] src

	positional arguments:
  		src         source code or file with source code

	optional arguments:
  		-h, --help  show this help message and exit


=============================
POUŽITÍ KONZERZE
=============================
Konvertor spouštíme:
 > python3 convertor.py src dst

 - src: zdrojový soubor formátu, ze kterého chceme konvertovat
 - dst: cílový soubor, do kterého se provede konverze

 Není třeba specifikovat typ jazyka ani typ konverze. Vše se rozhodne podle analýzy argumentů a souborů v argumentech.

 Druhy konverzí:
 1) BrainFuck to BrainLoller
 	- pokud je v argumentu src cesta k .txt nebo .b souboru a argumentem dst je cesta k neexistujícímu .png soubor
 2) BrainLoller to BrainFuck
 	- src argumentem je cesta k existujícímu .png soubor, konvertor rozpozná, že se jedná o o BrainLoller
 	- dst argumentem je cesta k .txt nebo .b souboru
 3) BrainFuck to BrainCopter
 	- src argumentem je cesta k existujícímu .txt nebo .b souboru s BrainFuckem
 	- dst je existující .png soubor s obrázkem, do kterého chceme zapsat

 	!! Varování !!
 	Pokud zvolíte moc malý obrázek pro zakódování do BrainCopteru, nezakóduje se všechen kód, při tomto riziku se objeví varování na standardní výstup!

 4) BrainCopter to BrainFuck
 	- src je existující .png soubor, konverter sám rozpozná, zda se jedná o BrainCopter
 	- dst je .txt nebo .b soubor
 5) BrainLoller to BrainCopter 
 	- src je existující .png soubor, konverter rozpozná, že jde o BrainLoller
 	- dst je existující .png soubor, který je určený pro zakódování 

 	!! Varování !!
 	Pokud zvolíte moc malý obrázek pro zakódování do BrainCopteru, nezakóduje se všechen kód, při tomto riziku se objeví varování na standardní výstup!

 6) BrainCopter to BrainLoller
 	- src je cesta k existujícímu .png soubor, konverter rozpozná typ jazyka
 	- dst je cesta k neexistujícímu .png souboru, BrainFuck tedy bude zakódovám BrainLollerem 

 Spuštění bez parametrů:
 > python3 convertor.py

 	usage: convertor.py [-h] src dst
 	convertor.py: error: the following arguments are required: src, dst


 Nápověda argumentem -h:
 > python3 convertor.py -h

 	usage: convertor.py [-h] src dst

	positional arguments:
	  src         path to the source file
	  dst         path to the destination file

	optional arguments:
	  -h, --help  show this help message and exit



Feel free to use or modify
	Jan Rudolf, 2014






