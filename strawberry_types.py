from typing import List
import strawberry


@strawberry.type
class Date:
    year: int
    month: int
    day: int


@strawberry.type
class AdditionalInfo:
    status: str
    birth_date: Date


@strawberry.type
class UserMeta:
    email: str
    name: str
    additional_info: AdditionalInfo


@strawberry.type
class Query:
    @strawberry.field
    def users(self, year: int) -> List[UserMeta]:
        return list(filter(lambda u: u.additional_info.birth_date.year == year, [
            UserMeta(
                "hello@world.ru",
                "Mike",
                AdditionalInfo(
                    "I am a hero",
                    Date(2001, 1, 1)
                )
            ),
            UserMeta(
                "hi@world.ru",
                "Pol",
                AdditionalInfo(
                    "DevOps",
                    Date(1001, 1, 1)
                )
            ),
        ]))
