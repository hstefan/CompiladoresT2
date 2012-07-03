package com.hstefan.compiladorest2;

import java.util.HashMap;

/**
 *
 * @author hstefan
 */
public class SymbolTable {

    private HashMap<String, SymbolTableEntry> mTable;
    private int mCurAddress;

    public static final int DEFAULT_ADDRESS = 0;
    
    public SymbolTable() {
        mTable = new HashMap<>();
        mCurAddress = DEFAULT_ADDRESS;
    }

    public void addRow(SymbolTableEntry entry) throws SymbolTableException {
        SymbolTableEntry last_entry = mTable.put(entry.identifier, entry);
        mCurAddress += getTypeSize(entry.var_type);
        if(last_entry != null) {
          throw new SymbolTableException("Overriding table entry.");
        } 
    }

    public void addRow(VarType type, String identifier)
            throws SymbolTableException {
        addRow(new SymbolTableEntry(type, identifier, getEntryType(type)));
    }

    private int getTypeSize(VarType type) {
        int sz = 8;

        if(type == VarType.INT) {
            sz = 4;
        }
        
        return sz;
    }

    private SymbolTableEntry.EntryType getEntryType(VarType type) {
        SymbolTableEntry.EntryType rtype = SymbolTableEntry.EntryType.DESCRIPTOR;
        
        if(type == VarType.INT || type == VarType.REAL || type == VarType.STRING) {
            rtype = SymbolTableEntry.EntryType.BASIC;
        }
        
        return rtype;
    }

    public SymbolTableEntry getElement(String id) {
        return mTable.get(id);
    }
}
