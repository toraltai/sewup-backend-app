from uuid import uuid4
from fastapi import APIRouter, UploadFile, Form, HTTPException
from typing import List
import aioboto3
from decouple import config
from models import Category, Image
from tortoise.exceptions import DoesNotExist


r2Router = APIRouter()


@r2Router.post('/upload', summary="Добавление картинок к категориям")
async def upload(
    file: List[UploadFile],
    category_id: int = Form(...)):
    try:
        category = await Category.get(id=category_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")

    session = aioboto3.Session()
    uploaded_images = []

    if file:
        for item in file:
            ext = item.filename.split('.')[-1].lower()
            filename = f"{category.title}/{uuid4().hex[:8]}.{ext}"
            url = f"https://{config('R2_PUBLIC_URL')}/{filename}"

            async with session.client(
                "s3",
                region_name="weur",
                endpoint_url=config("R2_ENDPOINT"),
                aws_access_key_id=config("ACCESS_KEY"),
                aws_secret_access_key=config("SECRET_KEY")
            ) as s3:
                await s3.upload_fileobj(item.file, "media-storage", filename)

            # Сохраняем в БД
            image = await Image.create(image_url=url, category=category)
            uploaded_images.append(image)

    return {"uploaded": [img.image_url for img in uploaded_images]}