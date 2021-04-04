# FTX-Telegram-Bot
Bot for sending telegram messages on order fills on cryptocurrency exchange FTX.
Just put in the right info into a file called settings.py as shown in example_settings.py.

TODO:

I have to deal with when orders are filled in 2 parts.
Maybe store the current fill and after 1s or smth send the message.
    Better alternative: Just use the rest position endpoint.
	https://docs.ftx.com/#get-positions
    Can only do for PERP.

I have to test if it runs for over 24h