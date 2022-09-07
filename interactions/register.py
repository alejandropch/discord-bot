import discord
from utils.userExists import handle as userExists
from utils.User import User



    value = requests.post(os.environ["API_URL"] + '/participants/', data=json.dumps(data), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    print(value.json())

    try:
        value.json()
        print(value.text)
    except json.decoder.JSONDecodeError:
        print("json empty")

    return
