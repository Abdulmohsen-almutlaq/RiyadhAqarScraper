import json
import random
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from multiprocessing import Pool


class Scraper:
    def __init__(self, area_url, file_name, num_processes=5):
        self.area_url = area_url
        self.file_name = file_name
        self.num_processes = num_processes
        self.chrome_options = self.get_chrome_options()

    def get_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheet": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--window-size=0,0')
        chrome_options.page_load_strategy = 'eager'
        return chrome_options

    def initialize_driver(self):
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

    def scrape_page(self, page_num):
        driver = self.initialize_driver()
        randomization = random.Random()
        url = f'{self.area_url}/{page_num}'

        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            delay1 = randomization.uniform(0, 4)
            time.sleep(delay1)
        except Exception as e:
            print(f"Error on page {page_num}: {e}")
            return []
        finally:
            driver.quit()

        delay = randomization.uniform(0, 6)
        time.sleep(delay)

        return self.parse_soup(soup)

    @staticmethod
    def parse_soup(soup):
        div_elements = soup.select('div._listingCard__PoR_B')
        data = []

        for div in div_elements:
            content_div = div.select_one('div._content__W4gas')
            description_div = div.select_one('._description__zVaD6')

            if content_div:
                title_element = content_div.find('h4')
                price_element = content_div.select_one('p._price__X51mi')
                specs_parent_div = content_div.select_one('div._specs__nbsgm')

                if title_element and price_element and specs_parent_div:
                    title = title_element.get_text(strip=True)
                    price = price_element.get_text(strip=True).split('/')[0].strip()

                    beds, living_rooms, bathrooms, area = "", "", "", ""

                    specs_elements = specs_parent_div.select('div._spec__SIJiK')
                    for spec in specs_elements:
                        area_match = re.search(r'(\d+(\.\d+)?)(?= م²)', spec.get_text(strip=True))
                        if area_match:
                            area = area_match.group(0)
                        else:
                            img_tag = spec.select_one('span img')
                            if img_tag:
                                icon_alt = img_tag['alt']
                                value = spec.get_text(strip=True)
                                if icon_alt == 'Bed':
                                    beds = value
                                elif icon_alt == 'Couch':
                                    living_rooms = value
                                elif icon_alt == 'Bath':
                                    bathrooms = value

                    description = description_div.get_text(strip=True) if description_div else ""

                    data.append({
                        "title": title,
                        "price": price,
                        "beds": beds,
                        "living_rooms": living_rooms,
                        "bathrooms": bathrooms,
                        "area": area,
                        "description": description
                    })
                else:
                    print("Title, price, or specs parent div not found within content div.")

        return data

    def save_data_to_json(self, results):
        with open(self.file_name, 'w', encoding='utf-8') as json_file:
            for result in results:
                for item in result:
                    json.dump(item, json_file, ensure_ascii=False)
                    json_file.write('\n')

    def scrape_until_no_more_pages(self):
        page_num = 1
        results = []
        while True:
            scraped_data = self.scrape_page(page_num)
            if not scraped_data:
                break
            results.append(scraped_data)
            page_num += 1
        return results

    def scrape_specified_number_of_pages(self, num_pages):
        page_nums = list(range(1, num_pages + 1))
        with Pool(self.num_processes) as pool:
            results = pool.starmap(self.scrape_page, [(page_num,) for page_num in page_nums])
        return results


def main():
    area_options = {
        "1": "https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%B4%D9%85%D8%A7%D9%84-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6",
        "2": "https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%BA%D8%B1%D8%A8-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6",
        "3": "https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%B4%D8%B1%D9%82-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6",
        "4": "https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%AC%D9%86%D9%88%D8%A8-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6"
    }

    print("Choose area to scrape:")
    print("1. North Riyadh")
    print("2. West Riyadh")
    print("3. East Riyadh")
    print("4. South Riyadh")
    area_choice = input("Enter your choice (1, 2, 3, or 4): ")

    if area_choice not in area_options:
        print("Invalid area option. Please choose 1, 2, 3, or 4.")
        return

    area_url = area_options[area_choice]
    file_name = input("Enter the file name for the output JSON file (without extension): ") + '.json'

    scraper = Scraper(area_url, file_name)

    print("Choose scraping option:")
    print("1. Scrape until there are no more pages")
    print("2. Specify number of pages to scrape")
    scrape_option = input("Enter your choice (1 or 2): ")

    if scrape_option == '1':
        results = scraper.scrape_until_no_more_pages()
    elif scrape_option == '2':
        num_pages = int(input("Enter the number of pages to scrape: "))
        results = scraper.scrape_specified_number_of_pages(num_pages)
    else:
        print("Invalid scraping option. Please choose 1 or 2.")
        return

    scraper.save_data_to_json(results)
    print("Scraping completed.")


if __name__ == '__main__':
    main()
