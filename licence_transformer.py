import sys
import json

for line in sys.stdin:
    raw_record = json.loads(line)

    licence_record = {
        "company_name": raw_record['Company'],
        "company_jurisdiction": "United States of America",
        "licence_jurisdiction": "Indiana",
        "regulator": "Indiana Department of Financial Institutions",
        "category": "Financial",
        "licence_number": raw_record['LicID'],
        "jurisdiction_classification": 'Mortgage lenders',
        "confidence": 'HIGH',
        "source_url": raw_record['source_url'],
        "sample_date": raw_record['sample_date'],
        }

    print json.dumps(licence_record)
