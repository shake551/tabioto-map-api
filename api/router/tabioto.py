from typing import List

from fastapi import APIRouter
from fastapi.responses import FileResponse

import api.schema.tabioto as tabioto_schema

router = APIRouter()


@router.get("/tabioto", response_model=List[tabioto_schema.Place])
async def place_list():
    return [
        tabioto_schema.Place(id=0, name="京都タワー", latitude=135.75937443779, longitude=34.987521642792),
        tabioto_schema.Place(id=1, name="京都駅", latitude=135.75842935264, longitude=34.985160306524)
    ]


@router.post('/tabioto')
async def post_tabioto(body: tabioto_schema.TabiotoCreateRequest):
    return tabioto_schema.TabiotoCreateResponse(title=body.title, sound_url=body.title)


@router.get('/tabioto/{id}', response_model=tabioto_schema.TabiotoDetailResponse)
async def tabioto_detail(id: int):
    return tabioto_schema.TabiotoDetailResponse(
        place=tabioto_schema.Place(id=0, name="京都タワー", latitude=135.75937443779, longitude=34.987521642792),
        sound_list=[
            tabioto_schema.SoundResponse(name='国歌', url='kimigayo.mp3'),
            tabioto_schema.SoundResponse(name='アルビノーニ　アダージョ', url='JS_Batch_Air.mp3'),
        ],
        place_count=2
    )


@router.get('/tabioto/user/{user_id}', response_model=tabioto_schema.TabiotoDetailResponse)
async def user_tabioto_list(user_id: int):
    return tabioto_schema.TabiotoDetailResponse(
        place=tabioto_schema.Place(id=0, name="京都タワー", latitude=135.75937443779, longitude=34.987521642792),
        sound_list=[
            tabioto_schema.SoundResponse(name='国歌', url='kimigayo.mp3'),
            tabioto_schema.SoundResponse(name='アルビノーニ　アダージョ', url='JS_Batch_Air.mp3'),
        ],
        place_list=2
    )


@router.get('/mp3')
async def mp3_player():
    return FileResponse('api/sound/kimigayo.mp3')
