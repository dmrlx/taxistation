import random

class Car(object):
    all_cars = []

    def __init__(self):
        self.name = "Car " + str(len(self.all_cars) + 1)

        if not (len(self.all_cars)+1) % 3:
            self.engine_type = "diesel"
            self.fuel_consumption = 0.06
            self.fuel_price = 1.8
            self.depreciation = 10.5
            self.mileage_to_overhaul = 150000
            self.overhaul_price = 700
            self.mileage_to_utilization = 1000000

        else:
            self.engine_type = "gasoline"
            self.fuel_consumption = 0.08
            self.fuel_price = 2.4
            self.depreciation = 9.5
            self.mileage_to_overhaul = 100000
            self.overhaul_price = 500
            self.mileage_to_utilization = 1200000

        if not (len(self.all_cars)+1) % 5:
            self.gas_tank_volume = 75.0
        else:
            self.gas_tank_volume = 60.0
        self.price = 10000.0
        self.__mileage = 0
        self.route = random.randint(56000, 286000)
        self.route_price = 0
        self.number_of_fueling = 0

        self.current_fuel_volume = self.gas_tank_volume

        self.all_cars.append(self)

    def run(self):
        for i in range(self.route):
            self.__mileage += 1
            i += 1

            self.current_fuel_volume -= self.fuel_consumption

            if self.current_fuel_volume < self.fuel_consumption:
                self.route_price += self.gas_tank_volume * self.fuel_price
                self.current_fuel_volume = self.gas_tank_volume
                self.number_of_fueling += 1

            if not self.__mileage % 1000:
                self.price = round(self.price - self.depreciation, 2)
                self.fuel_consumption *= 1.01

            if not self.__mileage % self.mileage_to_overhaul:
                self.route_price += self.overhaul_price

        print(self.name, self.__mileage, self.current_fuel_volume, self.route_price, self.price, self.fuel_consumption)

    def mileage(self):
        return self.__mileage

    def fuelings(self):
        return self.number_of_fueling

    def residual_value(self):
        return self.price

    def fuel_price_for_route(self):
        return self.number_of_fueling * (self.fuel_price * self.gas_tank_volume)

    def route_to_utilization(self):
        return self.mileage_to_utilization - self.__mileage


class Info:
    def sorter(self, list_of_cars):
        list_of_diesel_cars = []
        list_of_gasoline_cars = []
        list_of_dies_names = []
        list_of_gas_names = []

        for car in list_of_cars:
            if car.engine_type == "diesel":
                list_of_diesel_cars.append(car)
            elif car.engine_type == "gasoline":
                list_of_gasoline_cars.append(car)
        list_of_diesel_cars = sorted(list_of_diesel_cars, key=lambda car: car.price)
        list_of_gasoline_cars = sorted(list_of_gasoline_cars, key=lambda car: car.route_to_utilization())
        for car in list_of_gasoline_cars:
            list_of_gas_names.append("{}: {}".format(car.name, car.price))
        for car in list_of_diesel_cars:
            list_of_dies_names.append("{}: {}".format(car.name, car.route_to_utilization()))

        return list_of_dies_names, list_of_gas_names

    def full_price(self, list_of_cars):
        price = 0.0
        for car in list_of_cars:
            price += car.price
        return price


tank_volume = float
eng_type = str

# cars generator
for i in range(20):
    Car()

for car in Car.all_cars:
    print("Name: {}; engine type: {}; tank volume: {}; price: {}; fuel consumption: {}; route: {}".
          format(car.name, car.engine_type, car.gas_tank_volume, car.price, car.fuel_consumption, car.route))
    car.run()

print(Info.sorter(None, Car.all_cars))
print(Info.full_price(None, Car.all_cars))
