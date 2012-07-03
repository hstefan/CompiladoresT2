package com.hstefan.compiladorest2;

import java.util.HashMap;

/**
 *
 * @author hstefan
 */
public class TypeOperation {
    public enum Operator {
        SUM,
        MULT,
        DIVISION,
        MINUS,
        ASSIGNMENT,
        COMPARISON
    }

    private SymbolTable mTable;
    
    public TypeOperation(SymbolTable table) {
        mTable = table;
    }

    public boolean operationAllowed(VarType lhs, VarType rhs, Operator oper) {
        /*TODO*/
        return true;
    }

    public VarType resultingType(String lhs_id, String rhs_id, Operator oper) {
        SymbolTableEntry lhs_e = mTable.getElement(lhs_id);
        SymbolTableEntry rhs_e = mTable.getElement(rhs_id);

        if(lhs_e == null || rhs_e == null){
            //error, check on how to treat it
        } else {
            VarType lhs_type = lhs_e.var_type;
            VarType rhs_type = rhs_e.var_type;

            VarType res_type = VarType.UNKNOWN;

            if(lhs_type == rhs_type) {
                res_type = lhs_type;
            } else {
                VarType aux;
                /*Bloco de tratamento para stacks e queues no LHS*/
                aux = isQueue(lhs_type);
                if(aux != null && rhs_e.var_type == aux) {
                    //lhs is a queue of 'aux'
                }
                aux = isStack(lhs_type );
                if(aux != null && rhs_e.var_type == aux) {
                    //lhs is a stack of 'aux'
                }

                /*Bloco de tratamento para stacks e queues no RHS*/
                aux = isQueue(rhs_type);
                if(aux != null && lhs_e.var_type == aux) {
                    //rhs is a queue of 'aux'
                }
                aux = isStack(rhs_type);
                if(aux != null && lhs_e.var_type == aux) {
                    //rhs is a stack of 'aux'
                }
            }
        }

        return VarType.UNKNOWN;
    }

    /**
     * @param type the VarType which is being evaluated
     * @return null if it's not a queue, otherwise queue type
     */
    VarType isQueue(VarType type) {
        VarType res = null;
        switch(type) {
            case INT_QUEUE:
                res = VarType.INT;
                break;
            case STRING_QUEUE:
                res = VarType.STRING;
                break;
            case REAL_QUEUE:
                res = VarType.REAL;
                break;
        }
        return res;
    }

    /**
     * @param type the VarType which is being evaluated
     * @return null if it's not a stack, otherwise stack type
     */
    VarType isStack(VarType type) {
        VarType res = null;
        switch(type) {
            case INT_STACK:
                res = VarType.INT;
                break;
            case STRING_STACK:
                res = VarType.STRING;
                break;
            case REAL_STACK:
                res = VarType.REAL;
                break;
        }
        return res;
    }


}
