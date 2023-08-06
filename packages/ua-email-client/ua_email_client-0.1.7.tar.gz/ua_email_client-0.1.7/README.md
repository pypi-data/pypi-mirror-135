# UA-Email-Client

Provides easy interface for sending emails through Amazons Simple Email Service.

## Motivation

To make a python API that could obfuscate the details of sending emails using AWS SES service.

## Code Example

```python
from ua_email_client import ua_email_client

client = ua_email_client.EmailClient(email)
# The template name given should be relative name to a file.
client.add_template("success.html")

# Destinations 
client.send_email(destinations, "success.html", subject, body)
```

## Installation

pip install --user ua-email-client

## Tests

**NOTE:** Running this test suite *WILL* send emails. Please specify an email which can receive emails. The emails can all be ignored once received.

To run the tests you will need to create a json configuration with some user-specific values. This file will be ua_email_client/tests/email_creds.json. It will be populated with:
```json
{
    "email": "...",
    "default_recipient": "...",
    "secondary_recipient": "..."
}
```

Where `"email"` is the sending email, `"default_recipient"` is the main email you want to receive emails, and `"secondary_recipient"` is a second email to test sending emails to multiple recipients at once.

Once this file is created, just run:
```bash
cd ua_email_client/tests
nosetests test_ua_email_client.py
```

## Credits

[RyanJohannesBland](https://github.com/RyanJohannesBland)
[EtienneThompson](https://github.com/EtienneThompson)

## License

MIT
