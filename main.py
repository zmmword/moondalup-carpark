import carpark

main = carpark.Moondalup() # [7] Read and write configuration from a file

main.carparks[0].enter_carpark(carpark.Car()) # [9] Create a main.py demonstrating the core interaction between instances of your classes
main.carparks[0].enter_carpark(carpark.Ute())
main.save_moondalup()