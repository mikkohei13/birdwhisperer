
transcript = ""

filename = ""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Test data

#transcript = "Päivämäärä, seitsemästoista lokakuuta 1997, POP. Paikka, Suomenoja, POP. Kyhmijoutsen, kaksi P, POP. Haapana, kaksikymmentä kolme, P, POP. Harmaasorsa, kaksi P, POP. Tavi, yksi koiras, P, POP. Sinisorsa, viisikymmentäviisi koirasta, kolmekymmentä yksi naarasta, P, POP. Lapasorsa, kaksi naarasta, P, POP. Tukkasotka, kaksitoista, P, POP. Telkkä, neljä koirasta, kaksikymmentä neljä naarasta, P, POP. Nokikana, nelkäkymmentä neljä, P, POP. Västäräkki, yksi Ä, POP. Punarinta, seitsemän Ä, POP. Kivitasku, yksi P, POP."

#transcript = "Päivä 31.3.2001. Pop. Paikka Espoo. pop Kaakkuri. Yksi P. Pesällä. Atlas. Seitsemän. Pop. Tavi. Yksi koiras. Varoittelee. Atlas. Kuusi. Pop. Töhtötieinen. Yksi laulava. Yksi varoitteleva. Atlas. Kuusi. Pop."

#transcript = "päivämääri. 1.1.2023 pop. paikk. Latokaski pop. talitiainen 1 p pop. valkopäätiainen 1 ä pop. corjaus. pop. sinitiainen 1 ä pop. paikka. kuun kamara pop. korjas. pop. paikko Suomenoja pop. kuusitiainen 1 Ä pop. käpytikka 1 p"


# Test for date formats
'''
transcript = "\
Päivä 28.8.2000. Pop. Paikka. Ok. Pop. tavi, 1p pop \
Päivä. 1 12 1990. Pop. Paikka. Ok. Pop. tavi, 1.p. BOB \
aika, kahdeskymmenesviides.yhdeksättä.2000 Pop. Paikka Ok pop, tavi, pop \
Päivämäärä kolmastoista neljättä 2004 pop paikka Ok bob, tavi 1 pop \
aika 5 12 2000, BOB, paikka, Ok bob, tavi. 1p. bob, \
Aika viides 12 1999 POP, Paikka, Ok. Bob. tavi 1p pop \
päivä, 5 kahdettatoista 1998, Pop, Paikka ok, Bob, tavi 1p, pop \
Päivä. 28.2 2001. Pop. Paikka. ok. Pop. Tavi 2 m pop \
aika, kahdeskymmenesyhdeksäs.yhdeksättä.2000 Pop. Paikka Ok pop, tavi, pop \
päivämäärä, kolmaskymmenesensimmäinen kahdettatoista tuhatyhdeksänsataakahdeksankymmentäseitsemän Pop. Paikka Ok pop, tavi, pop \
päivä kolmas kymmenettä tuhat yhdeksäsataa yhdeksänkymmentä yhdeksän Pop. Paikka Ok pop, tavi, pop \
päivä viies kymmenet tuhat yhdeksästaa yhdeksäkymmentä yhdeksän Pop. Paikka Ok pop, tavi, pop \
päivä viides kymmenettä tuhat yhdeksästää yhdeksänkymmentä yhdeksän Pop. Paikka Ok pop, tavi, pop \
päivä seitsemäs kymmenet tuhat yhdeksästää yhdeksänkymmentä yhdeksän Pop. Paikka Ok pop, tavi, pop \
päivämäärä kahdeskymmenes.ensimmäinen.yhdeksättä.kaksituhatta Pop. paikka Fail pop, tilhi, 2m pop \
Päivä. kolmaskymmenestoinen ensimmäistä 2000. pop Paikka. Fail. Pop. Tilhi. 2. m. pop. \
Päivä. kahdeskymmenes ensimmäinen ensimmäistä 2000. pop Paikka. Fail. Pop. Tilhi. 2. m pop. \
Aika 1.13.1994 pop, paikka Fail pop, tilhi 2 m pop \
Päivä. 1.1.999 pop, paikka Fail pop, tilhi 2 m pop \
"
'''

# Test for number / count formats
'''
Määrä - Havainto	Oikea tulkinta
noin kahdeksymmentä p	80
40 1 m	41
40 8 m	48
100 70 3 m	173
5 sataa 60 m	560
2 tuhatta 100 70 3 m	2173
7 tuhatta 50 1 m	751
80 8	88
60 8	68
kuusikymmentäviisi m	65
viisikymmentäkaksi m	52
4 tuhatta 7 sataa 70 7 m	4777
seitsemänkymmentäyksi	71
kolmisaa 7	307
10 m	10
viisikymmentäkaksi m	52
9	9
8 100 19 m	8119
100 yhdeksänkymmentäkuusi m	196
satakuusikymmentäyksi m	161
kaksisataaneljäkymmentä m	240
viisisataaneljä m	504
14	14
satayhdeksankymmentäkuusi m	196
90 m	90
noin 40 p	40
2 sataa 33	233
7 p	8
90 8 p	98
20 p	20
2 k p	2
9 ad p	9
noin 7 p	7
70 m länteen	70
kaksisataa 40 2	242
200 neljäkymmentä 2	242
3 sataa neljä kymmentä 5	345
20 neljä	24
'''
