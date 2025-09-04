import httpx
import json
import logging
from typing import Dict, Any, List
from multipart import MultipartParser
import io

class ExtraClient:
    def __init__(self, config: Dict[str, Any]):
        self.name = config.get("name")
        self.base_url = config.get("url")
        self.apikey = config.get("apikey", {})
        self.dataids = config.get("dataids_for_camera", [])

    async def _make_request(self, method: str, endpoint: str, **kwargs):
        """Make a request to the API.

        Args:
            method: The HTTP method to use.
            endpoint: The API endpoint to call.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            The response from the API.

        Raises:
            ValueError: If the API key is not configured.
        """
        if not self.apikey:
            error_msg = f"API key not configured for {self.name}"
            raise ValueError(error_msg)

        headers = {"X-API-KEY": self.apikey}
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response
        except httpx.RequestError as exc:
            logging.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise
        except httpx.HTTPStatusError as exc:
            logging.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc}")
            raise

    async def get_image(self, farm_id: int = 1, data_id: int = None):
        """Get an image from the API.

        Args:
            farm_id: The ID of the farm.
            data_id: The ID of the data.

        Returns:
            The content of the response.

        Raises:
            ValueError: If data_id is None.
        """
        endpoint = "/image"
        if data_id is None:
            error_msg = f"data_id is None"
            raise ValueError(error_msg)
        params = {"farm_id": farm_id, "data_id": data_id}

        response = await self._make_request("GET", endpoint, params=params)
        
        # Parse multipart response
        try:
            parser = MultipartParser(io.BytesIO(response.content), response.headers['Content-Type'])
            parts = parser.get_parts()
            
            if len(parts) != 2:
                raise ValueError(f"Expected 2 parts in multipart response, but got {len(parts)}")

            metadata_part = parts[0]
            image_part = parts[1]

            if metadata_part.headers.get(b'Content-Type') != b'application/json':
                raise ValueError(f"Expected first part to be application/json, but got {metadata_part.headers.get(b'Content-Type')}")

            metadata = json.loads(metadata_part.get_payload())
            image_data = image_part.get_payload()
        except Exception as e:
            logging.error(f"Failed to parse multipart response: {e}")
            raise

        # Save image to file
        image_path = metadata.get('path')
        if image_path:
            with open(image_path, "wb") as f:
                f.write(image_data)

        return response.content

    async def get_forecast(self):
        """Get the forecast from the API.

        Returns:
            The forecast data.
        """
        endpoint = "/forecast"
        response = await self._make_request("GET", endpoint)
        try:
            forecast_data = json.loads(response.text)
            with open("forecasts/forecast.json", "w") as f:
                json.dump(forecast_data, f, indent=4)
            return forecast_data
        except (json.JSONDecodeError, SyntaxError) as e:
            error_msg = f"Failed to decode JSON from response. Status code: {response.status_code}, Response text: {response.text}"
            logging.error(error_msg)
            raise e

    async def post_heartbeat(self, content: str, farm_id: int = 1, category: str = "ai", created_time: str = None):
        """Post a heartbeat to the API.

        Args:
            content: The content of the heartbeat.
            farm_id: The ID of the farm. Defaults to 1.
            category: The component category. Defaults to "ai".
            created_time: The creation time of the heartbeat. Defaults to current time if None.

        Returns:
            The response from the API.
        """
        endpoint = "/heartbeat"
        data = {
            "farm_id": farm_id,
            "category": category,
            "content": content
        }
        if created_time:
            data["created_time"] = created_time

        response = await self._make_request("POST", endpoint, json=data)
        return response

    async def post_target(self, target_data: Dict[str, Any]):
        """Post new target settings to the API.

        Args:
            target_data: A dictionary, each representing a target setting.
                         Example: 
                             {
                                 "farm_id": 1,
                                 "temperature": 25.5,
                                 "humidity": 65.0,
                                 "CO2": 800.0,
                                 "VPD": 1.2,
                                 "targettime": "2025-01-15T15:30:00"
                             }

        Returns:
            The response from the API.
        """
        endpoint = "/target"
        response = await self._make_request("POST", endpoint, json=[target_data])
        return response
