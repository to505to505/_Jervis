import uvicorn


if __name__ == '__main__':
    uvicorn.run('app_api.app_api:app', port = 81, reload = True)
