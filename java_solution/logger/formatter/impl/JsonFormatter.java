package java_solution.logger.formatter.impl;

import java.util.Map;
import java.util.stream.Collectors;

import java_solution.logger.Log;
import java_solution.logger.formatter.LogFormatter;

public class JsonFormatter extends LogFormatter {

    @Override
    public String format(Log message) {
        Map<String, Object> data = Map.of(
            "time", message.getTime(),
            "loglevel", message.getLogLevel(),
            "message", message.getMessage()
        );
        return mapToJson(data);
    }

    public static String mapToJson(Map<String, Object> map) {
        return "{" + 
                map.entrySet()
            .stream()
                .map(entry -> "\"" + entry.getKey() + "\":" + formatValue(entry.getValue()))
                .collect(Collectors.joining(","))
                + "}";
    }

    @SuppressWarnings("unchecked")
    private static String formatValue(Object value) {
        if (value instanceof String) {
            return "\"" + value + "\"";   // Quote strings
        } else if (value instanceof Map) {
            return mapToJson((Map<String, Object>) value); // Handle nested maps
        } else {
            return String.valueOf(value); // For numbers, booleans
        }
    }
    
}
