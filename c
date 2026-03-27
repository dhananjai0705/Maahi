defaults.pcm.card 3
defaults.pcm.device 0
defaults.ctl.card 3

pcm.!default {
    type asym
    playback.pcm "playback"
    capture.pcm "capture"
}

pcm.playback {
    type hw
    card 3
    device 0
}

pcm.capture {
    type hw
    card 3
    device 0
}

ctl.!default {
    type hw
    card 3
}
