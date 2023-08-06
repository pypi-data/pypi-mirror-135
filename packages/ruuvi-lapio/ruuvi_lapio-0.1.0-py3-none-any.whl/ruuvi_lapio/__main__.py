"""
Copyright (c) 2022, Panu Oksiala

Derived from ruuvitag_sensor example by Tomi Tuhkanen.
https://github.com/ttu/ruuvitag-sensor/blob/master/examples/send_updated_async.py

MIT License

Copyright (c) 2016 Tomi Tuhkanen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse

from multiprocessing import Manager
import json
from concurrent.futures import ProcessPoolExecutor
import asyncio
from aiohttp import ClientSession

from ruuvitag_sensor.ruuvi import RuuviTagSensor


async def handle_queue(args: argparse.Namespace, queue):
    async def send_post(session, update_data):
        async with session.post(
            args.dest,
            data=json.dumps(update_data),
            headers={"content-type": "application/json"},
        ) as response:
            print(response.status)
            response = await response.read()
            print(response)

    async with ClientSession() as session:
        while True:
            if not queue.empty():
                data = queue.get()
                asyncio.create_task(send_post(session, data))
            else:
                await asyncio.sleep(0.1)


def format_data(data: dict) -> dict:
    keys_with_decimals = (
        "humidity",
        "temperature",
        "pressure",
        "acceleration",
    )
    keys_as_is = (
        "battery",
        "measurement_sequence_number",
        "movement_counter",
        "tx_power",
        "acceleration_x",
        "acceleration_y",
        "acceleration_z",
    )
    res = {}
    for key in keys_with_decimals:
        res[key] = int(data[key] * 100)  # precise enough
    for key in keys_as_is:
        res[key] = int(data[key])  # ensure int
    res["mac"] = data["mac"]
    return res


def run_get_datas_background(queue):
    def handle_new_data(new_data):
        sensor_data = new_data[1]
        formatted_data = format_data(sensor_data)
        queue.put(formatted_data)

    RuuviTagSensor.get_datas(handle_new_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ruuvi-lapio",
        description="A simple app that sends sensory data over http",
    )
    parser.add_argument(
        "dest",
        help="Where to send measurements including protocol and path.",
    )
    args = parser.parse_args()
    m = Manager()
    q = m.Queue()

    executor = ProcessPoolExecutor()
    executor.submit(run_get_datas_background, q)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle_queue(args, q))
