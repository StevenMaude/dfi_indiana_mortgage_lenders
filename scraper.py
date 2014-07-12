# -*- coding: utf-8 -*-

import json
import datetime

import turbotlib
import lxml.html
import requests


def get_column_names(etree):
    """ Return list of column names from mortgage lenders table. """
    column_name_xpath = '//tr[@bgcolor="#003399"]/td'
    return [column.text_content() for column in etree.xpath(column_name_xpath)]


def yield_row_data(etree):
    """ Yield column data for a row from mortgage lenders table. """
    row_data_xpath = '//tr[@bgcolor="White"]'
    column_data_xpath = './/td'
    for row in etree.xpath(row_data_xpath):
        columns = []
        for column in row.xpath(column_data_xpath):
            # Handle empty cells with non-breaking spaces.
            if column.text_content() == u'\xa0':
                columns.append('')
            else:
                columns.append(column.text_content())
        yield columns


def main():
    """ Scrape licensed mortgage lenders data from extranet.dfi.in.gov """
    turbotlib.log("Starting run...")  # Optional debug logging
    source_url = 'http://extranet.dfi.in.gov/dfidb/mortgage.aspx'
    r = requests.get(source_url)

    etree = lxml.html.fromstring(r.content)
    column_names = get_column_names(etree)
    assert len(column_names) == 9, 'Number of columns has changed on site'

    sample_date = datetime.datetime.now().isoformat()

    for column_data in yield_row_data(etree):
        collected_data = dict(zip(column_names, column_data))
        collected_data['source_url'] = source_url
        collected_data['sample_date'] = sample_date 
        print json.dumps(collected_data)

    turbotlib.log("Run finished")

if __name__ == '__main__':
    main()
