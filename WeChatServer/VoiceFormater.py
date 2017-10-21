import  subprocess
from WeChatCon import WeChatHandler
from AWSHandler import LexConnector

class VoiceFormater(object):
    def __init__(self):
        self.cmd = "/usr/local/bin/ffmpeg"
        pass

    def amr2wav(self, amr_file, wave_file):
        ret = subprocess.call([self.cmd, "-i", amr_file, wave_file, "-y"])
        return ret

    def wav2amr(self, wave_file, amr_file):
        ret = subprocess.call([self.cmd, "-i", wave_file, "-ar", "8000", amr_file, "-y"])
        return ret



if __name__ == "__main__":
    mediaID = "gX86aKyZeqMd40I9VByVmePGTkEv_KJCwQfpKzLmezD-gEQDnuLeJLxCOK9eAFhu"
    saveFile = "/tmp/abc.amr"
    waveFile = "/tmp/abc.wav"
    rspData = WeChatHandler().downloadVoiceAsFile(mediaID, saveFile)
    VoiceFormater().amr2wav(saveFile, waveFile)
    LexConnector().connectVoice("testID", rspData, "/tmp/tmp_save_aws_voice.wav")
    VoiceFormater().wav2amr("/tmp/tmp_save_aws_voice.wav", "/tmp/tmp_save_aws_voice.amr")
    WeChatHandler().uploadVoiceFile("/tmp/tmp_save_aws_voice.amr")
