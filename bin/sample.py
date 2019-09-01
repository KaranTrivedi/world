#!/projects/world/venv/bin/python

#DEFAULTS
import configparser
import logging
#Added

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read('/projects/world/conf/config.ini')
SECTION = 'world'

def show_sections(logger):
    '''
    Output all options for given section
    '''

    conf_str = "\n\n"
    for sect in CONFIG.sections():
        conf_str += "[" + sect + "]\n"
        for var in list(CONFIG[sect]):
            conf_str += var + "\t\t=\t" + CONFIG[sect][var] + "\n"
    logger.info(conf_str)

def main():
    '''
    Main function.
    '''
    logging.basicConfig(filename=CONFIG[SECTION]['log'],\
                        level=CONFIG[SECTION]['level'],\
                        format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',\
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(SECTION)
    logger.info("####################STARTING####################")

    if CONFIG[SECTION]['level'] == "DEBUG":
        show_sections(logger=logger)

if __name__ == "__main__":
    main()
