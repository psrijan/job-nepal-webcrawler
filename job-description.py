import requests, bs4
import pandas as pd
import logging  # Loggin Framework
import time  # Time
import re  # Support for Regular Expression

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')


def fetch_job_information():
    df = pd.read_csv("./test-data/jobnepal.csv", index_col=0)

    experience = []
    city = []
    education = []
    application_date = []

    for index, row in df.iterrows():
        print("Index: {}".format(index))
        link_to_job = row["job_link"]
        sauce = requests.get(link_to_job)
        soup = bs4.BeautifulSoup(sauce.text, features="html.parser")
        job_overview = soup.select("#job-overview li")

        apply_date = soup.select('.apply-before-date')
        application_date.append(apply_date[0].getText())

        for list_val in job_overview:
            label = list_val.label.getText()
            value = list_val.span.getText().strip()

            if re.match('experience', label.lower()):
                experience.append(value)
            elif re.match('city', label.lower()):
                city.append(value)
            elif re.match('education', label.lower()):
                value = value if not re.match('Please check vacancy details', value) else None
                education.append(value)

        logging.debug(experience)
        logging.debug(city)
        logging.debug(education)
        logging.debug(application_date)
        time.sleep(2)

    final_dataframe = df.assign(work_experience=experience) \
        .assign(location=city) \
        .assign(education_background=education) \
        .assign(deadline=application_date)

    export_to_csv = final_dataframe.to_csv(r'./test-data/jobnepal_additional.csv')


if __name__ == '__main__':
    fetch_job_information()
