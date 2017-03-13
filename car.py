class Car(object):
    all_cars = []

    def __init__(self, engine_type, gas_tank_volume, price=10000.0):
        self.name = "Car " + str(len(self.all_cars) + 1)
        self.engine_type = engine_type
        self.gas_tank_volume = gas_tank_volume
        self.price = price

        self.all_cars.append(self)

tank_volume = float
eng_type = str

for i in range(1, 101):
    if not i % 5:
        tank_volume = 75.0
    else:
        tank_volume = 60.0
    if not i % 3:
        eng_type = "diesel"
    else:
        eng_type = "gasoline"
    Car(engine_type=eng_type, gas_tank_volume=tank_volume)

for car in Car.all_cars:
    print("Name: {}; engine type: {}; tank volume: {}; price: {}.".format(car.name, car.engine_type, car.gas_tank_volume, car.price))
