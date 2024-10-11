from telethon.sync import TelegramClient
from telethon.errors import UsernameInvalidError
from telethon.tl.functions.channels import GetParticipantsRequest, GetForumTopicsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
from config import api_id, api_hash
from utils import display_logo
import csv
import asyncio

# Funcția pentru exportarea membrilor
async def export_members(client, entity):
    all_participants = []
    offset = 0
    limit = 200
    while True:
        participants = await client(GetParticipantsRequest(
            entity, ChannelParticipantsSearch(''), offset, limit, hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
    
    entity_name = entity.username or entity.id
    with open(f'membri_{entity_name}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'username', 'first_name', 'last_name', 'phone'])
        for user in all_participants:
            writer.writerow([user.id, user.username, user.first_name, user.last_name, user.phone])
    print(f"Export finalizat: {len(all_participants)} membri salvați în membri_{entity_name}.csv")

# Funcția pentru exportarea mesajelor
async def export_messages(client, entity, topic_id=None):
    messages = []
    if topic_id:
        # Accesăm corect topicul specific folosind InputChannel și identificatorul topicului
        input_channel = InputChannel(entity.id, entity.access_hash)
        async for message in client.iter_messages(input_channel, limit=1000, reply_to=topic_id):
            messages.append([message.id, message.date, message.sender_id, message.text])
    else:
        async for message in client.iter_messages(entity, limit=1000):
            messages.append([message.id, message.date, message.sender_id, message.text])
    
    # Scrierea mesajelor în CSV
    entity_name = entity.username or entity.id
    filename = f'mesaje_{entity_name}.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'date', 'sender_id', 'text'])
        for msg in messages:
            writer.writerow(msg)
    print(f"Export finalizat: {len(messages)} mesaje salvate în {filename}")

# Funcția pentru a lista toate topicurile dintr-un forum folosind GetForumTopicsRequest
async def list_forum_topics(client, entity):
    topics = []
    try:
        result = await client(GetForumTopicsRequest(
            channel=entity,
            offset_date=None,
            offset_id=0,
            offset_topic=0,
            limit=100
        ))
        topics.extend(result.topics)
    except Exception as e:
        print(f"A apărut o eroare la obținerea topicurilor: {e}")
    return topics

# Funcția pentru a determina tipul de entitate
async def determine_entity_type(entity):
    if hasattr(entity, 'forum') and entity.forum:
        return "Forum"
    elif entity.megagroup:
        return "Grup"
    elif entity.broadcast:
        return "Canal"
    return "Necunoscut"

# Funcția principală a aplicației
async def main():
    display_logo()
    
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    entity_username = input("Introdu username-ul sau link-ul entității (ex: @numele_canalului): ").strip()
    try:
        entity = await client.get_entity(entity_username)
    except UsernameInvalidError:
        print("Username-ul sau link-ul entității nu este valid.")
        return
    except Exception as e:
        print(f"A apărut o eroare la accesarea entității: {e}")
        return

    entity_type = await determine_entity_type(entity)
    print(f"\nEntitatea introdusă este un {entity_type}.")

    # Alege ce să exporți: membri sau mesaje
    print("\nCe vrei să exporți?")
    print("1. Membri")
    print("2. Mesaje")
    export_choice = input("Alege opțiunea (1 sau 2): ").strip()

    if export_choice == '1':
        # Export membri
        await export_members(client, entity)
    elif export_choice == '2':
        # Dacă este forum, afișează lista de topicuri înainte de exportul mesajelor
        if entity_type == "Forum":
            topics = await list_forum_topics(client, entity)
            if not topics:
                print("Nu există topicuri disponibile în acest forum.")
                return

            print("Topicuri disponibile:")
            for idx, topic in enumerate(topics):
                print(f"{idx + 1}. {topic.title or 'Fără titlu'} (ID: {topic.id})")

            topic_choice = int(input("Selectează un topic pentru export sau apasă Enter pentru toate: ").strip() or 0)
            if topic_choice > 0 and topic_choice <= len(topics):
                selected_topic = topics[topic_choice - 1].id
            else:
                selected_topic = None
            await export_messages(client, entity, selected_topic)
        else:
            # Export mesaje din canale sau grupuri obișnuite
            await export_messages(client, entity)
    else:
        print("Opțiune invalidă!")

if __name__ == "__main__":
    asyncio.run(main())
