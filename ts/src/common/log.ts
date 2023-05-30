import { Logger, transports, createLogger, format } from 'winston'
let logFormat = format.combine(format.json(),
  format.printf((info) => {
    if (typeof info.message === 'object') {
      info.message = JSON.stringify(info.message)
    }
    return info.message
  })
)
let level = 'debug'
if (process.env.colorize === '1') {
  logFormat = format.combine(format.json(),
    format.printf((info) => {
      if (typeof info.message === 'object') {
        info.message = JSON.stringify(info.message)
      }

      return info.message
    }),
    format.cli())
}

if (process.env.NODE_ENV === 'production') {
  level = 'warn'
}

export const logger = createLogger({
  level: level,
  transports: [new transports.Console()],
  format: logFormat
});

export const logDebug = (...args: any) => { logger.debug(args) }
export const logInfo = (...args: any) => { logger.info(args) }
export const logSuccess = (...args: any) => { logger.info(args) }
// export const logSuccess = (...args: any) => { logger.color('black').bgColor('green').log(args) }
export const logWarn = (...args: any) => { logger.warn(args) }
export const logError = (...args: any) => {
  let logged = false
  for (let key in args) {
    if (args[key] instanceof Error) {
      args[key] = args[key].stack
      logged = true
      logger.error(args[key])
    }
  }
  if (!logged) {
    logger.error(args)
  }
}
