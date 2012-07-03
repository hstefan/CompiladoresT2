
package com.hstefan.compiladorest2;

/**
 *
 * @author hstefan
 */
public class SymbolTableEntry {
    public VarType var_type;
    public EntryType entry_type;
    public String identifier;

    public SymbolTableEntry(VarType vtype, String identifier, EntryType etype) {
        this.var_type = vtype;
        this.identifier = identifier;
    }

    enum EntryType {
        DESCRIPTOR,
        BASIC
    }
}
