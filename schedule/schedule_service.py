import random

from deap import base
from deap import creator
from deap import tools

from .models import Staff
from .shift_service import ShiftService


class ScheduleService(object):
    def __init__(self, month_days):
        self.staff = Staff.objects.all().select_related()
        self.month_days = month_days

        creator.create("FitnessPeopleCount", base.Fitness, weights=(-100.0, -10.0))
        creator.create("Individual", list, fitness=creator.FitnessPeopleCount)

        self.toolbox = base.Toolbox()

        self.toolbox.register("attr_bool", random.randint, 0, 1)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool,
                              self.month_days * len(self.staff))
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

    def eval_shift(self, individual):
        s = ShiftService(self.staff, self.month_days, individual)

        # 想定人数とアサイン人数の差
        people_count_sub_sum = sum(s.abs_people_between_need_and_actual()) / self.month_days * len(self.staff)

        # 理学療法士のアサイン数が最低人数以下
        few_work_pt = sum(s.few_work_pt(2)) / self.month_days
        return people_count_sub_sum, few_work_pt

    def setting_toolbox(self):
        # 適応度計算
        self.toolbox.register("evaluate", self.eval_shift)
        # 交叉関数を定義(二点交叉)
        self.toolbox.register("mate", tools.cxTwoPoint)

        # 変異関数を定義(ビット反転、変異隔離が5%ということ?)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

        # 選択関数を定義(トーナメント選択、tournsizeはトーナメントの数？)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def generate_schedule(self):
        self.setting_toolbox()

        # 初期集団を生成する
        pop = self.toolbox.population(n=300)
        CXPB, MUTPB, NGEN = 0.6, 0.3, 500  # 交差確率、突然変異確率、進化計算のループ回数

        print("進化開始")

        # 初期集団の個体を評価する
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):  # zipは複数変数の同時ループ
            # 適合性をセットする
            ind.fitness.values = fit

        print("  %i の個体を評価" % len(pop))

        # 進化計算開始
        for g in range(NGEN):
            print("-- %i 世代 --" % g)

            # 選択
            # 次世代の個体群を選択
            offspring = self.toolbox.select(pop, len(pop))
            # 個体群のクローンを生成
            offspring = list(map(self.toolbox.clone, offspring))

            # 選択した個体群に交差と突然変異を適応する

            # 交叉
            # 偶数番目と奇数番目の個体を取り出して交差
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)
                    # 交叉された個体の適合度を削除する
                    del child1.fitness.values
                    del child2.fitness.values

            # 変異
            for mutant in offspring:
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # 適合度が計算されていない個体を集めて適合度を計算
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            print("  %i の個体を評価" % len(invalid_ind))

            # 次世代群をoffspringにする
            pop[:] = offspring

            # すべての個体の適合度を配列にする
            index = 1
            for v in ind.fitness.values:
                fits = [v for ind in pop]

                length = len(pop)
                mean = sum(fits) / length
                sum2 = sum(x * x for x in fits)
                std = abs(sum2 / length - mean ** 2) ** 0.5

                print(f"* パラメータ {index}")
                print(f"  Min {min(fits)}")
                print(f"  Max {max(fits)}")
                print(f"  Avg {mean}")
                print(f"  Std {std}")
                index += 1

        print("-- 進化終了 --")

        best_ind = tools.selBest(pop, 1)[0]
        print(f"最も優れていた個体: {best_ind}, {best_ind.fitness.values}")
        s = ShiftService(self.staff, self.month_days, best_ind)
        s.print_csv()
        s.save_schedule()
