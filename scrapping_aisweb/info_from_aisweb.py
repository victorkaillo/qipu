import sys
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

import logging
import argparse

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By



base_data = {
        'cartas': {
            'xpath': None,
            'coluna': 'cartas', 
            'tag': 'h4', 
            },
        'sunrise': {
            'xpath': '/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/h4/sunrise',
            'coluna': 'sunrise', 
            'tag': 'sunrise', 
            },
        'sunset': {
            'xpath': '/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/h4/sunset',
            'coluna': 'sunset', 
            'tag': 'sunset', 
            },
        'metar': {
            'xpath': '/html/body/div/div/div/div[2]/div[2]/p[2]',
            'coluna': 'metar', 
            'tag': 'p', 
            },
        'taf': {
            'xpath': '/html/body/div/div/div/div[2]/div[2]/p[3]',
            'coluna': 'taf', 
            'tag': 'p', 
            }
        }

class WebCrawlear():


    def __init__(self, url=None) -> None:
        spacemoney_url = 'https://www.spacemoney.com.br/ultimas-noticias'
        self.url = url or spacemoney_url
        self.driver = None
        self.data_frame_infos = pd.DataFrame()
        # self.data_frame_infos[f'{coluna}'] = pd.DataFrame([], columns = [f'{coluna}'])

        self._make_driver(url=self.url)

    def _make_driver(self, url=None):
        """ Make firefox webdriver to be used by other methods
        """
        logging.debug("--> _make_driver")
        option = Options()
        option.headless = True
        self.driver = webdriver.Firefox(options=option)
        self.driver.get(url or self.url)
        logging.debug("<-- _make_driver")

    
    def _get_elements(self, element):
        """ Takes elements of a specified class
        input: str class_name
        """
        logging.debug("--> _get_elements_by_class_name")
        xpath = element.get('xpath') or None
        tag = element.get('tag') or None
        logging.debug(f"xpath: {xpath}")
        logging.debug(f"tag: {tag}")
        if xpath:
            self.list_with_web_elements = self.driver.find_elements(
            By.XPATH, xpath
            )
            logging.info(f"element_drive: {self.list_with_web_elements}") 

        elif tag:
            self.list_with_web_elements = self.driver.find_elements(
                By.TAG_NAME, tag
                )
            logging.info(f"element_drive: {self.list_with_web_elements}")
        else:
            logging.info('Not enough information to get element')
            self.list_with_web_elements = None
        logging.info(f"element_drive: {self.list_with_web_elements}") 
        logging.debug("<-- _get_elements_by_class_name")
    def _html_fit_to_str(self, soup, tag=''):
        logging.debug(f"--> _html_fit_to_str soup: {soup} tag: {tag}")
        info = str(soup)
        logging.debug(f" info: {info}")
        if tag:
            info = info.replace(f'<{tag}>','').replace(f'</{tag}>','')
            logging.debug(f" info: {info}")
        return info
    def _extract_html(self,web_element,element_dict):
        """ Extracts tag elements with a specific title tag from xpath
        """
        logging.debug(f"--> _extract_html {web_element}")
        html_content = web_element.get_attribute('outerHTML')
        logging.debug(f" html_content: {html_content}")
        soup_format_element = BeautifulSoup(html_content, 'html.parser')
        logging.debug(f" soup_format_element: {soup_format_element}")
        info = self._html_fit_to_str(soup_format_element, tag=element_dict['tag'])
        logging.debug(f"<-- _extract_html {type(info)}")
        logging.debug(f"<-- _extract_html {element_dict}")
        if 'cartas' in element_dict['coluna'] and ('=' in info):
            return None
        return info

        # return soup_title
    # /html/body/div/div/div/div[2]/div[2]/h5[2]
    # /html/body/div/div/div/div[2]/div[2]/p[2]
    # /html/body/div/div/div/div[2]/div[2]/p[3] /html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/h4/sunrise
    # sunrise_path =  
    # sunset_path = '/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/h4/sunset' 
    # metar = '/html/body/div/div/div/div[2]/div[2]/p[2]' 
    # taf= '/html/body/div/div/div/div[2]/div[2]/p[3]'
    def make_data_frame_news(self, element_dict):
        """ Create dataframe from all elements [elements list] with same class_name
        input: str class_name
        output: dataframe (save in self argument)"""
        logging.debug(f"--> make_data_frame_news {element_dict}")
        self._get_elements(element_dict)
        # if not self.list_with_elements:
        #     return None
        lista_news = []
        for web_element in self.list_with_web_elements :
            news = self._extract_html(web_element, element_dict)
            if news:
                lista_news.append(news)
        self.data_frame_infos[element_dict["coluna"]] = pd.Series(lista_news)
        logging.info(f'dataframe maked: \n{self.data_frame_infos}')
        logging.debug("<-- make_data_frame_news")
        return self.data_frame_infos

    def get_list_news(self):
        """ Create news list from dataframe.   
        """
        logging.debug("--> get_list_news")
        for element in base_data:
            dataframe_infos = self.make_data_frame_news(base_data[element])
        self.dataframe_list_news = dataframe_infos.values.tolist()
        logging.info(f'list_news maked: {self.dataframe_list_news}')
        logging.debug("--> get_list_news")
        self.driver.quit()

        return self.dataframe_list_news, dataframe_infos

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-icao_list", type=str,
                help="set a code icao for test", nargs='+')
    arguments = parser.parse_args()
    codigo_icao_default = 'SBMT'
    icao_list = arguments.icao_list or [codigo_icao_default]

    from utils.load_parameter_util import AppParameterLoadUtil



    app_parameter_load_util = AppParameterLoadUtil()
    CONFIG_PARAMS = app_parameter_load_util.get_dictinary(
        file_name='',
    )
    
    # url=f'https://aisweb.decea.mil.br/?i=aerodromos&codigo={codigo_icao}'
    # webcrawlear_config = CONFIG_PARAMS.get('webcrawlear') or None
    # if webcrawlear_config:
    #     url = webcrawlear_config['url']
    # logging.info(f'url: {url}') #SBJD
    try:
        lista={}
        dataframe={}
        print(icao_list)
        for icao in icao_list:
            print(icao)
            url=f'https://aisweb.decea.mil.br/?i=aerodromos&codigo={icao}'
            logging.info(f'url: {url}')
            webscralear = WebCrawlear(url)
            lista[icao], dataframe[icao] = webscralear.get_list_news()
        # print(lista)
        for icao in dataframe:
            # print(dataframe[icao])
            cartas = list(dataframe[icao]['cartas'])
            sunrise = list(dataframe[icao]['sunrise'])[0] 
            sunset = list(dataframe[icao]['sunset'])[0] 
            metar = list(dataframe[icao]['metar'])[0] 
            taf = list(dataframe[icao]['taf'])[0]
            print(f'{icao}:')
            print(f'cartas: {cartas}')
            print(f'sunrise: {sunrise}')
            print(f'sunset: {sunset}')
            print(f'metar: {metar}')
            print(f'taf: {taf}')
            print()
        print('Legenda: nan: Não informações disponíveis no momento')
        # webscralear = WebCrawlear(url)
        # lista, dataframe = webscralear.get_list_news()
    except Exception as e:
        logging.error(e)
    
    
    

    # driver = webdriver.Firefox()

    # driver.implicitly_wait(10)  # in seconds

    
    # Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
    # with open('ranking.json', 'w', encoding='utf-8') as jp:
    #     js = json.dumps(top10ranking, indent=4)
    #     jp.write(js)