def Response(
    message,
    status_code,
    json_data=None,
):
    try:
        return {"status_code": status_code, "message": message, "data": json_data}
    except Exception as e:
        return Response(e, "Response Failed", True)
