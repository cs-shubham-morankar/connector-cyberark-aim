"""
Copyright start
MIT License
Copyright (c) 2026 Fortinet Inc
Copyright end
"""

import requests
from requests.adapters import HTTPAdapter
import ssl
from requests_ntlm import HttpNtlmAuth
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('cyberark-aim')


# --- ADD THIS CLASS (necessary for SECLEVEL=1 cipher) ---
class SSLAdapter(HTTPAdapter):
    def __init__(self, verify_ssl=True, cipher_string=None, *args, **kwargs):
        self.verify_ssl = verify_ssl
        self.cipher_string = cipher_string
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()

        # Apply user-provided cipher string if available
        if self.cipher_string:
            ctx.set_ciphers(self.cipher_string)

        # Disable validation only if verify_ssl=False
        if not self.verify_ssl:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)


class CyberARK:
    def __init__(self, config):
        self.base_url = config['server_url'].strip("/")
        if not self.base_url.startswith('https://'):
            self.base_url = 'https://{0}'.format(self.base_url)
        self.cipher_string = config.get("security_level")
        self.verify_ssl = config.get('verify_ssl')

        # --- CREATE A SESSION AND MOUNT THE CUSTOM SSL ADAPTER ---
        self.session = requests.Session()
        self.session.mount("https://", SSLAdapter(self.verify_ssl, cipher_string=self.cipher_string))

        self.auth_type = config.get('auth_type')
        if self.auth_type == 'Basic Auth':
            self.username = config.get('username')
            self.password = config.get('password')
            self.auth = HttpNtlmAuth(self.username, self.password)
        else:
            self.auth = None
        self.headers = {'Content-Type': 'application/json'}

    def make_request_call(self, endpoint, payload=None, query_params=None, method='GET'):
        url = '{base}{endpoint}'.format(base=self.base_url, endpoint=endpoint)
        try:
            response = self.session.request(
                method,
                url,
                data=payload,
                params=query_params,
                headers=self.headers,
                auth=self.auth,
                verify=self.verify_ssl
            )
            logger.debug("Response: {0}".format(response.text))
            if response.ok or response.status_code == 204:
                logger.info('Successfully got response for url {0}'.format(url))
                if 'json' in str(response.headers):
                    return response.json()
                else:
                    return response
            else:
                logger.debug("response_content {0}:{1}".format(response.status_code, response.content))
                raise ConnectorError("{0}:{1}".format(response.status_code, response.text))
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError(
                'The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid Credentials')
        except Exception as err:
            raise ConnectorError(str(err))


def get_password(config, params):
    try:
        cyber_ark = CyberARK(config)
        formatted_output = []
        object_list = config.get('Object')
        if params.get('Folder'):
            folder = params.get('Folder')
        elif config.get('Folder'):
            folder = config.get('Folder')
        else:
            folder = ""
        if isinstance(object_list, str):
            object_list = [obj.strip() for obj in object_list.split(",") if obj.strip()]
        for obj in object_list:
            query_parameters = {
                "Object": obj
            }
            if folder:
                query_parameters["Folder"] = folder
            endpoint = operations['get_credentials'][1].format(config.get('AppID'), config.get('Safe'))
            additional_attributes = params.get('additional_attributes')
            if additional_attributes:
                query_parameters.update(params.pop('additional_attributes'))
            query_parameters = {k: v for k, v in query_parameters.items() if v is not None and v != ''}
            retrieve_creds = cyber_ark.make_request_call(endpoint, method='GET', query_params=query_parameters)
            formatted_output.append(retrieve_creds)
        return formatted_output
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_credentials(config, params):
    cyber_ark = CyberARK(config)
    formatted_output = []
    object_list = config.get('Object')
    folder = config.get('Folder')
    if isinstance(object_list, str):
        object_list = [obj.strip() for obj in object_list.split(",") if obj.strip()]
    for obj in object_list:
        query_parameters = {
            "Object": obj
        }
        if folder:
            query_parameters["Folder"] = folder
        endpoint = operations['get_credentials'][1].format(config.get('AppID'), config.get('Safe'))
        get_account_det = cyber_ark.make_request_call(endpoint, method='GET', query_params=query_parameters)
        user_name = get_account_det.get('Name')
        formatted_output.append({
            "key": user_name if user_name else "No Name present on CyberArk UI",
            "display_name": user_name if user_name else "No Name present on CyberArk UI"
        })
    return formatted_output


def get_credentials_details(config, params):
    cyber_ark = CyberARK(config)
    Object = params.get('secret_id')
    query_parameters = {}
    if config.get('Folder'):
        query_parameters["Folder"] = config.get('Folder')
    endpoint = operations['get_credentials_details'][1].format(config.get('AppID'), config.get('Safe'), Object)
    get_account_det = cyber_ark.make_request_call(endpoint, method='GET', query_params=query_parameters)
    formatted_output = []
    list_items = list(get_account_det.keys())
    for item in list_items[:8]:
        formatted_output.append(
            {
                "field_name": item,
                "value": "*****"
            }
        )
    return formatted_output


def get_credential(config, params):
    cyber_ark = CyberARK(config)
    Object = params.get('secret_id')
    query_parameters = {}
    if config.get('Folder'):
        query_parameters["Folder"] = config.get('Folder')
    endpoint = operations['get_credentials_details'][1].format(config.get('AppID'), config.get('Safe'), Object)
    get_account_det = cyber_ark.make_request_call(endpoint, method='GET', query_params=query_parameters)
    attribute_name = params.get('attribute_name')
    if attribute_name in get_account_det:
        return {
            "password": get_account_det.get(attribute_name)
        }
    else:
        return {
            "message": "Invalid Attribute"
        }


def _check_health(config):
    try:
        response = get_password(config, params={})
        if response:
            return True
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


operations = {
    'get_credentials': [get_credentials, '/AIMWebService/api/Accounts?AppID={0}&Safe={1}'],
    'get_credentials_details': [get_credentials_details, '/AIMWebService/api/Accounts?AppID={0}&Safe={1}&Object={2}'],
    'get_credential': [get_credential, '/AIMWebService/api/Accounts?AppID={0}&Safe={1}&Object={2}']
}
