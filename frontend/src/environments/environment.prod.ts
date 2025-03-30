import { LogLevel } from "../app/shared/models/enums/LogLevel.enum";

export const environment = {
  production: true,
  apiUrl: 'https://your-production-backend-url.com/api', // Your production Flask backend API URL
  logLevel: LogLevel.Warn, // Log only warnings and errors in production
};
