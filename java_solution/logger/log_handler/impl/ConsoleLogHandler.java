package java_solution.logger.log_handler.impl;

import java_solution.logger.Log;
import java_solution.logger.formatter.LogFormatter;
import java_solution.logger.log_handler.LogHandler;

public class ConsoleLogHandler extends LogHandler {
    LogFormatter logFormatter;
    public ConsoleLogHandler(LogFormatter logFormatter){
        this.logFormatter = logFormatter;
    }

    @Override
    public void write(Log message) {
        System.out.println(this.logFormatter.format(message));
    }
    
}
