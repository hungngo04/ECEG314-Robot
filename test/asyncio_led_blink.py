from machine import Pin
import asyncio

shared_state = {
    'enabled': True,
    'counter': 0
}

leds = [Pin(6, Pin.OUT), Pin(26, Pin.OUT), Pin(27, Pin.OUT)]
btn = Pin(20, Pin.IN, Pin.PULL_DOWN)

async def blink_led(led, period_ms, name):
    while True:
        if shared_state['enabled']:
            led.toggle()

        await asyncio.sleep_ms(period_ms)

async def update_counter():
    while True:
        shared_state['counter'] += 1
        await asyncio.sleep_ms(1000)

async def main():
    task1 = asyncio.create_task(blink_led(leds[0], 500, "LED1"))
    task2 = asyncio.create_task(blink_led(leds[1], 300, "LED2"))
    task3 = asyncio.create_task(blink_led(leds[2], 100, "LED3"))
    task4 = asyncio.create_task(update_counter())

    await asyncio.gather(task1, task2, task3, task4)
