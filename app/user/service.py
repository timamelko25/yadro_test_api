import random
from loguru import logger

from app.service.base import BaseService
from .models import User, Location
from .schemas import UserScheme
from app.internal_api import RandomUsersAPI


class UserService(BaseService):
    model = User

    @classmethod
    async def add_users(cls):
        try:
            raw_request = await RandomUsersAPI.get_users(5)

            if raw_request:
                results = raw_request.get("results", "")
                for result in results:
                    data = UserScheme.model_validate(result)
                    user = await cls.add(
                        gender=data.gender,
                        name=data.name.first,
                        surname=data.name.last,
                        phone_number=data.phone,
                        email=data.email,
                        photo_url=data.picture.thumbnail,
                    )

                    await LocationService.add(
                        user_id=user.id,
                        user=user,
                        street_number=data.location.street.number,
                        street_name=data.location.street.name,
                        city=data.location.city,
                        state=data.location.state,
                        country=data.location.country,
                    )

                    logger.info(f"New user added {user.id}")

        except Exception as e:
            logger.error(f"Error while add new user: {e}")

    @classmethod
    async def get_random_user(cls):
        users = await cls.find_all()
        if not users:
            return None
        return random.choice(users)


class LocationService(BaseService):
    model = Location
