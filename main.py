from datetime import datetime
from itertools import chain
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


URL = 'https://globoesporte.globo.com/futebol/futebol-internacional/futebol-espanhol/'
teams_tb_xpath = '//*[@id="classificacao__wrapper"]/article/section[1]/div/table[1]/tbody/tr'
points_tb_xpath = '//*[@id="classificacao__wrapper"]/article/section[1]/div/table[2]/tbody/tr'


def setup():
    option = Options()
    option.headless = True
    driver = webdriver.Chrome(options=option)
    return driver


def request(driver, url):
    driver.get(url)
    # driver.maximize_window()


def tr_to_rank(tr):
    tds = tr.find_elements_by_xpath('./td')
    ranking, team, _ = [e.text for e in tds]
    return ranking, team


def tr_to_points(tr):
    tds = tr.find_elements_by_xpath('./td')
    points, _, _, _, _, goals, _, _, _, _ = [e.text for e in tds]
    last_matches = tr_to_last_matches(tr)
    return points, last_matches, goals


def tr_to_last_matches(tr):
    spans = tr.find_elements_by_xpath('./td[10]/span')
    span_class = [e.get_attribute('class')[-2] for e in spans]
    last_matches = ''.join([i[0] for i in span_class])
    return last_matches


def create_dataframe(table):
    df = pd.DataFrame(table)
    df.columns = ['Classificação', 'Time', 'Pontos',
                  'Histórico de jogos', 'Gols marcados']
    return df


def main():
    driver = setup()
    request(driver, URL)
    trs_ranking = driver.find_elements_by_xpath(teams_tb_xpath)
    trs_points = driver.find_elements_by_xpath(points_tb_xpath)
    ranking_and_team = [tr_to_rank(tr) for tr in trs_ranking]
    points = [tr_to_points(tr) for tr in trs_points]
    last_matches = [tr_to_last_matches(tr) for tr in trs_points]
    table = [list(chain(*i)) for i in zip(ranking_and_team, points)]
    df = create_dataframe(table)
    driver.quit()
    file_creation_date = datetime.now().strftime('%d-%m-%Y %H-%M')
    df.to_excel(f'classificação {file_creation_date}.xlsx', index=False)


if __name__ == "__main__":
    main()
