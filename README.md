# Event Database Automatization for Sportiq project

Automatization for time-based info. You can change the event deletion time in `.env`, along with the processing frequency.

## Related Sportiq services

- [API Gateway](https://github.com/Str1kez/SportiqAPIGateway)
- [User Service](https://github.com/Str1kez/SportiqUserService)
- [Event Service](https://github.com/Str1kez/SportiqEventService)
- [Subscription Service](https://github.com/Str1kez/SportiqSubscriptionService)
- [Frontend App](https://github.com/Str1kez/SportiqReactApp)

## Startup

1. Create `.env` file and fill it:
   ```commandline
   make env
   ```
2. Build Docker-image:
   ```commandline
   make build
   ```
3. Turn on Message Queue and Event DB services, that are defined in the [Event Service](https://github.com/Str1kez/SportiqEventService)
4. After that, start automatization:
   ```commandline
   make up
   ```
