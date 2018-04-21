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
        self.dir = STATIC_ROOT + f'{self.meeting.group.id}/'

    def generate_json(self):
        requirements = []
        recommendations = []
        for speech in self.meeting.speeches.get_queryset():
            for req in speech.requirements.get_queryset():
                requirements.append((req, speech.person))
            for rec in speech.recommendations.get_queryset():
                recommendations.append((rec, speech.person))

        return {
            'header': f'Podsumowanie spotkania grupy w mieście {self.meeting.group.city} z dnia {self.meeting.date}',
            'summary': f'W spotkaniu wzięło udział {self.meeting.count_guests + self.meeting.count_members} osób '
                       f'w tym {self.meeting.count_members} członków towarzystwa oraz {self.meeting.count_guests} gości. '
                       f'Zgłoszono {len(requirements)} potrzeb oraz {len(recommendations)} rekomendacji.',
            'requirements': [{'description': req.description, 'person': str(person)} for req, person in requirements],
            'recommendations': [{'description': rec.description, 'person': str(person)} for rec, person in requirements]
        }

    def generate_txt(self):
        json = self.generate_json()
        self.create_dir()
        file_path = self.dir + f'{self.meeting.id}'
        with open(file_path, 'w') as file:
            file.write(json['header'] + '\n')
            file.write('\n')
            file.write(json['summary'] + '\n')
            file.write('\n')
            for req in json['requirements']:
                file.write(req['description'] + '\n')
                file.write(req['person'] + '\n')
                file.write('\n')
            for req in json['recommendations']:
                file.write(req['description'] + '\n')
                file.write(req['person'] + '\n')
                file.write('\n')

        return file_path

    def create_dir(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
