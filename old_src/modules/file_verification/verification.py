import json
import os


class Verification:
    def __init__(self):
        self.check_result = ""
        self.check_queue = json.loads(open("modules/file_verification/verify_queue.json", "r", encoding="utf-8").read())["path"]

    def exist(self):
        for path in self.check_queue:
            if not os.path.exists(path[0]):
                if path[2] == "file":
                    if path[1] == "error":
                        self.check_result += f"[Error] 文件 {path[0]} 不存在\n"
                        return self.check_result, False
                    elif path[1] == "create":
                        self.check_result += f"[Warning] {path[0]} 不存在, 但成功创建\n"
                        open(path[0], "w", encoding="utf-8").write("")
                elif path[2] == "directory":
                    if path[1] == "error":
                        self.check_result += f"[Error] 文件夹 {path[0]} 不存在\n"
                        return self.check_result, False
                    elif path[1] == "create":
                        self.check_result += f"[Warning] 文件夹 {path[0]} 不存在, 但成功创建\n"
                        os.mkdir(path[0])
        return self.check_result, True
