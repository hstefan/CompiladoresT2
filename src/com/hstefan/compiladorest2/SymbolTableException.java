package com.hstefan.compiladorest2;

/**
 *
 * @author hstefan
 */
public class SymbolTableException extends Exception {

    public SymbolTableException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
        super(message, cause, enableSuppression, writableStackTrace);
    }

    public SymbolTableException(Throwable cause) {
        super(cause);
    }

    public SymbolTableException(String message) {
        super(message);
    }

    public SymbolTableException() {
    }
}
