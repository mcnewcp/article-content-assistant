import json
from airtable import Airtable

from ..utils.config import (
    AIRTABLE_API_KEY,
    AIRTABLE_BASE_ID,
    AIRTABLE_ARTICLE_TABLE_NAME,
    AIRTABLE_CONTENT_TABLE_NAME,
)


def save_to_airtable(data, table: str):
    """
    Save the provided data to Airtable.
    """
    try:
        if table == "article":
            table_name = AIRTABLE_ARTICLE_TABLE_NAME
        elif table == "content":
            table_name = AIRTABLE_CONTENT_TABLE_NAME
        else:
            raise ValueError("Unrecognized table name")
        airtable = Airtable(AIRTABLE_BASE_ID, table_name, api_key=AIRTABLE_API_KEY)
        record = airtable.insert(data)
        return record["id"]
    except Exception as e:
        return f"Error saving to Airtable: {str(e)}"


def get_from_airtable(record_id, table: str):
    """
    Retrieve a record from Airtable by its ID.
    """
    try:
        if table == "article":
            table_name = AIRTABLE_ARTICLE_TABLE_NAME
        elif table == "content":
            table_name = AIRTABLE_CONTENT_TABLE_NAME
        else:
            raise ValueError("Unrecognized table name")
        airtable = Airtable(AIRTABLE_BASE_ID, table_name, api_key=AIRTABLE_API_KEY)
        record = airtable.get(record_id)
        return record["fields"]
    except Exception as e:
        return f"Error retrieving from Airtable: {str(e)}"


def get_latest_record(table: str):
    """
    Retrieve the latest record from Airtable.
    """
    try:
        if table == "article":
            table_name = AIRTABLE_ARTICLE_TABLE_NAME
        elif table == "content":
            table_name = AIRTABLE_CONTENT_TABLE_NAME
        else:
            raise ValueError("Unrecognized table name")
        airtable = Airtable(AIRTABLE_BASE_ID, table_name, api_key=AIRTABLE_API_KEY)
        records = airtable.get_all(maxRecords=1, sort=[("datetime", "desc")])
        if records:
            return records[0]["fields"]
        else:
            return None
    except Exception as e:
        return f"Error retrieving latest record from Airtable: {str(e)}"


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    try:
        body = json.loads(event["body"])
        action = body["action"]
        table = body["table"]

        if action == "save":
            data = body["data"]
            result = save_to_airtable(data, table)
            return {"statusCode": 200, "body": json.dumps({"record_id": result})}
        elif action == "get":
            record_id = body["record_id"]
            result = get_from_airtable(record_id, table)
            return {"statusCode": 200, "body": json.dumps(result)}
        elif action == "get_latest":
            result = get_latest_record(table)
            return {"statusCode": 200, "body": json.dumps(result)}
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid action"})}
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}


# For local testing
if __name__ == "__main__":
    # Test saving data
    test_article_data = {
        "url": "https://example.com/article",
        "discord_user": "test_user",
        "title": "Test Article Title",
        "source": "Test News Outlet",
        "text": "This is a test article text.",
        "summary": "This is a summary of the test article.",
    }

    print("Testing save_to_airtable:")
    save_result = save_to_airtable(test_article_data)
    print(save_result)

    # Test retrieving the latest record
    print("\nTesting get_latest_record:")
    get_result = get_latest_record()
    print(json.dumps(get_result, indent=2))

    # If you want to test retrieval of a specific record, uncomment and update with a valid record ID
    # print("\nTesting get_from_airtable:")
    # specific_record = get_from_airtable("recKQUbGWrcUMZdEp")
    # print(json.dumps(specific_record, indent=2))
