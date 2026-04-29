from fastapi import FastAPI
import os

app = FastAPI(title="Devices Service", version="1.0")

@app.get("/api/devices")
async def get_devices():
    return {"devices": ["iPhone", "Pixel", "Galaxy"], "service": "devices-svc-s04"}

@app.post("/api/devices")
async def create_device():
    return {"message": "Device created", "port": 8106}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8106)