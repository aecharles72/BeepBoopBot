"""
Chat GPT functionality

"""
# chatgpt integration and database

no_no = ["site list", "shoe list", "find style",
         "add", "gimme", "freshen up beep", "help"]
punct = [".", "?", "!"]


async def message_to_dict(message):
    '''


    Parameters
    ------
    message : TYPE v
        DESCRIPTION.
        convert string to dict

    Returns
    -------
    dict
        DESCRIPTION.
        dict of string

    '''
    return {
        'content': message.content,
        'author': message.author.name,
        'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }


async def handle_message(aiomysql, openai, message, channel):
    '''


    Parameters
    ----------
    aiomysql : TYPE lib
    openai : TYPE lib
    message : TYPE v
    channel : TYPE v
        main ai

    Returns
    -------
    None.

    '''

    punct_message = message.content.endswith(('.', '?', '!'))
    discord_user_id = message.author.id
    username = message.author.name
    print(f"CHATUser Input: {punct_message}")

    # connect to ai db
    async with aiomysql.create_pool(
        host='Localhost',
        port=3306,
        user='root',
        password='root',
        db='beep_ai'
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    f"SELECT user_id FROM users WHERE discord_user_id='{discord_user_id}'")
                result = await cursor.fetchone()
                if result is None:
                    insert_user_query = "INSERT INTO users (discord_user_id, username) \
                        VALUES (%s, %s)"
                    await cursor.execute(insert_user_query, (discord_user_id, username))
                    await conn.commit()
                    print("CHAT added new user")
                else:
                    print("CHAT: known user")
                if punct_message is True:
                    print(f"CHAT: User:{message.content}")
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
                    print(f"CHAT: Beep:{generated_text}")
                    print(f"CHAT: {message.channel}")
                    print(f"CHAT: {message.channel.id}")
                    print(f"CHAT: {message.author.id}")
                    print(f"CHAT: {message.author}")
                    await channel.send(generated_text)
                    # await channel.send("gr^^^")
                    insert_interaction_query = "INSERT INTO interactions (discord_user_id, \
                        context, bot_response, thread_id, thread_name) VALUES (%s, %s, %s, %s, %s)"
                    await cursor.execute(
                        insert_interaction_query, (
                            discord_user_id, message.content, generated_text, channel.id, channel))
                    await conn.commit()
