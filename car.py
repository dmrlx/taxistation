# -*- coding: utf-8 -*-

# Task: Taxi station
# Author: Alexander Demura
# Tested with Python 2.7.13, 3.5.3 and 3.6.0

import sys
import logging
from random import randint

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.addHandler(logging.FileHandler("car_report.log"))


# Class for main constants
class Constants:
    # Diesel engines default params
    DIESEL_MILEAGE_TO_OVERHAUL = 150000
    DIESEL_OVERHAUL_PRICE = 700.0
    DIESEL_DEPRECIATION = 10.5
    DIESEL_FUEL_CONSUMPTION = 0.06
    DIESEL_ENGINE_LIFETIME = 650000.0
    # Gasoline engines default params
    GASOLINE_MILEAGE_TO_OVERHAUL = 100000
    GASOLINE_OVERHAUL_PRICE = 500.0
    GASOLINE_DEPRECIATION = 9.5
    GASOLINE_FUEL_CONSUMPTION = 0.08
    GASOLINE_ENGINE_LIFETIME = 750000.0

    START_PRICE = 10000.0

    ENGINE_REPLACING_COST = 3000.0


# Class for fuel prices
class FuelPrices:
    AI_92 = 2.2
    AI_95 = 2.5
    DIESEL = 2.4


# Main class for generate "cars"
class Car(object):
    # List for all initialized objects
    all_cars = []

    # Car initialization with all necessary params
    def __init__(self, engine_type, gas_tank_volume):
        self.name = "car_" + str(len(self.all_cars) + 1)
        self.engine_type = engine_type
        self.engine = Engine(engine_type, is_on_car=self)
        self.gas_tank_volume = gas_tank_volume

        if self.engine.fuel_type == "diesel":
            self.mileage_to_overhaul = Constants.DIESEL_MILEAGE_TO_OVERHAUL
            self.overhaul_price = Constants.DIESEL_OVERHAUL_PRICE
            self.depreciation = Constants.DIESEL_DEPRECIATION
        else:
            self.mileage_to_overhaul = Constants.GASOLINE_MILEAGE_TO_OVERHAUL
            self.overhaul_price = Constants.GASOLINE_OVERHAUL_PRICE
            self.depreciation = Constants.GASOLINE_DEPRECIATION

        self.price = Constants.START_PRICE

        self.__mileage = 0
        # Random route for every car
        self.route = randint(56000, 950000)

        # Some default params for init
        self.route_price = 0
        self.sum_fuel_price = 0
        self.number_of_fueling = 0
        self.refuelling_counter = 0

        # Start fuel level (full tank by default)
        self.current_fuel_level = self.gas_tank_volume

        # Add new car to list of all cars (Car.all_cars)
        self.all_cars.append(self)

    # Replacing of engine
    def remotor(self):
        old_engine_number = self.engine.engine_number
        # "Utilisation" of old engine
        Engine.reclaimed_engines.append(self.engine)
        del self.engine
        self.engine = Engine(self.engine_type, is_on_car=self)
        self.price -= self.engine.price
        new_engine_number = self.engine.engine_number
        logger.info("Engine {} replaced with {}".format(
            old_engine_number, new_engine_number))

    # The method for "traveling"
    def run(self):
        # Actions for every km in route
        for km in range(self.route):
            # Increase mileage for 1 km
            self.__mileage += 1
            self.engine.mileage += 1

            if self.engine.engine_condition <= 0:
                self.remotor()

            # Decrease fuel level for size of fuel consumption
            self.current_fuel_level -= self.engine.fuel_consumption

            # Check for sufficient fuel for the next step
            if self.current_fuel_level < self.engine.fuel_consumption:
                self.fuelling()

            # Change parameters (residual value and fuel consumption) after
            # every 1000 km
            if not self.__mileage % 1000:
                self.price -= self.depreciation
            # Add overhaul price to route price
            if not self.__mileage % self.mileage_to_overhaul:
                self.route_price += self.overhaul_price

    # Receiving of value mileage to utilisation, temporary hided inadequately
    # def mileage_to_utilisation(self):
    #     mileage = 0
    #     price = self.price
    #     while price > 0:
    #         mileage += 1000
    #         if not mileage % 1000:
    #             price -= self.depreciation
    #         if not mileage % self.mileage_to_overhaul:
    #             price -= self.overhaul_price
    #     return mileage

    # Action of fuelling
    def fuelling(self):
        self.route_price += self.gas_tank_volume * self.engine.current_fuel_price
        self.sum_fuel_price += self.gas_tank_volume * self.engine.current_fuel_price
        self.current_fuel_level = self.gas_tank_volume
        self.refuelling_counter += 1

    # Current route
    @property
    def current_route(self):
        return self.__mileage

    # Money spending for fuel
    @property
    def spending_on_fuel(self):
        return self.sum_fuel_price

    # Number of refuelling
    @property
    def number_of_refuelling(self):
        return self.refuelling_counter


class Engine(object):
    # List of all engines divided by type; 0 - diesel, 1 - gasoline
    all_engines = [[], []]
    # List of reclaimed engines
    reclaimed_engines = []

    def __init__(self, fuel_type, is_on_car=None):
        self.fuel_type = fuel_type
        self.is_on_car = is_on_car
        self.mileage = 0
        self.price = Constants.ENGINE_REPLACING_COST

        if fuel_type == "diesel":
            self.engine_number = "diesel_" + str(len(self.all_engines[0]) + 1)
            self.all_engines[0].append(self)
            self.engine_lifetime = Constants.DIESEL_ENGINE_LIFETIME
            self.fuel_consumption = Constants.DIESEL_FUEL_CONSUMPTION

        elif fuel_type == "gasoline":
            self.engine_number = "gasoline_" + str(len(self.all_engines[1]) + 1)
            self.all_engines[1].append(self)
            self.engine_lifetime = Constants.GASOLINE_ENGINE_LIFETIME
            self.fuel_consumption = Constants.GASOLINE_FUEL_CONSUMPTION

        # Change of fuel consumption every 1000 km
        self.fuel_consumption_delta = self.fuel_consumption * 0.01
        if not self.mileage % 1000:
            self.fuel_consumption += self.fuel_consumption_delta

    # Choose type of fuel based on type of engine and current mileage
    @property
    def current_fuel_price(self):
        if self.fuel_type == "gasoline":
            if self.mileage < 50000:
                self.fuel_price = FuelPrices.AI_92
            else:
                self.fuel_price = FuelPrices.AI_95
        else:
            self.fuel_price = FuelPrices.DIESEL
        return self.fuel_price

    # Calculation of engine conditions =>%
    @property
    def engine_condition(self):
        return 100 - (self.mileage/self.engine_lifetime) * 100


# Class with final info
class Info:

    # Method for sorting list of cars by conditions
    def sorter(self, list_of_cars):
        list_of_diesel_cars = []
        list_of_gasoline_cars = []
        list_of_dies_names = []
        list_of_gas_names = []

        for item in list_of_cars:
            if item.engine_type == "diesel":
                list_of_diesel_cars.append(item)
            elif item.engine_type == "gasoline":
                list_of_gasoline_cars.append(item)

        list_of_diesel_cars = sorted(
            list_of_diesel_cars, key=lambda car: car.price)
        list_of_gasoline_cars = sorted(
            list_of_gasoline_cars, key=lambda car: car.price)

        for elem in list_of_diesel_cars:
            list_of_dies_names.append("{}: {}".format(elem.name, elem.price))
        for elem in list_of_gasoline_cars:
            list_of_gas_names.append("{}: {}".format(elem.name, elem.price))

        return list_of_dies_names, list_of_gas_names

    # Method for calc price of all cars
    def full_price(self, list_of_cars):
        price = 0.0
        for car in list_of_cars:
            price += car.price
        return price

    # Method for calc credits
    def credits_sum(self):
        sum_of_credits = 0.0
        for car in Car.all_cars:
            if car.price < 0:
                sum_of_credits += car.price
        return sum_of_credits

# Cars generator
for i in range(1, 2):
    if not i % 3 and not i % 5:
        Car("diesel", 75.0)
    elif not i % 3:
        Car("diesel", 60.0)
    elif not i % 5:
        Car("gasoline", 75.0)
    else:
        Car("gasoline", 60)

# info generator and starter of route
for car in Car.all_cars:
    logger.info("Start status: Car: {}, engine: {}, tank volume: {}, route: {} км, price: {}, spending on fuel: {}, "
                "number of fuelling: {}, engine condition: {}%."
                .format(car.name, car.engine.engine_number, car.gas_tank_volume, car.route, car.price,
                        car.sum_fuel_price, car.number_of_refuelling, round(car.engine.engine_condition, 2)))

    car.run()

    logger.info(
        "Start status: Car: {}, engine: {}, tank volume: {}, route: {} км, price: {}, spending on fuel: {}, "
        "number of fuelling: {}, engine condition: {}%."
        .format(car.name, car.engine.engine_number, car.gas_tank_volume, car.route, car.price, car.sum_fuel_price,
                car.number_of_refuelling, round(car.engine.engine_condition, 2)))

# Output final info
informer = Info()

logger.info("Sum of credits: {}".format(informer.credits_sum()))
logger.info("Reclaimed engines: {}".format(Engine.reclaimed_engines))

for engine in Engine.reclaimed_engines:
    logger.info("Reclaimed engine number: {}".format(engine.engine_number))

lists = informer.sorter(Car.all_cars)

logger.info("List of diesel cars: {}".format(lists[0]))
logger.info("List of gasiline cars: {}".format(lists[1]))
logger.info("Price of all cars: {}".format(informer.full_price(Car.all_cars)))
