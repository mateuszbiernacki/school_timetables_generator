class LessonInfo:
    def __init__(self, lesson_name_id: int, class_id: int, teacher_id: int, room_id: int, period_id: int):
        self.lesson_name = lesson_name_id
        self.class_id = class_id
        self.teacher_id = teacher_id
        self.room_id = room_id
        self.period_id = period_id

    def __str__(self):
        return '[name: %d, class: %d, teacher: %d, room: %d]' \
               % (self.lesson_name, self.class_id, self.teacher_id, self.room_id)

    def get_list_of_all_IDs(self):
        return [self.class_id, self.teacher_id, self.room_id]


class Lesson:
    def __init__(self, lesson_info: LessonInfo, next_=None):
        self.info = lesson_info
        self.next = next_

    def __str__(self):
        return '<%s \n%s>' % (self.info, self.next)

    def add_lesson(self, lesson):
        if self.next is None:
            self.next = lesson
        else:
            self.next.add_lesson(lesson)


class PeriodUnit:
    def __init__(self, period_id: int, all_rooms: list, first=None):
        self.period_id = period_id
        self.next_lesson = first
        self.all_IDs = []
        self.free_rooms = all_rooms

    def check_IDs(self, ids: list):
        for ID in ids:
            if ID in self.all_IDs:
                return False
        return True

    def add_lesson(self, lesson: Lesson) -> bool:
        list_of_ids = lesson.info.get_list_of_all_IDs()
        if self.check_IDs(list_of_ids):
            for ID in list_of_ids:
                self.all_IDs.append(ID)
            if self.next_lesson is None:
                self.next_lesson = lesson
                return True
            else:
                self.next_lesson.add_lesson(lesson)
                return True
        else:
            return False


class TimeTableInfo:
    def __init__(self, input_data: dict):
        self.periods_on_one_day = input_data['periods_on_one_day']
        self.periods = input_data['periods']
        self.number_of_school_subjects = 0
        self.teachers = input_data['teachers']
        self.number_of_teachers = len(self.teachers)
        self.rooms = input_data['rooms']
        self.number_of_rooms = len(self.rooms)
        self.groups = input_data['groups']
        self.number_of_group = len(self.groups)
        self.subjects = input_data['subjects']
        self.number_of_subjects = len('subjects')
        self.school_subjects_to_teachers = dict()
        self.group_to_sub = dict()
        self.constrains = dict()
        self.names = dict()
        for subject_to_teachers in input_data['sub_to_tea']:
            self.number_of_school_subjects += 1
            self.school_subjects_to_teachers[subject_to_teachers[0]] = subject_to_teachers[1]
        for constrain in input_data['constrains']:
            self.constrains[constrain[0]] = constrain[1]
        for names_tuple in input_data['names']:
            self.names[names_tuple[0]] = names_tuple[1]
        for group in self.groups:
            self.group_to_sub[group] = []
        for g_s_n_tuple in input_data['groups_to_sub']:
            self.group_to_sub[g_s_n_tuple[0]].append([g_s_n_tuple[1], g_s_n_tuple[2], g_s_n_tuple[3]])

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
    def __init__(self, input_data: TimeTableInfo):
        self.info = input_data
        self.time_table_by_period = []
        for period in self.info.periods:
            self.time_table_by_period.append(PeriodUnit(period, self.info.rooms.copy()))

    def make_correct_timetable(self):
        list_of_all_possible_lessons = []
        for group_id in self.info.group_to_sub:
            for sub_and_num in self.info.group_to_sub[group_id]:
                for _ in range(sub_and_num[1]):
                    list_of_all_possible_lessons.append([group_id, sub_and_num[0], sub_and_num[2]])

        while len(list_of_all_possible_lessons) != 0:
            gro_sub_tea = list_of_all_possible_lessons.pop(0)
            for period_iter in range(len(self.info.periods)):
                if len(self.time_table_by_period[period_iter].free_rooms) == 0:
                    # period_iter += 1
                    continue
                r = self.time_table_by_period[period_iter].free_rooms.pop(0)
                g, s, t = gro_sub_tea[0], gro_sub_tea[1], gro_sub_tea[2]
                correct_adding = self.time_table_by_period[period_iter].add_lesson(Lesson(LessonInfo(s, g, t, r, period_iter + 4001)))
                if correct_adding:
                    break
                else:
                    self.time_table_by_period[period_iter].free_rooms.append(r)
                    # period_iter += 1
                    if period_iter > len(self.info.periods):
                        print('problem-01')
        return True


if __name__ == '__main__':
    import json

    f = open('Data/info.json', 'r')
    info = TimeTableInfo(json.loads(f.read()))
    time_table = TimeTable(info)
    time_table.make_correct_timetable()
    print('d')
