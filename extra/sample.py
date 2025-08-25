import asyncio
import json
import os
from client import ExtraClient

async def main():
    """
    This is a sample script to test the ExtraClient class.
    It reads the configuration from conf.json, creates an ExtraClient instance,
    and then calls the get_forecast and get_image methods.
    """
    # Load configuration from conf.json
    try:
        conf_path = "conf.json"
        with open(conf_path) as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: conf.json not found. Please make sure the configuration file exists.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode conf.json. Please check the file format.")
        return

    # Create an instance of ExtraClient
    client = ExtraClient(config)

    # Create forecasts directory if it doesn't exist
    if not os.path.exists("forecasts"):
        os.makedirs("forecasts")

    # Test get_forecast
    try:
        print("Getting forecast data...")
        forecast = await client.get_forecast()
        print("Forecast data received and saved to forecasts/forecast.json")
        # You can uncomment the line below to print the forecast data
        # print(json.dumps(forecast, indent=4))
    except Exception as e:
        print(f"Error getting forecast: {e}")

    # Test get_image for each dataid
    if client.dataids:
        for data_id in client.dataids:
            try:
                print(f"Getting image for data_id: {data_id}...")
                await client.get_image(data_id=data_id)
                print(f"Image for data_id {data_id} received and saved.")
            except Exception as e:
                print(f"Error getting image for data_id {data_id}: {e}")
    else:
        print("No dataids_for_camera found in the configuration file.")

    # Test post_heartbeats
    try:
        print("Posting heartbeat...")
        await client.post_heartbeats("This is a test heartbeat.")
        print("Heartbeat posted successfully.")
    except Exception as e:
        print(f"Error posting heartbeat: {e}")

if __name__ == "__main__":
    # To run this sample, you would typically execute `python sample.py` in your terminal.
    # This will run the asyncio event loop and execute the main coroutine.
    asyncio.run(main())
