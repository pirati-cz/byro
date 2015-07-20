---
title:    Byro – pomocník na byrokracii
authors:  [Jakub Michálek, Ondřej Profant]
license:  Affero GNU-GPL
---


Byro – pomocník na byrokracii
============================

Program `byro` je soubor utilit, které umožňují z příkazové řádky:

* sázet dobře upravené dokumenty,
* podepisovat dokumenty elektronickým podpisem,
* aktualizovat data v redmine,
* posílat dokumenty e-mailem nebo datovou schránkou,
* generovat výkazy z redmine. 

Program vytvořil klub Pirátů v zastupitelstvu hl. m. Prahy.

Zadání
-------

Program se používá podobně jako `git` zadáním hlavního příkazu `byro` a některého z následujících doprovodných příkazů. Požadavek je, aby se instaloval a aktualizoval jednoduchým způsobem jedním příkazem.

Klasická pracovní metoda: 

* upravím soubor `main.md` do potřebné podoby a přílohy umístím do složky `attachments`, 
* spustím příkaz `pdf`, abych zkontroloval, jak vypadá písemnost ve formátu PDF, a následně 
* spustím příkaz `full`, který obstará celý proces včetně odeslání do datové schránky a uložení poznámky do redmine.


Doprovodné příkazy
--------

## pdf [sablona]

Převede soubor `main.md` pomocí programu `pandoc` do formátu PDF s využitím šablon a formulářů definovaných v repozitáři [sazba](https://github.com/jmichalek/sazba). Skript je rozšířením dlouho používaného skriptu [makedopis](https://github.com/jmichalek/sazba/blob/master/scripts/makedopis.sh). Rovněž aplikuje před kompilací skript vlna, který se stará o nedělitelné mezery na konci řádku.

Šablony: letter, brochure, legal, form

## save

Stáhne aktualizace z repozitáře příkazem `git pull`, přidá všechny změny v daném adresáři `git add .`, zapíše `git commit` a nahraje výsledek na server `git push`.

## sign

Podepíše soubor elektronickým podpisem podle uživatele definovaného v hlavičce souboru `main.md`. Podepíše buď konkrétní PDF soubor uvedený za příkazem anebo podepíše všechny PDF dokumenty v adresáři, chybí-li konkrétní soubor k podpisu.

## ds

Odešle dokument `main_signed.pdf` a jeho přílohy uložené v adresáři `attachments` do datové schránky uvedené v hlavičce souboru `main.md`. Vychází z pythonovského skriptu dodaného Vaškem Klecandou. Po odeslání stáhne potvrzení o dodání datové zprávy. Následně vloží jako aktualizaci úkolu v redmine odkaz na odeslaný dokument na githubu spolu s datem a dodejkou. Správný úkol vybere podle spisové značky uvedené v hlavičce souboru `main.md`, která koresponduje se spisovou značkou v redmine.

## mail

Odešle dokument `main_signed.pdf` a jeho přílohy uložené v adresáři `attachments` na e-mail uvedený v hlavičce souboru `main.md`. Používá přitom utilitu msmtp, viz skript [zde](https://github.com/jmichalek/gapisend/blob/master/sendmail.sh). Následně vloží jako aktualizaci úkolu v redmine odkaz na odeslaný dokument na githubu spolu s datem odeslání.

## full

Aplikuje příkazy `pdf`, `sign`, `save` a podle informací v hlavičce souboru odešle datovou schránkou `ds` nebo e-mailem `mail`. 


## vycetka

Konfigurační soubor
------------------

```
[bin]:
jsign: java -jar /opt/jsignpdf/JSignPdf.jar
pandoc: pandoc
tex: xelatex

[sign]
sign_key: 

[vycetka]
redmine: https://redmine.pirati.cz
project: praha
year: this
month: last
user: kedrigern

[ds]
id:
```

## Povolené hodnoty

year: this, last, 2014, 2015, ... 
month: this, last, leden, únor, ..., prosinec, 1, ..., 12
user: id, nebo nickname



Postup při instalaci
--------------------


Používání
---------

Struktura adresáře
------------------

