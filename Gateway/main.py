import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Установка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
registry_url = "http://127.0.0.1:8001/main/get-service-info/"
client = httpx.AsyncClient()

services_cache = {}


async def get_service_url(service_name: str) -> str:
    if service_name in services_cache:
        print(service_name)
        return services_cache[service_name]

    try:
        response = await client.get(f"{registry_url}{service_name}/")
        print(response.json())
        response.raise_for_status()
        service_url = response.json()['versions'][0]['service_url']
        services_cache[service_name] = service_url
        print(services_cache)
        return service_url

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to service: {str(e)}")


async def proxy_request(method: str, service_url: str, path: str, headers: dict, data: bytes = None) -> dict:
    try:
        print(data)
        print(service_url)
        async with httpx.AsyncClient() as http_client:
            url = f"{service_url}{path}"
            if method.lower() == "get":
                if data:
                    url += f"?{data.decode()}"
                    response = await http_client.get(url, headers=headers)
                else:
                    response = await http_client.get(url, headers=headers)
            else:

                if data:
                    print(1)
                    headers["Content-Length"] = str(len(data))
                response = await http_client.request(method.upper(), url, headers=headers, content=data)

            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to service: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.post("/gateway/{service_name}/{path:path}")
async def gateway_post(service_name: str, path: str, request: Request):
    print(service_name, path)
    service_url = await get_service_url(service_name)
    print(service_url)
    headers = dict(request.headers)
    data = await request.body()
    return await proxy_request("post", service_url, path, headers, data)


@app.get("/gateway/{service_name}/{path:path}")
async def gateway_get(service_name: str, path: str, request: Request):
    service_url = await get_service_url(service_name)
    headers = dict(request.headers)
    return await proxy_request("get", service_url, path, headers)


@app.put("/gateway/{service_name}/{path:path}")
async def gateway_put(service_name: str, path: str, request: Request):
    service_url = await get_service_url(service_name)
    headers = dict(request.headers)
    data = await request.body()
    return await proxy_request("put", service_url, path, headers, data)


@app.patch("/gateway/{service_name}/{path:path}")
async def gateway_patch(service_name: str, path: str, request: Request):
    service_url = await get_service_url(service_name)
    headers = dict(request.headers)
    data = await request.body()
    return await proxy_request("patch", service_url, path, headers, data)


@app.delete("/gateway/{service_name}/{path:path}")
async def gateway_delete(service_name: str, path: str, request: Request):
    service_url = await get_service_url(service_name)
    headers = dict(request.headers)
    data = await request.body()
    return await proxy_request("delete", service_url, path, headers, data)
