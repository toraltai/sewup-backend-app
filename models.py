from uuid import uuid4
from fastapi import APIRouter
from typing import List
from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

##### Models #####

class Image(Model):
    id = fields.IntField(pk=True)
    image_url = fields.CharField(max_length=500)
    category = fields.ForeignKeyField(
        "models.Category", related_name="images", on_delete=fields.CASCADE)

    class Meta:
        table = "image"
        
GetImage = pydantic_model_creator(Image)


class Category(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    images: fields.ReverseRelation["Image"]
    title_image = fields.CharField(max_length=500, null=True)

    class Meta:
        table = "category"

Tortoise.init_models(["models"], "models")
GetCategory = pydantic_model_creator(Category)
CreateCategory = pydantic_model_creator(Category, name='CategoryIn',  exclude_readonly=True)

##### End #####

categoryRouter = APIRouter()


@categoryRouter.post('/add', response_model=GetCategory, summary="Создание категории")
async def create_category(category: CreateCategory): #type: ignore
    obj = await Category.create(**category.dict(exclude_unset=True))
    return await GetCategory.from_tortoise_orm(obj)


@categoryRouter.get("/list", response_model=List[GetCategory])
async def all():
    return await GetCategory.from_queryset(Category.all())


@categoryRouter.get('/images')
async def get_images(category_id: int):
    images = await Image.filter(category_id=category_id).select_related('category').all()
    return images