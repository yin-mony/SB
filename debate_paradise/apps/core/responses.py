from rest_framework.response import Response


def ok(data=None, msg="success", code=200):
    return Response({"code": code, "msg": msg, "data": data or {}})


def fail(msg="error", code=400, data=None):
    return Response({"code": code, "msg": msg, "data": data or {}}, status=code)

