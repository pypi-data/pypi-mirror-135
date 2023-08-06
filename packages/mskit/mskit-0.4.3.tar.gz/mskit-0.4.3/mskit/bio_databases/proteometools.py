import re

from mskit.utils import NonOverwriteDict

pep_per_tissue_url = (
    "https://www.proteomicsdb.org/proteomicsdb/logic/api/peptidespertissue.xsodata/"
    "InputParams(TISSUE_ID='{}',Q_VALUE_FILTER=0.01,TAXCODE=3702)/"
    "Results?$select="
    "IDENTIFICATION_ID,MSFILE_NAME,SCAN_NUMBER,PRECURSOR_MZ,PRECURSOR_CHARGE"
    ",RECALIBRATED_PRECURSOR_MZ,RESOLUTION,SEQUENCE,SCORE,DELTA_SCORE,THRESHOLD_SCORE"
    ",RETENTION_TIME,PEPTIDE_ID,Q_VALUE,PEP,LOCAL_LENGTH_DEPENDENT_CUTOFF"
    ",VARIABLE_MODIFICATION_STRING,FIXED_MODIFICATION_STRING,MODIFICATION_DELTA_SUM"
    ",THEORETICAL_PEPTIDE_MASS,OBSERVED_PEPTIDE_MASS,MASS_ERROR_DA,MASS_ERROR_PPM"
    ",PROTEASE_NAME,EXPERIMENT_NAME,EXPERIMENT_ID,SCOPE_ID,SCOPE_NAME,PROJECT_NAME,SEARCH_ENGINE_NAME"
    ",SAMPLE_NAME,SAMPLE_ID,MS_ID,MS,SCORE_RANK"
    "&$format=json")


def process_name_line(line_content):
    split_line = line_content.strip('\n').split(' ')
    stripped_pep, charge = split_line[1].split('/')
    return stripped_pep, charge


def process_comment_line(line_content):
    split_line = line_content.strip('\n').split(' ')
    mods = split_line[2]
    irt = split_line[4].strip('iRT=')
    mod_content_split = mods.split('/')
    mod_num = mod_content_split[0].strip('Mods=')
    if mod_num == '0':
        mod_list = None
    else:
        mod_list = [(int(_.split(',')[0]), _.split(',')[1], _.split(',')[2]) for _ in set(mod_content_split[1:])]
        mod_list = sorted(mod_list, key=lambda x: x[0])
    return mod_list, irt


def peptide_add_mod(stripped_peptide, mod_list):
    mod_pep = ''
    previous_mod_site = 0
    for each_mod in mod_list:
        mod_site = each_mod[0] + 1
        mod_aa = each_mod[1]
        mod_type = each_mod[2]
        mod_pep += stripped_peptide[previous_mod_site: mod_site] + f'[{mod_type} ({mod_aa})]'
        previous_mod_site = mod_site
    mod_pep += stripped_peptide[previous_mod_site:]
    return mod_pep


def process_fragment_line(line_content):
    split_line = line_content.strip('\n').split('\t')
    mz = split_line[0]
    intensity = float(split_line[1])
    fragment_description = split_line[2].replace('"', '').split('/')
    fragment_identifier = fragment_description[0]
    fragment_type_num = re.findall('([by]\d+)', fragment_identifier)[0]
    fragment_charge = re.findall('\^(\d)', fragment_identifier)
    fragment_losstype = re.findall('-(.+?)(\^|$)', fragment_identifier)
    fragment_name = fragment_type_num
    if fragment_charge:
        fragment_name += '+{}'.format(fragment_charge[0])
    else:
        fragment_name += '+1'
    if fragment_losstype:
        fragment_name += '-{}'.format(fragment_losstype[0][0])
    else:
        fragment_name += '-noloss'
    return fragment_name, intensity


def read_synthetic_data(synthetic_file):
    with open(synthetic_file, 'r') as f:
        synthetic_data = dict()
        fragment_info = NonOverwriteDict()
        for line_series, each_line in enumerate(f):
            if each_line.startswith(' '):
                continue
            elif each_line == '\n':
                if mod_list:
                    precursor = '_{}_.{}'.format(peptide_add_mod(stripped_pep, mod_list), charge)
                else:
                    precursor = '_{}_.{}'.format(stripped_pep, charge)
                synthetic_data[precursor] = {'iRT': irt, 'Fragment': fragment_info, 'Precursor': precursor,
                                             'Charge': charge, 'StrippedPeptide': stripped_pep}
                fragment_info = NonOverwriteDict()
            elif each_line.startswith('Name'):
                stripped_pep, charge = process_name_line(each_line)
            elif each_line.startswith('MW'):
                continue
            elif each_line.startswith('Comment'):
                mod_list, irt = process_comment_line(each_line)
            elif each_line.startswith('Num peaks'):
                continue
            elif each_line[0].isdigit():
                fragment_name, intensity = process_fragment_line(each_line)
                fragment_info[fragment_name] = intensity
            else:
                print('Error in line {}'.format(line_series + 1))
    return synthetic_data
