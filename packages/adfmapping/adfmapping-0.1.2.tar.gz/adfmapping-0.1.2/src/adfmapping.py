import click
import logging as logger
import pandas as pd
import json


APPIN_TO_ADLS2_TEXT = '''           _____  _____ _____ _   _   _______ ____             _____  _       _____ ___  
     /\   |  __ \|  __ \_   _| \ | | |__   __/ __ \      /\   |  __ \| |     / ____|__ \ 
    /  \  | |__) | |__) || | |  \| |    | | | |  | |    /  \  | |  | | |    | (___    ) |
   / /\ \ |  ___/|  ___/ | | | . ` |    | | | |  | |   / /\ \ | |  | | |     \___ \  / / 
  / ____ \| |    | |    _| |_| |\  |    | | | |__| |  / ____ \| |__| | |____ ____) |/ /_ 
 /_/    \_\_|    |_|   |_____|_| \_|    |_|  \____/  /_/    \_\_____/|______|_____/|____|
                                                                                         
                                                                                         '''
ADLS2_TO_ASQL_TEXT = '''            _____   _        _____  ___    _______  ____               _____   ____   _      
     /\    |  __ \ | |      / ____||__ \  |__   __|/ __ \      /\     / ____| / __ \ | |     
    /  \   | |  | || |     | (___     ) |    | |  | |  | |    /  \   | (___  | |  | || |     
   / /\ \  | |  | || |      \___ \   / /     | |  | |  | |   / /\ \   \___ \ | |  | || |     
  / ____ \ | |__| || |____  ____) | / /_     | |  | |__| |  / ____ \  ____) || |__| || |____ 
 /_/    \_\|_____/ |______||_____/ |____|    |_|   \____/  /_/    \_\|_____/  \___\_\|______|
                                                                                             
                                                                                             '''

@click.command()
@click.argument("arg")
@click.option('--csvfile',help='Specify the path csv file obtained from Source data', type=click.Path(), required=True)
def get_dynamic_mapping(arg,csvfile):
    logger.info('START')
    columns = getCSVColumns(csvfile)
    logger.info("APPIN TO ADLS2 mapping")
    mapping_data = get_AppInToADLSMapping(columns)
    print(APPIN_TO_ADLS2_TEXT)
    APPIN_TO_ADLS2 = "APPIN_TO_ADLS2", '[%s]' % ', '.join(map(str, mapping_data))
    click.echo(APPIN_TO_ADLS2)
    logger.info("ADLS2 TO ASQL mapping")
    mapping_data = get_ADLSToASQLMapping(columns)
    ADLS2_TO_ASQL = "ADLS2_TO_ASQL", '[%s]' % ', '.join(map(str, mapping_data))
    print(ADLS2_TO_ASQL_TEXT)
    click.echo(ADLS2_TO_ASQL)
    logger.info('DONE')


def getCSVColumns(csvFile):
    try:
        df = pd.read_csv(csvFile)
        columnNames = list(df.columns)
        return columnNames
    except FileNotFoundError as error:
        logger.error("ERROR READING CSV FILE",error)

class mapping_Dict(dict):
#{"source": {"path": "$[0]"},"sink": {"name": "TenantId","type": "String"}}
    # __init__ function
    def __init__(self):
        self = dict()
    # Function to add key:value
    def add(self, key, value):
        self[key] = value

def Merge(dict1, dict2):
    return(dict2.update(dict1))

def getDictClassObj():
    try:
        mapping_dict_source = mapping_Dict()
        mapping_dict_path = mapping_Dict()
        mapping_dict_sink = mapping_Dict()
        mapping_dict_name = mapping_Dict()
        mapping_dict_type = mapping_Dict()
        return mapping_dict_source ,mapping_dict_path,mapping_dict_sink,mapping_dict_name,mapping_dict_type
    except Exception as error:
        logger.error("Error in Dict factory method :",error)

def get_dict_mapping_json_source(index,column):
    try:
        mapping_dict_source, mapping_dict_path, mapping_dict_sink, mapping_dict_name, mapping_dict_type = getDictClassObj()
        mapping_dict_path.add("path", '$[{}]'.format(index))
        mapping_dict_source.add("source", mapping_dict_path)
        mapping_dict_name.add("name", column)
        mapping_dict_type.add("type", "String")
        mapping_dict_sink.add("sink", mapping_dict_type)
        Merge(mapping_dict_name, mapping_dict_type)
        Merge(mapping_dict_sink, mapping_dict_source)
        return mapping_dict_source
    except Exception as error:
        logger.error("ERROR in mapping json", error)

def get_dict_mapping_json_sink(index,column):
    mapping_dict_source, mapping_dict_path, mapping_dict_sink, mapping_dict_name, mapping_dict_type = getDictClassObj()
    mapping_dict_path.add("path", '[{}]'.format(index))
    mapping_dict_source.add("source", mapping_dict_path)
    mapping_dict_name.add("name", column)
    mapping_dict_type.add("type", "String")
    mapping_dict_sink.add("sink", mapping_dict_type)
    Merge(mapping_dict_name, mapping_dict_type)
    Merge(mapping_dict_sink, mapping_dict_source)
    return mapping_dict_source


def get_AppInToADLSMapping(columns):
    mapping_list = []
    for index, column in enumerate(columns):
        mapping_dict = get_dict_mapping_json_source(index,column)
        mapping_list.append(json.dumps(mapping_dict))
    return mapping_list

def get_ADLSToASQLMapping(columns):
    mapping_list = []
    for index, column in enumerate(columns):
        mapping_dict = get_dict_mapping_json_sink(column,column)
        mapping_list.append(json.dumps(mapping_dict))
    return mapping_list

if __name__ == '__main__':
    logger.basicConfig(level=logger.INFO)
    get_dynamic_mapping()
