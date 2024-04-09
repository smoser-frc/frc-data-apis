# frc-data-apis
my sloppy frc api tools and tools

## FRC Events API
1. Go to https://frc-events.firstinspires.org/services/api 
2. Hit "Register for API access"

 * [API Docs](https://frc-events.firstinspires.org/services/api)

## TBA API
1. Go to https://www.thebluealliance.com/account and set up an account
2. Create a new api key

 * [API Docs](https://www.thebluealliance.com/apidocs/v3)

## Statbotics
Does not need an api key.
  * [Python API docs](https://www.statbotics.io/api/python0)
  * [REST API docs](https://www.statbotics.io/api/rest)


## Creds
Put creds in a JSON file in ~/.frc-apis.json:

```
{
  "auth": {
    "tba": {"key": "abcdefgHIJKLMNOPQRStuvwxyx0123456789abcdefgjijklmnopqrstuvwxyzab"},
    "frc": {"user": "youruser", "key": "abcdef00-dead-beef-0000-abcdef012345"}
  }
}
```
