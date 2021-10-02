class LessonInfo:
    def __init__(self, lesson_name_id: int, class_id: int, teacher_id: int, room_id: int, period_id: int):
        self.lesson_name = lesson_name_id
        self.class_id = class_id
        self.teacher_id = teacher_id
        self.room_id = room_id
        self.period_id = period_id
        self.IDs = [self.lesson_name, self.class_id, self.teacher_id, self.room_id]

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

    def get_lesson(self, object_id):
        if self.next is None:
            return []
        elif object_id in self.next.info.IDs:
            return self.next.info.IDs
        else:
            return self.next.get_lesson(object_id)


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

    def get_lesson(self, object_id):
        if self.next_lesson is None:
            return []
        elif object_id in self.next_lesson.info.IDs:
            return self.next_lesson.info.IDs
        else:
            return self.next_lesson.get_lesson(object_id)

    def __str__(self):
        lesson = self.next_lesson
        counter = 1
        if not self.all_IDs:
            return '0 lessons'
        while lesson.next is not None:
            counter += 1
            lesson = lesson.next
        return '%d lessons' % counter


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
        self.bad_records = []
        for period in self.info.periods:
            self.time_table_by_period.append(PeriodUnit(period, self.info.rooms.copy()))

    def make_correct_timetable(self):
        import random

        list_of_all_possible_lessons = []
        for group_id in self.info.group_to_sub:
            for sub_and_num in self.info.group_to_sub[group_id]:
                for _ in range(sub_and_num[1]):
                    list_of_all_possible_lessons.append([group_id, sub_and_num[0], sub_and_num[2]])
        random.shuffle(list_of_all_possible_lessons)
        while len(list_of_all_possible_lessons) != 0:
            gro_sub_tea = list_of_all_possible_lessons.pop(0)
            is_good = False
            for period_iter in range(len(self.info.periods)):
                if len(self.time_table_by_period[period_iter].free_rooms) == 0:
                    # period_iter += 1
                    continue
                r = self.time_table_by_period[period_iter].free_rooms.pop(0)
                g, s, t = gro_sub_tea[0], gro_sub_tea[1], gro_sub_tea[2]
                correct_adding = self.time_table_by_period[period_iter].add_lesson(Lesson(LessonInfo(s, g, t, r, period_iter + 4001)))
                if correct_adding:
                    is_good = True
                    break
                else:
                    self.time_table_by_period[period_iter].free_rooms.append(r)
                    # period_iter += 1
                    if period_iter > len(self.info.periods):
                        print('problem-01')
            if not is_good:
                self.bad_records.append(gro_sub_tea)
        return True

    def get_object_timetable(self, object_id):
        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []
        for i in range(len(self.time_table_by_period)):
            if object_id in self.time_table_by_period[i].all_IDs:
                if i % 5 == 0:
                    monday.append(self.time_table_by_period[i].get_lesson(object_id))
                elif i % 5 == 1:
                    tuesday.append(self.time_table_by_period[i].get_lesson(object_id))
                elif i % 5 == 2:
                    wednesday.append(self.time_table_by_period[i].get_lesson(object_id))
                elif i % 5 == 3:
                    thursday.append(self.time_table_by_period[i].get_lesson(object_id))
                elif i % 5 == 4:
                    friday.append(self.time_table_by_period[i].get_lesson(object_id))
            else:
                if i % 5 == 0:
                    monday.append([-1, -1, -1, -1])
                elif i % 5 == 1:
                    tuesday.append([-1, -1, -1, -1])
                elif i % 5 == 2:
                    wednesday.append([-1, -1, -1, -1])
                elif i % 5 == 3:
                    thursday.append([-1, -1, -1, -1])
                elif i % 5 == 4:
                    friday.append([-1, -1, -1, -1])
        return [monday, tuesday, wednesday, thursday, friday]

    def get_string_timetable_by_id(self, object_id):
        [monday, tuesday, wednesday, thursday, friday] = self.get_object_timetable(object_id)
        string_to_return = 'Monday:\n'
        for lessons in monday:
            string_to_return += self.info.names[lessons[0]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[1]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[2]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[3]]
            string_to_return += '\n'
        string_to_return += 'Tuesday:\n'
        for lessons in tuesday:
            string_to_return += self.info.names[lessons[0]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[1]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[2]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[3]]
            string_to_return += '\n'
        string_to_return += 'Wednesday:\n'
        for lessons in wednesday:
            string_to_return += self.info.names[lessons[0]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[1]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[2]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[3]]
            string_to_return += '\n'
        string_to_return += 'Thursday:\n'
        for lessons in thursday:
            string_to_return += self.info.names[lessons[0]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[1]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[2]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[3]]
            string_to_return += '\n'
        string_to_return += 'Friday:\n'
        for lessons in friday:
            string_to_return += self.info.names[lessons[0]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[1]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[2]]
            string_to_return += ' '
            string_to_return += self.info.names[lessons[3]]
            string_to_return += '\n'
        return string_to_return

    def rate_it(self) -> int:
        def free_period_counter(day) -> int:
            number_of_free_periods = 0
            number_of_potential_free_periods = 0
            is_begin = True
            for lesson in day:
                if lesson[0] == -1:
                    if is_begin:
                        pass
                    else:
                        number_of_potential_free_periods += 1
                else:
                    if is_begin:
                        is_begin = False
                    else:
                        if number_of_potential_free_periods > 0:
                            number_of_free_periods += number_of_potential_free_periods
                            number_of_potential_free_periods = 0
                        else:
                            pass
            return number_of_free_periods

        rate = 1000000
        first_iteration = True
        for group_id in self.info.groups:
            [monday, tuesday, wednesday, thursday, friday] = self.get_object_timetable(group_id)
            week = [monday, tuesday, wednesday, thursday, friday]
            if first_iteration:
                rate -= len(monday) * 10000
                first_iteration = False
            for school_day in week:
                rate -= free_period_counter(school_day) * 10000
        for teacher_id in self.info.teachers:
            [monday, tuesday, wednesday, thursday, friday] = self.get_object_timetable(teacher_id)
            week = [monday, tuesday, wednesday, thursday, friday]
            if first_iteration:
                rate -= len(monday) * 10000
                first_iteration = False
            for school_day in week:
                rate -= free_period_counter(school_day) * 1000

        return rate


if __name__ == '__main__':
    import json

    f = open('Data/info.json', 'r')
    info = TimeTableInfo(json.loads(f.read()))
    best_rate = 0
    best = None
    for _ in range(10):
        time_table = TimeTable(info)
        time_table.make_correct_timetable()
        rate = time_table.rate_it()
        if rate > best_rate:
            best_rate = rate
            best = time_table
    print(best.rate_it())

