import { Injectable } from '@angular/core'; // Assuming you have environment files
import { LogLevel } from '../../models/enums/LogLevel.enum';
import { environment } from '../../../../environments/environments';
import { Logger } from '../../models/interfaces/logger.service.interface';

@Injectable({
  providedIn: 'root', // Makes the service a singleton
})
export class LoggerService implements Logger {
  logLevel: LogLevel = environment.logLevel || LogLevel.Debug; // Default to Debug in development

  debug(message: string, ...args: any[]): void {
    if (this.logLevel <= LogLevel.Debug) {
      console.debug(`[DEBUG] ${message}`, ...args);
    }
  }

  info(message: string, ...args: any[]): void {
    if (this.logLevel <= LogLevel.Info) {
      console.info(`[INFO] ${message}`, ...args);
    }
  }

  warn(message: string, ...args: any[]): void {
    if (this.logLevel <= LogLevel.Warn) {
      console.warn(`[WARN] ${message}`, ...args);
    }
  }

  error(message: string, ...args: any[]): void {
    if (this.logLevel <= LogLevel.Error) {
      console.error(`[ERROR] ${message}`, ...args);
    }
  }

  // You can add a delete method if you have a specific meaning for it
  // In standard logging, 'error' usually covers deletion failures or critical issues
  // For now, we'll stick to standard levels

  // Example of adding a custom log method
  log(level: LogLevel, message: string, ...args: any[]): void {
    if (this.logLevel <= level) {
      switch (level) {
        case LogLevel.Debug:
          console.debug(`[DEBUG] ${message}`, ...args);
          break;
        case LogLevel.Info:
          console.info(`[INFO] ${message}`, ...args);
          break;
        case LogLevel.Warn:
          console.warn(`[WARN] ${message}`, ...args);
          break;
        case LogLevel.Error:
          console.error(`[ERROR] ${message}`, ...args);
          break;
        default:
          console.log(`[LOG] ${message}`, ...args);
          break;
      }
    }
  }
}
