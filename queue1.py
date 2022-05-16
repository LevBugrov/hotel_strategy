import random as rm


class Queue:
    def __init__(self, days=50, lam=20, u=0.5, rooms=100, price=1):
        self.lam = lam  # скорость прибытия клиентов на стойку регистрации
        self.u = u  # 1\u - ожидаемое время пребывания клиента (дни) в отеле
        self.days = days  # ограничение очереди количеством дней
        self.rooms = rooms  # количество комнат

        time_of_arrive = 0 + rm.expovariate(lam)
        self.client_schedule = []

        self.last_leave = -1

        while time_of_arrive < days:
            if self.free_rooms(time_of_arrive, optimaze=True) > 0:
                time_of_leave = time_of_arrive + int(rm.expovariate(u))
                self.client_schedule.append((time_of_arrive, time_of_leave))
            else:  # отказ в обслуживании
                pass
            time_of_arrive += rm.expovariate(lam)

        self.profit = []
        for i in self.client_schedule:
            if int(i[0]) >= len(self.profit):
                self.profit.append((i[1]-i[0])*price)
            else:
                self.profit[int(i[0])] += (i[1]-i[0])*price

        

    def free_rooms(self, time, optimaze=False):
        counter = 0
        if not optimaze:
            for i in self.client_schedule:
                if i[0]<= time and i[1] > time:
                    counter += 1
            return self.rooms - counter
        else:
            start = self.last_leave
            for i in range(start+1, len(self.client_schedule)):
                if self.client_schedule[i][1] <= time:
                    self.last_leave = i
                else:
                    break
                
            start = self.last_leave
            for i in range(start+1, len(self.client_schedule)):
                if self.client_schedule[i][1] > time and self.client_schedule[i][0] < time:
                    counter += 1
            return self.rooms - counter



class CompleteSharing:
    def __init__(self, days=50, lam_offline=20, lam_online=20, u=0.5, rooms=100, price_of=1, price_on=1, tet=0.2):
        self.lam_of = lam_offline  # скорость прибытия клиентов на стойку регистрации
        self.lam_on = lam_online  # скорость прибытия клиентов на онлайн платформу
        self.u = u  # 1\u - ожидаемое время пребывания клиента (дни) в отеле
        self.days = days  # ограничение очереди количеством дней
        self.rooms = rooms  # количество комнат

        self.client_schedule = []
      
        self.profit = []
        time_of_arrive_of = rm.expovariate(self.lam_of)
        time_of_arrive_on = rm.expovariate(self.lam_on)
        now = ""  # клиент из какой очереди сейчас будет обслуживаться

        if time_of_arrive_of < time_of_arrive_on:
            time_of_arrive = time_of_arrive_of
            now = "offline"
        else:
            time_of_arrive = time_of_arrive_on
            now = "online"

        self.last_leave = -1


        while time_of_arrive < days:
            if self._get_free_rooms(time_of_arrive, optimaze=True) > 0:
                time_of_leave = time_of_arrive + int(rm.expovariate(u))
                self.client_schedule.append((time_of_arrive, time_of_leave, now))
            else:  # отказ в обслуживании
                pass

            if now == "offline":
                time_of_arrive_of += rm.expovariate(self.lam_of)
            else:
                time_of_arrive_on += rm.expovariate(self.lam_on)

            if time_of_arrive_of < time_of_arrive_on:
                time_of_arrive = time_of_arrive_of
                now = "offline"
            else:
                time_of_arrive = time_of_arrive_on
                now = "online"

        for i in self.client_schedule:
            if int(i[0]) >= len(self.profit):
                self.profit.append((i[1]-i[0])*(price_of if i[-1] == "offline" else (1-tet)*price_on))
            else:
                self.profit[int(i[0])] += (i[1]-i[0])*(price_of if i[-1] == "offline" else (1-tet)*price_on)


    def _get_free_rooms(self, time, optimaze=False):
        counter = 0
        if not optimaze:
            for i in self.client_schedule:
                if i[0]<= time and i[1] > time:
                    counter += 1
            return self.rooms - counter
        else:
            start = self.last_leave
            for i in range(start+1, len(self.client_schedule)):
                if self.client_schedule[i][1] <= time:
                    self.last_leave = i
                else:
                    break
                
            start = self.last_leave
            for i in range(start+1, len(self.client_schedule)):
                if self.client_schedule[i][1] > time and self.client_schedule[i][0] < time:
                    counter += 1
            return self.rooms - counter


if __name__ == '__main__':
    queue = Queue(days=10)
    shedule = queue.client_schedule

    for i in shedule:
        print(round(i[0], 2), round(i[1], 2))
    print(len(shedule))
    print(queue.last_leave)
    print(queue.free_rooms(10))