class DisplayInfo:
    def __init__(self, width: int, height: int, depth: int, fps: int) -> None:
        self.width = width
        self.height = height
        self.depth = depth
        self.fps = fps

    def __str__(self) -> str:
        return f"Width: {self.width}, Height: {self.height}, Depth: {self.depth}, FPS: {self.fps}"
