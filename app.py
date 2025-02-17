from fastapi import FastAPI , Response,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field, ValidationError
from uuid import UUID, uuid4

app = FastAPI()

tanks = []

class Tank(BaseModel):
    id: UUID = Field (default_factory= uuid4) # type: ignore
    location: str
    lat: float
    long: float
    
class Tank_Update(BaseModel):
    location: str| None = None
    lat: float| None = None
    long: float| None = None
    
#Get Handler Request to show all tanks in the list
@app.get("/tank")
def get_exsisting_tanks():
    return tanks

#Get Handler Request To Get Specific Tank
@app.get("/tank/{id}")
def get_specific_tanks(id: str):
    for tank in tanks:
        if "id" in tank and str(tank["id"]) == id:
            return tank
    raise HTTPException(status_code=404, detail="Tank Not Found")

#Post Handler Request to add a new tank to the list and provide the tank with an ID 
@app.post("/tank")
def create_new_tanks(tank:Tank):
        # Create a new tank entry with a unique ID
        new_tank = {
            "id": str(uuid4()),
            "location": tank.location,
            "lat": tank.lat,
            "long": tank.long
        }
        # Append the new tank to the list
        tanks.append(new_tank)
        return new_tank

#Patch Handler Request to 
@app.patch("/tank/{id}")
async def update_tank(id: UUID, tank_update: Tank_Update):
    for i, tank in enumerate(tanks):
        if "id" in tank and UUID(str(tank["id"])) == id:
            tank_update_dict = tank.model_dump(exclude_unset=True)
            
            try:
                updated_tank = tank_update(update = tank_update_dict)
                tanks[i]= tank.model_validate(updated_tank)
                
                json_updated_tank = jsonable_encoder(updated_tank)
                return JSONResponse(json_updated_tank, status_code=200)
            except ValidationError:
                raise HTTPException(status_code=400, detail="Invalid Input")
            
    raise HTTPException(status_code=404, detail="Tank not found")

#Delete Handler Request
@app.delete("/tank/{id}")
def delete_prson(id:UUID):
    for tank in tanks:
         if "id" in tank and UUID(str(tank["id"])) == id:
            tanks.remove(tank)
            return Response(status_code =204)
    raise HTTPException(status_code=404, detail="Tank not found")



    