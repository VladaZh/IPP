import httpx

BASE_URL = "https://api.github.com"

res = httpx.request(  # информация о профиле
    method="GET",
    url=f"{BASE_URL}/users/alex020160",
    headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
    },
)

print(res.json())

res = httpx.request(  # информация о коммитах в репозитории
    method="GET",
    url=f"{BASE_URL}/repos/alex020160/recipe-service/commits",
    headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
    },
)

res_json = res.json()
print(res_json)
print(len(res_json))  # количество коммитов в репозитории

for commit in res_json[::-1]:  # автор и описание коммитов, начиная с наиболее ранних
    print(
        f'committer: {commit["commit"]['committer']['name']}, message: {commit["commit"]["message"]}'
    )
