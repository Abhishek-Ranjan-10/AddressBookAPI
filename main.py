from fastapi import FastAPI, Depends, Response, status, HTTPException
import uvicorn
import schemas
import models
from database import engine, addressSession
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)


def getDb():
    db = addressSession()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "This is a address book API"}


@app.post("/addAdress", status_code=201)
async def adddAdress(request: schemas.Address, db: Session = Depends(getDb)):
    newAddress = models.AddressModel(title=request.title, pincode=request.pincode, state=request.state,
                                     fullAddress=request.fullAddress, coordinates=request.coordinates, publishedBy=request.publishedBy)

    db.add(newAddress)
    db.commit()
    db.refresh(newAddress)
    return {"date": newAddress, "message": "Successfully added Address"}


@app.get("/getAllAddress", status_code=202)
async def getAllAddress(db: Session = Depends(getDb)):
    addressAll = db.query(models.AddressModel).all()
    return {"data": addressAll, "message": "All addresses fetched"}


@app.get("/get/{id}", status_code=202)
async def getAddressById(id,  db: Session = Depends(getDb)):
    addressById = db.query(models.AddressModel).filter(
        models.AddressModel.id == id).first()
    if not (addressById):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return {"data": addressById, "message": f"Addresses fetched by {id}"}


@app.delete("/get/{id}", status_code=204)
async def getAddressById(id,  db: Session = Depends(getDb)):
    addressById = db.query(models.AddressModel).filter(
        models.AddressModel.id == id)
    if not (addressById):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    addressById.delete(synchronize_session=False)
    db.commit()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
