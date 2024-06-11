from typing import List
from . import Client
from .model.platform import Platform
from .model.price import Price
from .model.price_category import PriceCategory
from .model.result import Result


class Prices:
    @staticmethod
    def get_prices(client: Client, platform: Platform) -> Result[List[Price]]:
        """
        Returns all rates for a specific platform.

        See: https://api.reyden-x.com/docs#/Prices/prices_v1_prices__platform_code___get

        Parameters:
            client (Client): Instance of Client
            platform (Platform): twitch, youtube etc.

        Returns:
            Result[List[Price]]: Result object
        """
        r = client.get(f"/prices/{platform.value}/")
        return Result[List[Price]](**r)

    @staticmethod
    def get_categories(client: Client) -> Result[List[PriceCategory]]:
        """
        Returns all price categories.

        See: https://api.reyden-x.com/docs#/Price%20Categories/categories_v1_price_categories__get

        Parameters:
            client (Client): Instance of Client

        Returns:
            Result[List[PriceCategory]]: Result object
        """
        r = client.get("/price-categories/")
        return Result[List[PriceCategory]](**r)
