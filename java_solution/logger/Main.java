package java_solution.logger;

import java_solution.logger.formatter.LogFormatter;
import java_solution.logger.formatter.impl.JsonFormatter;
import java_solution.logger.formatter.impl.SimpleFormatter;
import java_solution.logger.log_handler.LogHandler;
import java_solution.logger.log_handler.impl.ConsoleLogHandler;
import java_solution.logger.log_handler.impl.FileLogHandler;


public class Main {
    public static void main(String[] args){
        Logger logger = new Logger(LogLevel.DEBUG);

        LogFormatter simpleFormatter = new SimpleFormatter();
        LogFormatter jsonFormatter = new JsonFormatter();

        // LogHandler consoleLogHandler = new ConsoleLogHandler(jsonFormatter);
        LogHandler fileLogHandler = new FileLogHandler(simpleFormatter, "java_log.txt");

        logger.addHandler(fileLogHandler);
        // logger.addHandler(consoleLogHandler);

        logger.info("This is message 1");
        logger.error("This is message 2");
        logger.warning("This is message 1");
        logger.debug("This is message 1");
    }
}