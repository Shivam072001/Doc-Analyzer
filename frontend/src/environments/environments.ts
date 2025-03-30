import { LogLevel } from "../app/shared/models/enums/LogLevel.enum";

export const environment = {
  production: false,
  apiUrl: 'http://127.0.0.1:5000/api', // Your Flask backend API URL
  logLevel: LogLevel.Debug, // Log everything in development
};
