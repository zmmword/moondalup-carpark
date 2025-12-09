import random, json
from string import ascii_uppercase, digits

class Car:
 def __init__(self, rego=None):
  """
  Car creator for carpark
  """
  self.rego = rego or self.generate_license()

 def generate_license(self):
  """
  WA-format license plate generator
  for rego generation
  """
  lic = "1%s-%s" % (
  "".join(random.choice(ascii_uppercase) for i in range(3)),
  "".join(random.choice(digits) for i in range(3))
  )

  return lic

 def __repr__(self):
  return "Car [%s]" % self.rego


class Ute(Car): # [3] At least one class must aggregate another class
 # Ute variant of the
 # Car class          # [12] Apply at least three different documentation conventions (readme, docstring, comments)

 def __init__(self, rego=None):
  super().__init__(rego)


 def __repr__(self):
  return "Ute [%s]" % self.rego


class CarPark:
 def __init__(self, name, temp, bays=None): # [2] at least one class must include three or more parameters
  """
  self: object reference
  name: Name of the car park that contains the bays
  bays: dictionary of bays free, used for loading from configuration file
  """
  self.name = name
  self.temp = temp
  self.bays = bays or self.generate_bays()

 def generate_bays(self):
  """
  Construct dictionary of Nones
  from 0-99 as placeholders
  """
  return dict.fromkeys([*range(100)]) # [4] at least one class must include a list of primitive data types

 def get_free_bay(self):
  """
  Fnction to iterate through
  all bays and resolve a free bay

  If no bays are free, None is returned
  to caller to switch to next car park
  """
  for k in self.bays:
   test = self.bays[k]
   if not test:
    return k

 def enter_carpark(self, car):
  """
  Add a car to the carpark

  Chains to self.get_free_bay,
  returns data and also notifies
  enterer of carpark upon success
  or failure
  """

  test_free = self.get_free_bay()
  if test_free is not None:
   self.bays[test_free] = car
   print("Successfully added `%s' to carpark `%s'" % (car, self.name))
   self.get_carpark_information()

  else:
   print("Could not add car `%s' to carpark `%s'" % (car, self.name))

  return test_free

 def exit_carpark(self, rego):
  """
  Removes a car from the carpark
  via car registration by iterating
  through all bays
  """

  for k in self.bays:
   test = self.bays[k]
   if test and test.rego == rego: # [5] You should demonstrate an example of polymorphism
    self.bays[k] = None
    break

  self.get_carpark_information()

 def get_carpark_information(self):
  """
  Retrieve carpark information
  about free bays, taken bays,
  and temperature (F/C)
  """

  free_spots = 0
  for k in self.bays:
   test = self.bays[k]
   if test is None:
    free_spots += 1

  taken_spots = len(self.bays) - free_spots
  temp_farenheit = (self.temp * (9 / 5)) + 32
  print("Carpark `%s', %s taken bays (%s free), at temperature %s(F) or %s(C)" % (self.name, taken_spots, free_spots, temp_farenheit, self.temp))


class Moondalup: # [1] Create at least three classes
 def __init__(self, carparks=None):
  """
  carparks: None: Load Moondalup Car Parks from file moondalup.json
            list: (assumes list but no checking unless I must add it)
                  Load Moondalup Car Parks as list from instantiation

Moondalup JSON structure in EBNF format:
Initial Item: [Carpark*]
Carpark:      {
               "name": string
               "temp": float // temp in celcius
               "bays": {(string: vehicle)*}
              }

vehicle: {"kind": ("Car" | "Ute"), "rego": string}
example.json:
[
 {
  "name": "carpark 1",
  "temp": 12.5,
  "bays": {},
  "comment": "empty carpark"
 },
 {
  "name": "carpark 2",
  "temp": 5.0,
  "bays": {
   "23": {
    "kind": "Car",
    "rego": "1ABC123"
   }
  },
  "comment": "carpark with one car at bay 23"
 },
 {
  "name": "carpark 3",
  "temp": 7.3,
  "bays": {
   "12": {
    "kind": "Ute",
    "rego": "1ABC123"
   },
   "34": {
    "kind": "Car",
    "rego": "1ABC456"
   }
  },
  "comment": "carpark with one ute at bay 12, one car at bay 34"
 }
]
  """
  self.carparks = carparks or self.deserialize_moondalup()

 def deserialize_moondalup(self): # [8] Allow carpark to be constructed either from a direct call or via the configuration file (two options for object construction)
  """
  Opens `moondalup.json', the file
  containing JSON defining the
  Moondalup ionstance which is also
  assumed to follow the defined
  JSON structure in the __init__
  docustring
  """

  jsonin = open("moondalup.json")
  jsonf = json.load(jsonin)
  jsonin.close()

  carparks = []
  for item in jsonf: # yea i know this couldve just been native
                     # but i think a custom parser for this specifically
                     # probably wouldve been unnecessary overkill
   carpark = CarPark(item["name"], item["temp"])
   for bay in item["bays"]:
    car = item["bays"][bay]
    bay = int(bay)
    if car["kind"] == "Car":
     carpark.bays[bay] = Car(car["rego"])

    elif car["kind"] == "Ute":
     carpark.bays[bay] = Ute(car["rego"])

   carparks.append(carpark)

  return carparks

 def save_moondalup(self):
  """
  Serializes and writes Moondalup
  instance to `moondalup.json'
  """ # [12] Apply at least three different documentation conventions (readme, docstring, comments)

  jsonified = []
  for item in self.carparks:
   carpark = {}
   carpark["name"] = item.name
   carpark["temp"] = item.temp
   carpark["bays"] = {}
   for bay in item.bays:
    bay_test = item.bays[bay]
    if bay_test:
     fmt_key = str(bay)
     carpark["bays"][fmt_key] = {}
     if type(bay_test) == Car:
      carpark["bays"][fmt_key]["kind"] = "Car"

     elif type(bay_test) == Ute:
      carpark["bays"][fmt_key]["kind"] = "Ute"

     carpark["bays"][fmt_key]["rego"] = bay_test.rego


   jsonified.append(carpark)

  jsonout = open("moondalup.json", "w")
  json.dump(jsonified, jsonout, indent=1)
  jsonout.close()