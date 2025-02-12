

class XVideoReader:
    def __init__(self, video_path, batch_frame, interval=1.0, with_idxs=False, **decord_params):
        import decord
        from decord import VideoReader
        decord.bridge.set_bridge('torch')
        self.video_path = video_path
        self.decord_params = decord_params
        self.batch_frame = batch_frame
        try:
            self.capture = VideoReader(video_path, **decord_params)
        except Exception as e:
            raise RuntimeError(e)

        self.interval = int(self.capture.get_avg_fps() * interval) if interval > 0 else 1
        self.nframe = len(self.capture)
        self.fidxs = self._gen_seq_idx()
        self.transforms = self._transforms_with_idxs if with_idxs else self._transforms

    def __len__(self):
        return len(self.fidxs) // self.batch_frame

    def _gen_seq_idx(self):
        return [i for i in range(0, self.nframe, self.interval)]

    def _transforms(self, frames, frame_index):
        return frames
    
    def _transforms_with_idxs(self, frames, frame_index):
        return frames, frame_index

    def __getitem__(self, idx):
        b = idx * self.batch_frame
        e = min(b + self.batch_frame, self.nframe)
        # RGB
        frames = self.capture.get_batch(self.fidxs[b:e])
        if idx > self.__len__():
            raise IndexError
        return self.transforms(frames, self.fidxs[b:e])

if __name__ == '__main__':
    v = IVideoReader(r'D:\Downloads\1004770199-1-208.mp4', 8)

    for data in v:
        print(data.shape)