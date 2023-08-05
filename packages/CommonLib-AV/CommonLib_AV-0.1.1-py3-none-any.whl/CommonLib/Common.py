import csv
from datetime import datetime as _datetime
from os import path as _path
from json import dumps as _dumps
from httplib2 import Http as _Http
from cryptography.fernet import Fernet as _Fernet
from google.cloud import bigquery as _bigquery
from google.oauth2 import service_account as _service_account
import requests
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize as _json_normalize

# BigQuery Lib Methods
class GCloud:
    def __init__(self, projectName, cred_filepath):
        self.Project = projectName
        if _path.exists(cred_filepath):
            try:
                cred = _service_account.Credentials.from_service_account_file(cred_filepath)
                self.Credentials = cred
            except Exception as ex:
                raise ex
        else:
            raise FileNotFoundError("Error: Big Query Credential File Not Found")

    def CreateTable_fromCSV(self, csv_filepath, new_tablename, getSchemaFromTable=None, getSchemaForColumns=None):
        bq_client = _bigquery.Client(project=self.Project, credentials=self.Credentials)
        if getSchemaFromTable is not None:
            if getSchemaForColumns is not None:
                a = bq_client.query("select {} from {} limit 1".format(getSchemaForColumns, getSchemaFromTable))
            else:
                a = bq_client.query("select * from {} limit 1".format(getSchemaFromTable))

            schema = a.result().schema

            jobConfig = _bigquery.LoadJobConfig(
                schema = schema,
                allow_jagged_rows = True,
                allow_quoted_newlines = True,
                ignore_unknown_values = True,
                skip_leading_rows = 1,
                source_format = _bigquery.SourceFormat.CSV
            )
        else:
            jobConfig = _bigquery.LoadJobConfig(
                autodetect = True,
                allow_jagged_rows = True,
                allow_quoted_newlines = True,
                ignore_unknown_values = True,
                skip_leading_rows = 1,
                source_format = _bigquery.SourceFormat.CSV
            )
        if _path.exists(csv_filepath):
            try:
                with open(csv_filepath, "rb") as file:
                    job = bq_client.load_table_from_file(file, new_tablename, job_config=jobConfig)
                job.result()
                return job
            except Exception as ex:
                raise ex
        else:
            raise FileNotFoundError("FileNotFound")

    def CreateTable_fromDataFrame(self, dataFrameTable, new_tablename, schema):
        bq_client = _bigquery.Client(project=self.Project, credentials=self.Credentials)

        jobConfig = _bigquery.LoadJobConfig(
            schema = schema,
            allow_jagged_rows=True,
            allow_quoted_newlines=True,
            ignore_unknown_values=True,
            write_disposition="WRITE_TRUNCATE",
            source_format=_bigquery.SourceFormat.CSV
        )

        try:
            job = bq_client.load_table_from_dataframe(dataFrameTable, new_tablename, job_config = jobConfig)
            job.result()
            return job
        except Exception as ex:
            return ex

    def CreateTable_fromJSON(self, json, newTableName, schema):
        bq_client = _bigquery.Client(project=self.Project, credentials=self.Credentials)

        jobConfig = _bigquery.LoadJobConfig(
            schema = schema,
            ignore_unknown_values=True,
            write_disposition="WRITE_TRUNCATE",
            source_format=_bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        )
        try:
            job = bq_client.load_table_from_json(json, newTableName, job_config=jobConfig)
            job.result()
            return job
        except Exception as ex:
            raise ex

    def DeleteTable(self, tableName):
        try:
            bq_client = _bigquery.Client(project=self.Project, credentials=self.Credentials)
            bq_client.delete_table(tableName, not_found_ok=True)
        except Exception as ex:
            raise ex

    def GetTableSchema(self, getSchemaFromTable, getSchemaForColumns=None):
        bq_client = _bigquery.Client(project=self.Project, credentials=self.Credentials)

        if getSchemaForColumns is not None:
            a = bq_client.query("select {} from {} limit 1".format(getSchemaForColumns, getSchemaFromTable))
        else:
            a = bq_client.query("select * from {} limit 1".format(getSchemaFromTable))

        return a.result().schema

    def DryRun(self, query):
        bq_client = _bigquery.Client(project=self.Project, credentials=self.Credentials)
        job_config = _bigquery.QueryJobConfig(
            dry_run=True,
            use_query_cache=False
        )
        try:
            queryJob = bq_client.query(query, job_config=job_config)
            return queryJob.total_bytes_processed
        except Exception as ex:
            raise ex

    def GetData(self, query):
        bq_client = _bigquery.Client(project=self.Project, credentials=self.Credentials)
        try:
            job = bq_client.query(query)
            job.result()
            return job
        except Exception as ex:
            raise ex

    def GetData_asDataFrame(self, query):
        bq_client = _bigquery.Client(project=self.Project, credentials=self.Credentials)
        try:
            job = bq_client.query(query)
            job.result()
            return job.to_dataframe()
        except Exception as ex:
            raise ex

# ServiceNow Lib Methods
class ServiceNow:
    def __init__(self, URL, userName, password):
        self.userName = userName
        self.password = password
        self.URL = URL

    def getServiceNowData(self, filterString):
        url = self.URL + filterString
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, auth=(self.userName, self.password), headers=headers)
            if response.status_code != 200:
                raise Exception("Error 200: Service Now query returned with error")

            #bigQueryObj = GCloud("irm-eit-infra-ops", 'E:\\keys\\irm-eit-infra-ops-da41c8a4bb41.json')
            #bigQueryObj.CreateTable_fromDataFrame(pd._json_normalize(json.loads(response.content), record_path=["result"]),"SWTest.testTable")
            data = response.json()
            return data
        except Exception as ex:
            raise ex

# SolarWinds Lib Methods
class SolarwindsOperations:
    def __init__(self, URL, userName, password):
        self.userName = userName
        self.password = password
        self.URL = URL

    def getSolarwindsData(self, filterString):
        url = self.URL + filterString
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, auth=(self.userName, self.password), headers=headers, verify=False)
            if response.ok != True:
                raise Exception("Error: Request Failed")

            return response.json()
        except Exception as ex:
            raise ex

# CommonLib Operations Methods
class CommonOperations:
    def convertJSONtoCSV(self, jsondata, csvFilePath):
        try:
            dt = _json_normalize(jsondata)
            dt = dt.reindex(sorted(dt.columns), axis=1)
            dt.to_csv(csvFilePath, index=False, quoting=csv.QUOTE_ALL)
        except Exception as ex:
            raise ex

    def convertCSVtoJSON(self, csvFilePath):
        try:
            df = pd.read_csv(csvFilePath)
            df.fillna('', inplace=True)
            return df.to_dict('records')
        except Exception as ex:
            raise ex

    def convertDataFrametoJSON(self, dataFrame):
        try:
            return dataFrame.to_dict('records')
        except Exception as ex:
            raise ex

    def convertdictionarytoDataFrame(self, dictionaryData, schema):
        dataFrame = DataFrame.from_dict(dictionaryData)

        for sc in schema:
            if sc.field_type == 'INTEGER':
                dataFrame[sc.name] = dataFrame[sc.name].astype('int64')
            else:
                print('OTHER')

        return dataFrame

    def formatKeyForBigQuery(self, dictionaryList):
        newDictionaryList = []
        for dictionary in dictionaryList:
            newDictionary = dict()
            for key in dictionary.keys():
                newKey = key.replace('.', '_')
                newKey = newKey.replace(' ', '')
                newDictionary[newKey] = dictionary[key]
            newDictionaryList.append(newDictionary)
        return newDictionaryList

    def formatDataForBigQuery(self, dictionaryList):
        for dictionary in dictionaryList:
            for key in dictionary:
                if type(dictionary[key]) == list:
                    dictionary[key] = ','.join("'{0}'".format(x) for x in dictionary[key])
        dictionaryList = CommonOperations().formatKeyForBigQuery(dictionaryList)
        return dictionaryList

    def sendErrorNotification(self, reportType, reportName, logFileName):
        url = 'https://chat.googleapis.com/v1/spaces/AAAAXvvwfts/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_xoHYo51B37bgWIx8c9rezWkPt3D5Bk_zTWcihWyktM%3D'
        bot_message = {
                            "cards": [
                                {
                                    "header": {
                                        "title": reportName,
                                        "subtitle": "Execution Failed!",
                                        "imageUrl": "https://img.icons8.com/external-flatart-icons-flat-flatarticons/50/000000/external-alert-web-security-flatart-icons-flat-flatarticons.png",
                                        "imageStyle": "IMAGE"
                                    },
                                    "sections": [
                                        {
                                            "widgets": [
                                                {
                                                    "keyValue": {
                                                        "topLabel": "Report Type",
                                                        "content": reportType,
                                                        "contentMultiline": "false",
                                                        "icon": "BOOKMARK",
                                                        # "bottomLabel": "Delayed",
                                                    }
                                                },
                                                {
                                                    "keyValue": {
                                                        "topLabel": "Log File Name",
                                                        "content": logFileName,
                                                        "contentMultiline": "false",
                                                        "icon": "STAR"
                                                    }
                                                },
                                                {
                                                    "keyValue": {
                                                        "topLabel": "UTC Time",
                                                        "content": _datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S"),
                                                        "contentMultiline": "false",
                                                        "icon": "MAP_PIN"
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }

        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

        http_obj = _Http()

        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=_dumps(bot_message),
        )

    def sendSuccessNotification(self, reportType, reportName, totalRowsUpdated, bqTableName, message=None):
        url = 'https://chat.googleapis.com/v1/spaces/AAAAXvvwfts/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_xoHYo51B37bgWIx8c9rezWkPt3D5Bk_zTWcihWyktM%3D'
        bot_message = {
                            "cards": [
                                {
                                    "header": {
                                        "title": reportName,
                                        "subtitle": "Execution Successful!",
                                        "imageUrl": "https://img.icons8.com/cute-clipart/64/000000/double-tick.png",
                                        "imageStyle": "IMAGE"
                                    },
                                    "sections": [
                                        {
                                            "widgets": [
                                                {
                                                    "keyValue": {
                                                        "topLabel": "Report Type",
                                                        "content": reportType,
                                                        "contentMultiline": "false",
                                                        "icon": "BOOKMARK",
                                                        # "bottomLabel": "Delayed",
                                                    }
                                                },
                                                {
                                                    "keyValue": {
                                                        "topLabel": "Total Rows Updated",
                                                        "content": totalRowsUpdated,
                                                        "contentMultiline": "false",
                                                        "icon": "STAR"
                                                    }
                                                },
                                                {
                                                    "keyValue": {
                                                        "topLabel": "BigQuery Table",
                                                        "content": bqTableName,
                                                        "contentMultiline": "false",
                                                        "icon": "MAP_PIN",
                                                        "button": {
                                                            "textButton": {
                                                                "text": "View",
                                                                "onClick": {
                                                                    "openLink": {
                                                                        "url": "https://console.cloud.google.com/bigquery?project=irm-eit-infra-ops&page=table&p=irm-eit-infra-ops&d={}&t={}".format(bqTableName.split('.')[0], bqTableName.split('.')[1])
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }

        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

        http_obj = _Http()

        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=_dumps(bot_message),
        )

    def call_key(self):
        return open("pass.key", "rb").read()

    def decrypt(self, encryptedString):
        try:
            key = self.call_key()
            b = _Fernet(key)
            return b.decrypt(encryptedString.encode()).decode('utf-8')
        except Exception as ex:
            raise ex

    def encrypt(self, stringToEncrypt):
        try:
            key = self.call_key()
            encodedString = stringToEncrypt.encode()
            a = _Fernet(key)
            return a.encrypt(encodedString).decode()
        except Exception as ex:
            raise ex

    def genwrite_key(self):
        key = _Fernet.generate_key()
        with open("pass.key", "wb") as key_file:
            key_file.write(key)

    def sendEmail(self, sender, to, subject, body, file=None):
        import smtplib

        message = """From: OneEngine
MIME-Version:1.0
Content-type:text/html
Subject: {}

{}
""".format(subject, body)

        try:
            smtpObj = smtplib.SMTP('xmail.ironmountain.com')
            smtpObj.sendmail(sender, to, message)
            print("MAIL")
        except Exception as ex:
            raise ex
