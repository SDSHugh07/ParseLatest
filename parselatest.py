# /bin/env python
# coding: utf-8

import sys, json, re, random;
from distutils.version import LooseVersion
from collections import OrderedDict

DEBUG = False

    #####################################################
    ##  Description: Represents a TranslationResource record with all pertinent information needed by this script
    ##
    #####################################################
class TranslationResource:

    def __init__(self, tr_hash, name, src_code, tgt_code, src_name, tgt_name, domain, version, distrib, key, owner, size):
        self.tr_hash = tr_hash
        self.name = name
        self.src_code = src_code
        self.tgt_code = tgt_code
        self.src_name = src_name
        self.tgt_name = tgt_name
        self.domain = domain
        self.version = version
        self.distrib = distrib
        self.key = key
        self.owner = owner
        self.size = size

dct_language_codes = {"SQ": "Albanian",
 "AM": "Amharic",
 "AR": "Arabic",
 "AI": "Arabizi",
 "HY": "Armenian",
 "AZ": "Azerbaijani",
 "EU": "Basque",
 "BN": "Bengali",
 "BS": "Bosnian (Latin)",
 "BC": "Bosnian (Cyrillic)",
 "BG": "Bulgarian",
 "CA": "Catalan",
 "KB": "Central Kurdish",
 "ZH": "Chinese (Simplified)",
 "ZT": "Chinese (Traditional)",
 "HR": "Croatian",
 "CS": "Czech",
 "DA": "Danish",
 "DR": "Dari",
 "NL": "Dutch",
 "EN": "English",
 "ET": "Estonian",
 "FI": "Finnish",
 "FR": "French",
 "KA": "Georgian",
 "DE": "German",
 "EL": "Greek",
 "HT": "Haitian",
 "HA": "Hausa",
 "HE": "Hebrew",
 "HI": "Hindi",
 "HU": "Hungarian",
 "IS": "Icelandic",
 "ID": "Indonesian",
 "IT": "Italian",
 "JA": "Japanese",
 "KM": "Khmer",
 "KO": "Korean",
 "KU": "Kurdish",
 "LV": "Latvian",
 "LT": "Lithuanian",
 "MS": "Malay",
 "ML": "Malayalam",
 "MT": "Maltese",
 "NE": "Nepali",
 "KT": "Northern Kurdish",
 "NO": "Norwegian",
 "PS": "Pashto",
 "FA": "Farsi",
 "PL": "Polish",
 "PT": "Portuguese",
 "PA": "Punjabi (Gurmukhi)",
 "PU": "Punjabi (Shahmukhi)",
 "RO": "Romanian",
 "RU": "Russian",
 "SR": "Serbian (Cyrillic)",
 "SB": "Serbian (Latin)",
 "SK": "Slovak",
 "SL": "Slovenian",
 "SO": "Somali",
 "ES": "Spanish",
 "SW": "Swahili",
 "SV": "Swedish",
 "TL": "Tagalog",
 "TG": "Tajik (Farsi)",
 "TJ": "Tajik (Cyrillic)",
 "TA": "Tamil",
 "TE": "Telugu",
 "TH": "Thai",
 "TR": "Turkish",
 "UK": "Ukrainian",
 "UR": "Urdu",
 "VI": "Vietnamese",
 "CY": "Welsh",
 "MY": "Burmese"}


if __name__ == "__main__":

    try:
        print("opening file " + sys.argv[1])
    except IndexError as ex:
        print("Please provide a JSON file to parse")
        raise SystemExit

    try:
        with open(sys.argv[1]) as json_file:
            c = json.load(json_file)
    except FileNotFoundError as ex:
        print("{}. Exiting...".format(ex))
        raise SystemExit

    if DEBUG:
        c_prime = {'translationResources': []}

#        lst_randomized_trs = c['translationResources']
#        lst_randomized_trs.reverse()
#        random.shuffle(lst_randomized_trs)
#        c['translationResources'] = lst_randomized_trs

    dct_trs = OrderedDict()

    try:
        for tr in c['translationResources']:
             if 'description' in tr and 'service' in tr['description'] and 'selectors' in tr and 'owner' in tr['selectors']:
                service = tr['description']['service']
                owner = tr['selectors']['owner']

                if re.search("^Translate_.._..$", service) and owner == 'Systran':
                    srclang_code = tr['description']['sourceLanguage']
                    tgtlang_code = tr['description']['targetLanguage']
                    size = tr['selectors']['size']
                    name = tr['description']['name']

                    if (srclang_code == 'en' or tgtlang_code == 'en') and re.search("^Translator NMT", name) and (size == 'L' or size == 'M'):
                        key = tr['description']['key']
                        distrib = tr['description']['distrib']

                        try:
                            srclang_name = dct_language_codes[srclang_code.upper()]
                            tgtlang_name = dct_language_codes[tgtlang_code.upper()]
                        except KeyError as ex:
                            print("Language code \'{}\' does not exist in dct_language_codes. Exiting...".format(ex))
                            raise SystemExit

                        domain = tr['selectors']['domain']

                        tr_hash = domain + srclang_code + tgtlang_code

                        version_major = tr['version']['major']
                        version_minor = tr['version']['minor']
                        version_patch = tr['version']['patch']
                        version = ('%d.%d.%d' % (version_major, version_minor, version_patch))

                        obj_new_tr = TranslationResource(tr_hash, name, srclang_code, tgtlang_code, srclang_name, tgtlang_name, domain, version, distrib, key, owner, size)

                        if DEBUG:
                            if tr_hash == 'Genericaren' or tr_hash == 'Genericenel' or tr_hash == 'Genericenfr' or tr_hash == 'Genericenfa':
                                c_prime['translationResources'].append(tr)

                        if tr_hash in dct_trs:
                            if dct_trs[tr_hash].size == 'M' and obj_new_tr.size == 'L':
                                dct_trs[tr_hash] = obj_new_tr
                            elif dct_trs[tr_hash].size == 'M' and obj_new_tr.size == 'M':
                                if LooseVersion(dct_trs[tr_hash].version) < LooseVersion(obj_new_tr.version):
                                    dct_trs[tr_hash] = obj_new_tr
                            elif dct_trs[tr_hash].size == 'L' and obj_new_tr.size == 'L':
                                if LooseVersion(dct_trs[tr_hash].version) < LooseVersion(obj_new_tr.version):
                                    dct_trs[tr_hash] = obj_new_tr
                        else:
                            dct_trs[tr_hash] = obj_new_tr
    except KeyError as ex:
        print("Incorrectly formatted TRS JSON dump \'{}\'. {} does not exist. Exiting...".format(sys.argv[1],ex))
        raise SystemExit

    try:
        with open('output_trs', 'w') as outF_csv_output:
            outF_csv_output.write("name\tsortcode\tsrccode\tsrcname\ttgtcode\ttgtname\tdomain\tversion\tdistrib\tkey\towner\tsize\n")

            for tr in dct_trs.values():
                outF_csv_output.write(tr.name + "\t" + tr.tr_hash + "\t" + tr.src_code + "\t" + tr.tgt_code + "\t" + tr.src_name + "\t" + tr.tgt_name + "\t" + tr.domain + "\t" + tr.version + "\t" + tr.distrib + "\t" + tr.key + "\t" + tr.owner + "\t" + tr.size + "\n")
    except OSError as ex:
        print("{}. Exiting...".format(ex))
        raise SystemExit

    print("parsing complete")

    if DEBUG:
        c['translationResources'] = c_prime['translationResources']

        with open('Golden_TR.json', 'w') as outfile:
            json.dump(c, outfile, indent=2)





