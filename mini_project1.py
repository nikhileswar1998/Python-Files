import json
from os import sep
import gzip

def determine_data_type(value):
    """
    The function takes a string input and determines its data type to be either a float, int, or string. 
    """
    # BEGIN SOLUTION
    
    try:
        int(value)
        return(int)
    except ValueError:
        try:
            float(value)
            return(float)
        except ValueError:
            return str
    # END SOLUTION


def determine_data_type_of_list(values):
    """
    Write a function whose input is a list of strings. 
    This function determines the correct data type of all the elements in the list. 
    For example, ['1', '2', '3'] is int, ['1.1', '2.2', '3.3'] is float, ['1.1', '2', '3.3'] 
    is also float, and ['1.1', '234String', '3.3'] is str. 
    The purpose of this function to figure out what to cast an array of strings to. 
    Some lists might be all ints, in which case the data type is int. 
    Some might be a mixture of ints and floats, in which case the data type will be a float. 
    Some lists might be a mixture of ints, floats, and strings, 
    in which case the data type of the list will be a string.
    NOTE: This function should use "determine_data_type" function you coded previously

    """
    # BEGIN SOLUTION
    num=len(values)
    num_int=0
    num_float=0
    num_str=0
    for i in range(num):
        ans=determine_data_type(values[i])
        if(ans==int):
            num_int+=1
        elif(ans==float):
            num_float+=1
        else :
            num_str+=1
            return str
    
    if(num_float !=0):
        return float
    else :
        return int                
    # END SOLUTION


def format_sample_fields(format_field, sample_field):
    """
    Write a function whose inputs are a format field and sample field. 
    The format field looks like format_field = 'GT:AD:DP:GQ:PGT:PID:PL' and 
    the sample field looks like

    sample_field = {'XG102': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
                'XG103': '1/1:0,52:52:99:.:.:1517,156,0',
                'XG104': '0/1:34,38:72:99:.:.:938,0,796',
                'XG202': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
                'XG203': '1/1:0,52:52:99:.:.:1517,156,0',
                'XG204': '0/1:34,38:72:99:.:.:938,0,796',
                'XG302': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
                'XG303': '1/1:0,52:52:99:.:.:1517,156,0',
                'XG304': '0/1:34,38:72:99:.:.:938,0,796',
                'XG402': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
                'XG403': '1/1:0,52:52:99:.:.:1517,156,0',
                'XG404': '0/1:34,38:72:99:.:.:938,0,796'}

    Transform the inputs such that the output looks like this:

    output = {
        'XG102': {'AD': '0,76',
            'DP': '76',
            'GQ': '99',
            'GT': '1/1',
            'PGT': '1|1',
            'PID': '48306945_C_G',
            'PL': '3353,229,0'},
        'XG103': {'AD': '0,52',
                'DP': '52',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '.',
                'PID': '.',
                'PL': '1517,156,0'},
        'XG104': {'AD': '34,38',
                'DP': '72',
                'GQ': '99',
                'GT': '0/1',
                'PGT': '.',
                'PID': '.',
                'PL': '938,0,796'},
        'XG202': {'AD': '0,76',
                'DP': '76',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '1|1',
                'PID': '48306945_C_G',
                'PL': '3353,229,0'},
        'XG203': {'AD': '0,52',
                'DP': '52',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '.',
                'PID': '.',
                'PL': '1517,156,0'},
        'XG204': {'AD': '34,38',
                'DP': '72',
                'GQ': '99',
                'GT': '0/1',
                'PGT': '.',
                'PID': '.',
                'PL': '938,0,796'},
        'XG302': {'AD': '0,76',
                'DP': '76',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '1|1',
                'PID': '48306945_C_G',
                'PL': '3353,229,0'},
        'XG303': {'AD': '0,52',
                'DP': '52',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '.',
                'PID': '.',
                'PL': '1517,156,0'},
        'XG304': {'AD': '34,38',
                'DP': '72',
                'GQ': '99',
                'GT': '0/1',
                'PGT': '.',
                'PID': '.',
                'PL': '938,0,796'},
        'XG402': {'AD': '0,76',
                'DP': '76',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '1|1',
                'PID': '48306945_C_G',
                'PL': '3353,229,0'},
        'XG403': {'AD': '0,52',
                'DP': '52',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '.',
                'PID': '.',
                'PL': '1517,156,0'},
        'XG404': {'AD': '34,38',
                'DP': '72',
                'GQ': '99',
                'GT': '0/1',
                'PGT': '.',
                'PID': '.',
                'PL': '938,0,796'}}
    """

    # BEGIN SOLUTION
    
    formats=format_field.split(':')
    dict1={}
    for k,v in sample_field.items():
        values=v.split(':')
        values=[str(i) for i in values]
        unsort=dict(zip(formats,values))
        dict1[k]=unsort
    return dict1 
    
    
        
    # END SOLUTION


def create_dict_from_line(header, line):
    """
    Given the header and a single line, transform them into dictionary as described above. 
    Header and line input are provided in this cell. 

    Write a function whose inputs are a list containing the vcf header and a variant line. 
    The function should return a dictionary using the header as keys and the variant line as values.
     The function should use the format_sample_fields you wrote previously to format the sample fields. 
     The output of the first line looks like this:

    {'ALT': 'G',
    'CHROM': '4',
    'FILTER': 'PASS',
    'ID': '.',
    'INFO': 'AC=1;AF=0.167;AN=6;BaseQRankSum=-2.542;ClippingRankSum=0;DP=180;ExcessHet=3.0103;FS=0;MLEAC=1;MLEAF=0.167;MQ=52.77;MQRankSum=-4.631;QD=0.39;ReadPosRankSum=1.45;SOR=0.758;VQSLOD=-8.209;culprit=MQ;ANNOVAR_DATE=2018-04-16;Func.refGene=intergenic;Gene.refGene=IL2,IL21;GeneDetail.refGene=dist=38536,dist=117597;ExonicFunc.refGene=.;AAChange.refGene=.;Func.ensGene=intergenic;Gene.ensGene=ENSG00000109471,ENSG00000138684;GeneDetail.ensGene=dist=38306,dist=117597;ExonicFunc.ensGene=.;AAChange.ensGene=.;cytoBand=4q27;gwasCatalog=.;tfbsConsSites=.;wgRna=.;targetScanS=.;Gene_symbol=.;OXPHOS_Complex=.;Ensembl_Gene_ID=.;Ensembl_Protein_ID=.;Uniprot_Name=.;Uniprot_ID=.;NCBI_Gene_ID=.;NCBI_Protein_ID=.;Gene_pos=.;AA_pos=.;AA_sub=.;Codon_sub=.;dbSNP_ID=.;PhyloP_46V=.;PhastCons_46V=.;PhyloP_100V=.;PhastCons_100V=.;SiteVar=.;PolyPhen2_prediction=.;PolyPhen2_score=.;SIFT_prediction=.;SIFT_score=.;FatHmm_prediction=.;FatHmm_score=.;PROVEAN_prediction=.;PROVEAN_score=.;MutAss_prediction=.;MutAss_score=.;EFIN_Swiss_Prot_Score=.;EFIN_Swiss_Prot_Prediction=.;EFIN_HumDiv_Score=.;EFIN_HumDiv_Prediction=.;CADD_score=.;CADD_Phred_score=.;CADD_prediction=.;Carol_prediction=.;Carol_score=.;Condel_score=.;Condel_pred=.;COVEC_WMV=.;COVEC_WMV_prediction=.;PolyPhen2_score_transf=.;PolyPhen2_pred_transf=.;SIFT_score_transf=.;SIFT_pred_transf=.;MutAss_score_transf=.;MutAss_pred_transf=.;Perc_coevo_Sites=.;Mean_MI_score=.;COSMIC_ID=.;Tumor_site=.;Examined_samples=.;Mutation_frequency=.;US=.;Status=.;Associated_disease=.;Presence_in_TD=.;Class_predicted=.;Prob_N=.;Prob_P=.;SIFT_score=.;SIFT_converted_rankscore=.;SIFT_pred=.;Polyphen2_HDIV_score=.;Polyphen2_HDIV_rankscore=.;Polyphen2_HDIV_pred=.;Polyphen2_HVAR_score=.;Polyphen2_HVAR_rankscore=.;Polyphen2_HVAR_pred=.;LRT_score=.;LRT_converted_rankscore=.;LRT_pred=.;MutationTaster_score=.;MutationTaster_converted_rankscore=.;MutationTaster_pred=.;MutationAssessor_score=.;MutationAssessor_score_rankscore=.;MutationAssessor_pred=.;FATHMM_score=.;FATHMM_converted_rankscore=.;FATHMM_pred=.;PROVEAN_score=.;PROVEAN_converted_rankscore=.;PROVEAN_pred=.;VEST3_score=.;VEST3_rankscore=.;MetaSVM_score=.;MetaSVM_rankscore=.;MetaSVM_pred=.;MetaLR_score=.;MetaLR_rankscore=.;MetaLR_pred=.;M-CAP_score=.;M-CAP_rankscore=.;M-CAP_pred=.;CADD_raw=.;CADD_raw_rankscore=.;CADD_phred=.;DANN_score=.;DANN_rankscore=.;fathmm-MKL_coding_score=.;fathmm-MKL_coding_rankscore=.;fathmm-MKL_coding_pred=.;Eigen_coding_or_noncoding=.;Eigen-raw=.;Eigen-PC-raw=.;GenoCanyon_score=.;GenoCanyon_score_rankscore=.;integrated_fitCons_score=.;integrated_fitCons_score_rankscore=.;integrated_confidence_value=.;GERP++_RS=.;GERP++_RS_rankscore=.;phyloP100way_vertebrate=.;phyloP100way_vertebrate_rankscore=.;phyloP20way_mammalian=.;phyloP20way_mammalian_rankscore=.;phastCons100way_vertebrate=.;phastCons100way_vertebrate_rankscore=.;phastCons20way_mammalian=.;phastCons20way_mammalian_rankscore=.;SiPhy_29way_logOdds=.;SiPhy_29way_logOdds_rankscore=.;Interpro_domain=.;GTEx_V6_gene=.;GTEx_V6_tissue=.;esp6500siv2_all=.;esp6500siv2_aa=.;esp6500siv2_ea=.;ExAC_ALL=.;ExAC_AFR=.;ExAC_AMR=.;ExAC_EAS=.;ExAC_FIN=.;ExAC_NFE=.;ExAC_OTH=.;ExAC_SAS=.;ExAC_nontcga_ALL=.;ExAC_nontcga_AFR=.;ExAC_nontcga_AMR=.;ExAC_nontcga_EAS=.;ExAC_nontcga_FIN=.;ExAC_nontcga_NFE=.;ExAC_nontcga_OTH=.;ExAC_nontcga_SAS=.;ExAC_nonpsych_ALL=.;ExAC_nonpsych_AFR=.;ExAC_nonpsych_AMR=.;ExAC_nonpsych_EAS=.;ExAC_nonpsych_FIN=.;ExAC_nonpsych_NFE=.;ExAC_nonpsych_OTH=.;ExAC_nonpsych_SAS=.;1000g2015aug_all=.;1000g2015aug_afr=.;1000g2015aug_amr=.;1000g2015aug_eur=.;1000g2015aug_sas=.;CLNALLELEID=.;CLNDN=.;CLNDISDB=.;CLNREVSTAT=.;CLNSIG=.;dbscSNV_ADA_SCORE=.;dbscSNV_RF_SCORE=.;snp138NonFlagged=.;avsnp150=.;CADD13_RawScore=0.015973;CADD13_PHRED=2.741;Eigen=-0.3239;REVEL=.;MCAP=.;Interpro_domain=.;ICGC_Id=.;ICGC_Occurrence=.;gnomAD_genome_ALL=0.0003;gnomAD_genome_AFR=0.0001;gnomAD_genome_AMR=0;gnomAD_genome_ASJ=0;gnomAD_genome_EAS=0.0007;gnomAD_genome_FIN=0.0009;gnomAD_genome_NFE=0.0002;gnomAD_genome_OTH=0.0011;gerp++gt2=.;cosmic70=.;InterVar_automated=.;PVS1=.;PS1=.;PS2=.;PS3=.;PS4=.;PM1=.;PM2=.;PM3=.;PM4=.;PM5=.;PM6=.;PP1=.;PP2=.;PP3=.;PP4=.;PP5=.;BA1=.;BS1=.;BS2=.;BS3=.;BS4=.;BP1=.;BP2=.;BP3=.;BP4=.;BP5=.;BP6=.;BP7=.;Kaviar_AF=.;Kaviar_AC=.;Kaviar_AN=.;ALLELE_END',
    'POS': '123416186',
    'QUAL': '23.25',
    'REF': 'A',
    'SAMPLE': {'XG102': {'AD': '51,8',
                      'DP': '59',
                      'GQ': '32',
                      'GT': '0/1',
                      'PL': '32,0,1388'},
            'XG103': {'AD': '47,0',
                      'DP': '47',
                      'GQ': '99',
                      'GT': '0/0',
                      'PL': '0,114,1353'},
            'XG104': {'AD': '74,0',
                      'DP': '74',
                      'GQ': '51',
                      'GT': '0/0',
                      'PL': '0,51,1827'},
            'XG202': {'AD': '51,8',
                      'DP': '59',
                      'GQ': '32',
                      'GT': '0/1',
                      'PL': '32,0,1388'},
            'XG203': {'AD': '47,0',
                      'DP': '47',
                      'GQ': '99',
                      'GT': '0/0',
                      'PL': '0,114,1353'},
            'XG204': {'AD': '74,0',
                      'DP': '74',
                      'GQ': '51',
                      'GT': '0/0',
                      'PL': '0,51,1827'},
            'XG302': {'AD': '51,8',
                      'DP': '59',
                      'GQ': '32',
                      'GT': '0/1',
                      'PL': '32,0,1388'},
            'XG303': {'AD': '47,0',
                      'DP': '47',
                      'GQ': '99',
                      'GT': '0/0',
                      'PL': '0,114,1353'},
            'XG304': {'AD': '74,0',
                      'DP': '74',
                      'GQ': '51',
                      'GT': '0/0',
                      'PL': '0,51,1827'},
            'XG402': {'AD': '51,8',
                      'DP': '59',
                      'GQ': '32',
                      'GT': '0/1',
                      'PL': '32,0,1388'},
            'XG403': {'AD': '47,0',
                      'DP': '47',
                      'GQ': '99',
                      'GT': '0/0',
                      'PL': '0,114,1353'},
            'XG404': {'AD': '74,0',
                      'DP': '74',
                      'GQ': '51',
                      'GT': '0/0',
                      'PL': '0,51,1827'}}}
    """
    # BEGIN SOLUTION
    dict1={}
    lines=line.split('\t')
    
    for i in range(8):
        dict1[header[i]]=str(lines[i])
    #dict1=dict(sorted(dict1.items()))
    dict3={}
    header1=lines[8]
    for j in range(9,len(header)):
        dict3[header[j]]=lines[j]
    dict1['SAMPLE']=format_sample_fields(header1,dict3)
    return dict1      
    
    # END SOLUTION
def create_dict_from_line2(header,line):
    dict1={}
    lines=line.split('\t')
    
    for i in [0,1,3,4,7]:
        dict1[header[i]]=str(lines[i])
    #dict1=dict(sorted(dict1.items()))
    return dict1
    

def read_vcf_file(filename):
    """
    Write a function whose input is a filename for a vcf. 
    The function reads the vcf file one variant at a time and transforms it 
    into a dictionary using the create_dict_from_line function. 
    It returns a list containing all the variant dictionaries. 
    NOTE: Your function should be able to handle multiple lines.
    """
    # BEGIN SOLUTION
    # if line.startswith('#CHROM')
    with open(filename,'r') as f:
        header=[]
        ans=[]
        for line in f:
            if(line.startswith('#CHROM')):
                if not header:
                    line1=line[1:]
                    header=line1.strip().split('\t')
                    continue
            #line=line[:-1]
            elif(header):
                ans.append(create_dict_from_line(header,line.strip()))   
        #ans[-1]['SAMPLE']['XG404']['PL']-'\n'    
        return ans    
    # END SOLUTION

def extract_info_field(data):
    """
    Write a function that extracts the info field from the data dictionary that was 
    created in the previous part. The function should return all the info field dictionaries as list. 
    """
    # BEGIN SOLUTION
    ans=[]
    for item in data:
        for i,v in item.items():
            if(i=='INFO'):
                ans.append(str(v))
    return ans
    # END SOLUTION


def create_dictionary_of_info_field_values(data):
    """
    You now need to figure out that data types for each of the info fields. Begin by writing a function that first takes the info fields and turns them into a dictionary. Make sure to skip any fields that do not have a value or are missing a value.

    Note: only return keys that have values! 
    """

    # BEGIN SOLUTION
    dict1={}
    for i in data:
        semi=i.split(';')
        for j in semi:
            if('dist=' in j):
                k=j.strip().split('=',1)
            else:    
                k=j.strip().split('=')
            z=k[0]
            if(len(k)==2):
                if(k[1]!='.'):
                    if(j.strip().split('=')[0] not in dict1):
                        dict1[z]=[k[1]]
                    
                    elif(dict1[k[0]][0]!= k[1]):
                        dict1[k[0]]+=[k[1]]
    return dict1    
    # END SOLUTION
    


def determine_data_type_of_info_fields(data):
    """
    Write a function whose input is the output from create_dictionary_of_info_field_values 
    and uses the previously written function determine_data_type_of_list to determine 
    the data type of each of the info fields. The output is a dictionary whose 
    keys are the name of the info fields and values are the data type. 
    """
    # BEGIN SOLUTION
    dict1={}
    for k,v in data.items():
        val=determine_data_type_of_list(v)
        dict1[k]=val
    return dict1    
    # END SOLUTION


def format_data(data, info_field_data_type):
    """
    Write a function whose first input is the data from read_vcf_file and 
    the second input is the output from determine_data_type_of_info_fields. 
    The function converts the info field into a dictionary and uses the data types 
    that you determined to cast each field into the correct data type. 
    Make sure to convert the POS to int and QUAL to float. 
    The output will look something like this (I have removed most of the fields):

    The output will look something like this

    {
            "ALT": "G",
            "CHROM": "4",
            "FILTER": "PASS",
            "ID": ".",
            "INFO": {

                "Gene.ensGene": "ENSG00000109471,ENSG00000138684",
                "Gene.refGene": "IL2,IL21",
                "GeneDetail.ensGene": "dist=38306,dist=117597",
                "GeneDetail.refGene": "dist=38536,dist=117597"
            },
            "POS": 123416186,
            "QUAL" :23.25,
            "REF": "A",
            "SAMPLE": {
                "XG102": {
                    "AD": "51,8",
                    "DP": "59",
                    "GQ": "32",
                    "GT": "0/1",
                    "PL": "32,0,1388"
                }
        }

    Additional hints: The function in part 9 takes in two inputs. 
    input #1 is all the data read from lab1_data.vcf and converted into a 
    list of dictionaries where each dictionary corresponds to a line in the vcf file. 
    input #2 is a dictionary that tells you what the data type of each of the info field is.

    The purpose of part 9 is update each of the fields in "data" input so 
    that the data type matches what you have determined it to be previously.
    POS is an integer and QUAL is a float. For the info fields, you have already 
    created a dictionary called info_field_data_type that contains the information 
    for the data type of each of the info field. Now use this to cast the info field 
    into the correct data types.

    And the info field goes from being a string to a nested dictionary.

    NOTE: You can only test this function in the last part! There are not tests for it    

    """
    # BEGIN SOLUTION
    #data2=create_dictionary_of_info_field_values(data1)
    for i in range(len(data)):
        data[i]['POS']=int(data[i]['POS'])
        data[i]['QUAL']=float(data[i]['QUAL'])
        dict1={}
        semi=data[i]['INFO'].split(';')
        for j in semi:
            if('dist=' in j):
                k=j.strip().split('=',1)
            else:    
                k=j.strip().split('=')
            z=k[0]
            if(len(k)==2):
                if(k[1]!='.'):
                    if(j.strip().split('=')[0] not in dict1):
                        dict1[z]=info_field_data_type[k[0]](k[1])
        data[i]['INFO']=dict1                

    return data            
              
        
    # END SOLUTION
    
def format_data2(data):
    for i in range(len(data)):
        dict1={}
        semi=data[i]['INFO'].split(';')
        for j in semi :
            k=j.strip().split('=')
            if(len(k)==2):
                if(k[1]!='.'and ('_pred' in k[0])):
                    dict1[k[0]]=k[1]
        data[i]['INFO']=dict1
    return data                                            
            


def save_data_as_json(data, filename):
    """
    Write a function whose inputs are a Python dictionary and filename. 
    The function will saves the dictionary as a json file using the filename given. 
    Use the json library. 
    Use these options to correctly format your JSON -- 
    sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False. 
    Use this function to save your parsed data as a json file.
    """
    # BEGIN SOLUTION
    save=json.dumps(data,sort_keys=True,indent=4,separators=(',',':'),ensure_ascii=False)
    with open(filename,'w') as f:
        f.write(save)
        f.close()
    
    # END SOLUTION


def load_data_from_json(filename):
    """
    Write a function whose input is a filename for a json file. 
    The function should use the filename to read the JSON file in 
    which you saved your final parsed data. 
    """
    # BEGIN SOLUTION
    with open(filename,'r') as f:
        data=json.load(f)
        return data
    # END SOLUTION


def find_variant(CHROM, REF, ALT, POS, filename):
    """
    Write a function whose inputs are CHROM, REF, ALT, POS, and filename. 
    Using these inputs, the function should load a JSON file using the given 
    filename and return a list of variants that match the given CHROM, REF, ALT, and POS. 
    """
    # BEGIN SOLUTION
    data=load_data_from_json(filename)
    ans=[]
    for i in data:
        if((i['CHROM']==CHROM) and (i['REF']==REF) and (i['ALT']==ALT) and (i['POS']==POS)):
            ans.append(i)
    return ans        
    # END SOLUTION


def pull_basic_and_predictor_fields(filename):
    """
    Load mini_project1_data.json and pull out all the variants that have a 
    """
    # BEGIN SOLUTION
    data=load_data_from_json(filename)
    ans=[]
    arr=["FATHMM_pred","LRT_pred","MetaLR_pred",'MetaSVM_pred','MutationAssessor_pred',
         'MutationTaster_pred','PROVEAN_pred','Polyphen2_HDIV_pred','Polyphen2_HVAR_pred',
         'SIFT_pred','fathmm_MKL_coding_pred']
    
    for i in data:
        if(set(i['INFO'].keys()).isdisjoint(set(arr))):
            continue
        sum=0
        counter=0
        y={}
        for j in i['INFO'].keys():
            if(j in arr):
                counter+=1
                if(j=='FATHMM_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                elif(j=='LRT_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                elif(j=='MetaLR_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1                        
                elif(j=='MetaSVM_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1                                                
                elif(j=='MutationAssessor_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='H'):
                        sum+=1
                    elif(y[j]=='L'):
                        sum+=0.25
                    elif(y[j]=='M'):
                        sum+=0.5
                                
                elif(j=='MutationTaster_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                    elif(y[j]=='A'):
                        sum+=1    
                elif(j=='PROVEAN_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                elif(j=='Polyphen2_HDIV_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                    elif(y[j]=='P'):
                        sum+=0.5    
                elif(j=='Polyphen2_HVAR_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                    elif(y[j]=='P'):
                        sum+=0.5                            
                elif(j=='SIFT_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1                                                
                elif(j=='fathmm_MKL_coding_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
        if(counter>0):
            y['sum_predictor_values']=sum            
            y["CHROM"]=i['CHROM']
            y['POS']=i['POS']
            y['REF']=i['REF']
            y['ALT']=i['ALT']
            ans.append(y)
    return ans                                                                                                
    # END SOLUTION

def pull_basic_and_predictor_fields_gzip(filename):
    # BEGIN SOLUTION
    arr=["FATHMM_pred","LRT_pred","MetaLR_pred",'MetaSVM_pred','MutationAssessor_pred',
         'MutationTaster_pred','PROVEAN_pred','Polyphen2_HDIV_pred','Polyphen2_HVAR_pred',
         'SIFT_pred','fathmm_MKL_coding_pred']
    header=[]
    ans=[]
    ans2=[]
    with gzip.open(filename,'rt') as fp:
        for line in fp:
            if(line.startswith('#CHROM')):
                if not header:
                    line1=line[1:]
                    header=line1.strip().split('\t')
                    continue
            #line=line[:-1]
            elif(header and ('_pred' in line)):
                ans.append(create_dict_from_line2(header,line.strip()))
    # v1=extract_info_field(ans)
    # v2=create_dictionary_of_info_field_values(v1)
    # v3=determine_data_type_of_info_fields(v2)
    # data=format_data(ans,v3)
    data=format_data2(ans)
    data1=[i for i in data if (i['INFO'])]
    for i in data1:
        sum=0
        counter=0
        y={}
        for j in i['INFO'].keys():
            if(j in arr):
                counter+=1
                if(j=='FATHMM_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                elif(j=='LRT_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                elif(j=='MetaLR_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1                        
                elif(j=='MetaSVM_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1                                                
                elif(j=='MutationAssessor_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='H'):
                        sum+=1
                    elif(y[j]=='L'):
                        sum+=0.25
                    elif(y[j]=='M'):
                        sum+=0.5
                                
                elif(j=='MutationTaster_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                    elif(y[j]=='A'):
                        sum+=1    
                elif(j=='PROVEAN_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                elif(j=='Polyphen2_HDIV_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                    elif(y[j]=='P'):
                        sum+=0.5    
                elif(j=='Polyphen2_HVAR_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
                    elif(y[j]=='P'):
                        sum+=0.5                            
                elif(j=='SIFT_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1                                                
                elif(j=='fathmm_MKL_coding_pred'):
                    y[j]=i['INFO'][j]
                    if(y[j]=='D'):
                        sum+=1
        if(counter>0):
            y['sum_predictor_values']=sum            
            y["CHROM"]=i['CHROM']
            y['POS']=str(i['POS'])
            y['REF']=i['REF']
            y['ALT']=i['ALT']
            ans2.append(y)
    save=json.dumps(ans2,sort_keys=True,indent=2,separators=(',',':'),ensure_ascii=False)
    with open("mini_project1_gzip.json",'w') as f:
        f.write(save)
        f.close()      
        

                
             
    # END SOLUTION
filename = 'test_4families_annovar.vcf.gz'
pull_basic_and_predictor_fields_gzip(filename)

def return_all_non_zero_sum_predictor_values():
    # BEGIN SOLUTION
    data=load_data_from_json("mini_project1_gzip.json")
    ans=[]
    for i in data:
        if(i["sum_predictor_values"]!=0):
            ans.append(i)
    save=json.dumps(ans,sort_keys=True,indent=2,separators=(',',':'),ensure_ascii=False)
    with open("sum_predictor_values_gt_zero.json",'w') as f:
        f.write(save)
        f.close()        
    # END SOLUTION
              

