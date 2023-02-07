import requests


# request_data = [
#     {"user_id": "xyz", "payload": "Hello"},
#     {"user_id": "xyz", "payload": "turn clockwise right now"},
#     {"user_id": "xyz", "payload": "You must move forward"},
#     {"user_id": "xyz", "payload": "You must move forward 10 metres"},
#     {"user_id": "xyz", "payload": "move forward 10 metres"},
#     {"user_id": "xyz", "payload": "detect this people"},
#     {"user_id": "xyz", "payload": "detect this car"},
# ]

request_data = [
    {"user_id": "xyz1", "payload": "Привет"},
    {"user_id": "xyz1", "payload": "Как дела, робот?"},
    {"user_id": "xyz1", "payload": "Кто тебя создал, робот"},
    {"user_id": "xyz1", "payload": "Сейчас же повернись направо"},
    {"user_id": "xyz1", "payload": "Едь вперед"},
    {"user_id": "xyz1", "payload": "Повернись налево на 10"},
    {"user_id": "xyz1", "payload": "Детектируй женщину"},
    {"user_id": "xyz1", "payload": "Let's speak about marketing"},
    {"user_id": "xyz1", "payload": "How are you?"},
    {"user_id": "xyz1", "payload": "MMMM"}
]



def main_test():
    url = "http://0.0.0.0:4242"
    # url = "http://localhost:4242"

    print("=========")
    for cur_request in request_data:
        r = requests.post(url=url, json=cur_request)
        # print(r.json())
        print("Request - ", cur_request["payload"], "\n", "Response - ", r.json()["response"])
        print("============")


if __name__ == "__main__":
    main_test()