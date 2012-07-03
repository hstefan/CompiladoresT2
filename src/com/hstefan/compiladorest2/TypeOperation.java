package com.hstefan.compiladorest2;

/**
 *
 * @author hstefan
 */
public class TypeOperation {
    public enum Operator {
        SUM,
        MULT,
        ASSIGNMENT,
        COMPARISON,
    }

    SymbolTable mTable;
    
    public TypeOperation(SymbolTable table) {
        mTable = table;
    }

    public boolean operationAllowed(VarType lhs, VarType rhs, Operator oper) {
        /*TODO*/
        return true;
    }

    public VarType resultingType(VarType lhs, VarType rhs, Operator oper) {
        /*TODO */
        return VarType.UNKNOWN;
    }
}
