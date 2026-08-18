# Mobile

Expo / React Native client for the SportsAI simulation project.

## Run

```bash
npm install
npx expo start
```

Create `.env` from `.env.example`.

```env
EXPO_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

When testing on a physical phone, replace `127.0.0.1` with the LAN IP address of the computer running FastAPI, for example:

```env
EXPO_PUBLIC_API_BASE_URL=http://192.168.1.25:8000
```

Do not place secrets in `EXPO_PUBLIC_` variables because values with that prefix are exposed to the client application.
