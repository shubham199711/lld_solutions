package java_solution.logger.formatter.impl;

import java_solution.logger.Log;
import java_solution.logger.formatter.LogFormatter;

public class SimpleFormatter extends LogFormatter  {
    @Override
    public String format(Log message) {
        return message.toString();
    }
    
}
