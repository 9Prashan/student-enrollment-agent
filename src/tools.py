# src/tools.py

PROGRAMS = {
    "Bachelor of Computer Science": {
        "duration": "3 years",
        "tuition": "$32,000 per year",
        "prerequisites": [
            "High school diploma or equivalent",
            "Mathematics qualification",
            "English language proficiency"
        ],
        "application_deadline": "30 November 2026",
        "document_deadline": "15 December 2026",
        "decision_date": "15 January 2027"
    },
    "Master of Computer Science": {
        "duration": "2 years",
        "tuition": "$38,000 per year",
        "prerequisites": [
            "Bachelor's degree in Computer Science or related field",
            "Programming experience",
            "English language proficiency"
        ],
        "application_deadline": "31 October 2026",
        "document_deadline": "15 November 2026",
        "decision_date": "15 December 2026"
    },
    "Bachelor of Data Science": {
        "duration": "3 years",
        "tuition": "$31,000 per year",
        "prerequisites": [
            "High school diploma or equivalent",
            "Mathematics qualification",
            "English language proficiency"
        ],
        "application_deadline": "30 November 2026",
        "document_deadline": "15 December 2026",
        "decision_date": "15 January 2027"
    }
}


APPLICANTS = {
    "APP-1042": {
        "name": "Alex Johnson",
        "program": "Bachelor of Computer Science",
        "status": "Documents Pending",
        "next_step": "Submit the remaining required documents",
        "pending_documents": [
            "Official academic transcript",
            "English language proficiency certificate"
        ]
    },
    "APP-1043": {
        "name": "Sarah Williams",
        "program": "Master of Computer Science",
        "status": "Under Review",
        "next_step": "Wait for the admissions decision",
        "pending_documents": []
    },
    "APP-1044": {
        "name": "Michael Brown",
        "program": "Bachelor of Data Science",
        "status": "Accepted",
        "next_step": "Accept the offer and complete enrollment",
        "pending_documents": []
    }
}


def get_program_info(program_name: str):
    """Return information about a university program."""

    program_name_lower = program_name.lower()

    for name, info in PROGRAMS.items():
        if (
            program_name_lower in name.lower()
            or name.lower() in program_name_lower
        ):
            return {
                "program_name": name,
                "duration": info["duration"],
                "tuition": info["tuition"],
                "prerequisites": info["prerequisites"]
            }

    return {
        "error": f"Program '{program_name}' was not found."
    }


def check_application_status(applicant_id: str):
    """Return application status for an applicant."""

    applicant = APPLICANTS.get(applicant_id.upper())

    if not applicant:
        return {
            "error": f"No application found for ID '{applicant_id}'."
        }

    return {
        "applicant_name": applicant["name"],
        "program": applicant["program"],
        "status": applicant["status"],
        "next_step": applicant["next_step"],
        "pending_documents": applicant["pending_documents"]
    }


def get_deadlines(program_name: str):
    """Return important application deadlines."""

    program_name_lower = program_name.lower()

    for name, info in PROGRAMS.items():
        if (
            program_name_lower in name.lower()
            or name.lower() in program_name_lower
        ):
            return {
                "program_name": name,
                "application_deadline": info["application_deadline"],
                "document_submission_deadline": info["document_deadline"],
                "decision_notification_date": info["decision_date"]
            }

    return {
        "error": f"Program '{program_name}' was not found."
    }