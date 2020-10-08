import datetime as dt
import random
import re

from django.core.exceptions import ObjectDoesNotExist

from .models import ShiftSchedule


# シフトを表すクラス
class ShiftService(object):
    def __init__(self, staff, month_days, individual):
        if individual is None:
            self.make_sample()
        else:
            self.individual = individual
        self.staff = staff
        self.month_days = month_days

        # コマの定義
        self.shift_box = [i for i in range(self.month_days)]
        # 各コマの想定人数
        self.need_staff = [4 for _ in range(self.month_days)]

    def save_schedule(self):
        for best_shifts, staff in zip(self.slice(), self.staff):
            for date, best_shift in enumerate(best_shifts, start=1):
                shift_type = int(best_shift) if int(best_shift) != 0 else 2
                date = dt.date(2020, 9, date)
                try:
                    shift = ShiftSchedule.objects.get(staff_id=staff, date=date)
                    shift.shift_type_id = shift_type
                except ObjectDoesNotExist:
                    shift = ShiftSchedule(staff_id=staff, date=date, shift_type_id=shift_type)
                shift.save()

    # ランダムなデータを生成
    def make_sample(self):
        sample_list = []
        for num in range(len(self.staff) * len(self.month_days)):
            sample_list.append(random.randint(0, 1))
        self.individual = tuple(sample_list)

    # タプルを1ユーザ単位に分割
    def slice(self):
        sliced = []
        start = 0
        for num in range(len(self.staff)):
            sliced.append(self.individual[start:(start + self.month_days)])
            start += self.month_days
        return tuple(sliced)

    # ユーザ別にアサインコマ名を出力する
    def print_inspect(self):
        user_no = 0
        for line in self.slice():
            print(f"ユーザ{user_no}")
            print(line)
            user_no = user_no + 1

            index = 0
            for e in line:
                if e == 1:
                    print(self.shift_box[index])
                index = index + 1

    # CSV形式でアサイン結果の出力をする
    def print_csv(self):
        for line in self.slice():
            print(','.join(map(str, line))+','+str(sum(line)))

    # コマ番号を指定してアサインされているスタッフ番号リストを取得する
    def get_user_nos_by_box_index(self, box_index):
        user_nos = []
        index = 0
        for line in self.slice():
            if line[box_index] == 1:
                user_nos.append(index)
            index += 1
        return user_nos

    # コマ名を指定してアサインされているユーザ番号リストを取得する
    def get_user_nos_by_box_name(self, box_name):
        box_index = self.shift_box.index(box_name)
        return self.get_user_nos_by_box_index(box_index)

    # 想定人数と実際の人数の差分を取得する
    def abs_people_between_need_and_actual(self):
        result = []
        for index, need in enumerate(self.need_staff):
            actual = len(self.get_user_nos_by_box_index(index))
            result.append(abs(need - actual))
        return result

    def few_work_pt(self, lowest_number_of_pt):
        """"""
        result = []
        for box_name in self.shift_box:
            user_nos = self.get_user_nos_by_box_name(box_name)
            count_pt = 0
            for user_no in user_nos:
                e = self.staff[user_no]
                if e.job_id.name == '理学療法士':
                    count_pt += 1
            if count_pt < lowest_number_of_pt:
                result.append(box_name)
        return result

    def get_max_shift_type(self, shift_schedule, shift_type=1):
        def judge(shift_type):
            if shift_type == 0:
                return shift_type > 0
            else:
                return shift_type < 0

        step = 1
        tmp_list = [0 for _ in range(len(shift_schedule))]
        for i, shift_type in enumerate(shift_schedule):
            if judge(shift_type):
                tmp_list[i] += step
                step += 1
            else:
                step = 1
        return max(tmp_list)

    def over_non_stop_work(self, max_non_stop_work_number):
        result = []
        for staff in self.slice():
            staff_map = map(str, staff)
            for shift in re.split('[0]+', ''.join(staff_map)):
                result.append(abs(max_non_stop_work_number - len(shift)))
        return result

    def less_day_off(self, less_day_off_number):
        count = 0
        for staff in self.slice():
            if self.get_max_shift_type(list(staff), 0) <= less_day_off_number:
                count += 1
        return count

    def abs_work_time_between_need_and_actual(self):
        result = []
        need = self.month_days * 4 // 6
        for staff in self.slice():
            actual = staff.count(1)
            result.append(abs(need - actual))
        return result
