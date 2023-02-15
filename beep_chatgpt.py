# -*- coding: utf-8 -*-
# chatgpt integration and database
async def message_to_dict(message):
    return {
        'content': message.content,
        'author': message.author.name,
        'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }

no_no = ["site list", "shoe list", "find style",
         "add", "gimme", "freshen up beep", "help"]
punct = [".", "?", "!"
         ]


async def handle_message(aiomysql, openai, message, cursor):

    punct_message = message.content.endswith(('.', '?', '!'))
    discord_user_id = message.author.id
    username = message.author.name
    print(punct_message)

    async with aiomysql.create_pool(
        host='Localhost',
        port=3306,
        user='root',
        password='root',
        db='beep_ai'
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                select_user_query = "SELECT user_id FROM users WHERE discord_user_id=%s"
                await cursor.execute(select_user_query, (discord_user_id))
                result = await cursor.fetchone()

                if result is None:
                    insert_user_query = "INSERT INTO users (discord_user_id, username) VALUES (%s, %s)"
                    await cursor.execute(insert_user_query, (discord_user_id, username))
                    await conn.cssswommit()
                    print("added new user")
                else:
                    print("known user")

                user_id = result[0]
                # message_dict = await message_to_dict(message)
                # params = {'prompt': message_dict['content']}
                # message_content = message.content + "."
                # select_query = "SELECT bot_response FROM interactions WHERE user_id=%s ORDER BY interaction_timestamp DESC LIMIT 10"
                # await cursor.execute(select_query, (user_id))
                # previous_resp = await cursor.fetchall()
                # prev_resp_list = [resp[0] for resp in previous_resp]
                # prev_resp_str = " ".join(prev_resp_list)
                # prompt = prev_resp_str + " " + message.content
                if punct_message == True:
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=message.content,
                        max_tokens=100,
                        n=1,
                        top_p=1,
                        stop=None,
                        frequency_penalty=0,
                        presence_penalty=0,
                        temperature=0
                    )
                    generated_text = response["choices"][0]["text"]

                    # Send generated text back to Discord
                    print(generated_text)
                    await message.channel.send(generated_text)
                    # await channel.send("gr^^^")
                    insert_interaction_query = "INSERT INTO interactions (user_id, context, bot_response) VALUES (%s, %s, %s)"
                    await cursor.execute(insert_interaction_query, (user_id, message.content, generated_text))
                    await conn.commit()

    # result = await handle_message(discord_user_id, username, message)
    # await channel.send(result)
    # await channel.send("res^^^")
