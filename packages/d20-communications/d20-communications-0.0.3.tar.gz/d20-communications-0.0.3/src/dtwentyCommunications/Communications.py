# File: ORM supported communication module
# Author: alexsanchezvega
# Company: d20
# Version: 1.0


from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from dtwentyORM import BasicElement, Metadata
import json
import requests
import os
import sendgrid
from .Exceptions import *
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError

class Communications():
    if os.environ.get('D20_COMM_CONF') != None:
        conf = json.loads(os.environ.get('D20_COMM_CONF'))
        arangoURL=conf.get('D20_COMM_DBURL')
        username=conf.get('D20_COMM_DBUSERNAME')
        password=conf.get('D20_COMM_DBPASSWORD')        
    else:
        print("No configuration given, cannot start.")
        raise Exception

    db_client = Connection(arangoURL=arangoURL, username=username, password=password, verify=True, verbose=True, statsdClient=None, reportFileName=None, loadBalancing='round-robin', use_grequests=False, use_jwt_authentication=False, use_lock_for_reseting_jwt=True, max_retries=10)
    db_name = 'communications'

    def __init__(self):
        if not self.db_client.hasDatabase('communications'):
            self.db = self.db_client.createDatabase('communications')
            self.db.createCollection(className='Collection', name='Messages')
            self.db.createCollection(className='Collection', name='Status')
            self.db.createCollection(className='Collection', name='Optative')
        else:
            self.db = self.db_client['communications']

    class Messages(Collection):
        _fields = {
        }

    class Status(Collection):
        _fields = {
        }

    class Optative(Collection):
        _fields = {
        }

    class Email(BasicElement):
        db_name = 'communications'

        @classmethod
        def get_collection(cls):
            return 'Messages'

        def get_class(self):
            return 'Email'

        def make(self):
            self.attributes = ['sender', 'receiver', 'type', 'params', 'channel', 'status_code']
            for key in self.attributes:
                setattr(self, key, None)
            self.channel = 'email'

        def add_contacts(self, contacts_data : list, lists: list, ignore_errors=False):
            requirement = ['email', 'firstname', 'f_lastname']
            for contact_data in contacts_data:
                if False in [a in contact_data for a in requirement]:
                    if ignore_errors:
                        return
                    else:
                        raise MissingRequiredParametersException
            url = "https://api.sendgrid.com/v3/marketing/contacts"

            lists_ids = [Metadata.Parameter('find', {'_key' : list_id}).get('value') for list_id in lists  if Metadata.Parameter('find', {'_key' : list_id}).get('value') != None and Metadata.Parameter('find', {'_key' : list_id}).get('value') != '']

            contacts = []
            
            for contact_data in contacts_data:
                if '_key' in contact_data:
                    contact_data['uid'] = contact_data['_key']
                if "gender" in contact_data and contact_data["gender"] == 'Femenino':
                    contact_data["gender_ao"] = 'a'
                else:
                    contact_data["gender_ao"] = 'o'
                if "firstname" not in contact_data or contact_data["firstname"] is None:
                    contact_data["firstname"] = 'Socio'
                if "f_lastname" not in contact_data or contact_data["f_lastname"] is None:
                    contact_data["f_lastname"] = ''
                if "m_lastname" not in contact_data or contact_data["m_lastname"] is None:
                    contact_data["m_lastname"] = ''
                data =  {
                    "email": contact_data.get('email'),
                    "first_name": contact_data.get('firstname'),
                    "last_name": " ".join([contact_data.get("f_lastname"),contact_data.get("m_lastname")]),
                    "custom_fields": {
                            "w4_T": contact_data.get('uid', ''),
                            "w3_T": contact_data["gender_ao"]
                    }
                }
                contacts.append(data)

            payload = {
                "list_ids": lists_ids,
                "contacts": contacts
            }


            p = Metadata.Parameter('find', {'_key' : 'sg_conf'})

            sg = p.get('value')['api_key']     

            headers = {
                'authorization': f"Bearer {sg}",
                'content-type': "application/json"
                }

            print("PUT", url, json.dumps(payload), headers)
            response = requests.request("PUT", url, data=json.dumps(payload), headers=headers)

            print(response.text)
            if response.status_code == "200":
                return {'res': True}
            return {'res': False}

        
        def personalize(self):
            if "gender" in self.get('params') and self.get('params')["gender"] == 'Femenino':
                self.get('params')["gender_ao"] = 'a'
            else:
                self.get('params')["gender_ao"] = 'o'
            if "firstname" not in self.get('params') or self.get('params')["firstname"] is None:
                self.get('params')["firstname"] = 'Socio'
            if "f_lastname" not in self.get('params') or self.get('params')["f_lastname"] is None:
                self.get('params')["f_lastname"] = ''
            if "m_lastname" not in self.get('params') or self.get('params')["m_lastname"] is None:
                self.get('params')["m_lastname"] = ''
            data = {
                'personalizations': [
                    {
                    'to': [
                        {
                        'email': self.get('receiver'),
                        'name': " ".join([self.get('params')["firstname"],self.get('params')["f_lastname"],self.get('params')["m_lastname"]])
                        },
                    ],
                    'dynamic_template_data': self.get('params')
                    }
                ]
            }
            return data


        def send(self):
            p = Metadata.Parameter('find', {'_key' : self.get('type')})
            template_id = p.get('value')
            return self.sg_send(template_id)

        def send_by_id(self, template_id):
            return self.sg_send(template_id)

        def sg_send(self, template_id):
            if self.get('receiver', None) == None or self.get('receiver', None) == '':
                raise MissingRequiredParametersException 
            p = Metadata.Parameter('find', {'_key' : 'sg_conf'})

            sg = sendgrid.SendGridAPIClient(api_key=p.get('value')['api_key'])            
            email_from_name = p.get('value')['email_from_name']
            email_from_inbox = p.get('value')['email_from_inbox']

            data = self.personalize()
            data['template_id'] = template_id
            data['from'] = {
                    'name': email_from_name,
                    'email': email_from_inbox
                }

            try:
            # print(data)
            # print(sg)
            # print(template_id)
                response = sg.client.mail.send.post(request_body=data)
                self.sender = email_from_inbox
                self.status_code = response.status_code
                # print(response.status_code)
                # print(response.headers)
                self.create()
            except Exception:
                self.status_code = response.status_code
                self.create()
                return {'res': False, 'err_code': self.status_code, 'err_desc': 'Cannot send email', 'err_params': '?error=invalid_request'}
            if self.status_code in [200,202,'200','202']:
                return {'res': True}
            return {'res': False, 'err_code': self.status_code, 'err_desc': 'Cannot send email', 'err_params': '?error=invalid_request'}



    class PushNotification(BasicElement):
        db_name = 'communications'

        type_buttons = {
            "intake" : [
                    {
                        "id": "intake-confirm-button",
                        "text": "Registrar toma",
                        "icon": "https://icons.getbootstrap.com/icons/check2-circle.svg",
                    },
                    {
                        "id": "intake-view-button",
                        "text": "Ver tomas",
                        "icon": "https://icons.getbootstrap.com/icons/eye-fill.svg",
                    }
                ],
        }
        type_web_buttons = {
            "intake" : [
                    {
                        "id": "intake-confirm-button",
                        "text": "Registrar toma",
                        "icon": "https://icons.getbootstrap.com/icons/check2-circle.svg",
                        "url": "https://webapp.vitiacare.com/Reminders?confirm_intake={intakeID}"
                    },
                    {
                        "id": "intake-view-button",
                        "text": "Ver tomas",
                        "icon": "https://icons.getbootstrap.com/icons/eye-fill.svg",
                        "url": "https://webapp.vitiacare.com/Reminders"
                    }
            ],
        }

        @classmethod
        def get_collection(cls):
            return 'Messages'

        def get_class(self):
            return 'PushNotification'



        def make(self):
            self.attributes = ['heading', 'content', 'type', 'receivers', 'channel', 'status', 'additional_data']
            for key in self.attributes:
                setattr(self, key, None)
            self.channel = 'push'


        def send(self):
            if self.get('channel') == 'desktop':
                return self.send_desktop()
            elif self.get('channel') == 'mobile':
                return self.send_mobile()


        def send_mobile(self):
            push_messages = []
            for i, _ in enumerate(self.get('receivers')):
                to=self.get('receivers')[i]
                try:
                    if isinstance(self.get('content'), list):
                        body = self.get('content')[i]
                    else: 
                        body = self.get('content')
                except:
                    body = ''
                try:
                    if isinstance(self.get('additional_data'), list):
                        data = self.get('additional_data')[i]
                    else: 
                        data = self.get('additional_data')
                except:
                    data = {}
                try:
                    if isinstance(self.get('heading'), list):
                        title = self.get('heading')[i]
                    else: 
                        title = self.get('heading')
                except:
                    title = ''
                try:
                
                    push_messages.append(PushMessage(to=to,
                            body=body,
                            data=data,
                            title=title))
                except:
                    raise
                
            try:
                responses = PushClient().publish_multiple(push_messages)
            except PushServerError as exc:
                raise
            except (ConnectionError, HTTPError) as exc:
                raise self.retry(exc=exc)
            sent = 0
            for i, response in enumerate(responses):
                try:
                    # We got a response back, but we don't know whether it's an error yet.
                    # This call raises errors so we can handle them with normal exception
                    # flows.
                    response.validate_response()
                    sent += 1
                    self.create()
                except DeviceNotRegisteredError:
                    pass
                except PushTicketError as exc:
                    raise self.retry(exc=exc)
            return sent

        def send_desktop(self):

            p = Metadata.Parameter('find', {'_key' : 'os_conf'})
            api_key=p.get('value')['api_key']
            app_id=p.get('value')['app_id']



            header = {"Content-Type": "application/json; charset=utf-8",
                    "Authorization": f"Basic {api_key}"}


            buttons = []
            if self.get("type", "generic") in self.type_buttons:
                buttons = self.type_buttons[self.get("type", "generic")]
                for i,u in enumerate(buttons):
                    for k in u:
                        buttons[i][k] = buttons[i][k].format(**self.get('additional_data', {}))
            web_buttons = []
            if self.get("type", "generic") in self.type_web_buttons:
                web_buttons = self.type_web_buttons[self.get("type", "generic")]
                for i,u in enumerate(web_buttons):
                    for k in u:
                        web_buttons[i][k] = web_buttons[i][k].format(**self.get('additional_data', {}))
            payload = {
                "app_id": app_id,
                "include_external_user_ids": self.get('receivers'),
                "channel_for_external_user_ids": "push",
                "icon": "https://webapp.vitiacare.com/logo.png",
                "web_url": "https://webapp.vitiacare.com",
                "app_url": "https://webapp.vitiacare.com",
                "headings": {
                    "es": self.get('heading'),
                    "en": self.get('heading')
                },
                "contents": {
                    "es": self.get('content'),
                    "en": self.get('content')
                },
                "android_group": f'vitiacare_push_group_{self.get("type", "generic")}',
                "adm_group": f'vitiacare_push_group_{self.get("type", "generic")}',
                "thread_id": f'vitiacare_push_group_{self.get("type", "generic")}',
                "data": {
                    "notificationType": self.get("type", "generic"),
                },
                "buttons" : buttons,
                "web_buttons": web_buttons
            }

            payload['data'].update(self.get('additional_data', {}))

            try:

                req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
                self.status = req.status_code
                self.create()
            except Exception:
                return {'res': False, 'err_code': 500, 'err_desc': 'Cannot send', 'err_params': '?error=invalid_request'}
            if req.status_code == "200" or req.status_code == 200:
                return {'res': True}
            return {'res': False, 'err_code': 500, 'err_desc': 'Cannot send', 'err_params': '?error=invalid_request'}

    class Whatsapp(BasicElement):
        db_name = 'communications'

        @classmethod
        def get_collection(cls):
            return 'Messages'

        def get_class(self):
            return 'Whatsapp'

        def make(self):
            self.attributes = ['sender', 'receiver', 'type', 'params', 'channel', 'status_code']
            for key in self.attributes:
                setattr(self, key, None)
            self.channel = 'whatsapp'

        def send_oneway(self):

            p = Metadata.Parameter('find', {'_key' : 'twilio_conf'})
            api_key=p.get('value')['TWILIO_ACCOUNT_SID']
            app_id=p.get('value')['TWILIO_AUTH_TOKEN']

        