class LessonInfo:
    def __init__(self, lesson_name_id: int, class_id: int, teacher_id: int, room_id: int):
        self.lesson_name = lesson_name_id
        self.class_id = class_id
        self.teacher_id = teacher_id
        self.room_id = room_id

    def __str__(self):
        return '[name: %d, class: %d, teacher: %d, room: %d]' \
               % (self.lesson_name, self.class_id, self.teacher_id, self.room_id)


class Lesson:
    def __init__(self, lesson_info: LessonInfo, next_):
        self.info = lesson_info
        self.next = next_

    def __str__(self):
        return '<%s \n%s>' % (self.info, self.next)


class PeriodUnit:
    def __init__(self, period_id: int, first: Lesson):
        self.period_id = period_id
        self.next_lesson = first


class TimeTableInfo:
    def __init__(self, info: dict):
        self.number_of_school_subjects = 0
        self.teachers = info['teachers']
        self.number_of_teachers = len(self.teachers)
        self.rooms = info['rooms']
        self.number_of_rooms = len(self.rooms)
        self.groups = info['groups']
        self.number_of_group = len(self.groups)
        self.subjects = info['subjects']
        self.number_of_subjects = len('subjects')
        self.school_subjects_to_teachers = dict()
        self.group_to_sub = dict()
        self.constrains = dict()
        self.names = dict()
        for subject_to_teachers in info['sub_to_tea']:
            self.number_of_school_subjects += 1
            self.school_subjects_to_teachers[subject_to_teachers[0]] = subject_to_teachers[1]
        for constrain in info['constrains']:
            self.constrains[constrain[0]] = constrain[1]
        for names_tuple in info['names']:
            self.names[names_tuple[0]] = names_tuple[1]
        for group in self.groups:
            self.group_to_sub[group] = []
        for g_s_n_tuple in info['groups_to_sub']:
            self.group_to_sub[g_s_n_tuple[0]].append([g_s_n_tuple[1], g_s_n_tuple[2]])

    def __str__(self):
        teachers_template = ' '
        for teacher in self.teachers:
            teachers_template += self.names[teacher] + ', '
        rooms_template = ' '
        for room in self.rooms:
            rooms_template += self.names[room] + ', '
        subject_template = ' '
        for sub in self.subjects:
            subject_template += self.names[sub] + ', '
        st_template = ' '
        for subject in self.school_subjects_to_teachers:
            st_template += self.names[subject]
            st_template += ': <'
            for teacher in self.school_subjects_to_teachers[subject]:
                st_template += self.names[teacher]
                st_template += ', '
            st_template += '>'
        gs_template = ' '
        for group in self.group_to_sub:
            gs_template += '[ '
            gs_template += self.names[group] + ': '
            for _tuple in self.group_to_sub[group]:
                gs_template += self.names[_tuple[0]] + ' - ' + self.names[_tuple[1]] + ', '
            gs_template += ' ]'

        template = '[number_of_school_subjects:' + str(self.number_of_subjects) + '\n' \
                   + 'teachers:' + str(teachers_template) + '\n' \
                   + 'number_of_teachers:' + str(self.number_of_teachers) + '\n' \
                   + 'rooms:' + str(rooms_template) + '\n' \
                   + 'subjects:' + str(subject_template) + '\n' \
                   + 'number_of_subjects:' + str(self.number_of_subjects) + '\n' \
                   + 'school_subjects_to_teachers:' + str(st_template) + '\n' \
                   + 'group_to_sub:' + str(gs_template) + '\n' \
                   + 'constrains:' + str(self.constrains) + ']'
        return template


class TimeTable:
    def __init__(self, info: TimeTableInfo):
        pass


if __name__ == '__main__':
    import json

    f = open('Data/info.json', 'r')
    info = TimeTableInfo(json.loads(f.read()))
    print(info)