import requests
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


@router.post('/tabioto', response_model=tabioto_schema.TabiotoCreateResponse)
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
        place_count=2,
        color=[0.4490342503266062, 0.32979157405188686, 0.22117417901766545]
    )


@router.get('/tabioto/user/{user_id}', response_model=tabioto_schema.TabiotoDetailResponse)
async def user_tabioto_list(user_id: int):
    return tabioto_schema.TabiotoDetailResponse(
        place=tabioto_schema.Place(id=0, name="京都タワー", latitude=135.75937443779, longitude=34.987521642792),
        sound_list=[
            tabioto_schema.SoundResponse(name='国歌', url='kimigayo.mp3'),
            tabioto_schema.SoundResponse(name='アルビノーニ　アダージョ', url='JS_Batch_Air.mp3'),
        ],
        place_count=2,
        color=[0.4490342503266062, 0.32979157405188686, 0.22117417901766545]
    )


@router.get('/mp3')
async def mp3_player():
    return FileResponse('api/sound/D510694E-0C21-4509-B44B-8464B472E06D.m4a')


class MiniAPIUtil:
    def get_access_token_for_mini_API(self):
        files = {
            'grant_type': (None, 'https://auth.mimi.fd.ai/grant_type/application_client_credentials'),
            'client_id': (None, '147d2ff020d645049712614cf37f9632:e04a72e8e9ed4f24b842a8ec8adac94f'),
            'client_secret': (None,
                              'ed03b4d4cd93f87735ebe1657aab8b0f32c8411d38667e350b3c04184f646dbab68cfffbfa4e300e678381b17e6f7d65feb8fc6b0fbe76faa3c2c02fc3f42c78cf9d2ce2cb1df3b9cad062c4f1822ca3f63d719fa0f841110d8a51e59ca3a9e2b2602954caf38efa2281a39f8f0faf07223a70bf9f68e7ed57b5facd4eb350965854015e51dd40f95ad59458de2971b78275e6466dc725330a3fc4c0e4780d40a7c0c18026f8b2e52feec779f979da7aae431027f5a8161ac916dbf06b2f56603a31cb0a460eebef9c04b2077981ce7145566185e244603116750aa75cc10b76376dc63f5938baf37e3ec8f2b6aca5df3afc66ea13ad09327600673ddb990128'),
            'scope': (None, 'https://apis.mimi.fd.ai/auth/emo-categorical/http-api-service'),
        }

        response = requests.post('https://auth.mimi.fd.ai/v2/token', files=files)
        return response.json()['accessToken']

    def get_emotion_score_from_audio_by_mini_API(self):
        access_token = self.get_access_token_for_mini_API()

        headers = {
            'Content-Type': 'audio/x-pcm;bit=16;rate=16000;channels=1',
            'x-mimi-process': 'emo-categorical',
            'Authorization': 'Bearer ' + access_token,
        }

        with open('api/sound/D510694E-0C21-4509-B44B-8464B472E06D.m4a', 'rb') as f:
            data = f.read().replace(b'\n', b'')

        response = requests.post('https://service.mimi.fd.ai', headers=headers, data=data)

        return response.json()['response']['scores']

    def get_color_from_audio(self):
        emo_raw_data = self.get_emotion_score_from_audio_by_mini_API()

        print(emo_raw_data)

        weight = [[3 / 6, 2 / 6, 1 / 6],
                  [1 / 3, 1 / 3, 1 / 3],
                  [1 / 2, 0, 1 / 2],
                  [0, 0, 1],
                  [1 / 4, 2 / 4, 1 / 4]]

        emo_data = [
            emo_raw_data['sadness'],
            emo_raw_data['disgust'],
            emo_raw_data['neutral'],
            emo_raw_data['happiness'],
            emo_raw_data['anger'],
        ]

        cmy = [0, 0, 0]

        for i in range(len(weight)):
            for j in range(len(weight[i])):
                cmy[j] += weight[i][j] * emo_data[i]

        print(cmy)
        return cmy


MiniAPIUtil().get_color_from_audio()
