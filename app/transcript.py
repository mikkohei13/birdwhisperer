

from fuzzywuzzy import fuzz
import pandas as pd
import re
import editdistance
from datetime import datetime

# Finnish species except most rare ones, most common species groups & codes, based on Laji.fi abundance data
# Added species synonyms: heinäsorsa, isokuovi, kalasääski, kesykyyhky, pulu
# Added some mammals
valid_species = ['kyhmyjoutsen', 'pikkujoutsen', 'laulujoutsen', 'metsähanhi', 'taigametsähanhi', 'tundrametsähanhi', 'lyhytnokkahanhi', 'tundrahanhi', 'kiljuhanhi', 'merihanhi', 'tiibetinhanhi', 'kanadanhanhi', 'pikkukanadanhanhi', 'valkoposkihanhi', 'sepelhanhi', 'punakaulahanhi', 'ruostesorsa', 'ristisorsa', 'mandariinisorsa', 'haapana', 'amerikanhaapana', 'harmaasorsa', 'tavi', 'amerikantavi', 'sinisorsa', 'heinäsorsa', 'jouhisorsa', 'heinätavi', 'sinisiipitavi', 'lapasorsa', 'punapäänarsku', 'punasotka', 'amerikantukkasotka', 'ruskosotka', 'tukkasotka', 'lapasotka', 'haahka', 'kyhmyhaahka', 'allihaahka', 'alli', 'mustalintu', 'pilkkaniska', 'pilkkasiipi', 'telkkä', 'uivelo', 'tukkakoskelo', 'isokoskelo', 'kuparisorsa', 'viiriäinen', 'pyy', 'riekko', 'kiiruna', 'teeri', 'metso', 'peltopyy', 'fasaani', 'kaakkuri', 'kuikka', 'amerikanjääkuikka', 'jääkuikka', 'pikku-uikku', 'silkkiuikku', 'härkälintu', 'mustakurkku-uikku', 'mustakaulauikku', 'myrskylintu', 'suula', 'merimetso', 'kaulushaikara', 'yöhaikara', 'lehmähaikara', 'silkkihaikara', 'jalohaikara', 'harmaahaikara', 'mustahaikara', 'kattohaikara', 'mehiläishaukka', 'haarahaukka', 'isohaarahaukka', 'merikotka', 'hanhikorppikotka', 'munkkikorppikotka', 'käärmekotka', 'ruskosuohaukka', 'sinisuohaukka', 'arosuohaukka', 'niittysuohaukka', 'kanahaukka', 'varpushaukka', 'hiirihaukka', 'lännenhiirihaukka', 'idänhiirihaukka', 'arohiirihaukka', 'piekana', 'kiljukotka', 'pikkukiljukotka', 'maakotka', 'arokotka', 'sääksi', 'kalasääski', 'tuulihaukka', 'punajalkahaukka', 'ampuhaukka', 'nuolihaukka', 'muuttohaukka', 'luhtakana', 'luhtahuitti', 'pikkuhuitti', 'kääpiöhuitti', 'ruisrääkkä', 'liejukana', 'nokikana', 'kurki', 'neitokurki', 'pikkutrappi', 'paksujalka', 'pitkäjalka', 'avosetti', 'meriharakka', 'siperiankurmitsa', 'amerikankurmitsa', 'kapustarinta', 'tundrakurmitsa', 'arohyyppä', 'töyhtöhyyppä', 'pikkutylli', 'tylli', 'mustajalkatylli', 'keräkurmitsa', 'pikkukuovi', 'kuovi', 'isokuovi', 'mustapyrstökuiri', 'punakuiri', 'karikukko', 'isosirri', 'suokukko', 'suippopyrstösirri', 'jänkäsirriäinen', 'kuovisirri', 'lapinsirri', 'pulmussirri', 'suosirri', 'etelänsuosirri', 'merisirri', 'pikkusirri', 'tundravikla', 'palsasirri', 'vesipääsky', 'isovesipääsky', 'rantakurvi', 'rantasipi', 'metsäviklo', 'mustaviklo', 'valkoviklo', 'keltajalkaviklo', 'lampiviklo', 'liro', 'punajalkaviklo', 'jänkäkurppa', 'tundrakurppelo', 'lehtokurppa', 'taivaanvuohi', 'amerikantaivaanvuohi', 'heinäkurppa', 'siperiankurppa', 'pääskykahlaaja', 'aropääskykahlaaja', 'leveäpyrstökihu', 'merikihu', 'tunturikihu', 'lunni', 'riskilä', 'ruokki', 'pikkuruokki', 'etelänkiisla', 'pohjankiisla', 'pikkutiira', 'hietatiira', 'räyskä', 'mustatiira', 'valkosiipitiira', 'riuttatiira', 'kalatiira', 'lapintiira', 'pikkulokki', 'ruusulokki', 'tiiralokki', 'pikkukajava', 'naurulokki', 'mustanmerenlokki', 'kalalokki', 'selkälokki', 'harmaalokki', 'aroharmaalokki', 'etelänharmaalokki', 'ohotanlokki', 'grönlanninlokki', 'isolokki', 'merilokki', 'arokyyhky', 'kalliokyyhky', 'kesykyyhky', 'pulu', 'uuttukyyhky', 'sepelkyyhky', 'turkinkyyhky', 'turturikyyhky', 'idänturturikyyhky', 'käki', 'idänkäki', 'tornipöllö', 'kyläpöllönen', 'huuhkaja', 'hiiripöllö', 'varpuspöllö', 'lehtopöllö', 'viirupöllö', 'lapinpöllö', 'sarvipöllö', 'suopöllö', 'helmipöllö', 'kehrääjä', 'tervapääsky', 'kuningaskalastaja', 'mehiläissyöjä', 'sininärhi', 'harjalintu', 'käenpiika', 'harmaapäätikka', 'palokärki', 'käpytikka', 'valkoselkätikka', 'pikkutikka', 'pohjantikka', 'arokiuru', 'lyhytvarvaskiuru', 'töyhtökiuru', 'kangaskiuru', 'kiuru', 'tunturikiuru', 'törmäpääsky', 'haarapääsky', 'räystäspääsky', 'ruostepääsky', 'isokirvinen', 'mongoliankirvinen', 'nummikirvinen', 'taigakirvinen', 'metsäkirvinen', 'niittykirvinen', 'lapinkirvinen', 'luotokirvinen', 'keltavästäräkki', 'sitruunavästäräkki', 'virtavästäräkki', 'västäräkki', 'tilhi', 'koskikara', 'peukaloinen', 'rautiainen', 'taigarautiainen', 'mustakurkkurautiainen', 'punarinta', 'satakieli', 'etelänsatakieli', 'sinirinta', 'valkotäpläsinirinta', 'sinipyrstö', 'mustaleppälintu', 'leppälintu', 'pensastasku', 'nokitasku', 'sepeltasku', 'mustapäätasku', 'arotasku', 'kivitasku', 'nunnatasku', 'rusotasku', 'aavikkotasku', 'kirjorastas', 'sepelrastas', 'mustarastas', 'harmaakurkkurastas', 'ruostesiipirastas', 'mustakaularastas', 'räkättirastas', 'laulurastas', 'punakylkirastas', 'kulorastas', 'viirusirkkalintu', 'pensassirkkalintu', 'viitasirkkalintu', 'ruokosirkkalintu', 'pikkukultarinta', 'kultarinta', 'ruokokerttunen', 'kenttäkerttunen', 'viitakerttunen', 'luhtakerttunen', 'rytikerttunen', 'rastaskerttunen', 'rusorintakerttu', 'samettipääkerttu', 'kääpiökerttu', 'kirjokerttu', 'hernekerttu', 'pensaskerttu', 'lehtokerttu', 'mustapääkerttu', 'idänuunilintu', 'lapinuunilintu', 'hippiäisuunilintu', 'taigauunilintu', 'kashmirinuunilintu', 'siperianuunilintu', 'ruskouunilintu', 'vuoriuunilintu', 'sirittäjä', 'tiltaltti', 'idäntiltaltti', 'pajulintu', 'hippiäinen', 'tulipäähippiäinen', 'harmaasieppo', 'pikkusieppo', 'idänpikkusieppo', 'sepelsieppo', 'kirjosieppo', 'viiksitimali', 'pyrstötiainen', 'valkopäätiainen', 'sinitiainen', 'talitiainen', 'kuusitiainen', 'töyhtötiainen', 'viitatiainen', 'hömötiainen', 'lapintiainen', 'pähkinänakkeli', 'puukiipijä', 'pussitiainen', 'kuhankeittäjä', 'punapyrstölepinkäinen', 'pikkulepinkäinen', 'mustaotsalepinkäinen', 'isolepinkäinen', 'punapäälepinkäinen', 'närhi', 'kuukkeli', 'harakka', 'pähkinähakki', 'naakka', 'mustavaris', 'varis', 'nokivaris', 'korppi', 'kottarainen', 'punakottarainen', 'varpunen', 'pikkuvarpunen', 'peippo', 'järripeippo', 'keltahemppo', 'viherpeippo', 'tikli', 'vihervarpunen', 'hemppo', 'vuorihemppo', 'urpiainen', 'ruskourpiainen', 'tundraurpiainen', 'kirjosiipikäpylintu', 'pikkukäpylintu', 'isokäpylintu', 'punavarpunen', 'taviokuurna', 'punatulkku', 'nokkavarpunen', 'lapinsirkku', 'pulmunen', 'mäntysirkku', 'keltasirkku', 'peltosirkku', 'pohjansirkku', 'pikkusirkku', 'kultasirkku', 'pajusirkku', 'ruskopääsirkku', 'mustapääsirkku', 'harmaasirkku', 'loxia', 'sterna', 'gavia', 'aves', 'anser', 'anserbranta', 'anatidae', 'cygnus', 'larus', 'passer', 'pernisbuteo', 'jalohaukat', 'alcauria', 'anserini', 'buteo', 'anthus', 'passeriformes', 'laridae', 'turdus', 'charadriiformes', 'haukat', 'anas', 'acanthis', 'paridae', 'falco', 'phylloscopus', 'hirundininae', 'stercorarius', 'pöllöt', 'turdidae', 'päiväpetolinnut', 'numenius', 'sternidae', 'sylvia', 'asio', 'circus', 'columba', 'accipiter', 'parus', 'accipitriformes', 'sirosuohaukka', 'anseriformes', 'pluvialis', 'columbidae', 'tikat', 'dendrocopos', 'fringillidae', 'kotkat', 'melanitta', 'picidae', 'fringilla', 'motacilla', 'tringa', 'accipitridae', 'tsik-sirkku', 'medium picidae', 'koskelot', 'piciformes', 'carduelis', 'corvus', 'hirundinidae', 'larinae', 'passeridae', 'ficedula', 'sylviidae', 'corvidae', 'gaviiformes', 'mergus', 'poecile', 'aquila', 'varpuslinnut', 'käpylinnut', 'tiirat', 'kuikkalinnut', 'linnut', 'harmaahanhet', 'hanhet', 'sorsalinnut', 'pieni kahlaaja', 'joutsenet', 'iso kahlaaja', 'lokit', 'varpuset', 'hiirihaukat', 'päiväpetolinnut', 'ruokkilinnut', 'sorsat', 'kahlaajalinnut', 'kirviset', 'varpuslinnut', 'lokkilinnut', 'rastaat', 'kahlaajat', 'tiaislinnut', 'urpiaiset', 'tiaiset', 'jalohaukkalinnut', 'uunilinnut', 'pääskyt', 'kihut', 'pöllölinnut', 'rastaslinnut', 'petolinnut', 'kuovit', 'keskikokoinen kahlaaja', 'tiiralinnut', 'kertut', 'sarvipöllöt', 'suohaukat', 'kyyhkyt','kettu','rusakko','kaniini','metsäkauris','valkohäntäkauris','orava','liito-orava','piisami','minkki','supikoira','siili', 'lisälaji']


keywords_to_separate = [
    "paikallinen",
    "paikallista",
    "paikallisia",
    "muuttava",
    "muuttavaa",
    "muuttavia",
    "kiert",
    "kiertelevää",
    "kiertelevä",
    "kierteleviä",
    "kiertelemässä",
    "kiertelee",
    "kiertelevät",
    "ääntelevä",
    "äänteleviä",
    "ääntelevää",
    "laulava",
    "laulavia",
    "laulavaa",
    "laulaa",
    "soidintava",
    "soidintavia",
    "soidintavaa",
    "varoitteleva",
    "varoittelevia",
    "varoittelevaa",

    "pohjoiseen",
    "koilliseen",
    "itään",
    "kaakkoon",
    "etelään",
    "lounaaseen",
    "länteen",
    "luoteeseen"
]

numbers = {
    "nolla": "0",
    "yksi": "1",
    "kaksi": "2",
    "kolme": "3",
    "neljä": "4",
    "viisi": "5",
    "kuusi": "6",
    "kuusikymmentäyksi": "61",
    "kuusikymmentäkaksi": "62",
    "kuusikymmentäkolme": "63",
    "kuusikymmentäneljä": "64",
    "kuusikymmentäviisi": "65",
    "kuusikymmentäkuusi": "66",
    "seitsemän": "7",
    "seitsemänkymmentäyksi": "71",
    "seitsemänkymmentäkaksi": "72",
    "seitsemänkymmentäkolme": "73",
    "seitsemänkymmentäneljä": "74",
    "seitsemänkymmentäviisi": "75",
    "kahdeksan": "8",
    "kahdeksankymmentäyksi": "81",
    "kahdeksankymmentäkaksi": "82"
}

convert = {
    "nolla": "0",
    "yksi": "1",
    "kaksi": "2",
    "kolme": "3",
    "neljä": "4",
    "viisi": "5",
    "kuusi": "6",
    "seitsemän": "7",
    "kahdeksan": "8",
    "yhdeksän": "9",
    "kymmenen": "10",
    "yksitoista": "11",
    "kaksitoista": "12",
    "kolmetoista": "13",
    "neljätoista": "14",
    "viisitoista": "15",
    "kuusitoista": "16",
    "seitsemäntoista": "17",
    "kahdeksantoista": "18",
    "yhdeksäntoista": "19",
    "kaksikymmentä": "20",
    "kaksikymmentäyksi": "21",
    "kaksikymmentäkaksi": "22",
    "kaksikymmentäkolme": "23",
    "kaksikymmentäneljä": "24",
    "kaksikymmentäviisi": "25",
    "kaksikymmentäkuusi": "26",
    "kaksikymmentäseitsemän": "27",
    "kaksikymmentäkahdeksan": "28",
    "kaksikymmentäyhdeksän": "29",
    "kolmekymmentä": "30",
    "kolmekymmentäyksi": "31",
    "kolmekymmentäkaksi": "32",
    "kolmekymmentäkolme": "33",
    "kolmekymmentäneljä": "34",
    "kolmekymmentäviisi": "35",
    "kolmekymmentäkuusi": "36",
    "kolmekymmentäseitsemän": "37",
    "kolmekymmentäkahdeksan": "38",
    "kolmekymmentäyhdeksän": "39",
    "neljäkymmentä": "40",
    "neljäkymmentäyksi": "41",
    "neljäkymmentäkaksi": "42",
    "neljäkymmentäkolme": "43",
    "neljäkymmentäneljä": "44",
    "neljäkymmentäviisi": "45",
    "neljäkymmentäkuusi": "46",
    "neljäkymmentäseitsemän": "47",
    "neljäkymmentäkahdeksan": "48",
    "neljäkymmentäyhdeksän": "49",
    "viisikymmentä": "50",
    "kuusikymmentä": "60",
    "seitsemänkymmentä": "70",
    "kahdeksankymmentä": "80",
    "yhdeksänkymmentä": "90",
    "sata": "100",
    "satakymmenen": "110",
    "satakaksikymmentä": "120",
    "satakolmekymmentä": "130",
    "sataneljäkymmentä": "140",
    "sataviisikymmentä": "150",
    "satakuusikymmentä": "160",
    "sataseitsemänkymmentä": "170",
    "satakahdeksankymmentä": "180",
    "satayhdeksänkymmentä": "190",
    "kaksisataa": "200",
    "kolmesataa": "300",
    "neljäsataa": "",
    "viisisataa": "",
    "kuusisataa": "",
    "seitsemänsataa": "",
    "kahdeksansataa": "",
    "yhdeksänsataa": "",
    "tuhat": "1000",
    "viisitoistatuhatta": "15000",
    "kymmenentuhatta": "10000",

    "paikallinen": "p",
    "paikallista": "p",
    "paikallisia": "p",
    "muuttava": "m",
    "muuttavaa": "m",
    "muuttavia": "m",
    "kiertelevää": "kiert",
    "kiertelevä": "kiert",
    "kierteleviä": "kiert",
    "kiertelemässä": "kiert",
    "kiertelee": "kiert",
    "kiertelevät": "kiert",
    "ääntelevä": "ä",
    "äänteleviä": "ä",
    "ääntelevää": "ä",
    "laulava": "Äx", # Temp solution to avoid case-sensitivity issues
    "laulavia": "Äx",
    "laulavaa": "Äx",
    "laulaa": "Äx",
    "soidintava": "Äx",
    "soidintavia": "Äx",
    "soidintavaa": "Äx",
    "varoitteleva": "var ä",
    "varoittelevia": "var ä",
    "varoittelevaa": "var ä",
    "nuori": "juv",
    "vanha": "ad",
    "untuvikko": "pull",
    "untuvikkoa": "pull",
    "nuori": "juv",
    "nuorta": "juv",
    "vanha": "ad",
    "vanhaa": "ad",
    "esiaikuinen": "subad",
    "esiaikuista": "subad",
    "juhlapukuinen": "jp",
    "juhlapukuista": "jp",
    "talvipukuinen": "tp",
    "talvipukuista": "tp",
    "vaihtopukuinen": "vp",
    "vaihtopukuista": "vp",
    "koiras": "k",
    "koirasta": "k",
    "uros": "k",
    "urosta": "k",
    "naaras": "n",
    "naarasta": "n",

    # codes
    "kautta": "/",
    "plus": "+",
    "b": "p",
    "pee": "p",
    "äp": "ä p",
    "äb": "ä p",
    "äm": "m",
    "ääm": "m",
    "a": "ä",
    "ää": "ä",

    # taxa
    "loksia": "loxia",
    "kygnus": "cygnus",
    "kyknus": "cygnus",
    "falko": "falco",
    "falkko": "falco",
    "puteo": "buteo",
    "kavia": "gavia"
}


def replace_ignorecase(substring, replacement, string):
    # Compile a regular expression pattern for case-insensitive matching
    pattern = re.compile(re.escape(substring), re.IGNORECASE)
    
    # Use the regular expression to replace the substring with a space
    new_string = pattern.sub(replacement, string)
    
    return new_string


def cleanup_terms(words):

    new_words = []
    for word in words:
        word = word.replace(".", "")
        if word in convert:
            new_words.append(convert[word])
        else:
#            word = word.replace("-", "/") # Removed because affects ranges as well
            new_words.append(word)
    
    return new_words


# TODO: This is partly redundant with cleanup_terms, but is it worthwhile to combine them? 
def cleanup_keywords(string):
    # Add spaces so that matching can be done for beginning and end of string as well
    string = " " + string + " "

#    for key, value in convert.items():
#        string = replace_ignorecase(f" {key} ", f" {value} ", string)

    # First separate important keywords from numbers etc.
    for key in keywords_to_separate:
        string = replace_ignorecase(key, f" {key} ", string)

    # Then cleanup (convert) them to codes
    for key, value in convert.items():
        string = replace_ignorecase(f" {key} ", f" {value} ", string)
#        string = replace_ignorecase(value, f" {value} ", string)
        string = string.replace("  ", " ")

    # Return trimmed string
    return string.strip()


def get_probable_species_and_distance(string):

    best_match = None
    best_dist = 100

    for valid in valid_species:
        dist = editdistance.eval(string, valid)

        if dist < best_dist:
            best_match = valid
            best_dist = dist

#    print(f"DEBUG: {string} -> {best_match}, ratio {best_dist}")
    return best_match, best_dist


def index_of_smallest(numbers):
  smallest = min(numbers)
  index = numbers.index(smallest)
  return index


def clean_atlas_code(code):
    code = str(code)
    if code in numbers:
        code = numbers[code]

    valid_codes = ['1', '2', '3', '4', '5', '6', '61', '62', '63', '64', '65', '66', '7', '71', '72', '73', '74', '75', '8', '81', '82']
    if code in valid_codes:
        return code
    return ""


def get_atlas_code(words):
    # Find the index of the item that matches 'atlas'
    try:
        index = words.index('atlas')
    except ValueError:
        # If 'atlas' is not in the list, return None
        return ""

    # Return the item at the index after 'atlas'
    # If the index is the last item in the list, return None
    if index == len(words) - 1:
        return ""
    else:
        code = words[index + 1]
        return clean_atlas_code(code)


def split_abbreviations(words):
    pattern = re.compile(r"^[0-9]{1,5}[pbmäkn]{1,5}$")

    new_words = []
    for word in words:
        word = str(word)
        match = pattern.match(word)
        if match:
            numbers = re.sub(r'[a-zåäö]', '', word)
            letters = re.sub(r'[0-9]', '', word)
#            print(f"DEBUG: {numbers} / {letters}")
            new_words.append(numbers)
            new_words.append(letters)
        else:
            new_words.append(word)

    return new_words


days = { "ensimmäinen": "1", "toinen": "2", "kolmas": "3", "neljäs": "4", "viides": "5", "kuudes": "6", "seitsemäs": "7", "kahdeksas": "8", "yhdeksäs": "9", "kymmenes": "10", "yhdestoista": "11", "kahdestoista": "12", "kolmastoista": "13", "neljästoista": "14", "viidestoista": "15", "kuudestoista": "16", "seitsemästoista": "17", "kahdeksastoista": "18", "yhdeksästoista": "19", "kahdeskymmenes": "20", "kahdeskymmenesensimmäinen": "21", "kahdeskymmenestoinen": "22", "kahdeskymmeneskolmas": "23", "kahdeskymmenesneljäs": "24", "kahdeskymmenesviides": "25", "kahdeskymmeneskuudes": "26", "kahdeskymmenesseitsemäs": "27", "kahdeskymmeneskahdeksas": "28", "kahdeskymmenesyhdeksäs": "29", "kolmaskymmenes": "30", "kolmaskymmenesensimmäinen": "31" }

months = {
    'ensimmäistä': '1', 
    'toista': '2', 
    'kolmatta': '3', 
    'neljättä': '4', 
    'viidettä': '5', 
    'kuudetta': '6', 
    'seitsemättä': '7', 
    'kahdeksatta': '8', 
    'yhdeksättä': '9', 
    'kymmenettä': '10', 
    'yhdettätoista': '11', 
    'kahdettatoista': '12', 
    'tammikuuta': '1', 
    'helmikuuta': '2', 
    'maaliskuuta': '3', 
    'huhtikuuta': '4', 
    'toukokuuta': '5', 
    'kesäkuuta': '6', 
    'heinäkuuta': '7', 
    'elokuuta': '8', 
    'syyskuuta': '9', 
    'lokakuuta': '10', 
    'marraskuuta': '11',
    'joulukuuta': '12'
}

years = {
    "tuhatyhdeksänsataakahdeksankymmentä": "1980",
    "tuhatyhdeksänsataakahdeksankymmentäyksi": "1981",
    "tuhatyhdeksänsataakahdeksankymmentäkaksi": "1982",
    "tuhatyhdeksänsataakahdeksankymmentäkolme": "1983",
    "tuhatyhdeksänsataakahdeksankymmentäneljä": "1984",
    "tuhatyhdeksänsataakahdeksankymmentäviisi": "1985",
    "tuhatyhdeksänsataakahdeksankymmentäkuusi": "1986",
    "tuhatyhdeksänsataakahdeksankymmentäseitsemän": "1987",
    "tuhatyhdeksänsataakahdeksankymmentäkahdeksan": "1988",
    "tuhatyhdeksänsataakahdeksankymmentäyhdeksän": "1989",
    "tuhatyhdeksänsataayhdeksänkymmentä": "1990",
    "tuhatyhdeksänsataayhdeksänkymmentä": "1991",
    "tuhatyhdeksänsataayhdeksänkymmentäkaksi": "1992",
    "tuhatyhdeksänsataayhdeksänkymmentäkolme": "1993",
    "tuhatyhdeksänsataayhdeksänkymmentäneljä": "1994",
    "tuhatyhdeksänsataayhdeksänkymmentäviisi": "1995",
    "tuhatyhdeksänsataayhdeksänkymmentäkuusi": "1996",
    "tuhatyhdeksänsataayhdeksänkymmentäseitsemän": "1997",
    "tuhatyhdeksänsataayhdeksänkymmentäkahdeksan": "1998",
    "tuhatyhdeksänsataayhdeksänkymmentäyhdeksän": "1999",
    "kaksituhatta": "2000",
    "kaksituhattayksi": "2001",
    "kaksituhattakaksi": "2002",
    "kaksituhattakolme": "2003",
    "kaksituhattaneljä": "2004",
    "kaksituhattaviisi": "2005",
    "kaksituhattakuusi": "2006",
    "kaksituhattaseitsemän": "2007",
    "kaksituhattakahdeksan": "2008",
    "kaksituhattayhdeksän": "2009",
    "kaksituhattakymmenen": "2010",
    "kaksituhattayksitoista": "2011",
    "kaksituhattakaksitoista": "2012",
    "kaksituhattakolmetoista": "2013",
    "kaksituhattaneljätoista": "2014",
    "kaksituhattaviisitoista": "2015",
    "kaksituhattakuusitoista": "2016",
    "kaksituhattaseitsemäntoista": "2017",
    "kaksituhattakahdeksantoista": "2018",
    "kaksituhattayhdeksäntoista": "2019",
    "kaksituhattakaksikymmentä": "2020",
    "kaksituhattakaksikymmentäyksi": "2021",
    "kaksituhattakaksikymmentäkaksi": "2022",
    "kaksituhattakaksikymmentäkolme": "2023"
}


def validate_date2(string):
    pattern = r"^(?:[1-9]|[12]\d|3[01])\.(?:[1-9]|1[012])\.([12]\d{3})$"
    if bool(re.match(pattern, string)):
        return string, True
    return string, False


def clean_date2(string):
    string = string.strip(" ,.")
    string = string.replace(",", ".")
    string = string.replace(" ", ".")
    string = string.replace("..", ".")

    print("CLEANING DATE " + string)

    string = string.rstrip("p")

    if "" == string:
        return "", False

    # If year is in pieces, join them
    count_dots = string.count(".")
    if count_dots > 2:
        pieces = string.split(".")
        string = pieces[0] + "." + pieces[1] + "." + "".join(pieces[2:])

    # dd.mm.yyyy
    pattern = r"^(?:[1-9]|[12]\d|3[01])\.(?:[1-9]|1[012])\.([12]\d{3})$"
    if bool(re.match(pattern, string)):
        return validate_date2(string)
    
    parts = string.split(".")
    print("---> date string:/" + string + "/")
    if parts[0] in days:
        parts[0] = days[parts[0]]
    if parts[1] in months:
        parts[1] = months[parts[1]]
    if parts[2] in years:
        parts[2] = years[parts[2]]
    
    string = parts[0] + "." + parts[1] + "." + parts[2] 

    return validate_date2(string)



'''
Ideas for future:

- Warn about pyy
- Warn about missing date
- Warn byt pyy on last row
- Bug: if last word is pop, outputs it as "pyy"
- Add row for named place
- Add possibility to add keywords, people
- Test korjauslogiikka. korjaus on liian lähellä nimeä corvus.
- Miten numerot järkeviksi? "kaksi 100 50 kuusi"
- Empty columns to beginning: observer, country, municipality
- Observation notes column
- Fuzzy match keywords, but how? The observation can contain any words, how to know what to match? Would require separating count field from notes field; matching would be done only for count field.
- Separating genders into different fields. Would require separating k & n from numbers.
- Common misspellings:
    - parveja
- Warn about unusual single-letter codes, also those with numbers.
- Fuzzy matching for korjaus & korjaan
- Cannot make fix to last row, e.g. if ends with this: "Sinisorsa. Yli 100b. Pop. Päivä. 16.4. 2001. Pop. Korjaus. Pop."
- n parvi / n parvea -> this and anything that follows to Notes (Unless there's a keyword for notes)
- Possibility to add loppupivä, which is cleared whenever start date is cleared


Challenges:

- Use always large model, since medium tends to ignore pop's and do its own interpretations too often. 
- aika is too close to paikka
- än vs. naaras

Käyttöohjeita:

- Puhu normaalilla tavalla. Jos äännät esim. lukuarvot hitaasti ja painottaen jokaista numeroa erikseen, "1999" voi muuttua muotoon "1000 900 90 9".
- Aloita jokainen rivi jollakin näistä:
    - "paikka" ja sitten paikannimi
    - "päivä" ja sitten päivämäärä, esim. "viides ensimmäistä kaksituhattakaksikymmentäkolme"
    - lintulajin tai -ryhmän nimi, ja sitten muut tiedot kuten lukumäärä, havainnon tyyppi, lisätiedot jne.
- Sano "pop" jokaisen rivin jälkeen. Pidä tauko ennen tätä sanaa ainakin ensimmäisillä havaintoriveillä.
- Lajinimissä vältä lyhenteitä ja tieteellisiä nimiä. Tämä vähentää virheitä. Sano "iso päiväpetolintu" äläkä "IP", sano "kerttuset" äläkä "acrocephalus".
- Äännä täsmällisesti, erityisesti numerot.
- Erottele paikalliset ja muuttavat yksilöt omiksi havainnoikseen.
- Erottele sukupuolet, iät yms. omiksi havainnoikseen, jos haluat.
- Muuttaville havainnoille sano "m" tai "muuttava".
- Sano ilmansuunnat suomeksi, esim. "koilliseen". Älä luota, että pelkän ilmansuunnan sanominen ei tee havainnosta muuttohavaintoa.
- Ilmaise koiraat ja naaraat sanomalla k, n, koiras tai naaras. Älä sano "kautta". 
- p ja m ovat ok lyhenteitä, mutta sano muut suomeksi. Esim. laulava, ääntelevä, parvi, vanha, nuori, untuvikko... Kirjainlyhenteet pilkkoutuvat helposti osiin, esim. "ad" -> "A D"
- Älä anna vaihteluvälejä, esim. "viisi viiva kymmenen paikallista" tai ylipäätään sanaa "viiva"
- Tarkista pyyhavainnot. Whisper tulkitsee monet epämääräiset äännähdykset pyy-nimeksi.

'''


# Get data
import data_transcript
transcript = data_transcript.transcript
filename = data_transcript.filename

# This helps to get rid of trailing "pop"
transcript = transcript + " "

# Remove extra characters
#transcript = transcript.replace(".", "") # must not remove dots, since important for dates
transcript = transcript.replace(",", "")
transcript = transcript.replace("  ", " ")
transcript = transcript.replace("-", " ") # because Whisper adds dashes in many places
transcript = transcript.lower()

# Split and clean data
# Different ways Whisper interprets 'pop'
transcript = transcript.replace(" bob.", " pop ")
transcript = transcript.replace(" bob ", " pop ")
transcript = transcript.replace(" bop.", " pop ")
transcript = transcript.replace(" bop ", " pop ")
transcript = transcript.replace(" bop. ", " pop ")
transcript = transcript.replace(" bop ", " pop ")
transcript = transcript.replace(" pp", " p pop")
transcript = transcript.replace(" pop.", " pop ")

# Common location names
transcript = transcript.replace("suomen oja", "suomenoja")
transcript = transcript.replace("suomenoja tulvaniitty", "suomenoja, tulvaniitty")
transcript = transcript.replace("suomenoja satama", "suomenoja, satama")
transcript = transcript.replace("friisin kallio", "friisinkallio")
transcript = transcript.replace("porkkala kärki", "porkkala, pampskatan")



rows = transcript.split(" pop ")

# For each row
rows = [item.strip() for item in rows]

# debug
#for row in rows:
#    print(row)
#exit()

prev_row_type = ""
location = ""
date = ""

# Create an empty dataframe
df = pd.DataFrame()

for row in rows:

    # Skip empty rows
    if "" == row:
        continue

    warning = ""
    atlas_code = ""
    rest = ""

    words = row.split(" ")
    print(f"/{row}/")

    # Check if we need to skip the previous row / location / date
    fixword = words[0].replace(".", "")
    distance_korjaus = editdistance.eval(fixword, "korjaus")

    if distance_korjaus < 2:
        print("!!!!! Fix word:" + fixword + ":")
        print(f"prev_row_type: {prev_row_type}")
        if "obs" == prev_row_type:
            print("Dropping the last row")
            df = df.drop(df.index[-1])
        elif "location" == prev_row_type:
            location = ""
        elif "date" == prev_row_type:
            date = ""
        continue

    # Date
    date_word = words[0].replace(".", "")
    distance_paiva = editdistance.eval(date_word, "päivä")
    distance_paivamaara = editdistance.eval(date_word, "päivämäärä")
    # Closest species: tavi/4, ruisrääkkä/7, härkä
    if "aika" == date_word or distance_paiva < 3 or distance_paivamaara < 5:
        print("Date word:" + words[0] + ":")
        raw_date = words[1:]
        print(f"RAW DATE: {raw_date}")
#        date, date_is_valid = clean_date(".".join(raw_date))
        date, date_is_valid = clean_date2(".".join(raw_date))
        print(f"   CLEANED DATE: {date}")
        print(f"   DATE VALIDITY: {date_is_valid}")
        prev_row_type = "date"
        continue

    # Remove dots, since they are not needed for anything else than dates
    row = row.replace(".", "")
    words = row.split(" ")

    # Location
    distance = editdistance.eval(words[0], "paikka")
    # Closest species: kuikka/2
    if distance < 2:
        print("Location word:" + words[0] + ":")
        location = ' '.join(words[1:])
        location = location.title()
        print(f"LOCATION: {location}")
        prev_row_type = "location"
        continue

    # Observation
    prev_row_type = "obs"

    # Taxon
    # Try different combinations of words to parse what looks like most probable taxon name
    species_tentative = []
    species_tentative.append(words[0])
    species_tentative.append(''.join(words[0:2]))
    species_tentative.append(''.join(words[0:3]))

    species_distance = []
    species_matched = []

    species_m, species_d = get_probable_species_and_distance(species_tentative[0])
    species_matched.append(species_m)
    species_distance.append(species_d)
    species_m, species_d = get_probable_species_and_distance(species_tentative[1])
    species_matched.append(species_m)
    species_distance.append(species_d)
    species_m, species_d = get_probable_species_and_distance(species_tentative[2])
    species_matched.append(species_m)
    species_distance.append(species_d)

    most_probable_species_index = index_of_smallest(species_distance)
    most_probable_species = species_matched[most_probable_species_index]
    most_probable_distance = species_distance[most_probable_species_index]
#    print(most_probable_species, most_probable_distance)

    # If taxon name seems uncertain, store a warning
    if most_probable_distance > 4:
        warning += "taxonwarning "
        print(f"TAXON WARNING: {words[0]} {most_probable_species} {most_probable_distance}")

    # Rest of the data goes to cound field
    rest = words[(most_probable_species_index+1):]
#    print(f" SPECIES: {most_probable_species} REST: /{rest}/") # debug

    # Get atlasCode
    # Todo: remove from 'rest'
    atlas_code = get_atlas_code(rest)

    # ABBA
    # split_int_and_letters(string)

    # Do cleanup of individual terms
    rest = split_abbreviations(rest)
    rest = cleanup_terms(rest)

#    print(f" SPECIES: {most_probable_species} REST: /{rest}/") # debug

    # Join everything as a string, without dots
    rest = [str(x) for x in rest]
    count = ' '.join(rest)
#    count = cleanup_keywords(count) # TODO: is this needed? Only if there are keywords or terms that Whisper concatenate to numbers without space. Are there such with the large model?

    # Identify statuses. This can be done using individual words, if we can trust that Whisper does not concatenate numbers and letters together.
    # Valid values: M, P, kiert, Ä, ä
    status_set = set()
    count_set = " " + count + " "
    if " m " in count_set:
        status_set.add("M")
    if " p " in count_set:
        status_set.add("P")
    if " atlas " in count_set:
        status_set.add("P")
    if " kiert " in count_set:
        status_set.add("kiert")
    if " Äx " in count_set:
         status_set.add("Ä")
    if " ä " in count_set:
         status_set.add("ä")

    # Finalizing
    status = ";".join(status_set)
    count = count.replace("Äx", "Ä").replace("  ", " ")
    today = datetime.today().strftime('%-d.%-m.%Y')

    # Create a data row
#    df = df.append({'col1': date, 'location': location, 'species': most_probable_species, 'count': rest, 'atlas_code': atlas_code}, ignore_index=True)

    if date_is_valid != True:
        warning += "datewarning "

    new_row = pd.DataFrame({
        "Havainnoijat - Yleinen keruutapahtuma": "MA.3", # TODO: How to have this?
        "Alku - Yleinen keruutapahtuma": date,
        "Avainsanat - Havaintoerä": "lintukuiskaaja",
        "Lisätiedot - Keruutapahtuma": f"Digitoitu Lintukuiskaajalla {today}, tiedosto {filename}",
        "Maa - Keruutapahtuma": "",
        "Kunta - Keruutapahtuma": "",
        "Nimetty paikka - Keruutapahtuma": "",
        "Koordinaatit - Keruutapahtuma": location,
        "Paikannimet - Keruutapahtuma": location,
        "Laji - Määritys": most_probable_species,
        "Määrä - Havainto": count,
        "Lisätiedot - Havainto": "",
        "Havainnointitapa - Havainto": "Havaittu",
        "Linnun tila - Havainto": status,
        "Pesimävarmuusindeksi - Havainto": atlas_code,
        "Kokoelma/Avainsanat - Havainto": "",
        "warning": warning 
        }, index=[0])

    # Add row to dataframe
    df = pd.concat([df, new_row], ignore_index = True)
    new_row = False


# Save the dataframe as a TSV file
df.to_csv("data.tsv", sep="\t", index=False)


