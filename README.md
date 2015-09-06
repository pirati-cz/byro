---
title:    Byro – pomocník na byrokracii
authors:  Jakub Michálek a Ondřej Profant
license:  Affero GNU-GPL
---


Pomocník na byrokracii Byro
============================

**Tenhle cvičený opičák za vás rád udělá byrokracii,
kterou byste ztratili hodiny práce.** 

![Travis-CI](https://travis-ci.org/pirati-cz/byro.svg) ![Scrutinizer](https://scrutinizer-ci.com/g/pirati-cz/byro/badges/quality-score.png?b=master)

![Maskot programu Byro](files/mascot.png)

----

Program `byro` je soubor utilit, které umožňují z příkazové řádky:

* sázet dobře upravené dokumenty,
* podepisovat dokumenty elektronickým podpisem,
* aktualizovat data v redmine,
* posílat dokumenty e-mailem nebo datovou schránkou,
* generovat výkazy z redmine. 

Program vytvořil [klub Pirátů](http://praha.pirati.cz) v zastupitelstvu hl. m. Prahy.


Postup při instalaci
--------------------

See [INSTALL.md](./INSTALL.md) file.

Zapojete se!
------------

Velmi rádi uvítáme další programátory a testy. Program sám je psán v Pythonu 3, 
ale pro vylepšení není potřeba mít hluboké znalosti.
Program většinou jen obaluje běžné aplikace (LaTeX, pandoc, git, ...),
čili můžete pomoci i pokud jen dodáte nápad na svoji oblíbenou utilitku.

Chyby a náměty hlaste v [issues](https://github.com/pirati-cz/byro/issues) (česky nebo anglicky).


Používání
---------

Klasická pracovní metoda: 

* upravím soubor `main.md` do potřebné podoby a přílohy umístím do složky `attachments`, 
* spustím příkaz `byro pdf`, abych zkontroloval, jak vypadá písemnost ve formátu PDF, a následně 
* spustím příkaz `byro full`, který obstará celý proces včetně odeslání do datové schránky a uložení poznámky do redmine.

Program se používá podobně jako `git` zadáním hlavního příkazu `byro` a některého z následujících doprovodných příkazů: 

### byro pdf [-t template] <dokument>.md

Převede soubor `main.md` pomocí programu `pandoc` do formátu PDF s využitím šablon a formulářů definovaných v repozitáři [sazba](https://github.com/jmichalek/sazba). Skript je rozšířením dlouho používaného skriptu [makedopis](https://github.com/jmichalek/sazba/blob/master/scripts/makedopis.sh). V dokumentu lze používat standardní pole šablon v [popisu pandocu](http://pandoc.org/demo/example9/templates.html). Rovněž aplikuje před kompilací skript vlna, který se stará o nedělitelné mezery na konci řádku.

Šablony: letter, brochure, legal, form <<= zatím není implementováno

### byro save

Stáhne aktualizace z repozitáře příkazem `git pull`, přidá všechny změny v daném adresáři `git add .`, zapíše `git commit` a nahraje výsledek na server `git push`.

### byro sign

Podepíše soubor elektronickým podpisem podle uživatele definovaného v hlavičce souboru `main.md`. Podepíše buď konkrétní PDF soubor uvedený za příkazem anebo podepíše všechny PDF dokumenty v adresáři, chybí-li konkrétní soubor k podpisu.

### byro ds

Odešle dokument `main_signed.pdf` a jeho přílohy uložené v adresáři `attachments` do datové schránky uvedené v hlavičce souboru `main.md`. Vychází z pythonovského skriptu dodaného Vaškem Klecandou. Po odeslání stáhne potvrzení o dodání datové zprávy. Následně vloží jako aktualizaci úkolu v redmine odkaz na odeslaný dokument na githubu spolu s datem a dodejkou. Správný úkol vybere podle spisové značky uvedené v hlavičce souboru `main.md`, která koresponduje se spisovou značkou v redmine.

### byro mail

Odešle dokument `main_signed.pdf` a jeho přílohy uložené v adresáři `attachments` na e-mail uvedený v hlavičce souboru `main.md`. Používá přitom utilitu msmtp, viz skript [zde](https://github.com/jmichalek/gapisend/blob/master/sendmail.sh). Následně vloží jako aktualizaci úkolu v redmine odkaz na odeslaný dokument na githubu spolu s datem odeslání.

### byro full

Aplikuje příkazy `pdf`, `sign`, `save` a podle informací v hlavičce souboru odešle datovou schránkou `ds` nebo e-mailem `mail`. 

### byro ocr

```
byro [-o <text>.txt] file1.jpg file2.jpg
```
