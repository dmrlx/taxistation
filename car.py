# -*- coding: utf-8 -*-

# Task: Taxi station
# Author: Alexander Demura
# Tested with Python 2.7.13, 3.5.3 and 3.6.0

from random import randint


# Class for fuel prices
class Fuel:
    gasoline_price = 1.8
    diesel_price = 2.4


# Main class for generate "cars"
class Car(object):
    # List for all initialized objects
    all_cars = []

    # Car initialization with all necessary params
    def __init__(self):
        self.name = "Car #" + str(len(self.all_cars) + 1)

        # Engine type selection by condition
        if not (len(self.all_cars) + 1) % 3:
            self.engine_type = "diesel"
            self.fuel_consumption = 0.06
            self.fuel_price = Fuel.diesel_price
            self.depreciation = 10.5
            self.mileage_to_overhaul = 150000
            self.overhaul_price = 700
        else:
            self.engine_type = "gasoline"
            self.fuel_consumption = 0.08
            self.fuel_price = Fuel.gasoline_price
            self.depreciation = 9.5
            self.mileage_to_overhaul = 100000
            self.overhaul_price = 500.0

        # Gas tank volume selection by condition
        if not (len(self.all_cars) + 1) % 5:
            self.gas_tank_volume = 75.0
        else:
            self.gas_tank_volume = 60.0

        self.price = 10000.0
        # Divisor - average price of 1 km of run.
        #self.mileage_to_util = self.price / (self.depreciation / 1000.0 + self.overhaul_price / self.mileage_to_overhaul)
        self.mileage_to_util = self.mileage_to_utilisation()
        self.__mileage = 0
        # Random route for every car
        self.route = randint(56000, 286000)
        self.route_price = 0
        self.number_of_fueling = 0
        # Initial value of fuel level (full tank for example)
        self.current_fuel_volume = self.gas_tank_volume

        self.all_cars.append(self)

    # The method for "traveling"
    def run(self):
        # Actions for every km in route
        for km in range(self.route):
            # Increase mileage for 1 km
            self.__mileage += 1
            # Decrease fuel level for size of fuel consumption
            self.current_fuel_volume -= self.fuel_consumption
            # Check for sufficient fuel for the next step
            if self.current_fuel_volume < self.fuel_consumption:
                self.route_price += self.gas_tank_volume * self.fuel_price
                self.current_fuel_volume = self.gas_tank_volume
                self.number_of_fueling += 1
            # Change parameters (residual value and fuel consumption) after
            # every 1000 km
            if not self.__mileage % 1000:
                self.price = round(self.price - self.depreciation, 2)
                self.fuel_consumption *= 1.01
            # Add overhaul price to route price
            if not self.__mileage % self.mileage_to_overhaul:
                self.route_price += self.overhaul_price

    # Methods for car state

    def mileage_to_utilisation(self):
        mileage = 0
        price = self.price
        while price > 0:
            mileage += 1000
            if not mileage % 1000:
                price -= self.depreciation
            if not mileage % self.mileage_to_overhaul:
                price -= self.overhaul_price
        return mileage


    def mileage(self):
        return self.__mileage

    def residual_value(self):
        return self.price

    def fuelings(self):
        return self.number_of_fueling

    def fuel_price_for_route(self):
        return self.number_of_fueling * (self.fuel_price * self.gas_tank_volume)

    def route_to_utilization(self):
        return self.mileage_to_util - self.__mileage


# Class with final info
class Info:

    # Method for sorting list of cars by conditions
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
        list_of_diesel_cars = sorted(
            list_of_diesel_cars, key=lambda car: car.price)
        list_of_gasoline_cars = sorted(
            list_of_gasoline_cars, key=lambda car: car.route_to_utilization())

        for car in list_of_diesel_cars:
            list_of_dies_names.append("{}: {}".format(
                car.name, car.route_to_utilization()))
        for car in list_of_gasoline_cars:
            list_of_gas_names.append("{}: {}".format(car.name, car.price))

        return list_of_dies_names, list_of_gas_names

    def full_price(self, list_of_cars):
        price = 0.0
        for car in list_of_cars:
            price += car.price
        return price


# cars generator
for i in range(100):
    Car()
# Info about every car and runing to route
for car in Car.all_cars:
    print("Name: {}; engine type: {}; tank volume: {}; price: {}; fuel consumption: {}; route: {}; mileage to utilization: {}.".
          format(car.name, car.engine_type, car.gas_tank_volume, car.price, car.fuel_consumption, car.route, car.mileage_to_util))

    car.run()

# Output final info
informer = Info()
print(informer.sorter(Car.all_cars))
print(informer.full_price(Car.all_cars))
