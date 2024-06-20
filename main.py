from fastapi import FastAPI, HTTPException
from schemas import Airline, Flight
import json

app = FastAPI()

with open("airlines.json", "r") as file:
    airline_data = json.load(file)

airline_list = []

for airline_name, flights in airline_data.items():
    flights = [Flight(**flight) for flight in flights]
    airline = Airline(name=airline_name, flights=flights)
    airline_list.append(airline)

@app.get("/")
async def get_airlines():
    
    return [airline.name for airline in airline_list]

@app.get("/{airline_name}")
async def get_flight_nums(airline_name: str):
    
    for airline in airline_list:
        if airline.name == airline_name:
            return [flight.flight_num for flight in airline.flights]
    
    raise HTTPException(status_code=404, detail='Airline not found')

@app.get("/{airline_name}/{flight_num}")
async def get_flight_info(airline_name: str, flight_num: str):
    
    for airline in airline_list:
        if airline.name == airline_name:
            for flight in airline.flights:
                if flight.flight_num == flight_num:
                    return flight
    
    raise HTTPException(status_code=404, detail='Flight not found')

@app.post("/{airline}")
async def create_flight(airline: str, new_flight: Flight):
    
    for airline_obj in airline_list:
        if airline_obj.name == airline:
            airline_obj.flights.append(new_flight)
            return new_flight
    
    raise HTTPException(status_code=404, detail="Airline not found")

@app.put("/{airline}/{flight_num}")
async def update_flight(airline: str, flight_num: str, updated_flight: Flight):
    
    for airline_obj in airline_list:
        if airline_obj.name == airline:
            for i, flight in enumerate(airline_obj.flights):
                if flight.flight_num == flight_num:
                    airline_obj.flights[i] = updated_flight
                    return updated_flight
   
    raise HTTPException(status_code=404, detail='Flight not found')

@app.delete("/{airline}/{flight_num}")
async def delete_flight(airline: str, flight_num: str):
    
    for airline_obj in airline_list:
        if airline_obj.name == airline:
            for i, flight in enumerate(airline_obj.flights):
                if flight.flight_num == flight_num:
                    deleted_flight = airline_obj.flights.pop(i)
                    return deleted_flight
    
    raise HTTPException(status_code=404, detail='Flight not found')




    
    
    
    


