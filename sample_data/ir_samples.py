"""Realistic Oracle Forms IR samples for MVP testing and demos."""

VALIDATION_IR = {
    "form": {
        "blocks": [
            {
                "name": "EMP",
                "table": "EMP",
                "items": [{"name": "ENAME"}, {"name": "SAL"}],
            }
        ]
    },
    "triggers": [
        {
            "type": "WHEN-VALIDATE-ITEM",
            "code": "IF :SAL > 5000 THEN MESSAGE('Too high'); END IF;",
        }
    ],
}

ASSIGNMENT_IR = {
    "form": {
        "blocks": [
            {
                "name": "EMP",
                "table": "EMP",
                "items": [{"name": "BONUS"}],
            }
        ]
    },
    "triggers": [
        {
            "type": "WHEN-NEW-RECORD-INSTANCE",
            "code": ":BONUS := 1000;",
        }
    ],
}

MULTI_TRIGGER_IR = {
    "form": {
        "blocks": [
            {
                "name": "EMP",
                "table": "EMP",
                "items": [{"name": "SAL"}, {"name": "DEPTNO"}],
            }
        ]
    },
    "triggers": [
        {
            "type": "WHEN-VALIDATE-ITEM",
            "code": "IF :SAL = 0 THEN MESSAGE('Salary required'); END IF;",
        },
        {
            "type": "KEY-COMMIT",
            "code": "INSERT INTO EMP_AUDIT VALUES (SYSDATE);",
        },
    ],
}

MIXED_LOGIC_IR = {
    "form": {
        "blocks": [
            {
                "name": "EMP",
                "table": "EMP",
                "items": [{"name": "SAL"}, {"name": "GRADE"}],
            }
        ]
    },
    "triggers": [
        {
            "type": "WHEN-BUTTON-PRESSED",
            "code": "IF :SAL > 7000 THEN MESSAGE('Needs director approval'); :GRADE := 5; END IF;",
        },
        {
            "type": "KEY-NEXT-ITEM",
            "code": "GO_ITEM('EMP.ENAME');",
        },
    ],
}
