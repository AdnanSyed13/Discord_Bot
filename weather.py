import discord

# Retrieves these weather outputs for location specified.
color = 0xFF6500
key_features = {
    'temp' : 'Temperature',
    'feels_like' : 'Feels Like',
    'temp_min' : 'Minimum Temperature',
    'temp_max' : 'Maximum Temperature'
}

# Deletes these fields from the returned weather information.
def parse_data(data):
    del data['humidity']
    del data['pressure']
    return data

# Formats the banner with these fields.
def weather_message(data, location):
    location = location.title()
    message = discord.Embed(
        title=f'{location} Weather',
        description=f'Here is the weather in {location}.',
        color=color
    )
    for key in data:
        message.add_field(
            name=key_features[key],
            value=str(data[key]),
            inline=False
        )
    return message

# Displays an error message if location is invalid.
def error_message(location):
    location = location.title()
    return discord.Embed(
        title='Error',
        description=f'There was an error retrieving weather data for {location}.',
        color=color
    )