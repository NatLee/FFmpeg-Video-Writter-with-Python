import ffmpeg
import numpy as np

class FFmpegVideoWritter():

    def __init__(self, in_filename, out_filename, fps=27, video_format='rawvideo', input_pix_fmt='rgb24'):
        self.in_filename = in_filename
        self.out_filename = out_filename
        self.video_format = video_format
        self.input_pix_fmt = input_pix_fmt

        probe = ffmpeg.probe(self.in_filename)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        self.input_width = int(video_stream['width'])
        self.input_height = int(video_stream['height'])
        self.input_frames = int(video_stream['nb_frames'])
        self.input_length = int(self.input_frames/eval(video_stream['avg_frame_rate']))
        self.output_frames = int(fps*self.input_length)

        self.__input_process = (
            ffmpeg
            .input(self.in_filename)
            .filter('fps', fps=fps, round='up')
            .output('pipe:', format=self.video_format, pix_fmt=self.input_pix_fmt, vframes=self.output_frames)
            .run_async(pipe_stdout=True)
        )

        self.__output_process = None
        self.__INITIAL_OUTPUT_PROCESS = False


    def get_frame(self):
        in_bytes = self.__input_process.stdout.read(self.input_width * self.input_height * 3)
        if not in_bytes:
            return None
        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([self.input_height, self.input_width, 3])
        )
        return in_frame
    def write(self, frame):
        height, width, _ = frame.shape
        if not self.__INITIAL_OUTPUT_PROCESS:
            self.__output_process = (
                ffmpeg
                .input('pipe:', format=self.video_format, pix_fmt=self.input_pix_fmt, s='{}x{}'.format(width, height))
                .output(self.out_filename, **{'qscale:v': 0.01}) # 0.01-255 lower has higher quality
                .overwrite_output()
                .run_async(pipe_stdin=True)
            )
            self.__INITIAL_OUTPUT_PROCESS = True
        self.__output_process.stdin.write(
                frame
                .astype(np.uint8)
                .tobytes()
        )
        return True


    def close(self):
        self.__output_process.stdin.close()
        self.__input_process.wait()
        self.__output_process.wait()


    def output_to_gif(self, out_filename):
        gif_process = (
            ffmpeg
            .input(self.out_filename)
            .output(self.out_filename + '.gif')
            .run(overwrite_output=True)
        )
        return True