from outcome import Value
import scrapy
from webbrowser import Chrome
from typing import List
from scrapy.http import Response
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from procore_contractors.items import ProcoreContractorsItem
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time

class ContractorsSpider(scrapy.Spider):
    name = "contractors"
    start_url = "https://www.procore.com/network/en-US/ca"

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_url,
            callback=self.parse_contractors,
            wait_time=20,
            wait_until=EC.presence_of_all_elements_located((By.XPATH, "//h2[text()='Construction Professionals in Canada by Province']/parent::div//a"))
        )

    def parse_contractors(self, response: Response):
        # Initialize driver
        driver: Chrome = response.meta["driver"]
        
        # Run for each province
        provinces = response.xpath("//h2[text()='Construction Professionals in Canada by Province']/parent::div//a/@href").getall()
        for province in provinces:
            driver.get(response.urljoin(province))
            WebDriverWait(driver, timeout=20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-test-id="filter-Company Type"]//span[(@data-test-id="highlighted-text-part") and (text()="General Contractors" or text()="Specialty Contractors")]')))
            
            open_at_first_time: bool = True

            while True:
                # Filter for general and specialty contractors
                company_types_to_filter_tags_str: str = '//div[@data-test-id="filter-Company Type"]//span[(@data-test-id="highlighted-text-part") and (text()="General Contractors" or text()="Specialty Contractors")]'
                company_types_to_filter_checkbox_input_tags_str: str = company_types_to_filter_tags_str + '/ancestor::span[2]/preceding-sibling::span/input'

                if open_at_first_time:
                    company_types_to_filter_checkbox_input_tags = driver.find_elements(by=By.XPATH, value=company_types_to_filter_checkbox_input_tags_str)

                    for input_tag in company_types_to_filter_checkbox_input_tags:
                        driver.execute_script("arguments[0].click();", input_tag)

                    open_at_first_time: bool = False
                
                # Wait a moment until the display changes
                time.sleep(2)

                # Obtain list of companies per page
                response_obj: Selector = Selector(text=driver.page_source)
                contractors = response_obj.xpath('//div[contains(@class, "MuiBox-root")]/a[starts-with(@data-track-click, "Search Results, Navigation")]')

                # Extract company name, website, company type, and province
                for idx, contractor in enumerate(contractors):
                    contractor_item: ProcoreContractorsItem = self.parse_contractor_item(response, contractor, idx)
                    yield contractor_item

                # Move to next page
                try:
                    next_page_btn = driver.find_element(by=By.XPATH, value='//button[@aria-label="Go to next page"]')

                except NoSuchElementException:
                    break

                else:
                    driver.execute_script("arguments[0].click();", next_page_btn)
                    WebDriverWait(driver, timeout=20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "MuiBox-root")]/a[starts-with(@data-track-click, "Search Results, Navigation")]')))

    def parse_contractor_item(self, main_response: Response, contractor_selector: Selector, idx: int):
        contractor_item = ProcoreContractorsItem()
                
        contractor_item["company_name"] = contractor_selector.xpath('.//h2[@data-test-id="business-name"]/span/text()').get()
        contractor_item["website"] = main_response.urljoin(contractor_selector.xpath("./@href").get())
        contractor_item["company_type"] = contractor_selector.xpath(f'((//div[contains(@class, "MuiBox-root")]/a[starts-with(@data-track-click, "Search Results, Navigation")])[{idx+1}]//div[(@data-test-id="items-container")])[2]/span/text()').get()
        contractor_item["province"] = " ".join(contractor_selector.xpath('//h1[@data-test-id="header-title"]/text()').get().split(" ")[2:])
        return contractor_item