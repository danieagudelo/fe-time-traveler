from fastapi import APIRouter, status
from schemas.location import LocationSchema
from services.location import get_locations, save_location

router = APIRouter(
    tags=["Locations"],
    responses={201: {"description": "OK"}},
)

markers = [
    {
        "id": 1,
        "lat": 4.622707385290953,
        "lng": -74.07323253584825,
        "title": "Edificación esquina noroccidental de la calle 33 #18",
        "text": "Edificación ordenada, basada en la reglamentación del barrio Teusaquillo en la  década de 1930. Esta edificación da muestra de el Plan de edificación de la época, en donde solo se aprobaban licencias de construcción a las edificaciones que cumplieran con el Proyecto de urbanización vigente. Tomado de: PEMP Teusaquillo (decada 1930) y Google Maps (2012 y 2020).",
        "images": [
            "https://i.imgur.com/EKDO53H.jpg",
            "https://i.imgur.com/6co1ATP.jpg",
            "https://i.imgur.com/AFB2b5G.jpg",
        ],
    },
    {
        "id": 2,
        "lat": 4.621148485899155,
        "lng": -74.0706258937353,
        "title": "Text for Marker 2",
        "images": [
            "https://i.imgur.com/6R3RY6U.jpg",
            "https://i.imgur.com/EKDO53H.jpg",
        ],
    },
]


@router.get(
    "/locations",
    description="Get all the location",
    status_code=status.HTTP_200_OK
)
def get_markers():
    return get_locations()


@router.post(
    "/locations",
    description="Create location",
    status_code=status.HTTP_200_OK
)
def get_markers(location: LocationSchema):
    return save_location(location)
