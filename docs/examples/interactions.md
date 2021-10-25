# Interactions

Interactions are the new method in which discord suggests User/Bot interactions occur. See the [API Documentation](https://discord.com/developers/docs/interactions/receiving-and-responding) for an in-depth understanding of how they work.

In general, the flow can be seen as the following:

1. A bot registers a command with Discord.
1. A user uses the command.
1. The bot receives a INTERACTION_CREATE event from the API.
1. The API expects a **single** response from the bot with respects to the Interaction from the user.

This flow results in some strange complications. When the bot gets an [Interaction][dyscord.objects.interactions.Interaction] it must map the ID within the `data` attribute to a specific response in it's code base. This makes using a simple static system difficult, as every time you register a new command with Discord you will get a new ID and would need to somehow map that again to the desired code to handle the new Interactions you will get.

In order to help alleviate this insanity, there are several Dyscord gives you to handle this.

## Command Handler

The [CommandHandler][dyscord.helper.CommandHandler] enables you to map a command to code. The flow is as follows:

1. Using the [Command][dyscord.objects.interactions.Command] object, create and register a new command. Keep track of the command's `name`.
1. Create a callback function which will service the given Interactions generated by the command.
    - The callback should accept one positional argument, which is the [Interaction][dyscord.objects.interactions.Interaction] generated when a user invokes the command.
1. Register the callback with Dyscord.
    - `dyscord.helper.CommandHandler.register_guild_callback('<name>', <callback_function>)`

When Dyscord receives an event from Discord, it will do a lookup against it's internal cache to determine if it knows which command the ID maps to. If it fails to find it, it will reach out to the Discord API to get the full command data in order to get the `name` field. It will then look at your instances internal cache to find the correct `callback_function` and invoke it.

'*But wait*!' you ask, 'Why do we need to talk to Discord? The Invocation already has the `name` within the `data`! I can just use that!'

Well, yes. **Sometimes**. Discord allows you to have duplicate names between Guild and Global scopes. This means you can have a `/foo` command for a specific Guild, and a *different* `/foo` command at the global scope. *And your users can see both*. By registering a local mapping, and then referencing the API, we can always map the right callback to the right function.

Lets look at an example.

```python
import dyscord

token = "YOUR TOKEN GOES HERE"
application_id = "YOUR APPLICATION ID GOES HERE"

client = dyscord.DiscordClient(token=token, application_id=application_id)

# We only even need to invoke this against the API once!
async def registration_function():
    new_command = dyscord.objects.interactions.Command()
    new_command.generate(
        name='test',
        description='Generic test slash command.',
        type=dyscord.objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )
    registration = await new_command.register_globally()

async def callback_function(interaction):
    response = interaction.generate_response()
    response.generate('I got your command!')
    await response.send()

dyscord.helper.CommandHandler.register_guild_callback('test', callback_function)

client.run()
```

The users is left to determine how to handle the `registration_function()` invocation, as you only even need to do this when you create a new command, or change an existing one.