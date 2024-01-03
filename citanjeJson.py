import os
import json


class Accessibility:

    def __init__(self, requested_url, final_url, audits, audit_refs, score):
        self.requested_url = requested_url
        self.final_url = final_url
        self.audits = [Audit.from_json(audit_data) for audit_data in audits.values()]
        self.audit_refs = [AuditRefs.from_json(audit_ref_data) for audit_ref_data in audit_refs]
        self.score = score

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get('requestedUrl'),
            json_data.get('finalUrl'),
            json_data.get('audits', {}),
            json_data.get('categories', {}).get('accessibility', {}).get('auditRefs', {}),
            json_data.get('categories', {}).get('accessibility', {}).get('score')
        )


class Audit:

    def __init__(self, id, title, description, score):
        self.id = id
        self.title = title
        self.description = description
        self.score = score

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get('id'),
            json_data.get('title'),
            json_data.get('description'),
            json_data.get('score')
        )


class AuditRefs:

    def __init__(self, id, weight, group):
        self.id = id
        self.weight = weight
        self.group = group

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get('id'),
            json_data.get('weight'),
            json_data.get('group')
        )


current_directory = os.getcwd()

files = os.listdir(current_directory)

json_files = [file for file in files if file.endswith('.json')]

for json_file in json_files:
    file_path = os.path.join(current_directory, json_file)

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # Create Accessibility instance from JSON data
        accessibility_instance = Accessibility.from_json(data)

        # Access attributes as needed
        print(f"Requested URL: {accessibility_instance.requested_url}")
        print(f"Final URL: {accessibility_instance.final_url}")
        print(f"Audits: {len(accessibility_instance.audits)}")
        print(f"Audit Refs: {len(accessibility_instance.audit_refs)}")
        print(f"Score: {accessibility_instance.score}")

