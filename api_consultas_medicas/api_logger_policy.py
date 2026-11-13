def metadata_only_policy(context):
    return {
        "headers": False,
        "request_body": False,
        "response_body": False,
        "mask_keys": [
            "nome",
            "contato",
            "endereco",
            "profissao",
            "data",
            "profissional",
        ],
        "reason": "metadata_only",
    }