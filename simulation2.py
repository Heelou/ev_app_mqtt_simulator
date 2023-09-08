import paho.mqtt.client as mqtt
import json
import os

# Hàm xử lý tin nhắn MQTT


def on_message(client, userdata, message):
    # In ra thông tin tin nhắn
    print("Tiêu đề:", message.topic)
    print("Nội dung:", message.payload.decode())

    # Tách JSON thành các đối tượng
    data = json.loads(message.payload.decode())

    # Tạo thư mục để lưu các file JSON
    directory = "data"
    if not os.path.exists(directory):
        os.mkdir(directory)

    # Lưu từng đối tượng JSON vào một file riêng
    for object in data:
        file_name = f"{directory}/{object['id']}.json"
        with open(file_name, "w") as f:
            json.dump(object, f)

    # In ra nội dung của từng file JSON
    for file in os.listdir(directory):
        with open(f"{directory}/{file}", "r") as f:
            print(f"Nội dung của file {file}:")
            print(json.load(f))


# Tạo client MQTT
client = mqtt.Client()

# Thiết lập callback để xử lý tin nhắn
client.on_message = on_message

# Kết nối với broker MQTT
client.connect("171.244.57.88", 1883)

# Subscribe topic
client.subscribe("evse_service/EVSE45678/#")

# Bắt đầu vòng lặp lắng nghe tin nhắn
while True:
    # Chờ nhận tin nhắn
    client.loop(100)
