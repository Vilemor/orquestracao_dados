import json
import uuid
import os
import sys
import traceback
from datetime import datetime
from pytz import timezone
from typing import Optional


_EXECUTION_ID = str(uuid.uuid4())
_TZ = timezone("America/Sao_Paulo")


def log_json(
    message: str,
    level: str = "INFO",
    group: str = "orquestracao",
    context: Optional[dict] = None,
    exc: Optional[Exception] = None,
    log_to_file: Optional[str] = None,
    **kwargs
) -> None:
    frame = sys._getframe(1)
    file_name = os.path.basename(frame.f_code.co_filename)
    function_name = frame.f_code.co_name
    line_no = frame.f_lineno  # Captura a linha do log

    if function_name == "<module>":
        function_name = "__main__"

    log_entry = {
        "timestamp": datetime.now(_TZ).isoformat(),
        "level": level,
        "log_groups": group,
        "message": message,
        "execution_id": _EXECUTION_ID,
        "function": function_name,
        "file": file_name + ':' + str(line_no)
    }

    if context:
        log_entry["context"] = context

    if exc:
        tb = traceback.extract_tb(exc.__traceback__)
        if tb:
            last = tb[-1]
            log_entry["error_location"] = f"{os.path.basename(last.filename)}:{last.lineno}"
        log_entry["stacktrace"] = f"{type(exc).__name__}: {exc}"

    log_entry.update(kwargs)

    if log_json._last_group != group:
        print(f"\n{'='*20} {group.upper()} {'='*20}\n")
        log_json._last_group = group

    log_str = json.dumps(log_entry, indent=2, ensure_ascii=False)
    print(log_str)
    if log_to_file:
        with open(log_to_file, "a", encoding="utf-8") as f:
            f.write(log_str + "\n")

log_json._last_group = None