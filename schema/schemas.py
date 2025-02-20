
def individual_serial_odpoved(res) -> dict:
    return {
        "id": str(res.get("_id")),
        "fname": res.get("fname"),
        "lname": res.get("lname"),
        "firma": res.get("firma"),
        "ico": res.get("ico"),
        "dic": res.get("dic"),
        "p_dic": res.get("p_dic"),
        "phone": res.get("phone"),
        "email": res.get("email"),
        "date": res.get("date"),
        "message": res.get("message")
    }

def individual_serial_portfolio(res) -> dict:
    return {
        "id": str(res.get("_id")),
        "title": res.get("title"),
        "slug": res.get("slug"),
        "text": res.get("text", ""),
        "imgs": res.get("imgs", []),
    }


def list_serial(res, res_func='individual_serial_odpoved') -> list:
    return [eval(res_func)(r) for r in res]

