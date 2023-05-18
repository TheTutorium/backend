import asyncio
import aiohttp


async def make_request(session):
    async with session.get(
        "https://backend-production-0aaf.up.railway.app/bookings/all-by-user/",
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Imluc18yUFBhWE54VG0wd0h6V243YTZpMnB2cXYyemIiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwOi8vbG9jYWxob3N0OjUxNzMiLCJleHAiOjE2ODQ0Mzg2ODgsImlhdCI6MTY4NDQzODYyOCwiaXNzIjoiaHR0cHM6Ly9kb21pbmFudC1jb25kb3ItMjkuY2xlcmsuYWNjb3VudHMuZGV2IiwibmJmIjoxNjg0NDM4NjE4LCJzaWQiOiJzZXNzXzJQeW9MYXg2Z3lHSFA2ejlCU0Q4cnZhazhLViIsInN1YiI6InVzZXJfMlB5b0xnSlk3N0I4ZWNZeXpzVlVvU1VhYzRFIn0.hnPOnp9n9t3VVNF-eho20uAeWeUJ07Slr2qLfm3lo9mwlFaMS17Kac810ePQcloW4ctmJfHDI17Eea-UDNNOYVtG3gRgOc0Q84Xn7GViHSJQOZ3eAZPOgkUtD7ecVP77Ut-lFb8N826RWykE_PUmi9T_P3EPATmh3fO5KS7LAyIhjxhscdozppOrcMSYW_26mybKqTSSxg84HR4VUzI9ix46OiHdEBj6s2yECSKCfSJUwQNYdVGbcWz36XAvq4SeL3pYb-Hs8dGKiFR0LooNb-X0oKBtK9QOf3-64J-qa7M23Y5JeLjiAmL7srf9I-mquYkIoCzz5zdd2JCIN-tWyA"
        },
    ) as response:
        result = await response.text()
        print(f"Response: {result}")


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(500):
            task = asyncio.create_task(make_request(session))
            tasks.append(task)

        await asyncio.gather(*tasks)


asyncio.run(main())
