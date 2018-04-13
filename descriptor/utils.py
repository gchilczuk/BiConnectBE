from django.utils.datetime_safe import datetime


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
