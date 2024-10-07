import os
import uuid

from app.utils import templates, files
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse

router = APIRouter(prefix='/upload')

@router.get("/dataset", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("upload_dataset.html", {"request": request})

@router.post("/dataset")
async def upload_file(name: str = Form(...), dataset: UploadFile = File(...)):
    if files.dataset_exist(name + '.zip'):
        raise HTTPException(status_code=400, detail="Dataset already exists")
    
    await force_upload_file(name, dataset)
   
@router.post('/dataset/force') 
async def force_upload_file(name: str = Form(...), dataset: UploadFile = File(...)):
    os.makedirs("temp/", exist_ok=True)
    
    file_id = str(uuid.uuid4())
    zip_path = os.path.join('temp', file_id)
    
    with open(zip_path, "wb") as buffer:
        buffer.write(await dataset.read())
        
    try:
        files.copy_dataset(zip_path, name)
    finally:
        os.remove(zip_path)
        
    return {name: dataset.filename}