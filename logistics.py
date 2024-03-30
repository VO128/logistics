from termcolor import cprint


class Road:

    def __init__(self, start, end, distance):
        self.start = start
        self.end = end


class Warehouse:

    def __init__(self, name, content=0):
        self.name = name
        self.content = content
        self.set_road_out = None
        self.queue_in = []
        self.queue_out = []
        self.truck = Truck

    def __str__(self):
        return 'Склад {} груза {}'.format(self.name, self.content)

    def set_road_out(self, road):
        self.set_road_out = road

    def truck_arrived(self, truck):
        self.queue_in.append(truck)
        print('{} прибыл грузовик {} '.format(self.name, self.truck))

    def get_next_truck(self):
        if self.queue_in:
            truck = self.queue_in.pop()
            return truck

    def truck_ready(self, truck):
        self.queue_out.append(truck)
        print(' {} грузовик готов {} '.format(self.name, self.truck))

    def act(self):
        while self.queue_out:
            truck = self.queue_iout.pop()
            truck.go_to(road=self.road_out())


class Vehicle:
    fuel_rate = 0
    total_fuel = 0

    def __init__(self, model):
        self.model = model
        self.fuel = 0

    def __str__(self):
        return '{} топливо '.format(self.model, self.fuel)

    def tank_up(self):
        self.fuel += 1000
        Vehicle.total_fuel += 1000
        print(' {} заправился {}'.format(self.model, self.fuel))

    def act(self):
        if self.fuel <= 10:
            self.tank_up()
            return False
        return True


class Truck(Vehicle):
    fuel_rate = 50
    dead_time = 0

    def __init__(self, model, body_space=1000):
        super().__init__(model=model)
        self.body_space = body_space
        self.cargo = 0
        self.velocity = 100
        self.place = None
        self.distance_to_target = 0

    def __str__(self):
        res = super().__str__()
        return res + 'груз {}'.format(self.cargo)

    def ride(self):
        if self.distance_to_target > self.velocity:
            self.distance_to_target -= self.velocity
            print('{} едет по дороге, осталось {}'.format(self.model, self.distance_to_target))
        else:
            self.place.truck_arrived(self)
            print('доехал'.format(self.model))

    def go_to(self, road):
        self.place = road
        self.distance_to_target = road.distance
        print('{} выехал в путь'.format(self.model))

    def act(self):
        super().act()
        if isinstance(self.place, Road):
            self.ride()
        else:
            Truck.dead_time += 1


class AutoLoader(Vehicle):

    def __init__(self, model, bucket_capacity=100, warhouse=None, role='loader', body_space=1000):
        super().__init__(model=model)
        self.bucket_capacity = bucket_capacity
        self.warehouse = warhouse
        self.role = role
        self.truck = None
        self.body_space = body_space

    def __str__(self):
        res = super().__str__()
        return res + 'груза {}'.format(self.truck)

    def act(self):
        super().act()
        if self.truck is None:
            self.truck = self.warehouse.get_next_truck()
            print('{} взял в работу {}'.format(self.model, self.truck))
        elif self.role == 'loader':
            self.load()
        else:
            self.unload()

        if self.truck is None:
            Truck.dead_time += 1

    def load(self):
        self.warehouse.content == 0
        print('{} На складе ничего нет'.format(self.model))
        if self.truck:
            self.warehouse.truck_ready(self.truck)
            self.truck = None
            return
        self.fuel -= self.fuel_rate
        truck_cargo_rest = self.body_space - self.truck_cargo
        if truck_cargo_rest >= self.bucket_capacity:
            self.warehouse.content -= self.bucket_capacity
        cargo = self.bucket_capacity

        else:
            cargo = truck_cargo_rest
        if self.warehouse.content:
    self.warehouse.content -= truck_cargo_rest
    self.truck.cargo += cargo
print('{} грузил'.format(self.model, self.truck))
if self.truck.cargo == self.truck.body_space:
    self.warehouse.truck_ready(self.truck)
    self.truck = None


def unload(self):
    if self.truck.cargo >= self.bucket_capacity:
        self.warehouse.content -= self.bucket_capacity
        self.truck.cargo += self.bucket_capacity
    else:
        self.warehouse.content -= self.truck.cargo
        self.truck.cargo += self.truck.cargo
        print('{} разгружал {}'.format(self.model, self.truck))
    if self.truck.cargo == 0:
        self.warehouse.truck_ready(self.truck)
        self.truck = None


TOTAL_CARGO = 100000

moscow = Warehouse(name='Москва', content=TOTAL_CARGO)
piter = Warehouse(name='Питер', content=0)

moscow_piter = Road(start=moscow, end=piter, distance=715)
piter_moscow = Road(start=piter, end=moscow, distance=780)

# moscow.set_road_out(moscow_piter)
# piter.set_road_out(piter_moscow)

loader_1 = AutoLoader(model='Bodcat', bucket_capacity=1000, warhouse=moscow, role='loader')
loader_2 = AutoLoader(model='Lonking', bucket_capacity=500, warhouse=piter, role='unloader')

trucks = []
for number in range(10):
    truck = Truck(model='Камаз #{}'.format(number), body_space=5000)
    moscow.truck_arrived(truck)

hour = 0
while piter.content < TOTAL_CARGO:
    hour += 1
    cprint('------Час {} ------'.format(hour, color='red'))
    for truck in trucks:
        truck.act()
    loader_1.act()
    loader_2.act()
    moscow.act()
    piter.act()
    for truck in trucks:
        cprint(truck, color='cyan')
    cprint(loader_1, color='cyan')
    cprint(loader_2, color='cyan')
    cprint(moscow, color='cyan')
    cprint(piter, color='cyan')

cprint('всего затрачено топлива {}'.format(Vehicle.total_fuel), color='yellow')
