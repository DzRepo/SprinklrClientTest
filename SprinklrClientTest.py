#! /usr/bin/python3

import SprinklrClient as sc
import json
from easysettings import EasySettings
import sys
from datetime import timezone
import datetime
import time
import webbrowser as wb
import logging

"""
Sprinklr Client Test App

This application uses the SprinklrClient library to make calls to against the Sprinklr API, documented at https://developer.sprinklr.com 
The application expects a file named Sprinklr.conf to contain the following fields (do not include the [] characters):

# Configuration
access_token=[ACCESS TOKEN FROM OBTAINED FROM GENERATING CODE]
refresh_token=[REFRESH TOKEN FROM OBTAINED FROM GENERATING CODE]
redirect_uri=[REDIRECT URL defined in the application]
key=[APPLICATION KEY]
secret=[APPLICATION SECRET]

"""

client = None
settings = None

def authorize(api_key, redirect_uri, path=None):
    global client
    url = client.authorize(redirect_uri)
    wb.open(url, new=2)

def add_comment_to_case(case_number, comment):
    global client
    process_response(client.add_comment("CASE", case_number, comment))
    
def fetch_case_comment(case_number, comment_id):
    global client
    process_response(client.fetch_comment("CASE", case_number, comment_id))

def fetch_case_comments(case_number):
    global client
    process_response(client.search_comments(case_number, "UNIVERSAL_CASE"))

def fetch_access_token(code):
    logging.info("fetch_access_token called")
    global client
    global settings
    secret = settings.get('secret')
    redirect = settings.get('redirect')

    success = client.fetch_access_token(secret=secret, redirect_uri=redirect, code=code)

    if not success:
        logging.error(client.status_message)
        if client.status_message is not None:
            j_result = json.loads(client.status_message)
            print("Error: ", json.dumps(j_result, indent=4, sort_keys=True))


def refresh_access_token():
    global client
    secret = settings.get('secret')
    redirect = settings.get('redirect')
    code = settings.get('code')

    success = client.fetch_access_token(
        secret=secret, redirect_uri=redirect, code=code)

    if success:
        print("Encoding:", client.encoding)
        print("Last Status Code:", client.last_status_code)
        print("Access Token:", client.access_token)
        print("Refresh Token:", client.refresh_token)
    else:
        logging.error(client.status_message)
        if client.status_message is not None:
            j_result = json.loads(client.status_message)
            print("Error: ", json.dumps(j_result, indent=4, sort_keys=True))


def fetch_account(account_type, channel_id):
    global client
    process_response(client.fetch_account_by_channel_id(account_type, channel_id))

def fetch_all_dashboards():
    global client
    process_response(client.fetch_all_dashboards())


def fetch_dashboard_by_name(dashboard_name):
    global client
    process_response(client.fetch_dashboard_by_name(dashboard_name))


def fetch_dashboard_stream(dashboard_id, start, rows):
    global client
    process_response(client.fetch_dashboard_stream(
        dashboard_id=dashboard_id, start=start, rows=rows))


def fetch_listening_topics():
    global client
    process_response(client.fetch_listening_topics())


def fetch_listening_stream(filter_value, since_time, until_time, timezone_offset=14400000,  time_field="SN_CREATED_TIME",
                           details="STREAM", dimension="TOPIC", metric="MENTIONS", trend_aggregation_period=None, start=1,
                           rows=100, echo_request=False, tag=None, sort_key=None, message_format_options=None):
    global client

  #  process_response(client.fetch_listening_stream(filter_value, since_time, until_time, timezone_offset, time_field,
   #                                                details, dimension, metric, trend_aggregation_period, start,
    #                                               rows, echo_request, tag, sort_key, message_format_options))


def fetch_resources(types):
    global client
    process_response(client.fetch_resources(types))


def fetch_partner_accounts():
    global client
    process_response(client.fetch_partner_accounts())


def fetch_partner_campaigns():
    global client
    process_response(client.fetch_partner_campaigns())


def fetch_partner_account_groups():
    global client
    process_response(client.fetch_partner_account_groups())


def fetch_partner_users():
    global client
    process_response(client.fetch_partner_users())


def fetch_client_users():
    global client
    process_response(client.fetch_client_queues())


def fetch_clients():
    global client
    process_response(client.fetch_clients())


def fetch_client_url_shortners():
    global client
    process_response(client.fetch_client_url_shortners())


def fetch_inbound_custom_fields():
    global client
    process_response(client.fetch_inbound_custom_fields())


def fetch_outbound_custom_fields():
    global client
    process_response(client.fetch_outbound_custom_fields())


def fetch_profile_custom_fields():
    global client
    process_response(client.fetch_profile_custom_fields())


def fetch_media_asset_custom_fields():
    global client
    process_response(client.fetch_media_asset_custom_fields())


def fetch_account_custom_fields():
    global client
    process_response(client.fetch_account_custom_fields())


def fetch_um_statuses():
    global client
    process_response(client.fetch_um_statuses())


def fetch_um_priorities():
    global client
    process_response(client.fetch_um_priorities())


def fetch_accessible_users():
    global client
    process_response(client.fetch_accessible_users())


def fetch_approval_paths():
    global client
    process_response(client.fetch_approval_paths())


def fetch_partner_queues():
    global client
    process_response(client.fetch_partner_queues())


def fetch_client_queues():
    global client
    process_response(client.fetch_client_queues())


def fetch_partner_profile_lists():
    global client
    process_response(client.fetch_partner_profile_lists())


def fetch_client_profile_lists():
    global client
    process_response(client.fetch_client_profile_lists())


def fetch_macros():
    global client
    process_response(client.fetch_macros())

def fetch_permissions():
    global client
    process_response(client.fetch_permissions())

def fetch_user_groups():
    global client
    process_response(client.fetch_user_groups())

def fetch_report_by_file(file_name):
    global client
    report_object = None
    if file_name is not None:
        with open(file_name) as f_in:
            report_object = json.load(f_in)
        process_response(client.fetch_report(report_object))


def fetch_archived_cases():
    filter = {"query": "",
              "filters": [
                  {
                      "filterType": "IN",
                      "field": "channelType",
                      "values": ["SPRINKLR"]
                  },
                  {
                      "filterType": "IN",
                      "field": "archived",
                      "values": ["true"]
                  }
              ],
              "paginationInfo": {
                  "start": 0,
                  "rows": 100,
                  "sortKey": "caseModificationTime"
              }}

    if client.search_case_v1(filter):
        cases = client.result
        print(json.dumps(cases))
    else:
        print("Search Failed:", client.raw)


def fetch_webhook_types():
    global client
    process_response(client.fetch_webhook_types())


def fetch_case_by_number(case_number):
    global client
    process_response(client.fetch_case_by_number(case_number))


def fetch_message_by_umid(umid):
    global client
    process_response(client.fetch_message_by_UMID(umid))


def fetch_case_messages(case_id):
    global client
    process_response(client.fetch_case_associated_messages(case_id))


def fetch_user():
    global client
    process_response(client.fetch_user())


def fetch_user_by_id(user_id):
    global client
    process_response(client.fetch_user_by_id(user_id))

def send_email(account_id, from_email, subject, message):
    global client
    if client.send_email(account_id, from_email, subject, message):
        print("Sent successfully")
    else:
        print("Send failed:", client.raw)

def custom_field_add_option(id, option):
    global client
    option_data = {"addOptions": [option]}
    if client.update_custom_field_options(id, option_data):
        process_response(client.fetch_custom_field(id))
    else:
        print(client.raw)

def custom_field_delete_option(id, option):
    global client
    option_data = {"deleteOptions": [option]}
    if client.update_custom_field_options(id, option_data):
        process_response(client.fetch_custom_field(id))
    else:
        print(client.raw)


def date_time_toepoch(date_time):
    return datetime_toepoch(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute)

def datetime_toepoch(year: int, month: int, day: int, hour=0, minute=0):
    return int(float(time.mktime(datetime.datetime(year, month, day, hour, minute).timetuple())) * 1000)

def datetime_fromepoch(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S:{0:.0f}'.format(epoch % 1000), time.localtime(epoch))

def process_response(success):
    try:
        logging.debug("Success:" + str(success))
        if success:
            if client.result is None:
                logging.debug("No Results")
                logging.debug("Status Message:" + client.status_message)
                print(client.status_message)
            else:
                logging.debug("Result Type:" + str(type(client.result)))
                # logging.debug("Result:" + str(client.result))
                if type(client.result) is dict or type(client.result) is list:
                    print(json.dumps(client.result, sort_keys=False, indent=4))
                else:
                    print(client.result)
        else:
            if client.status_message is None:
                if type(client.result) is dict:
                    logging.debug("Result is a dictionary")
                    print(json.dumps(client.result, sort_keys=False, indent=4))
                else:
                    print(client.result)
            else:
                print(client.status_message)
    except Exception as ex:
        logging.error(str(ex))
        print("Error: " + str(ex))


def print_usage():
    print("Usage:")
    print("SprinklrClientTest AddCommentToCase {Case_Number} {Comment}")
    print("                   Authorize {apikey} {redirect_uri} [environment]")
    print("                   CustomFieldAddOption {field_id} {option_to_add}" )
    print("                   CustomFieldDeleteOption {field_id} {option_to_delete}" )
    print("                   FetchAccessToken {apikey} {secret} {code} {redirect uri}")
    print("                   FetchAccessibleUsers")
    print("                   FetchAccount {channel_type} {channel_id}")
    print("                   FetchAccountCustomFields")
    print("                   FetchAllDashboards")
    print("                   FetchArchivedCases")
    print("                   FetchCaseByNumber {case_number}")
    print("                   FetchCaseMessagesById {case_id}")
    print("                   FetchCaseAudit {raw_flag}")
    print("                   FetchClients")
    print("                   FetchClientProfileLists")
    print("                   FetchClientUrlShortners")
    print("                   FetchClientQueues")
    print("                   FetchClientUsers")
    print("                   FetchCaseComment {case_number} {comment_id}")
    print("                   FetchDashboardByName {name}")
    print(
        "                   FetchDashboardStream {stream_id} {start} {rows} [{echo request} (True or False)]")
    print("                   FetchInboundCustomFields")
    print("                   FetchListeningTopics")
    print(
        "                   FetchListeningStream {id} {sinceTime} {untilTime}")
    print("                   FetchMacros")
    print("                   FetchMediaAssetCustomFields")
    print("                   FetchMessageByUMId {message_id}")
    print("                   FetchOutboundCustomFields")
    print("                   FetchPartnerAccountGroups")
    print("                   FetchPartnerAccounts")
    print("                   FetchPartnerCampaigns")
    print("                   FetchPartnerQueues")
    print("                   FetchPartnerUsers")
    print("                   FetchPermissions")
    print("                   FetchProfileCustomFields")
    print("                   FetchReportByFile {report_request.json}")
    print("                   FetchResources {resource type}")
    print("                   FetchUMPriorities")
    print("                   FetchUMStatuses")
    print("                   FetchUser")
    print("                   FetchUserById {User_id}")
    print("                   FetchUserGroups")
    print("                   FetchWebhookTypes")
    print("                   RefreshAccessToken")
    print("                   SendEmail {to_address} {from_address} {subject} {message}")
    

def main():
    global settings
    global client

    try:
        logging.basicConfig(filename='SprinklrClient.log', level=logging.DEBUG)
        logging.debug("Starting SprinklrClientTest with " +
                      str(len(sys.argv) - 1) + " actual parameters")
                      
        settings = EasySettings("Sprinklr.conf")
        key = settings.get('key')
        path = settings.get('path')
        access_token = settings.get('access_token')

        if len(path) == 0:
            path = None

        # If using a differnent enviornment other that Prod, set path to that value (like 'prod2')
        client = sc.SprinklrClient(
            key=key, access_token=access_token, path=path)

        if len(sys.argv) > 1:
            command = str(sys.argv[1]).upper()

            if command == 'ADDCOMMENTTOCASE':
                add_comment_to_case(sys.argv[2], sys.argv[3])
            elif command == 'AUTHORIZE':
                if len(sys.argv) > 5:
                    print(
                        "Invalid command line - Usage: SprinklrClientTest Authorize {apikey} {redirect_uri} [environment]")
                else:
                    key = sys.argv[2]
                    redirect_uri = sys.argv[3]
                    if len(sys.argv) == 5:
                        path = sys.argv[4]
                    else:
                        path = None
                    client = sc.SprinklrClient(key)
                    authorize(key, redirect_uri, path)
            elif command == "CUSTOMFIELDADDOPTION":
                custom_field_add_option(sys.argv[2], sys.argv[3])
            elif command == "CUSTOMFIELDDELETEOPTION":
                custom_field_delete_option(sys.argv[2], sys.argv[3])
            elif command == 'FETCHALLDASHBOARDS':
                fetch_all_dashboards()
            elif command == 'FETCHACCESSTOKEN':
                if len(sys.argv) != 6:
                    print(
                        "Invalid command line - Usage: SprinklrClientTest GetAccessToken {path} {apikey} {secret} "
                        "{code} {redirect URI}")
                else:
                    path = sys.argv[2]
                    key = sys.argv[3]
                    secret = sys.argv[4]
                    code = sys.argv[5]
                    redirect = sys.argv[6]

                    client = sc.SprinklrClient(key, path)
                    success = client.fetch_access_token(
                        secret=secret, code=code, redirect_uri=redirect)

                    if success:
                        settings.set('access_token', client.access_token)
                        settings.set('refresh_token', client.refresh_token)
                        settings.set('redirect_uri', redirect)
                        settings.set('key', key)
                        settings.set('secret', secret)
                        settings.set('path', path),
                        settings.save()
                        print("Success")
                    else:
                        print(client.result)

                    key = settings.get('key')
                    access_token = settings.get('access_token')
                    client = sc.SprinklrClient(
                        key=key, access_token=access_token)
            elif command == 'FETCHACCESSIBLEUSERS':
                fetch_accessible_users()
            elif command == 'FETCHACCOUNT':
                fetch_account(sys.argv[2], sys.argv[3])
            elif command == 'FETCHACCOUNTCUSTOMFIELDS':
                fetch_account_custom_fields()
            elif command == 'FETCHARCHIVEDCASES':
                fetch_archived_cases()
            elif command == "FETCHCASEBYNUMBER":
                fetch_case_by_number(sys.argv[2])
            elif command == "FETCHCASECOMMENT":
                fetch_case_comment(sys.argv[2], sys.argv[3])
            elif command == "FETCHCASECOMMENTS":
                fetch_case_comments(sys.argv[2])
            elif command == "FETCHCASEMESSAGESBYID":
                fetch_case_messages(sys.argv[2])
            elif command == "FETCHCLIENTS":
                fetch_clients()
            elif command == 'FETCHCLIENTPROFILELISTS':
                fetch_client_profile_lists()
            elif command == "FETCHCLIENTURLSHORTNERS":
                fetch_client_url_shortners()
            elif command == 'FETCHCLIENTQUEUES':
                fetch_client_queues()
            elif command == 'FETCHCLIENTUSERS':
                fetch_client_users()
            elif command == 'FETCHDASHBOARDBYNAME':
                if len(sys.argv) != 3:
                    print(
                        "Invalid command line - Usage: SprinklrClientTest GetDashboardByName {name}")
                else:
                    fetch_dashboard_by_name(sys.argv[2])
            elif command == 'FETCHDASHBOARDSTREAM':
                fetch_dashboard_stream(sys.argv[2], sys.argv[3], sys.argv[4])
            elif command == 'FETCHINBOUNDCUSTOMFIELDS':
                fetch_inbound_custom_fields()
            elif command == 'FETCHLISTENINGTOPICS':
                fetch_listening_topics()
            elif command == 'FETCHLISTENINGSTREAM':
                if len(sys.argv) == 5:
                    fetch_listening_stream(
                        sys.argv[2], sys.argv[3], sys.argv[4])
                elif len(sys.argv) == 6:
                    fetch_listening_stream(
                        sys.argv[2], sys.argv[3], sys.argv[4], echo_request=sys.argv[5])
            elif command == 'FETCHMACROS':
                fetch_macros()
            elif command == 'FETCHMEDIAASSETCUSTOMFIELDS':
                fetch_media_asset_custom_fields()
            elif command == 'FETCHMESSAGEBYUMID':
                fetch_message_by_umid(sys.argv[2])
            elif command == 'FETCHOUTBOUNDCUSTOMFIELDS':
                fetch_outbound_custom_fields()
            elif command == 'FETCHPARTNERACCOUNTGROUPS':
                fetch_partner_account_groups()
            elif command == 'FETCHPARTNERACCOUNTS':
                fetch_partner_accounts()
            elif command == 'FETCHPARTNERCAMPAIGNS':
                fetch_partner_campaigns()
            elif command == 'FETCHPARTNERQUEUES':
                fetch_partner_queues()
            elif command == 'FETCHPARTNERUSERS':
                fetch_partner_users()
            elif command == 'FETCHPERMISSIONS':
                fetch_permissions()
            elif command == 'FETCHPROFILECUSTOMFIELDS':
                fetch_profile_custom_fields()
            elif command == "FETCHREPORTBYFILE":
                fetch_report_by_file(sys.argv[2])
            elif command == 'FETCHRESOURCES':
                fetch_resources(sys.argv[2])
            elif command == 'FETCHUSER':
                fetch_user()
            elif command == 'FETCHUSERBYID':
                fetch_user_by_id(sys.argv[2])
            elif command == 'FETCHUMPRIORITIES':
                fetch_um_priorities()
            elif command == 'FETCHUMSTATUSES':
                fetch_um_statuses()
            elif command == "FETCHUSERGROUPS":
                fetch_user_groups()
            elif command == "FETCHWEBHOOKTYPES":
                fetch_webhook_types()
            elif command == "REFRESHACCESSTOKEN":
                key = settings.get('key')
                secret = settings.get('secret')
                redirect = settings.get('redirect_uri')
                refresh_access_token = settings.get('refresh_token')
                path=settings.get('path')

                client = sc.SprinklrClient(key)

                success = client.refresh_access_token(secret, redirect, refresh_access_token)

                if success:
                    settings.set('access_token', client.access_token)
                    settings.set('refresh_token', client.refresh_token)
                    settings.set('redirect_uri', redirect)
                    settings.set('key', key)
                    settings.set('secret', secret)
                    settings.save()
                    print("Success")
                else:
                    print(client.result)
            elif command == "SENDEMAIL":
                send_email(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
            else:
                print_usage()
        else:
            print_usage()
    except Exception as ex:
        print("Error:" + str(ex))
        print_usage()

if __name__ == "__main__":
    main()
