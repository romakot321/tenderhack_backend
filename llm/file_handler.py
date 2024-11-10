import os.path


class FileHandler:
    paginated_parts = 5

    def read_file(self, path: str, paginate: bool = True) -> list[str] | str | None:
        if not os.path.exists('../' + path):
            return
        with open('../' + path, 'r') as f:
            filesize = os.fstat(f.fileno()).st_size
            content = f.read()
        if not paginate:
            return content
        step = filesize // 5
        return [
            content[bias:bias + step]
            for bias in range(0, filesize, step)
        ]

