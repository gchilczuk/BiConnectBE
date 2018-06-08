import os
from django.utils.datetime_safe import datetime

from BiConnect.settings import STATIC_ROOT


def sound_file_path(instance, filename):
    """
    Creates path to save sound file with speech.

    :param instance: an instance of Speech model
    :param filename: the filename that was originally given to the file
    :return:
    """
    if instance.meeting:
        group_id = instance.meeting.group.id
    else:
        group_id = 0
    meeting_date = instance.date or datetime.today().date()
    ymd = f'{meeting_date.year}/{meeting_date.month}/{meeting_date.day}'
    person_id = instance.person.id
    return f'sound/speeches/{group_id}/{ymd}/{person_id}_{filename}'


class Note(object):

    def __init__(self, meeting):
        self.meeting = meeting
        self.dir = STATIC_ROOT + f'{self.meeting.group.city}_{self.meeting.group.id}/'

    def generate_json(self):
        speeches = []
        for speech in self.meeting.speeches.get_queryset():
            bussiness_desc = speech.business_description
            req_desc = speech.requirements.first()
            rec_desc = speech.recommendations.first()
            speeches.append((speech.person, bussiness_desc, req_desc, rec_desc))

        return {
            'header': f'Podsumowanie spotkania grupy w mieście {self.meeting.group.city} z dnia {self.meeting.date}',
            'summary': f'W spotkaniu wzięło udział {self.meeting.count_guests + self.meeting.count_members} osób '
                       f'w tym {self.meeting.count_members} członków towarzystwa oraz {self.meeting.count_guests} gości.',
            'speeches': [{
                             'person': str(person),
                             'bus_description': bussiness_desc,
                             'req_description': req_desc,
                             'rec_description': rec_desc
                         } for person, bussiness_desc, req_desc, rec_desc in speeches]
        }

    def generate_txt(self):
        newline = '\r\n'
        json = self.generate_json()
        self.create_dir()
        file_path = self.dir + f'{self.meeting.id}_{self.meeting.date}'
        with open(file_path, 'w') as file:
            file.write(json['header'] + newline)
            file.write(newline)
            file.write(json['summary'] + newline)
            file.write(newline)
            file.write('WYSTĄPIENIA:' + newline)
            for speech in json['speeches']:
                file.write(speech.get('person') + newline)
                if speech.get('bus_description'):
                    file.write(speech.get('bus_description') + newline)
                if speech.get('req_description'):
                    file.write(speech.get('req_description').description + newline)
                if speech.get('rec_description'):
                    file.write(speech.get('rec_description').description + newline)
                file.write(newline)

        return file_path

    def create_dir(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
