import requests, bs4
import pandas as pd
import logging  # Loggin Framework
import time  # Time
import re  # Support for Regular Expression


def populate_data_frame(job_listing):
    df = pd.DataFrame(columns=["job", "job_link", "company", "company_link"])
    for job in job_listing:
        cur_dict = {}
        cur_job = job.select('.job-item')

        cur_office = job.select('.joblist')

        if (len(cur_job) > 0 and len(cur_office) > 0):
            job_title = cur_job[0].getText().strip()
            job_link = cur_job[0].attrs['href']
            company_title = cur_office[0].getText().strip()
            company_link = cur_office[0].attrs['href']

            cur_dict["job"] = job_title
            cur_dict["job_link"] = job_link
            cur_dict["company"] = company_title
            cur_dict["company_link"] = company_link
            df = df.append(cur_dict, ignore_index=True)
    return df


def iterate_through_pages():
    end_of_page = False
    index = 0
    df = pd.DataFrame(columns=["job", "job_link", "company", "company_link"])

    while (not end_of_page):
        logging.debug("Loading Page : {}".format(index))
        try:
            index += 1
            # The pages are of format base-url/page-<index>
            # Request for a page using requests.
            res = requests.get("https://www.jobsnepal.com/premium-listings/page-{}".format(str(index)))
            res.raise_for_status()

            # Parse the page using beautifulsoup so that we can access specific tags
            soup = bs4.BeautifulSoup(res.text, features="html.parser")
            job_listing = soup.find_all("tr")

            # Get the required value using populate_data_frame
            cur_df = populate_data_frame(job_listing)
            logging.info("Current Data Frame Count: {} ".format(cur_df.count))

            # No Value in the new df indicates that we have reached a page where there is no data.
            if len(cur_df.index) == 0:
                end_of_page = True
                logging.debug("You have reached End of Page -  @ index {}".format(index))
            else:
                df = df.append(cur_df, ignore_index=True)
            logging.debug(df)

            time.sleep(1)
        except requests.exceptions.HTTPError:
            logging.debug("Http Error For Page : {}".format(index))
            end_of_page = True

    return df


def write_to_file(df):
    logging.debug("Writing into csv ")
    try:
        export_to_csv = df.to_csv(r'./test-data/jobnepal.csv')
        logging.info('Successfully wrote to a csv file')
    except:
        logging.error("Some Error occured while writing to csv file")


def create_job_link():
    df = iterate_through_pages()
    write_to_file(df)


if __name__ == '__main__':
    create_job_link()
