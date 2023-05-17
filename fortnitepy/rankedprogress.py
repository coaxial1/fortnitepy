import datetime
from typing import List

from .enums import RankingType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


class SingleRankedProgress:
    __slots__ = ('raw', 'client')

    def __init__(self, client: 'Client', data: dict) -> None:
        self.raw = data
        self.client = client

    def __repr__(self):
        return ('<SingleRankedProgress ranking_type={0.ranking_type} current_division={0.current_division} '
                'highest_division={0.highest_division} promotion_progress={0.promotion_progress} '
                'last_updated={0.last_updated}>'.format(self))

    @property
    def ranking_type(self) -> RankingType:
        return RankingType(self.raw['rankingType'])

    @property
    def last_updated(self) -> datetime.datetime:
        return self.client.from_iso(self.raw['lastUpdated'])

    @property
    def current_division(self) -> int:
        return self.raw['currentDivision']

    @property
    def highest_division(self) -> int:
        return self.raw['highestDivision']

    @property
    def promotion_progress(self) -> float:
        return self.raw['promotionProgress']


class RankedProgress:
    __slots__ = ('raw', 'type_to_ranked_progress')

    def __init__(self, client: 'Client', data: List[dict]) -> None:
        self.raw = data
        self.type_to_ranked_progress = {
            RankingType(ranked_progress['rankingType']): SingleRankedProgress(client, ranked_progress)
            for ranked_progress in data
            if (ranked_progress['rankingType'] in [RankingType.ZERO_BUILD.value, RankingType.BATTLE_ROYALE.value]
                and ranked_progress['gameId'] == 'fortnite')
        }

    def __repr__(self):
        return ('<RankedProgress battle_royale_ranked_progress={0.battle_royale_ranked_progress} '
                'zero_build_ranked_progress={0.zero_build_ranked_progress}>'.format(self))

    def for_type(self, ranking_type: RankingType) -> SingleRankedProgress:
        return self.type_to_ranked_progress[ranking_type]

    @property
    def battle_royale(self) -> SingleRankedProgress:
        return self.for_type(RankingType.BATTLE_ROYALE)

    @property
    def zero_build(self) -> SingleRankedProgress:
        return self.for_type(RankingType.ZERO_BUILD)
