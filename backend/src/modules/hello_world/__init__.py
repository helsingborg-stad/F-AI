"""
An example module.

Sample usage below:
"""
import asyncio

from src.modules.hello_world.factory import HelloWorldFactory

if __name__ == '__main__':
    async def main():
        service = await HelloWorldFactory('en').get()
        print(service.greet())

        service = await HelloWorldFactory('sv').get()
        print(service.greet())

        try:
            service = await HelloWorldFactory('fr').get()
            print(service.greet())
        except ValueError as e:
            print(e)


    asyncio.run(main())
