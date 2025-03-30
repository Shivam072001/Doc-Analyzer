import { LogLevel } from '../enums/LogLevel.enum';

export interface Logger {
  logLevel: LogLevel;
  debug(message: string, ...args: any[]): void;
  info(message: string, ...args: any[]): void;
  warn(message: string, ...args: any[]): void;
  error(message: string, ...args: any[]): void;
  // You can add more methods if needed, e.g., trace, fatal
}
