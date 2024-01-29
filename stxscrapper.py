from telethon import TelegramClient, events
import re
import asyncio
import os
import time
import random

API_ID = 13586086
API_HASH = "c3b5390a93d5244e722fc4b8a0c1ac2a"

client = TelegramClient('my_account', api_id=API_ID, api_hash=API_HASH)

@client.on(events.NewMessage(pattern='/scrmail'))
async def email_scrape(event):
    try:
        args = event.text.split()[1:]
        chat = args[0]
        limits = int(args[1])
    except (IndexError, ValueError):
        await event.reply("<b>Wrong Format! Use /scrmail [Username or URL] [Amount].</b>", parse_mode='html')
        return

    loading_message = await event.reply("<b>Processing, Please Wait....</b>", parse_mode='html')
    out = ""
    count = 0

    try:
        chat_entity = await client.get_entity(chat)
    except Exception as e:
        print(e)
        await event.reply(f"<b>Sorry Bruh, No Emails Found! 🥲</b>", parse_mode='html')
        return

    start_time = time.time()

    async for mail_ss in client.iter_messages(chat_entity, limit=limits, reverse=True):
        if mail_ss.text:
            msg1 = mail_ss.text.split("\n")
        elif hasattr(mail_ss, 'media') and mail_ss.media and hasattr(mail_ss.media, 'caption'):
            msg1 = mail_ss.media.caption.split("\n")
        else:
            msg1 = []

        for text in msg1:
            # Updated pattern to collect popular email domains
            pattern = re.findall(r"(\w+@(?:gmail\.com|outlook\.com|yahoo\.com|proton\.me|example\.com)):(\w+)", text)
            match = "\n".join(":".join(pair) for pair in pattern)
            out += match + "\n"
            count += 1

    out = "\n".join(set(filter(None, out.split("\n"))))
    removed_count = count - len(out.split("\n"))
    fcount = count - removed_count

    # Replace this path with the absolute path where you want to save the file
    absolute_path = "/storage/emulated/0/STxScrap/Files/"
    
    file_name = f"{fcount}stxscrape.txt"

    # Ensure the directory exists
    os.makedirs(absolute_path, exist_ok=True)

    with open(os.path.join(absolute_path, file_name), 'w+') as f:
        f.write(f"{out}\n")

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 1)

    output_message = f"""<b>COMPLETED ✅
    
┌ Source » {chat}
├ Amount » {count}
├ Found » {fcount}
└ Removed » {removed_count}

┌ Time » {elapsed_time}s
├ Developer » @sabbir69x
└ Bot by » @sabbir69x</b>"""

    # Send the file using the same client instance
    await client.send_file(event.chat_id, os.path.join(absolute_path, file_name), caption=output_message, parse_mode='html')
    await loading_message.delete()

    # Remove the file after sending
    os.remove(os.path.join(absolute_path, file_name))

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())